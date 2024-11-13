# Python-PEP-Progress-Tracker
!["Project Description part 1"](https://jump-december-python-materials.s3.amazonaws.com/PythonPEP-1.png)
!["Project Description part 2"](https://jump-december-python-materials.s3.amazonaws.com/PythonPEP-2.png)


<!-- before starting
get db set up using the files provided
set up a venv and run 
pip install -r requirements.txt to install required files
modify db password in config.py
run populate topic function in main.py so that the topics can be populated into the database table
run createAdmin() to create the admin user.
grade web version only -->


Project Overview
This project is a Progress Tracker that allows users to keep track of their progress on different topics, including books, movies, and songs. The application has both a terminal-based version and a web version built using Flask, with MySQL as the database backend.


Setup Instructions
Before starting, follow these steps to set up the project:

Database Setup:
Set up the database using the provided database files.
Virtual Environment Setup:
Create and activate a virtual environment

Install Required Packages:
Run the following command to install all necessary dependencies:
pip install -r requirements.txt

Database Configuration:
Modify the config.py file to include your database password and other configuration settings.

Populate Database:
Run the populate_topic() function in main.py to populate the database with initial topics.

Create Admin User:
Run createAdmin() in main.py to create the initial admin user.

Running the Application
You can run either the terminal-based or the web version of the application:
Terminal Version(not for grade)
To start the terminal-based version, run:
python main.py
Web Version (for grade)
To start the Flask web application, run:
python app.py
Then, open your browser and go to http://127.0.0.1:5000 to access the web interface.