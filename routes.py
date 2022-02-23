#from Project import app
import os
import psycopg2
from flask import Flask,flash, request, redirect, url_for, send_from_directory, render_template,session
from .forms import RegistrationForm,LoginForm,DashboardForm

app=Flask(__name__)

app.config['SECRET_KEY'] = 'thisisfirstflaskapp'

def get_db_connection():
    conn=psycopg2.connect(
    host="localhost",
    database="project",
    user='postgres',
    password='pass'
    )
    return conn


'''
    def home():
        #conn=get_db_connection()
        #cur=conn.cursor()
        #cur.execute('SELECT * from users;')
        #username = cur.fetchall()
        #print(username)
        return render_template("account.html",title='Account')
'''
@app.route('/')
@app.route('/dashboard', methods=['POST','GET'])
def homepage():
    form = DashboardForm()
    return render_template('homepage.html',title='Homepage',form=form)

@app.route('/register', methods=['POST','GET'])
def register():
    conn=get_db_connection()
    cur=conn.cursor()
    form = RegistrationForm()
    #print(form.validate_on_submit())
    if form.validate_on_submit():
        user_email=form.email.data
        user_pwd=form.password.data
        sql="INSERT INTO users(username, emailid, password) VALUES ('{}', '{}', '{}');".format(form.username.data,user_email,user_pwd)
        cur.execute(sql)
        conn.commit()
        flash(f'Account created for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    conn=get_db_connection()
    cur=conn.cursor()
    form=LoginForm()
    #print(form.validate_on_submit())
    if form.validate_on_submit():
        #print("hello")
        user_email=form.email.data
        user_pwd=form.password.data
        sql="SELECT password from users where emailid='{}';".format(user_email)
        cur.execute(sql)
        pwd=cur.fetchone()
        #print(pwd[0])
        if(pwd==None):
           flash(f'Login unsuccessful for (form.username.data)', category='danger')
        else:
         if pwd[0]==user_pwd:
            flash(f'Login successful for (form.username.data)', category="success")
            return redirect(url_for('homepage'))
         else:
           flash(f'Login unsuccessful for (form.username.data)', category='danger')
    return render_template('login.html',title='Login', form=form)
if __name__ == "__main__":
    app.run(debug=True)
