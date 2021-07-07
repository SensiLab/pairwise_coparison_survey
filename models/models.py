from flask_sqlalchemy import SQLAlchemy
import math

db = SQLAlchemy()

## CONSTANTS
q = 0.00575646273   #constant (magic number to calculate Glicko Ratings?)

## Utility classes/functions
class bcolors:
    GREEN = '\033[92m' #GREEN
    YELLOW = '\033[93m' #YELLOW
    RED = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

##================================
## SQLALCHEMY MODELS
##================================
# A class to store demographic data about participants
class Voter(db.Model):
    __tablename__ = 'voters'
    # __bind_key__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(20), unique=False, nullable=False)
    location = db.Column(db.String(20), unique=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    creativity = db.Column(db.Integer, nullable=False)
    matches = db.Column(db.String, default='')

    # def __init__(self):
    #     try:
    #         self.location = ipInfo(addr=self.ip_address)
    #     except:
    #         self.location = 'NA'

    def __repr__(self):
        return f"Voter('ID: '{self.id}', Location: '{self.location}', Age:'{self.age}', gender:'{self.gender}', experience:'{self.creativity}', matches:'{self.matches}')"
    # @matches.setter
    def add_match(self, match_id):
        self.matches += ';%s' % match_id

class Match(db.Model):
    __bind_key__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    selected_db = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String, nullable=False)
    contender0 = db.Column(db.Integer, nullable=False)
    contender1 = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float, nullable=False)


# CLASS TO STORE DATASETS
class ImageDb(db.Model):
    __abstract__ = True
    file_name = db.Column(db.String(120), unique=True, nullable=False)
    rating_aesthetics = db.Column(db.Float, default=1000)
    rating_dev_aesthetics = db.Column(db.Float, default=350)
    rating_complexity = db.Column(db.Float, default=1000)
    rating_dev_complexity = db.Column(db.Float, default=350)
    matches_aesthetics = db.Column(db.String, default='')
    matches_complexity = db.Column(db.String, default='')
 
    def updateRating(self, question, s, r_other, rd_other):
        # question 0 means aesthetics, 1 means complexity
        # s is the result of comparison (1 if selected, .5 if can't decide, 0 if not selected
        r0 = 0
        rd = 0
        if question == 0:
            r0 = self.rating_aesthetics
            rd = self.rating_dev_aesthetics
        else:
            r0 = self.rating_complexity
            rd = self.rating_dev_complexity
        
        g_rd_other = 1/math.sqrt(1 + (3 * (q**2)*(rd_other**2)/pow(math.pi,2)))
        e_exp = -g_rd_other * (r0 - r_other)/400
        e = 1/(1 + pow(10,e_exp))
        d_square = pow(pow(q,2) * pow(g_rd_other,2)*e*(1-e),-1)
        r = r0 + (q/(1/(pow(rd,2)+(1/d_square))) * g_rd_other * (s - e))

        new_rd = math.sqrt(pow((1/pow(rd,2)+(1/d_square)),-1))

        print(bcolors.GREEN+"Q = {},S = {}, R0 = {}, R = {}, RD = {}, NEW_RD = {}".format(question, s, r0, r, rd, new_rd)+bcolors.RESET)

        if question == 0:
            self.rating_aesthetics = r
            self.rating_dev_aesthetics = new_rd
        else:
            self.rating_complexity = r
            self.rating_dev_complexity = new_rd
    
    def addMatch(self, question, match_id):
        if question == 0:
            self.matches_aesthetics+=';%s' % match_id
        else:
            self.matches_complexity+=';%s' % match_id


# A class to store data about the 3D printable organisms database
class ImgSet1(ImageDb):
    __table_name__ = 'imh_set1'
    __bind_key__ = 'img_set1'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"Img Db: '{self.__bind_key__}'('{self.file_name}', AR:'{self.rating_aesthetics}', CR:'{self.rating_complexity}')"

# A class to store data about the linedrawings database
class ImgSet2(ImageDb):
    __table_name__ = 'img_set2'
    __bind_key__ = 'img_set2'
    id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return f"Img Db: '{self.__bind_key__}'('{self.file_name}', AR:'{self.rating_aesthetics}', CR:'{self.rating_complexity}')"