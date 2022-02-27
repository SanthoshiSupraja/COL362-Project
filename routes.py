#from Project import app
import os
import psycopg2
from flask import Flask,flash, request, redirect, url_for, send_from_directory, render_template,session
from forms import RegistrationForm,LoginForm,DashboardForm,HomepageForm,artistLoginForm,artistshomepageForm

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
def dashboard():
    form = DashboardForm()
    return render_template('dashboard.html',title='Dashboard',form=form)

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
    return render_template('register.html',title='Sign Up',form=form)

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

@app.route('/artistlogin', methods=['POST','GET'])
def artistlogin():
    conn=get_db_connection()
    cur=conn.cursor()
    form=artistLoginForm()
    if form.validate_on_submit():
        user_name = form.name.data
        sql="Select name from artists where name='{}'".format(user_name)
        cur.execute(sql)
        check=cur.fetchall()
        if(len(check)>0):
            print(check[0])
            flash(f'Login successful for (form.username.data)', category="success")
            return redirect(url_for('artisthomepage', user_name=user_name))
        else:
            flash(f'Login unsuccessful for (form.username.data), artist does not exist', category="danger")
    return render_template('artistlogin.html',title='Login', form=form)
@app.route('/homepage', methods=['POST','GET'])
def homepage():
    conn=get_db_connection()
    cur=conn.cursor()
    form = HomepageForm()
    artists = []
    albums = []
    tracks = []
    if form.validate_on_submit():
        #print(form.search.data)
        search_key=form.search.data
        #sql_artists="SELECT name, followers from artists where name='{}'".format(search_key)
        sql_artists="SELECT name, followers from artists where name like '%{}%' order by followers desc limit 10".format(search_key)
        sql_albums="SELECT albums.name , artists.name , albums.name from albums join artists on albums.artist_id = artists.id where albums.name like '%{}%' order by artists.followers desc limit 10".format(search_key)
        sql_tracks="select tracks.duration_ms , tracks.name , artists.name from public.tracks join public.artists on substring(tracks.artists_id, 3, LENGTH(tracks.artists_id)-4) = artists.id where tracks.name like '%{}%' order by artists.followers desc limit 10".format(search_key)
        cur.execute(sql_artists)
        artists = cur.fetchall()
        print("artists: ")
        print(artists)
        cur.execute(sql_albums)
        albums=cur.fetchall()
        print("albums: ")
        print(albums)
        cur.execute(sql_tracks)
        tracks=cur.fetchall()
        print("tracks: ")
        print(tracks)
        #return redirect(url_for('search'))
    return render_template('homepage.html',title='Homepage',form=form,artists = artists,albums=albums,tracks=tracks)

@app.route('/artisthomepage', methods=['POST','GET'])
def artisthomepage():
    conn=get_db_connection()
    cur=conn.cursor()
    user_name=request.args['user_name']
    artist_id="select id from artists where name='{}'".format(user_name)
    sql_albums= """select albums.name,albums.total_tracks,albums.album_type,substring(albums.release_date,1,4) from artists join albums on albums.artist_id=artists.id
                 Where artists.name='{}'
                 Order by substring(albums.release_date,1,4) desc
                 Limit 5""".format(user_name)
    cur.execute(sql_albums)
    albums=cur.fetchall()
    print("albums: ")
    print(albums)
    form=artisthomepageForm()
    #should add search
    '''
    form=CreateAlbum()
    if(form.validate_on_submit()):
        #(type, artist_id, name, release_date, total_tracks, track_name_prev)
        album_type=form.album_type.data
        name=form.name.data
        release_date=form.release_date.data
        release_date=form.release_date.data
        total_tracks=form.total_tracks.data
        track_name_prev=form.track_name_prev.data

        sql_insalbum="INSERT INTO albums (album_type, artist_id, name, release_date, total_tracks, track_name_prev) VALUES (album_type, artist_id, name, release_date, total_tracks, track_name_prev)"
        cur.execute(sql_insalbum)
        cur.commit()
    '''
    return render_template('artisthomepage.html',title='ArtistHomepage',form=form)
    #return render_template('homepage.html',title='Homepage')#,form=form,artists = artists,albums=albums,tracks=tracks)
@app.route('/artistclick', methods=['POST','GET'])
def artistclick():
    conn=get_db_connection()
    cur=conn.cursor()
    user_name=request.args['user_name']
    artist_id="select id from artists where name='{}'".format(user_name)
    sql_albums= """select albums.name,albums.total_tracks,albums.album_type,substring(albums.release_date,1,4) from artists join albums on albums.artist_id=artists.id
                 Where artists.name='{}'
                 Order by substring(albums.release_date,1,4) desc
                 Limit 5""".format(user_name)
    cur.execute(sql_albums)
    albums=cur.fetchall()
#    return render_template('search.html',title='search')
@app.route('/albumclick', methods=['POST','GET'])
def albumclick():
    conn=get_db_connection()
    cur=conn.cursor()
    album=request.args['album_id']
    sql_details1="select * from tracks where name='{}'".format(album) #album details
    sql_details2="select tracks.duration_ms , tracks.name , artists.name from public.tracks join public.artists on substring(tracks.artists_id, 3, LENGTH(tracks.artists_id)-4) = artists.id where tracks.albums_id='{}' order by artists.followers desc limit 10".format(album)
@app.route('/trackclick', methods=['POST','GET'])
def trackclick():
    conn=get_db_connection()
    cur=conn.cursor()
    track=request.args['track_name']
    album=request.args['album_id']
    sql_details= "select * from tracks where name='{}' and album_id='{}'".format(track,album)
    cur.execute(sql_details)
    details=cur.fetchall()
    print(details[0])
  return #trackclick.html
if __name__ == "__main__":
    app.run(debug=True)
