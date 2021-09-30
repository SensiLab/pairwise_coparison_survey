from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models.models import Voter, Match, ImgSet1, ImgSet2, db
from app import app
from os import listdir
from os.path import join, isdir, isfile


# Create all the necessary databases
# voters.db, img_setN.db, matches.db
with app.app_context():
    db.create_all()

root_path1 = 'static/imgs/img_set1/'
file_names_img_set1 = []
for f in listdir(root_path1):
    if '.DS_Store' not in f:
        fn = join('img_set1/',f)
        file_names_img_set1.append(fn)

root_path2 = 'static/imgs/img_set2/'
file_names_img_set2 = []
for f in listdir(root_path2):
    if '.DS_Store' not in f:
        fn = join('img_set2/',f)
        file_names_img_set2.append(fn)

print("Databases successfully created")
