from dotenv import load_dotenv  
import os
import requests
import json
import time
import random
import sqlite3
import tkinter as tk


##Using https://opentdb.com/api_config.php to create a trivia game where you can select the number of questions you'd like, the category, and the difficulty. 
##Should allow you to choose from multiple choice questions and selecting the letter associated with the correct answer. 
##Should keep a record of how many you've gotten right and wrong

##GUI work

window = tk.Tk()




window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2, 3], minsize=50, weight=1)

question_view = tk.Label(master=window, text="What is the answer?")
question_view.grid(row=0, columnspan=4, sticky="nsew")

btn_decrease = tk.Button(master=window, text="A")
btn_decrease.grid(row=1, column=0, sticky="nsew")

lbl_value = tk.Button(master=window, text="B")
lbl_value.grid(row=1, column=1, sticky='nsew')

btn_increase = tk.Button(master=window, text="C")
btn_increase.grid(row=1, column=2, sticky="nsew")

btn_d = tk.Button(master=window, text='D')
btn_d.grid(row=1, column=3, sticky="nsew")

##Database connection for keeping highscores

load_dotenv()

con = sqlite3.connect("scoreboard.db")

cur = con.cursor()










## Give an intro to the game and explain the rules

def intro():
    print('Welcome to Crazy Trivia!\n')
    time.sleep(1)
    print("""In a moment you will be given the opportunity to select the number
questions you'd like to be asked and what category those questions come from.
For a list of the categories, type 'help' after being asked for the category. 
Find the number associated with the category you want and choose type it in. \n""")
    
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

    user_score = 0

    for result in trivia['results']:
        data = result
        answer_bank = []
        category = data['category']
        question = data['question']
        answer_bank.append(data['correct_answer'])
        answer_bank.extend(data['incorrect_answers'])
        answer = data['correct_answer'] 
        
        
        print(f'\nThe category is: \n{category}!')
        time.sleep(2)
        print(f'{question}')
        random.shuffle(answer_bank)      
        
        

        if data['type'] == 'multiple':
            answer_a = answer_bank[0]
            answer_b = answer_bank[1]
            answer_c = answer_bank[2]
            answer_d = answer_bank[3]
            print(f'\nA.{answer_a} \nB.{answer_b} \nC.{answer_c} \nD.{answer_d}')
        else:
            answer_a = answer_bank[0]
            answer_b = answer_bank[1]
            print(f'A.{answer_a}, or B.{answer_b}')
            
        user_answer = input('')
        
        if user_answer.lower() == 'a':
            user_answer = answer_a
        elif user_answer.lower() == 'b':
            user_answer = answer_b
        elif user_answer.lower() == 'c':
            user_answer = answer_c
        elif user_answer.lower() == 'd':
            user_answer = answer_d
        else:
            print('That is not an answer')
        
        if user_answer == data['correct_answer']:
            print("That\'s right! 1 point to you.")
            user_score += 1
        else:
            print('That is not the right answer.')
            time.sleep(1)
            print(f'The correct answer is \n{answer}')
        
        time.sleep(2)


    print(f'\nYour score is {user_score}')    

##Get Answers



window.mainloop()
