from flask import Flask, render_template, request, session,redirect, url_for,flash
from Configurations.config import Base, engine,db_session
Base.metadata.create_all(engine)
import pandas as pd
from models import Progress, Topics, User
from Exceptions.LoginError import LoginError
from Exceptions.DuplicateEntry import DuplicateEntry
from Exceptions.RecordNotFound import RecordNotFound
from functools import wraps

app = Flask(__name__)
app.secret_key='Crystal'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method=='POST'):
        username=request.form['username']
        password=request.form['password']
        try:
            users = db_session.query(User).all()
            for u in users:

                if(username==u.name and password==u.password):
                    session['user_id']=u.user_id
                    session['role']=u.role
                    #print(f"welcome {u.name}")
                    return redirect(url_for('dashboard'))
        
            raise LoginError("Incorrect username or password! Try again or signup.")

        except LoginError as e:
            error=e.message
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods = ['GET','POST'])
def signUp():
 
    if(request.method=='POST'):
        username=request.form['username']
        password=request.form['password']
        try:
            existing_user = db_session.query(User).filter_by(name=username).first()
            if existing_user:
                raise DuplicateEntry("Username already exists. Please choose a different username")
             

            new_user = User(name=username,password=password)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('login'))
            
        except DuplicateEntry as e:
            error = e.msg
            return render_template('signUp.html', error=error)
            
    return render_template('signUp.html')
        
       

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id=session['user_id']

        user=db_session.query(User).filter_by(user_id=user_id).first()
        return render_template('dashboard.html',user=user)
    
    return redirect(url_for('login'))


@app.route('/displayProgress')
def display_user_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    u = db_session.query(User).filter_by(user_id=user_id).first()
    p = db_session.query(Progress).filter_by(user_id = user_id).all()
    u_p = db_session.query(Topics,Progress).join(Topics,Progress.topic_id == Topics.topic_id).filter(Progress.user_id==user_id).all()
    if not u_p:
        msg="You have no topics added. Please add topics so you can track their progress here."
        return render_template('displayProgress.html',u_p=u_p,msg=msg)        
    return render_template('displayProgress.html',u_p=u_p)

@app.route('/updateProgress', methods=['POST', 'GET'])

def updateProgress():
    success="Updated!"
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id=session['user_id']
    u_p = db_session.query(Topics,Progress).join(Topics,Progress.topic_id == Topics.topic_id).filter(Progress.user_id==user_id).all()
    if not u_p:
        msg="Currently you do not have any topics to update progress of. Please add topic before you update progress."
        return redirect(url_for('addTopic',msg=msg))
    completed= False
    not_started=False
    in_progress=False
    print("*"*50)
    print(type(u_p))
    user_topic_ids=[]
    for i in u_p:
        user_topic_ids.append(i.Progress.topic_id)
        print(type(i.Progress.topic_id))
    
    print("Session user_id:", session.get('user_id'))


    try:
        if(request.method=='POST'):
   
                topic_id = int(request.form['topic_id'])
               
                print(type(topic_id))
                print("topic_id:", topic_id)
                if(topic_id not in user_topic_ids):
                    raise RecordNotFound(f"Topic id '{topic_id}' does not exist. Please add a topic id that is listed under your topic ids.")
                else:
                    print("yes topic id exists!!")

                    completed_f = request.form['completed']
                    if(completed_f=='True'):
                        completed=True
                    elif (completed_f=='False'):
                        completed=False

                    not_started_f=request.form['not_started']
                    if(not_started_f=='True'):
                        not_started=True
                    elif(not_started_f=='False'):
                        not_started=False

                    in_progress_f=request.form['in_progress']
                    if(in_progress_f=='True'):
                        in_progress=True
                    elif(in_progress_f=='False'):
                        in_progress=False

                    curr_progress=db_session.query(Progress).filter(Progress.topic_id==topic_id, Progress.user_id==user_id).first()
                    print("CURRENT PROGRESS")
                    print(curr_progress)
                    print(type(curr_progress))
                    curr_progress.update_progress(completed,not_started,in_progress,db_session)
    
                 
    except RecordNotFound as e:
            error= e.message
            return render_template('updateProgress.html',error=error,u_p=u_p)

    return render_template('updateProgress.html',u_p=u_p)
  
@app.route('/displayTopics', methods=['POST','GET'])
def displayTopics():
    df = pd.read_sql("SELECT * FROM TOPICS",con=engine)
    df_records = df.to_dict(orient='records')
    if request.method=='POST':
        
        print("here2")
        user_input=request.form.get('user_input')
        
        if(user_input=='Song'):

            song_df=pd.read_sql("select * from Topics where type='Song'",con=engine)
            song_record=song_df.to_dict(orient='records')
            return render_template('displayTopics.html',df=song_record)
        if(user_input=='TV Show'):
           
            show_df=pd.read_sql("select * from Topics where type='TV Show'",con=engine)
            show_record=show_df.to_dict(orient='records')
            return render_template('displayTopics.html',df=show_record)

        if(user_input=='Book'):
     
            book_df=pd.read_sql("select * from Topics where type='Book'",con=engine)
            book_record=book_df.to_dict(orient='records')
            return render_template('displayTopics.html',df=book_record)


    return render_template('displayTopics.html',df=df_records)

@app.route('/addTopic', methods=['POST', 'GET'])
def addTopic():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    msg = request.args.get('msg')
    user_id = session['user_id']
    df = pd.read_sql("SELECT * FROM TOPICS", con=engine)
    df_records = df.to_dict(orient='records')

    try:
        if request.method == 'POST':
    
            title = request.form['title']

            title_record = db_session.query(Topics).filter_by(title=title).first()

            if title_record is None:

                raise RecordNotFound(f"'{title}' not found in Database, please choose a title that exists")
            else:
                topic_id = title_record.topic_id
                exists=db_session.query(Progress).filter_by(topic_id=topic_id,user_id=user_id).first()
                if(exists):
                    raise DuplicateEntry(f"'{title}' exists already. Try different or track progress of '{title}'.")
                p = Progress(user_id=user_id, topic_id=topic_id, completed=False, not_started=True, in_progress=False)
                db_session.add(p)
                db_session.commit()
                success=f"{title_record.type} '{title}' added! Add more or go to update progress."
                return render_template('addTopic.html', success=success, df=df_records)

    except RecordNotFound as e:
        error = e.message
        return render_template('addTopic.html', error=error, df=df_records)
    except DuplicateEntry as e:
        error=e.msg
        return render_template('addTopic.html',error=error,df=df_records)

    return render_template('addTopic.html', df=df_records,msg=msg)



@app.route('/editUser', methods=['POST','GET','DELETE'])
def editUser():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user_role=session['role']
    print(50*'*')
    print("USER ROLE:",user_role)
  
    if(user_role=="admin"):
        df = pd.read_sql("SELECT * FROM USER",con=engine)
        df=df.to_dict(orient='records')
        print(50*'*')
        if request.method=='POST':
            user_input=request.form['user_input']
            print(user_input)
            # if(user_input=="delete"):
            #     print("inside delete if")
            #     user_id_to_del=request.form['user_id']
            #     user_to_del=db_session.query(User).filter_by(user_id=user_id_to_del).first()
            #     if(user_to_del):
            #         db_session.delete(user_to_del)
            #         db_session.commit()
            #         print("user deleted", user_to_del)

        return render_template('editUser.html', df=df)
    return "Unauthorized",403



if __name__ == "__main__":

    app.run(debug=True,port=8000)