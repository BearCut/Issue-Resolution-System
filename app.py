import pymysql as sql
import hashlib
import os
from prettytable import PrettyTable
from random import randint

connection = sql.connect(
    host="127.0.0.1",
    port = 3306,
    user="root",
    password="ItsNotRoot",
    database="irs",
    autocommit="True"
)

cursor = connection.cursor()

def yn(prompt):
    answer = input("\033[1;31m{}[y/n]\033[1;36m".format(prompt))
    if answer == 'y':
        return True
    else:
        return False

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

def hash(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def register(userid,name,password,gender,contactno,address):
    try:
        if not userid or not name or not password or not gender or not contactno or not address:
            input("\033[1;31mAll fields are required!")
            return
        if gender not in ["M", "F"]:
            input("\033[1;31mInvalid gender input. Please enter M or F.")
            return
        else:
            sqlregq = "INSERT INTO userid (userid, uname, gender, contactno, address, passhash) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
            cursor.execute(sqlregq.format(userid,name,gender,contactno,address,hash(password)))
            input("\033[1;32mAccount Successfully Registered. Please Login-")
    except Exception as e:
        print(f"An error occurred: {e}")

def input_issue(id,issueid,title,desc):
    try:
        query = 'INSERT INTO issue (issue_id, userid, title, description_, status_) VALUES ("{}","{}","{}","{}","{}");'
        cursor.execute(query.format(issueid,id,title,desc,"Open"))
        input("\033[1;32mYour Issue id successfully submitted. Please note your issue ID:-"+str(issueid))
    except Exception as e:
        input   (f"An error occurred: {e}")
    
def authorize_user(user_id, input_password):
    connection = None
    try:
        # Fetch the password hash for the given user ID
        query = "SELECT passhash FROM userid WHERE userid = '{}'"
        cursor.execute(query.format(user_id))
        result = cursor.fetchone()

        if result:
            stored_hash = result[0]
            input_hash = hash(input_password)
            # Compare the input hash with the stored hash
            if input_hash == stored_hash:
                input("\033[1;32mAuthorization successful!")
                authorization = user_id
                return authorization
            else:
                input("\033[1;31mInvalid password. Please try again.")
                return False
        else:
            input("\033[1;31mUser not found. Please register first.")
            return False

    except Exception as e:
        input(f"\033[1;31mAn error occurred: {e}")
        return False

def fetch_user_issues(user_id):
    try:
        # SQL query to fetch issues for the specified userid
        query = "SELECT issue_id,title,description_,created_at,status_ FROM issue WHERE userid = '{}';"
        cursor.execute(query.format(user_id))
        
        # Fetch all results
        issues = cursor.fetchall()
        
        table = PrettyTable()
        table.field_names = ["Issue ID","Title","Details","Date","Status"]

        # Check if any issues were found
        if not issues:
            input("\033[1;31mNo issues found for this user.")
            return
        
        # Print each issue in a formatted table
        for issue,tit,des,date,status  in issues:
            table.add_row([issue,tit ,des,date,status])
        input(table)

    except Exception as e:
        print(f"An error occurred: {e}")

intro = """
 \033[1;36m
 __       _______.     _______. __    __   _______                                                      
|  |     /       |    /       ||  |  |  | |   ____|                                                     
|  |    |   (----`   |   (----`|  |  |  | |  |__                                                        
|  |     \   \        \   \    |  |  |  | |   __|                                                       
|  | .----)   |   .----)   |   |  `--'  | |  |____                                                      
|__| |_______/    |_______/     \______/  |_______|                                                     
                                                                                                        
.______       _______     _______.  ______    __       __    __  .___________. __    ______   .__   __. 
|   _  \     |   ____|   /       | /  __  \  |  |     |  |  |  | |           ||  |  /  __  \  |  \ |  | 
|  |_)  |    |  |__     |   (----`|  |  |  | |  |     |  |  |  | `---|  |----`|  | |  |  |  | |   \|  | 
|      /     |   __|     \   \    |  |  |  | |  |     |  |  |  |     |  |     |  | |  |  |  | |  . `  | 
|  |\  \----.|  |____.----)   |   |  `--'  | |  `----.|  `--'  |     |  |     |  | |  `--'  | |  |\   | 
| _| `._____||_______|_______/     \______/  |_______| \______/      |__|     |__|  \______/  |__| \__| 
                                                                                                        
.______     ______   .______     .___________.    ___       __                                          
|   _  \   /  __  \  |   _  \    |           |   /   \     |  |                                         
|  |_)  | |  |  |  | |  |_)  |   `---|  |----`  /  ^  \    |  |                                         
|   ___/  |  |  |  | |      /        |  |      /  /_\  \   |  |                                         
|  |      |  `--'  | |  |\  \----.   |  |     /  _____  \  |  `----.                                    
| _|       \______/  | _| `._____|   |__|    /__/     \__\ |_______|
"""
option_i="""
\033[1;31mPlease Select One Option:
\033[1;32mLogin - \033[1;36mAlready Have an account ------> \033[1;31m1
\033[1;32mRegister - \033[1;36mMake an account -----------> \033[1;31m2
\033[1;32mExit - \033[1;36mDon't want to make an account--> \033[1;31m3
\033[0m
"""
dashboard = '''\033[1;31m
 _______       ___          _______. __    __ .______     ______        ___     .______       _______     
|       \     /   \        /       ||  |  |  ||   _  \   /  __  \      /   \    |   _  \     |       \    
|  .--.  |   /  ^  \      |   (----`|  |__|  ||  |_)  | |  |  |  |    /  ^      |  |_)  |    |  .--.  |   
|  |  |  |  /  /_\  \      \   \    |   __   ||   _  <  |  |  |  |   /  /_\  \  |      /     |  |  |  |   
|  '--'  | /  _____  \ .----)   |   |  |  |  ||  |_)  | |  `--'  |  /  _____  \ |  |\  \----.|  '--'  |   
|_______/ /__/     \__\|_______/    |__|  |__||______/   \______/  /__/     \__\| _| `._____||_______/    
'''
option_d ='''                                                                                                             
\033[1;31mPlease Select One Option:
\033[1;32mAdd Issue - \033[1;36m------------------> \033[1;31m1
\033[1;32mCheck Issue Submitted - \033[1;36m------> \033[1;31m2
\033[1;32mExit - \033[1;36m-----------------------> \033[1;31m3

'''

while True:
    clear_screen()
    print(intro)
    print(option_i)
    inputPrompt = "\033[1;32mapp.py->\033[1;31m  "
    mainoption = input(inputPrompt)
    if mainoption == '1':
        while True:
            clear_screen()
            print(intro)
            print("\033[1;31mLOGIN-Please Provide the details")
            userid = input("\033[1;32mUserId---------> \033[1;31m")
            password = input("\033[1;32mPassword-------> \033[1;31m")
            authorized_id = authorize_user(userid,password)
            if authorized_id != False:
                break
        break
    elif mainoption == '2':
        consent = False
        while consent == False:
            clear_screen()
            print(intro)
            print("\033[1;31mREGISTER-Please Provide the details")
            userid = input("\033[1;32mUserId---------> \033[1;31m")
            password = input("\033[1;32mPassword-------> \033[1;31m")
            name = input("\033[1;32mName-----------> \033[1;31m")
            Gender = input("\033[1;32mGender[M/F]----> \033[1;31m")
            contactno = input("\033[1;32mContact No.----> \033[1;31m")
            address = input("\033[1;32mAddress--------> \033[1;31m")
            consent = yn('Is The Data Correct?')
        register(userid,name,password,Gender,contactno,address)
    
    elif mainoption == '3':
        exit()
        print("\033[37mBYE")

    else:
        input("\033[1;31mPlease Enter A VALID Response")
while True:
    clear_screen()
    print(dashboard)
    print(option_d)
    mainoption = input(inputPrompt)
    if mainoption == '1':
        consent = False
        while consent == False:
            clear_screen()
            print(intro)
            print("\033[1;31mREGISTER-Please Provide the details")
            title = input("\033[1;32mSubject------------------------------> \033[1;31m")
            descr = input("\033[1;32mPlease Describe Your Issue In datails> \033[1;36m \n")
            consent = yn('You Sure Bro?')
            issueid = randint(1000000000, 9999999999)
            input_issue(authorized_id,issueid,title,descr)  
    if mainoption == '2':
        fetch_user_issues(authorized_id)
    if mainoption == '3':
        exit()
        print("\033[37mBYE")

