from sqlalchemy import create_engine
from Configurations.config import Base, engine,db_session
Base.metadata.create_all(engine)
import pandas as pd
from models import Progress, Topics, User
from Exceptions.LoginError import LoginError
from Exceptions.RecordNotFound import RecordNotFound


def populate_topics():
    df = pd.read_csv('topics_data.csv')
    df.to_sql('topics', con=engine,if_exists='append',index=False)
    print ("done!")


def create_admin():
    new_user=User(name="Arooj", password="10MixDb", role="Admin")
    db_session.add(new_user)
    db_session.commit()
    print("admin created")



def create_acc(username, password):
    new_user = User(name=username,password=password)
    db_session.add(new_user)
    db_session.commit()
    print("***User added u can login now!***")
    handle_user_login_or_signup()


def login(username, password):
    try:
        users = db_session.query(User).all()
        for u in users:

            if(username==u.name and password==u.password):
                print(f"welcome {u.name}")
                return (u.user_id)
       
        raise LoginError("incorrect username or password")

    except LoginError as e:
        print(e.message)
    

print("outside main")
def display_topics():
    df = pd.read_sql("SELECT * FROM TOPICS",con=engine)
    print(df)
def add_topic(user_id):
    display_topics()
    user_resp = input("what title would u like to track?")
    try:
        title_record = db_session.query(Topics).filter_by(title=user_resp).first()
        if(db_session.query(Topics).filter_by(title=user_resp).first()is None):
            raise RecordNotFound(f"{user_resp} not found in Database please choose a title that exists")
        else:
            topic_id = title_record.topic_id
            p = Progress(user_id = user_id,topic_id=topic_id,completed= False, not_started= True, in_progress=False)
            db_session.add(p)
            db_session.commit()


            userProgress = db_session.query(Progress).filter_by(user_id=user_id).all()
            print(userProgress)
            print(f"your progress '\n'{userProgress}")
            display_user_progress(user_id)
    except RecordNotFound as e:
        print(e)

    
def update_progress(user_id):
    u_topic_id=input("What topic will you like to update? enter topic id please.")
    topic_progress=db_session.query(Progress).filter_by(topic_id=u_topic_id).first()
    completed= False
    not_started=False
    in_progress=False
    completed_input = input("is it completed?y/n").lower()
    if(completed_input=='y'):
        completed=True
    elif (completed_input=='n'):
        completed=False
    
    not_started_input = input("did u start it?y/n").lower()
    if(not_started_input=='y'):
        not_started=False
    elif(not_started_input=='n'):
        not_started=True
   
    in_progress_input = input("is it in progress?y/n").lower()
    if(in_progress_input=='y'):
        in_progress=True
    elif(in_progress_input=='n'):
        in_progress=False
  
    topic_progress.update_progress(completed,not_started,in_progress,db_session)
    print("completed,not_started,in_progress,db_session")
    print(completed,not_started,in_progress,db_session)
    print("added?")


def display_user_progress(user_id):
    u = db_session.query(User).filter_by(user_id=user_id).first()
    p = db_session.query(Progress).filter_by(user_id = user_id).all()
    u_p = db_session.query(Topics,Progress).join(Topics,Progress.topic_id == Topics.topic_id).filter(Progress.user_id==user_id).all()
    print("your progress:")
    for topic,progress in u_p:
        print(f"TOPICS INVENTORY:'\n'Topic Id: {progress.topic_id} Type: {topic.type}, Title: {topic.title} '\n'PROGRESS:'\n'Completed: {progress.completed}, Not Started: {progress.not_started}, In Progress: {progress.in_progress}")

    user_input = input("want to add a topic?(y/n)")
    if(user_input=='y'):
        add_topic(user_id)
    if(user_input=='n'):
        user_input = input("want to update progress?(y/n)")
        if(user_input=='y'):
            update_progress(user_id)
        else:
            exit


def handle_user_login_or_signup():
    loggedIn=False
    user_id = 0
    user_selection = input("do you have an account(y/n)")
    if(user_selection == 'n'):
        u=input("Choose username: ")
        p = input("Choose pass:")
        
        create_acc(u,p)
    if(user_selection == 'y'):
        u=input("Username: ")
        p=input("Password: ")
        user_id=login(u,p)
        if(user_id!=None):
            loggedIn=True
        print("inside if u id",user_id)

    print("outside if u id",user_id)
    if(loggedIn==True):
        print("*"*60)
        print("WELCOME to your account. What would u like to do today?")
        print("*"*60)
        user_resp=input("Display Progress(d)    Update Progress(u)     Add Topic to Track(a)").lower()
        if user_resp=='d':
            display_user_progress(user_id)
        if user_resp == 'u':
            update_progress(user_id)
        if(user_resp=='a'):
            add_topic(user_id)



if __name__ == "__main__":


    #populate_topics()
    #create_admin()
    print("WELCOME TO PROGRESS TRACKER")
    print("MENU:")
    user_selection=input(("login/signup (l)          browse topics(b)")).lower()
    if(user_selection=='l'):
       handle_user_login_or_signup()
    

    if(user_selection=='b'):
        display_topics()
        

    


    

        
   
    
