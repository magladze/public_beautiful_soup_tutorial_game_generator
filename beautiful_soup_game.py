# Import necessary libraries
import sqlite3
import random
import ast

# Instantiate the AI assistant
# Instantiate the AI assistant
from openai import OpenAI
client = OpenAI()

#function to send prompts to openAI
def get_one_answer(user_question):

    prompt = user_question

    messages_config = [
                    {"role": "user", "content": prompt},
                ]

    response = client.chat.completions.create(
                          model="gpt-3.5-turbo-0125",
                        messages=messages_config,
                        max_tokens=4000,
                        temperature=0.5
                        )



# Connect to SQLite database
conn = sqlite3.connect('beautifulsoup_learning.db')
c = conn.cursor()

# Create tables if not exists
c.execute('''CREATE TABLE IF NOT EXISTS user_progress (
                username TEXT PRIMARY KEY,
                exercises_completed INTEGER,
                lessons_completed INTEGER,
                quizzes_completed INTEGER
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY,
                lesson_text TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY,
                exercise_text TEXT,
                exercise_category TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                quiz_question TEXT,
                quiz_answer TEXT
            )''')

# Function to handle user registration
def register_user():
    username = input("Enter your username: ")
    c.execute("INSERT OR IGNORE INTO user_progress (username, exercises_completed, lessons_completed, quizzes_completed) VALUES (?, 0, 0, 0)", (username,))
    conn.commit()
    return username

# Function to get random exercise
def get_random_exercise():
    c.execute("SELECT exercise_text FROM exercises ORDER BY RANDOM() LIMIT 1")
    exercise = c.fetchone()[0]
    print("Exercise: ", exercise)
    answer = input("Enter your answer: ")
    # Log the result
    # Code to log the result in the database

# Function to get random lesson
def get_random_lesson():
    c.execute("SELECT lesson_text FROM lessons ORDER BY RANDOM() LIMIT 1")
    lesson = c.fetchone()[0]
    print("Lesson: ", lesson)

# Function to get random example code
def get_random_example():
    c.execute("SELECT exercise_text FROM exercises ORDER BY RANDOM() LIMIT 1")
    example_code = c.fetchone()[0]
    print("Example Code: ", example_code)



# Function to take True/False quiz
def take_quiz():
    c.execute("SELECT quiz_question, quiz_answer FROM quizzes ORDER BY RANDOM() LIMIT 1")
    quiz_question, quiz_answer = c.fetchone()
    user_answer = input("True or False: " + quiz_question)
    if user_answer.lower() == quiz_answer.lower():
        print("Correct!")
    else:
        print("Incorrect!")
    # Log the result
    # Code to log the result in the database



#---------------------------------
#content generation examples below
#---------------------------------

def generate_lesson_plan(num_lessons=10):
    string_response = get_one_answer('generate a list of 10 distinct topics in beautiful soup and return it in python list format, make sure the response is in the format ["a","b","c",]')
    list_topics = ast.literal_eval(string_response)

    for i in list_topics:
        string_response2 = get_one_answer(f'generate a tutorial of beautifulsoup that relate to the topic -- {i} ')
        lesson = ast.literal_eval(string_response2)
        lesson_content = f"Topic: {i}\n\n LESSON: {lesson}"
        c.execute("INSERT INTO lessons (lesson_text) VALUES (?)", (lesson_content,))
        conn.commit()

def generate_example_code(num_snippets=20):
    string_response = get_one_answer("""
    generate an example code snippet showcasing BeautifulSoup functionality, and the category of the functiinality 
    and return it in python list format, with each item in the list being at tuple,
    make sure the response is in the format ["(a1,a1_category)","(b2,b2_category)","(c3,c3_category)",]
    """)
    list_of_snippets = ast.literal_eval(string_response)
    for i in list_of_snippets:
        c.execute("INSERT INTO exercises (exercise_text, exercise_category) VALUES (?, ?)", (i[0], i[1]))
        conn.commit()

def generate_quiz_content():
    string_response = get_one_answer("""
    generate a list of 50 quiz questions related to BeautifulSoup with answers as True or False and  return it in python list format, with each item in the list being at tuple,
    make sure the response is in the format ["(a1,a1_category)","(b2,b2_category)","(c3,c3_category)",]
    """)
    quiz_questions = ast.literal_eval(string_response)
    for i in quiz_questions:
        c.execute("INSERT INTO quizzes (quiz_question, quiz_answer) VALUES (?, ?)", (i[0],i[1] ))
        conn.commit()

# Call the content generation functions if you want to populate a sample db

#-------------------------------------------------------------------------------------------------------------
#NOTE -- you may need to parse differently than shown above in order to extract values returned by AI endpoint
#-------------------------------------------------------------------------------------------------------------
# generate_lesson_plan()
# generate_example_code()
# generate_quiz_content()







# User interface loop
while True:
    print("Choose an option:")
    print("1. Get a random exercise to practice using BeautifulSoup Library.")
    print("2. Get a random lesson about using BeautifulSoup.")
    print("3. Get a random example code that showcases BeautifulSoup functionality.")
    print("4. Take a True/False quiz based on BeautifulSoup library.")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        get_random_exercise()
    elif choice == '2':
        get_random_lesson()
    elif choice == '3':
        get_random_example()
    elif choice == '4':
        take_quiz()
    else:
        print("Invalid choice. Please choose again.")

    # Option to continue or exit
    another = input("Do you want to continue? (yes/no): ")
    if another.lower() != 'yes':
        break

# Close the database connection
conn.close()