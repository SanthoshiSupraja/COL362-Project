#from Project import app
import os
import psycopg2
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template,session,requ
from forms import RegistrationForm,LoginForm

app=Flask(__name__)

def get_db_connection():
    conn=psycopg2.connect(
    host="localhost",
    database="project",
    user='postgres',
    password='pass'
    )
    return conn

@app.route("/")
def home():
    #conn=get_db_connection()
    #cur=conn.cursor()
    #cur.execute('SELECT * from users;')
    #username = cur.fetchall()
    #print(username)
    return render_template("account.html",title='Account')

@app.route('/register', methods=['POST','GET'])
def register():
   conn=get_db_connection()
   cur=conn.cursor
   form=RegistrationForm()
   if form.valididate_on_submit():
      flash(f'Account created for {form.username.data}', category='success')
      user_email=form.email.data
      user_pwd=form.password.data
      user_name=form.username.data
      cur.execute('INSERT INTO users(username, emailid, password) VALUES ({}, {}, {});'.format(user_name,user_email,user_pwd))
      return redirect(url_for('login'))
   return render_template('register.html',title='Register',form='form')


@app.route('/login', methods=['POST','GET'])
def home():
    conn=get_db_connection()
    cur=conn.cursor
    form=LoginForm()
    if form.validate_on_submit():
        user_email=form.email.data
        user_pwd=form.password.data
        cur.execute('SELECT password from users where emailid={};'.format(user_email))
        pwd=cur.fetchone
        if(pwd==None):
           flash(f'Login unsuccessful for (form.username.data)', category='danger')
        else:
         if pwd==user_pwd:
            flash(f'Login successful for (form.username.data)', category="success")
            return redirect (url_for('account'))
         else:
           flash(f'Login unsuccessful for (form.username.data)', category='danger')
    return render_template('login.html',title='Login', form='form')
if __name__ == "__main__":
    app.run(debug=True)
