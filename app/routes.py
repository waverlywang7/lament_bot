# Authors: CS-World Domination Summer19 - JG
try:
    from flask import render_template
except:
    print("Make sure to pip install Flask twilio")
from app import app


from apscheduler.schedulers.background import BackgroundScheduler
from app import bot_code


animal = "Not generated yet"
poem = "Not generated yet"
def bot_job():
    global animal 
    global poem
    
    animal, poem = bot_code.bot_code()
    article = open("app/animal_of_the_day.txt", "w")
    article.write(animal)
    article2 = open("app/poem_of_the_day.txt", "w")
    article2.write(poem)
    article2.close()
    return animal,poem

sched = BackgroundScheduler()
sched.start() 
sched.add_job(bot_job, trigger='cron', hour='8', minute='0')


@app.route('/animal_read')
def read_file_for_animal():
    #reads a file and returns the animal
    file1 = open('app/animal_of_the_day.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        if line != "":
            return line


@app.route('/poem_read')
def read_file_for_poem():
    #reads a file and returns the poem
    file1 = open('app/poem_of_the_day.txt', 'r')
    Lines = file1.readlines()
   
    for line in Lines:
        if line != "":
            return line



# # Home page, renders the index.html template
@app.route('/index',methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    global animal
    global poem
    # file1 = open('app/animal_of_the_day.txt', 'r')
    # Lines = file1.readlines()
    # for line in Lines:
    #     if line != "":
    #         animal = line
    # file1 = open('app/poem_of_the_day.txt', 'r')
    # Lines = file1.readlines()
    # for line in Lines:
    #     if line != "":
    #         poem = line
    return render_template('index.html', title= 'Home', animal=animal+"weeee", poem=poem)

@app.route('/about')
def about():
    return render_template('about.html')






