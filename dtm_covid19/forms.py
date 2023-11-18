from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from dtm_covid19.models import User
from wtforms.fields.html5 import DateTimeLocalField


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EntryForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=30)])
    state = SelectField('State', choices=[ ('', ''), ('AL','AL'), ("AK","AK"), ("AZ","AZ"), ("AR","AR"), 
        ("CA","CA"), ("CO", "CO"), ("CT","CT"), ("DC","DC"), ("DE","DE"), ("FL","FL"), ("GA","GA"), 
        ("HI","HI"), ("ID","ID"), ("IL","IL"), ("IN","IN"), ("IA","IA"), ("KS","KS"), ("KY","KY"), ("LA","LA"), ("ME","ME"), ("MD","MD"), 
        ("MA","MA"), ("MI","MI"), ("MN","MN"), ("MS","MS"), ("MO","MO"), ("MT","MT"), ("NE","NE"), ("NV","NV"), ("NH","NH"), ("NJ","NJ"), 
        ("NM","NM"), ("NY","NY"), ("NC","NC"), ("ND","ND"), ("OH","OH"), ("OK","OK"), ("OR","OR"), ("PA","PA"), ("RI","RI"), ("SC","SC"), 
        ("SD","SD"), ("TN","TN"), ("TX","TX"), ("UT","UT"), ("VT","VT"), ("VA","VA"), ("WA","WA"), ("WV","WV"), ("WI","WI"), ("WY","WY")],
        validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(min=1, max=5)])
    datetime =  DateTimeLocalField('Date & Time', format='%Y-%m-%dT%H:%M')
    #DateTimeField('Date & Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Submit')