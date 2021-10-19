# Online Pairwise comparison system

## Overview
This repository contains al the required files to deploy a simple pairwise image comparison web application. This app was developed using the Flask "micro-framework" in the back end, and a combination of HTML, Bootstrap and Javascript for the UI.

To perform the pairwise comparison we used a modified version of Professor Mark Glickman's [Glicko System](http://www.glicko.net/glicko/glicko.pdf), in which each image starts with a score, which increases or decreases based on how they fare against other images in a given dataset. By the end of the comparison cycle (i.e. when all images have been compared at least once), they are ranked based on their score.


<!-- ## Table of contents -->
<!-- 
In this readme file we provide information regarding two main aspects of this project:
- Pairwise comparison method implementation
- How to use the app  -->

<!-- ## Pairwise comparison method
The development of this app responded to a specific research goal: we needed to quickly determine how computer generated abstract images  were perceived by humans in terms of their complexity and aesthetics.

Given the characteristics of our image datasets we opted for a pairwise comparison method, as it would give us a notion of how the images were perceived in relationship to other images in the same dataset, and also it makes the decision-making process easier for the participant, as all decisions are made in context. -->

## How the app works
From a participant's perspective, the app is simple: The landing page is accessed, minimal demographic information is entered (age range, gender, experience with visual arts) and then the survey starts by showing the participant two images from the same dataset, and one of two possible prompts: which one of these images do you like the most/ or, which one of these images is more complex?

<!-- Images are selected by clicking on them, but no data is recorded until the participant hits the "next" button -->

<!-- In the background the app is set to select  -->


<!-- ### Glicko system
To rank the images we used a modified version of Professor Mark Glickman's [Glicko System](http://www.glicko.net/glicko/glicko.pdf), which extends the [Elo Rating System](https://en.wikipedia.org/wiki/Elo_rating_system) by introducing a measure of certainty associated to each individual's rating, based on the number of times it has been evaluated, and the time between evaluations.

In our implementation, assuming that the quality of an image won't change over time, we disregard the influence of time on the certainty of the ratings.

We impleme

```python
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
```
We introduced two small modifications that respond to the nature of the material being compared. The Glicko System was designed to rank human chess players based on the results of matches against other players. The underlying assumption is that if a player has not played any matches for a while,, and it assumes that  -->

## Installation (as a local server for testing)

- Clone the repository to your local drive
- Create a virtual environment and install dependencies using the provided requirements.txt file
- Copy your images to /static/img_set1
- Create databases using db_creation.py script:
  - If you are using one image set, comment out line 57 in app.py and lines 21 to 26 (both included) in db_creation.py
- Deploy server by running app.py (The server is set up by default to run in debug mode.)
  - To access the app, open a web browser and go to localhost:5000
  - To close the app, use ctrl+c on your terminal (this will kill the Flask server)

## Usage
- To bias the selection of questions, comment out line 142 in app.py, uncomment line 143 and set the value of question to 0 for aesthetics and 1 for complexity.

## Credits

## License