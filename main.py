import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
import json

API_URL = "http://127.0.0.1:5001"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-string'
bootstrap = Bootstrap5(app)

class AddCafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Google Maps URL', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    has_toilet = BooleanField('Has toilet?')
    has_wifi = BooleanField('Has wifi?')
    has_sockets = BooleanField('Has sockets?')
    can_take_calls = BooleanField('Can take calls?')
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    submit = SubmitField('Add Cafe')

class SearchCafeForm(FlaskForm):
    location = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route("/", methods=['GET'])
def home():
    response = requests.get(url=f"{API_URL}/all")
    all_cafes = response.json()
    return render_template("index.html", cafes=all_cafes)

@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    
    if form.validate_on_submit():

        params = {
            "name": form.cafe_name.data,
            "map_url": form.map_url.data,
            "img_url": form.img_url.data,
            "location": form.location.data,
            "seats": form.seats.data,
            "has_toilet": form.has_toilet.data,
            "has_wifi": form.has_wifi.data,
            "has_sockets": form.has_sockets.data,
            "can_take_calls": form.can_take_calls.data,
            "coffee_price": form.coffee_price.data,
        }

        response = requests.post(url=f"{API_URL}/add", params=params)
        if response.status_code == 200:
            return redirect(url_for('home'))
        else:
            return render_template("error.html", message="Error adding cafe to API")
        
    return render_template("add.html", form=form)

@app.route("/delete/<id>", methods=['GET'])
def delete_cafe(id):
    with open("sensitive_data.json") as f:
        data = json.load(f)
        api_key = data["cafe_api"]["api_key"]

    print(api_key)
    params = {
        "api_key": api_key,
    }
    print(api_key)

    response = requests.delete(url=f"{API_URL}/report-closed/{id}", params=params)

    if response.status_code == 200:
        return redirect(url_for('home'))
    else:
        return render_template("error.html", message="Error deleting cafe from API")

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchCafeForm()

    if form.validate_on_submit():
        params = {
            "loc": form.location.data,
        }

        response = requests.get(url=f"{API_URL}/search", params=params)
        if response.status_code == 200:
            cafe_from_location = response.json()
            return render_template("index.html", cafes=cafe_from_location)
        else:
            return render_template("error.html", message="Error searching cafe")
    
    return render_template("search.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
