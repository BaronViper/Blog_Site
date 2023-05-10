from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, URLField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, URL


class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")


class BlogForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(message='Title required'), Length(min=3, max=40,
                                                                                            message='Title must be 40 characters or less')])
    subject = SelectField('- Person Focused On -',
                          validators=[DataRequired(message='Subject required. If no subject available in '
                                                           'drop-down, add one!')], choices=[("", "- "
                                                                                                  "Subject "
                                                                                                  "Focused "
                                                                                                  "On -")], default="")
    quote = StringField('quote', validators=[DataRequired(message='Quote required'),
                                             Length(min=3, max=500, message="Quote too long!")])
    quote_author = StringField('quote_author',
                               validators=[DataRequired(message='Quote Author required'), Length(min=3, max=500)])
    subtitle = StringField('subtitle', validators=[DataRequired(message='Description of blog post required'),
                                                   Length(min=10, message='Description of blog post too short!')])
    image = URLField('image', validators=[DataRequired(message='Image URL required'),
                                          URL(require_tld=False, message='Invalid Image URL')])
    message = StringField('message', validators=[DataRequired(message='Blog post body required'),
                                                 Length(min=10, message='Blog post body too short')])
    submit = SubmitField('Post')


class SubjectForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(message='Name required'), Length(min=3, max=40)])
    location = StringField('location', validators=[DataRequired(message='Location required')])
    quote = StringField('quote', validators=[DataRequired(message='Quote required'), Length(min=3, max=500)])
    subtitle = StringField('subtitle',
                           validators=[DataRequired(message='Brief description of biography required'), Length(min=10)])
    birth = StringField('birth', validators=[DataRequired(message='Year of birth required (XXXX) if unknown')])
    death = StringField('death', validators=[DataRequired(message='Year of death required (XXXX) if unknown')])
    image = URLField('image', validators=[DataRequired(message='Image URL required'),
                                          URL(require_tld=False, message='Invalid Image URL')])
    message = StringField('message', validators=[DataRequired(message='Biography required'),
                                                 Length(min=10, message='Biography too short')])
    visibility = BooleanField('visibility')
    submit = SubmitField('Add')

# class ContactForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#     email = EmailField('email', validators=[DataRequired()])
#     message = StringField('name', validators=[DataRequired()])
