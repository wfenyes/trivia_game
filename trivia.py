from dotenv import load_dotenv  
import os
import requests
import json
import time
import random
import mysql.connector


##Using https://opentdb.com/api_config.php to create a trivia game where you can select the number of questions you'd like, the category, and the difficulty. 
##Should allow you to choose from multiple choice questions and selecting the letter associated with the correct answer. 
##Should keep a record of how many you've gotten right and wrong

##Database connection
load_dotenv()

host_info = os.getenv("host_info")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host=host_info,
    user=db_user,
    passwd=db_password
)

mycursor = mydb.cursor()

for db in mycursor:
    print(db)


## Give an intro to the game and explain the rules

def intro():
    print('Welcome to Crazy Trivia!')
    time.sleep(1)
    print("""In a moment you will be given the opportunity to select the number
          questions you'd like to be asked and what category those questions come from.
          For a list of the categories, type 'help' after being asked for the category. 
          Find the number associated with the category you want and choose type it in. """)
    
    while True:
        user_begin = input('Are you ready to begin?\n')
        if user_begin.lower() == 'yes':
            get_questions()
            break
        elif user_begin.lower() == 'no':
            time.sleep(1)
            print("Maybe another time then.")
            exit()
        else:
            time.sleep(1)
            print("I'm sorry, I don't understand. Please type yes or no when prompted.")
            continue

##prints the options for the categories

def print_category_options():
    print('Here are the category options')
    
    cat_list_response = requests.get('https://opentdb.com/api_category.php')
 
    available_categories = json.loads(cat_list_response.text)
    

    for x in available_categories['trivia_categories']:
        print(f'{x["id"]} {x["name"]}')

##Used in get_questions() to build the URL for the request

def construct_url():
    number_of_questions = input('How many questions would you like? (1-10)\n')
    
    while True:
        category_choice = input('What category would you like? \n')

        if category_choice.lower() == 'help':
            print_category_options()
        else:
            break
        
        
    url = 'http://opentdb.com/api.php?'

        
    return f'http://opentdb.com/api.php?amount={number_of_questions}&category={category_choice}&difficulty=easy'

##Gets and asks questions

def get_questions():
    x = requests.get(construct_url())
                    
    trivia = json.loads(x.text)

    for result in trivia['results']:
        data = result
        answer_bank = []
        category = data['category']
        question = data['question']
        answer_bank.append(data['correct_answer'])
        answer_bank.extend(data['incorrect_answers'])
        answer = data['correct_answer'] 
        
        
        print(f'The first category is: \n{category}!')
        time.sleep(2)
        print(f'{question}')
        random.shuffle(answer_bank)      
        
        
        if data['type'] == 'multiple':
            print(f'A.{answer_bank[0]}, B.{answer_bank[1]}, C.{answer_bank[2]}, or D.{answer_bank[3]}')
        else:
            print(f'A.{answer_bank[0]}, or B.{answer_bank[1]}')
        
        user_answer = input('')
        time.sleep(2)
        print(f'The correct answer is \n{answer}')
        time.sleep(2)

"""
x = requests.get('http://opentdb.com/api.php?amount=1&category=9&difficulty=easy')

response = json.loads(x.text)

print(response)

"""



