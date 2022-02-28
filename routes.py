#from Project import app
import os
import psycopg2
from flask import Flask,flash, request, redirect, url_for, send_from_directory, render_template,session
from forms import RegistrationForm,LoginForm,DashboardForm,HomepageForm,artistLoginForm,artisthomepageForm,artistclickForm,albumclickForm,trackclickForm,createalbum1

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
    
    sql_famart="SELECT artists.name, artists.followers from artists join albums on albums.artist_id=artists.id group by artists.id having COUNT(albums.id)>10 order by artists.followers desc limit 10"
    sql_newrel="SELECT albums.name , substring(albums.release_date,1,4) as release_year from albums join artists on albums.artist_id = artists.id join tracks on tracks.album_id=albums.id group by albums.id having COUNT(albums.id)>10 order by substring(albums.release_date,1,4) desc limit 10"
    sql_poptracks="select tracks.duration_ms , tracks.name , artists.name from public.tracks join public.artists on substring(tracks.artists_id, 3, LENGTH(tracks.artists_id)-4) = artists.id order by tracks.popularity desc limit 10"
    sql_acc="select albums.name from (select temp.id from (Select albums.name, albums.id from albums join artists on albums.artist_id = artists.id join (Select AVG(acousticness) as ac, album_id from tracks group by album_id ) as accou on albums.id=accou.album_id order by accou.ac) as temp join tracks on tracks.album_id=temp.id group by temp.id having COUNT(album_id)>10) temp join albums on albums.id=temp.id limit 10"
    sql_dance="select albums.name from (select temp.id from (Select albums.name, albums.id from albums join artists on albums.artist_id = artists.id join (Select AVG(danceability) as ac, album_id from tracks group by album_id ) as accou on albums.id=accou.album_id order by accou.ac) as temp join tracks on tracks.album_id=temp.id group by temp.id having COUNT(album_id)>10) temp join albums on albums.id=temp.id limit 10"
    sql_live="select albums.name from (select temp.id from (Select albums.name, albums.id from albums join artists on albums.artist_id = artists.id join (Select AVG(liveness) as ac, album_id from tracks group by album_id ) as accou on albums.id=accou.album_id order by accou.ac) as temp join tracks on tracks.album_id=temp.id group by temp.id having COUNT(album_id)>10) temp join albums on albums.id=temp.id limit 10"
    sql_loud="select albums.name from (select temp.id from (Select albums.name, albums.id from albums join artists on albums.artist_id = artists.id join (Select AVG(loudness) as ac, album_id from tracks group by album_id ) as accou on albums.id=accou.album_id order by accou.ac) as temp join tracks on tracks.album_id=temp.id group by temp.id having COUNT(album_id)>10) temp join albums on albums.id=temp.id limit 10"

    cur.execute(sql_famart)
    famous_artists = cur.fetchall()

    cur.execute(sql_newrel)
    new_releases = cur.fetchall()

    cur.execute(sql_poptracks)
    popular_tracks = cur.fetchall()

    cur.execute(sql_acc)
    acousticness = cur.fetchall()

    cur.execute(sql_dance)
    danceability = cur.fetchall()

    cur.execute(sql_live)
    liveness = cur.fetchall()

    cur.execute(sql_loud)
    loudness = cur.fetchall()

    if form.validate_on_submit():
        #print(form.search.data)
        search_key=form.search.data
        #sql_artists="SELECT name, followers from artists where name='{}'".format(search_key)
        sql_artists="SELECT name, followers from artists where name like '%{}%' order by followers desc limit 10".format(search_key)
        sql_albums="SELECT albums.name , artists.name , albums.name from albums join artists on albums.artist_id = artists.id join tracks on tracks.album_id=albums.id where albums.name like '%{}%' group by albums.id, artists.name having COUNT(albums.id)>10 limit 10".format(search_key)
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
        return render_template('search.html',form=form,artists = artists,albums=albums,tracks=tracks)
    return render_template('homepage.html',title='Homepage',form=form,artists = artists,albums=albums,tracks=tracks,famous_artists = famous_artists,new_releases=new_releases,popular_tracks=popular_tracks,acousticness=acousticness,danceability=danceability,liveness=liveness,loudness=loudness)

artist_id = ""
@app.route('/artisthomepage', methods=['POST','GET'])
def artisthomepage():
    conn=get_db_connection()
    cur=conn.cursor()
    user_name=request.args['user_name']
    artistid="select id from artists where name='{}'".format(user_name)
    cur.execute(artistid)
    artist_id=cur.fetchone()
    sql_albums= """select albums.name,albums.total_tracks,albums.album_type,substring(albums.release_date,1,4) from artists join albums on albums.artist_id=artists.id
                 Where artists.name='{}'
                 Order by substring(albums.release_date,1,4) desc
                 Limit 5""".format(user_name)
    cur.execute(sql_albums)
    albums=cur.fetchall()
    print("albums: ")
    print(albums)
    form=artisthomepageForm()
    #form=createalbum()
    
    return render_template('artisthomepage.html',title='ArtistHomepage',form=form,albums=albums,user_name=user_name,artist_id= artist_id)
    #return render_template('homepage.html',title='Homepage')#,form=form,artists = artists,albums=albums,tracks=tracks)
@app.route('/createalbum', methods=['POST','GET'])
def createalbum():
    form = createalbum1()
    conn=get_db_connection()
    cur=conn.cursor()
    #user_name=request.args['user_name']
    #artist_id=request.args['artist_id']
    if(form.validate_on_submit()):
        album_type=form.album_type.data
        album_id = form.album_id.data
        name=form.name.data
        release_date=form.release_date.data
        total_tracks=form.total_tracks.data
        sql_insalbum="INSERT INTO albums (album_type,artist_id,id,name,release_date, total_tracks) VALUES ('{}', '{}','{}','{}','{}',{}) ".format(album_type, artist_id,album_id,name, release_date, total_tracks)
        cur.execute(sql_insalbum)
        return redirect(url_for('artisthomepage'))
    return render_template('createalbum.html',title='Create Album',form=form)

@app.route('/search', methods=['POST','GET'])
def search():
    form=request.args['form']
    artists=request.args['artists']
    albums=request.args['albums']
    tracks=request.args['tracks']
    return render_template('search.html',title='search',form=form,artists = artists,albums=albums,tracks=tracks)

@app.route('/artistclick/<string:a>', methods=['POST','GET'])
def artistclick(a):
    conn=get_db_connection()
    cur=conn.cursor()
    user_name = a
    form=artistclickForm()
    artist_id="select id from artists where name='{}'".format(user_name)
    sql_albums= """select albums.name,albums.total_tracks,albums.album_type,substring(albums.release_date,1,4) from artists join albums on albums.artist_id=artists.id
                 Where artists.name='{}'
                 Order by substring(albums.release_date,1,4) desc
                 Limit 5""".format(user_name)
    cur.execute(sql_albums)
    albums=cur.fetchall()
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
        return render_template('search.html',form=form,artists = artists,albums=albums,tracks=tracks)
    return render_template('artist.html',title=a,form=form,albums=albums,user_name=user_name)

@app.route('/albumclick/<string:b>', methods=['POST','GET'])
def albumclick(b):
    conn=get_db_connection()
    cur=conn.cursor()
    album_name=b
    form=albumclickForm()
    sql_details1="select * from albums where name='{}'".format(album_name) 
    sql_details2="select tracks.duration_ms , tracks.name , artists.name from public.tracks join public.artists on substring(tracks.artists_id, 3, LENGTH(tracks.artists_id)-4) = artists.id join albums on albums.id=tracks.album_id where albums.name='{}' order by artists.followers desc limit 10".format(album_name)
    cur.execute(sql_details1)
    albums = cur.fetchall()
    cur.execute(sql_details2)
    tracks = cur.fetchall()
    print(tracks)
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
        return render_template('search.html',form=form,artists = artists,albums=albums,tracks=tracks)
    return render_template('album.html',title=b,form=form,albums=albums,tracks=tracks,album_name=album_name)

@app.route('/trackclick/<string:c>', methods=['POST','GET'])
def trackclick(c):
    conn=get_db_connection()
    cur=conn.cursor()
    form = trackclickForm()
    track_name= c
    sql_details= "select * from tracks where name='{}'".format(track_name)
    cur.execute(sql_details)
    tracks=cur.fetchall()
    print(tracks[0])
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
        return render_template('search.html',form=form,artists = artists,albums=albums,tracks=tracks)
    return render_template('track.html',title=c,form=form,tracks=tracks,track_name=track_name)
if __name__ == "__main__":
    app.run(debug=True)
