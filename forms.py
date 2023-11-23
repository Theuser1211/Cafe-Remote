from wtforms import StringField, SubmitField,SelectField,DecimalField
from wtforms.validators import DataRequired,URL
from flask_wtf import FlaskForm

class NewCafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url=StringField('Location Url',validators=[DataRequired(),URL()])
    img_url=StringField('Image Link',validators=[DataRequired(),URL()])
    location=StringField('Location', validators=[DataRequired()])
    has_sockets=SelectField("Has Power Sockets",choices=['Yes','No'],coerce=str,validators=[DataRequired()])
    has_toilet=SelectField("Restroom Facility",choices=['Yes','No'],coerce=str,validators=[DataRequired()])
    has_wifi=SelectField("Wifi Availablity",choices=['Yes','No'],coerce=str,validators=[DataRequired()])
    can_take_calls=SelectField("Phone Friendly",choices=['Yes','No'],coerce=str,validators=[DataRequired()])
    seats=SelectField("Number of seats",choices=['0-10','10-20','20-30','30-40','40-50','50+'],coerce=str,validators=[DataRequired()])
    coffee_price=StringField("Coffee Price",validators=[DataRequired()])
    submit = SubmitField('Submit')



    # opentime=StringField("Open Time(Hour:MinuteAM/PM)",validators=[DataRequired()])
    # closetime=StringField("Close Time(Hour:MinuteAM/PM)",validators=[DataRequired()])
    #
    # coffee=SelectField("Coffee Rating",choices=['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'],validators=[DataRequired()])
    # # coffee=SelectField("Coffee",choices=[('☕', '☕'), ('☕☕', '☕☕'),('☕☕☕', '☕☕☕'),],validators=[DataRequired()])
    # wifi=SelectField("Wifi Strength Rating",choices=['💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪','✘'],validators=[DataRequired()])
    # power=SelectField("Power Socket Availability",choices=['🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌','✘'],validators=[DataRequired()])
    # submit = SubmitField('Submit')


    #     name=request.form.get("name"),
    #     map_url=request.form.get("map_url"),
    #     img_url=request.form.get("img_url"),
    #     location=request.form.get("location"),
    #     has_sockets=bool(request.form.get("has_sockets")),
    #     has_toilet=bool(request.form.get("has_toilet")),
    #     has_wifi=bool(request.form.get("has_wifi")),
    #     can_take_calls=bool(request.form.get("can_take_calls")),
    #     seats=request.form.get("seats"),
    #     coffee_price=request.form.get("coffee_price"),
    # )