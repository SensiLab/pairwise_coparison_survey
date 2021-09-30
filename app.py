from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import flask_monitoringdashboard as fmd
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import json
import logging
import math
from numpy import random as np_rand
import os
import random
import requests
from models.models import Voter, Match, ImgSet1, ImgSet2, db

def deltatime(end, start):
    d = end-start
    return d.seconds*1000+d.microseconds/1000

class bcolors:
    GREEN = '\033[92m' #GREEN
    YELLOW = '\033[93m' #YELLOW
    RED = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    country = None
    try:
        country = data['country']
    except:
        country = 'NA'
    return country

q = 0.00575646273   #constant (magic number?)


logging.basicConfig(filename='demo.log', level=logging.DEBUG)
app = Flask(__name__)

fmd.config.init_from(file='/config.cfg')
fmd.bind(app)
# Bootstrap(app)
app.secret_key = "dkjfbwi7KJG*Ykhfhj*9%4))6$kjhGLOP"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///voters.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voters.db'
app.config['SQLALCHEMY_BINDS'] = {
    'matches':   'sqlite:///matches.db',
    'img_set1': 'sqlite:///img_set1.db',
    'img_set2': 'sqlite:///img_set2.db'
}

# db = SQLAlchemy(app)
db.init_app(app)
auth = HTTPBasicAuth()

# =============================================================
# =============================================================
# ============WEBSITE STRUCTURE STARTS HERE====================
# =============================================================
# =============================================================

# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data())

@app.route("/", methods = ["POST", "GET"])
@app.route("/home", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        
        # return redirect(url_for("survey", age=age, gender=gender, creativity=creativity))
        return redirect(url_for("start_survey"))

    else:
        return render_template('home.html')

@app.route("/explanatory_statement")
def explanatory_statement():
    return render_template("explanatory_statement.html")

@app.route("/start_survey", methods=["POST", "GET"])
def start_survey():
    if request.method == "POST":
        try:
            user_ip = '127.0.0.1'
            try:
                user_ip = request.headers['X-Real-IP']
            except:
                user_ip = request.remote_addr
            session['ip'] = user_ip
            session['matches'] = []
            age = request.form["age"]
            gender = request.form["gender"]
            creativity = request.form["creativity"]
            print("IP: {}, age: {}, gender: {}, creativity: {}".format(user_ip, age, gender, creativity))
            new_user = Voter(ip_address=user_ip, age=age, gender=gender, creativity=creativity)
            # print(bcolors.YELLOW+"New user location: {}".format(ipInfo(addr=user_ip))+bcolors.RESET)
            new_user.location = ipInfo(addr=user_ip)
            db.session.add(new_user)
            db.session.commit()
            session['comp_count'] = 0
            session['user_id'] = new_user.id
            print('A new user has been created. User id: {}'.format(new_user.id))
            app.logger.info(f"User ip: {session['ip']}")
            return redirect(url_for("survey", user_ip=user_ip, user_id=new_user.id), code=307)
        except Exception as e:
            app.logger.error(e)
            print('Error: {}'.format(e))
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


        
#This is the main function, where the voting data will be recorded
@app.route("/survey", methods = ["POST", "GET"])
def survey():
    if request.method == "POST":
        print("=====Survey Called=====")
        # selected_db = None
        #randomly select one database
        selected_db = np_rand.choice([ImgSet1, ImgSet2], p = [2/3,1/3]) # p determines the probability distribution for random
     
        if selected_db == ImgSet1:
            session['sel_db_index'] = 0
        else:
            session['sel_db_index'] = 1
        
        #randomly select a question
        #and define the probability distribution to sample from
        #databases using rating distributions
        rds = []        #a list to hold the appropriate rating_dev scores
        question = random.randint(0,1)
        if question == 0:
            session['q'] = 'rating_aesthetics'
            for img in selected_db.query.all():
                rds.append(img.rating_dev_aesthetics)
        else:
            session['q'] = 'rating_complexity'
            for img in selected_db.query.all():
                rds.append(img.rating_dev_complexity)

        
        # Set the probability distribution of selection based on number of matches
        norm_rds = [(rd/max(rds)) for rd in rds]
        prob_distrib = [rd/sum(norm_rds) for rd in norm_rds]
        
        contenders = np_rand.choice(selected_db.query.all(), 2, p=prob_distrib)
        contender0 = contenders[0]
        contender1 = contenders[1]
        
        session['contender0'] = contender0.id
        session['contender1'] = contender1.id

        #  images to be displayed
        rand_imgs = []
        rand_imgs.append('imgs/' + contender0.file_name)
        rand_imgs.append('imgs/' + contender1.file_name)

        session['start_time'] = datetime.now()
        print('=====Survey Finished=====')
        # return redirect(url_for("#"))
        return render_template('survey.html', rand_imgs=rand_imgs, question=question, counter=session.get('comp_count'))

    else:
        return render_template('home.html')

@app.route("/next", methods = ["POST", "GET"])
def next():
    if request.method == "POST":
        print('=====Next Called=====')
        #read values
        user_id = session.get('user_id')
        sel_db_index = session.get('sel_db_index')
        contender0_id = session.get('contender0')
        contender1_id = session.get('contender1')

        selected_db = None

        if sel_db_index == 0:
            selected_db = ImgSet1
        else:
            selected_db = ImgSet2
        
        winner = int(request.form["selection"])

        # get ratings for both contenders
        contender0 = selected_db.query.get(contender0_id)
        contender0_rating = 0
        contender0_rd = 0
        contender0_score = 0
        contender1 = selected_db.query.get(contender1_id)
        contender1_rating = 0
        contender1_rd = 0
        contender1_score = 0
        
        if winner == 0:
            contender0_score = 1
            contender1_score = 0
        elif winner == 1:
            contender0_score = 0
            contender1_score = 1
        else:
            contender0_score = 0.5
            contender1_score = 0.5

        question_index = 0
        if session.get('q') == 'rating_aesthetics':
            contender0_rating = contender0.rating_aesthetics
            contender0_rd = contender0.rating_dev_aesthetics
            contender1_rating = contender1.rating_aesthetics
            contender1_rd = contender1.rating_dev_aesthetics
        else:
            contender0_rating = contender0.rating_complexity
            contender0_rd = contender0.rating_dev_complexity
            contender1_rating = contender1.rating_complexity
            contender1_rd = contender1.rating_dev_complexity
            question_index = 1
        
        #update images database
        #calculate contenders expected score
        contender0.updateRating(question_index, contender0_score, contender1_rating, contender1_rd)
        contender1.updateRating(question_index, contender1_score, contender0_rating, contender0_rd)
        db.session.commit()

        #generate match
        session['end_time'] = datetime.now()
        match_duration = deltatime(session.get('end_time'), session.get('start_time'))
        new_match = Match(user_id = session.get('user_id'), selected_db=session.get('sel_db_index'), question=session.get('q'), contender0=contender0_id, contender1=contender1_id, winner=winner, duration=match_duration)
        db.session.add(new_match)
        db.session.commit()

        contender0.addMatch(question_index,new_match.id)
        contender1.addMatch(question_index,new_match.id)
        db.session.commit()


        print(bcolors.YELLOW+"User id: {}".format(user_id))
        print("Data_base: {}".format(sel_db_index))
        print("Question: {}".format(session.get('q')))
        print("Contenders: {}, {}".format(contender0_id, contender1_id))
        print("Contender0: {}, {}".format(contender0_rating, contender0_rd))
        print("Contender1: {}, {}".format(contender1_rating, contender1_rd))
        print("Winner: {}".format(winner)+bcolors.RESET)

        #add match to user
        user = Voter.query.get(user_id)
        user.add_match(new_match.id)
        db.session.commit()
        session['comp_count'] = session.get('comp_count') + 1
        print("Comparison count = {}".format(session.get('comp_count')))
        print("Voter: {}".format(user))
        print("Match id: {}".format(new_match))
        print('=====Next Finished======')
        #render survey page again
        return redirect(url_for("survey"), code=307)
    else:
        return redirect(url_for("home"))

@app.route("/exit", methods = ["POST", "GET"])
def exit():
    return render_template('exit.html')

@auth.verify_password
def verify(username,password):
    if username == 'SensiLab' and password == 'SensiLabSurvey2021':
        return True
    else:
        return False

if __name__ == '__main__':
    # app.run(debug=False,host="0.0.0.0")
    app.run(debug=True)