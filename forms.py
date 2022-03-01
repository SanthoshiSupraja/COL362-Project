from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class DashboardForm(FlaskForm):
    email = StringField (label='Email', validators=[DataRequired(), Email()])
    password = PasswordField (label='Password', validators=[DataRequired(), Length (min=6,max=16)])
    submit =SubmitField(label='Login')

class RegistrationForm(FlaskForm):

   username =StringField(label='Username',validators=[DataRequired(), Length (min=3,max=20)])
   email = StringField (label='Email',validators=[DataRequired(), Email()])
   password = PasswordField (label='Password', validators=[DataRequired(), Length (min=6,max=16)])
   confirm_password=PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField (label='Sign Up')


class LoginForm(FlaskForm):
    email = StringField (label='Email',validators=[DataRequired(), Email()])
    password = PasswordField (label='Password', validators=[DataRequired(), Length (min=6,max=16)])
    submit =SubmitField(label='Login')

class artistLoginForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    submit =SubmitField(label='Login')
class HomepageForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')
class artisthomepageForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')
class artistclickForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')
class albumclickForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')
class artistalbumclickForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')
class trackclickForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')

class createalbum1(FlaskForm):
   album_type = StringField(label='AlbumType',validators=[DataRequired()])
   album_id = StringField(label='AlbumId',validators=[DataRequired()])
   name = StringField(label='name', validators=[DataRequired()])
   release_date = StringField(label='Release year',validators=[DataRequired()])
   total_tracks = IntegerField(label='Total tracks',validators=[DataRequired()])
   submit =SubmitField(label='submit')

class deleteForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')

class addtrackForm(FlaskForm):
    acousticness = DecimalField(label='acousticness', validators=[DataRequired()])
    danceability = DecimalField(label='danceability', validators=[DataRequired()])
    duration_ms = IntegerField(label='duration_ms', validators=[DataRequired()])
    id = StringField(label='TrackId',validators=[DataRequired()])
    liveness = DecimalField(label='liveness', validators=[DataRequired()])
    loudness = DecimalField(label='loudness', validators=[DataRequired()])
    name = StringField(label='name', validators=[DataRequired()])
    submit =SubmitField(label='search')

class deleteTrackForm(FlaskForm):
    search = StringField (label='search', validators=[DataRequired()])
    submit =SubmitField(label='search')

class changePasswordForm(FlaskForm):
    emailid= StringField (label='Email',validators=[DataRequired(), Email()])
    cur_pwd= PasswordField (label='Current Password', validators=[DataRequired(), Length (min=6,max=16)])
    new_pwd= PasswordField (label='New Password', validators=[DataRequired(), Length (min=6,max=16)])
    submit =SubmitField(label='submit')

