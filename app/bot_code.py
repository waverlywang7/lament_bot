import os
import openai
import tweepy


# importing os module 
import os
  
from dotenv import load_dotenv, find_dotenv
from dotenv import dotenv_values
import requests


from requests_oauthlib import OAuth1
import re

import pandas as pd



# Load environment variables from .env file
load_dotenv(find_dotenv("app/.env"))

# Set up logging
print("Starting Twitter bot")


# Read Twitter API and chat credientials

openai.api_key = os.environ.get("OPENAI_API_KEY")
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

def get_animal():
    #takes in csv of extinct animals and picks an animal from the red list csv file, checks a animal.txt file
    # which contains a list of animals that have already been tweeted about
   
    df=pd.read_csv("app/redlist_species_data_7809d9c8-6a5a-4577-933e-a348de6d7343/assessments.csv")
    specific_column=df["scientificName"] # get the row of the scientific name
    no_animal = "No animal left"
    for row in specific_column:
        # Using readlines()
        file1 = open('app/animals.txt', 'r')
        Lines = file1.readlines()
        animal_lookup = row + "\n"
        #check if we already have tweeted about the animal
        if animal_lookup not in Lines: 
            animal = row 
            file1 = open("app/animals.txt", "w")
            written_animal = f"{animal}\n"
            file1.writelines(Lines)
            file1.write(written_animal)
            file1.close()
            return animal
        else:
            df=pd.read_csv("app/redlist_species_data_7809d9c8-6a5a-4577-933e-a348de6d7343/taxonomy.csv")
            specific_column=df["scientificName"] # get the row of the scientific name
            no_animal = "No animal left"
            for row in specific_column:
                # Using readlines()
                file1 = open('app/animals.txt', 'r')
                Lines = file1.readlines()
                animal_lookup = row + "\n"
                #check if we already have tweeted about the animal
                if animal_lookup not in Lines: 
                    animal = row 
                    file1 = open("app/animals.txt", "w")
                    written_animal = f"{animal}\n"
                    file1.writelines(Lines)
                    file1.write(written_animal)
                    file1.close()
                    return animal

    return no_animal


def generate_image(query):
    #takes in a query and generates an image. 

    print("Scraping Google Image") 
    os.chdir("Google-Image-Scraper") # change direectory
    os.system(f"python3 main.py --query \'{query}\'") 
    os.chdir("..")

    
    folder = "Google-Image-Scraper/photos" + "/" + query
    for root, dirs, files in os.walk(folder, topdown=True):
        for name in files: 
            f = os.path.join(root, name)
            ext = os.path.splitext(f)[-1].lower()
            # Now we can simply use == to check for equality, no need for wildcards.
            if (ext != ".jpeg") and (ext != ".jpg") and (ext != ".png") and (ext != ".JPG"):
                print(f, "Not a picture. will remove")
                os.remove(f)
            else:
                return f # choose the first pic that is an actual image
  

def chat_with_chatgpt(prompt, model="text-davinci-003"):
    # chats with chatgpt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def generate_poem(chosen_animal):
    animal = chosen_animal
  
    prompt = f"Create a poem under 280 characters for the {animal} that has gone extinct and include the species name, and common name if possible, and include only salient details about the species and try to show, instead of tell and include #TwitterBot and #ChatGPT"
    print(f"prompt: {prompt}")
    response = chat_with_chatgpt(prompt) 


    # TODO: add a hashtag. 
    while len(response) > 280:    
        print("This is longer than 280 characters\n")
        print("Let's regenerate the poem")
        prompt = f"Make the following response shorter than 280 characters:{response}"
        new_response = chat_with_chatgpt(prompt)
        response = new_response 
        print("here is the new response", response)
    # TODO: check for 280 characters.
    split_response = response.split()
    if split_response[0] == "Poem":
        x = response.split("Poem")
        response = x[1]
    elif split_response[0] == "Poetry":
        x = response.split("Poetry")
        print(response.split("Poetry"))
        response = x[1]


    # pick an animal on here. 
    return response

def format_fact(fact):
    return {"text": "{}".format(fact)}


def connect_to_oauth(consumer_key, consumer_secret, access_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    return url, auth

def upload_text(poem):
    payload = {
        "text": "{}".format(poem),
        }
    return payload

def upload_media(poem, query):
    tweepy_auth = tweepy.OAuth1UserHandler(
        "{}".format(os.environ.get("API_KEY")),
        "{}".format(os.environ.get("API_SECRET")),
        "{}".format(os.environ.get("ACCESS_TOKEN")),
        "{}".format(os.environ.get("ACCESS_TOKEN_SECRET")),
    )
    tweepy_api = tweepy.API(tweepy_auth)
    image_path = generate_image(query)

    
    post = tweepy_api.simple_upload(image_path)
    text = str(post)
    media_id = re.search("media_id=(.+?),", text).group(1)

    payload = {
        "text": "{}".format(poem),
        "media": 
        {"media_ids": ["{}".format(media_id)]}
        }
    payload = {
         "text": "{}".format(poem)
        }
    os.remove(image_path)
    return payload
    
def bot_code():
    animal = get_animal()

    print(f"The chosen animal is {animal}\n")
    poem = "poem about " + animal
    #TODO: activate later! and uncomment
    # poem = generate_poem(animal)
 
    print(f"The generated chat-gptpoem is {poem}\n")
    
    #TODO: activate later! and uncomment
    # payload = upload_text(poem)

    # url, auth = connect_to_oauth(
    #     consumer_key, consumer_secret, access_token, access_token_secret
    # )
    # request = requests.post(
    #     auth=auth, url=url, json=payload, headers={"Content-Type": "application/json"}
    # )
    print(f"Wrote a tweet: {poem}")
    
    return animal, poem

# if __name__ == "__main__":
#     main(self)