import werkzeug.exceptions
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from random import choice
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('flask_key')
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    map_url = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired()])

    def validate_map_url(self, field):
        if 'http' not in field.data:
            raise ValidationError('Please enter the full URL, including http.')

    img_url = StringField(label='Cafe Img (URL)', validators=[DataRequired()])
    location = StringField(label='Part of City', validators=[DataRequired()])
    coffee_price = StringField(label='Coffee Price', validators=[DataRequired()])
    wifi = SelectField(label='Free Wifi?', choices=['Yes', 'No'])
    plugs = SelectField(label='Sockets Available?', choices=['Yes', 'No'])
    toilets = SelectField(label='Toilets available?', choices=['Yes', 'No'])
    calls = SelectField(label='Can you take calls?', choices=['Yes', 'No'])
    seats = StringField(label='How many seats are there?', validators=[DataRequired()])

    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe)).scalars().fetchall()
        cafe = choice(cafes)

        return render_template('random_cafe.html', cafe=cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().fetchall()
    cafe_list = []
    for cafe in cafes:
        cafe_list.append(cafe.to_dict())
    return render_template('cafes.html', cafes=cafe_list)


@app.route("/search")
def search_for_cafe():
    query_location = request.args.get("loc").title()
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)).scalars().all()
    if cafes:
        return jsonify(cafe=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"Not Found": "Sorry we don't have a cafe at that location."})


# HTTP POST - Create Record
@app.route("/add", methods=["POST", "GET"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        with app.app_context():
            true_or_false = [form.toilets.data, form.wifi.data, form.plugs.data, form.calls.data]
            db_inputs = []
            for data in true_or_false:
                if data == 'Yes':
                    db_inputs.append(1)
                else:
                    db_inputs.append(0)
            new_cafe = Cafe(
                name=f'{form.cafe.data}',
                map_url=f'{form.map_url.data}',
                img_url=f'{form.img_url.data}',
                location=f'{form.location.data}',
                seats=f'{form.seats.data}',
                has_toilet=bool(db_inputs[0]),
                has_wifi=bool(db_inputs[1]),
                has_sockets=bool(db_inputs[2]),
                can_take_calls=bool(db_inputs[3]),
                coffee_price=f'{form.coffee_price.data}',
            )
            db.session.add(new_cafe)
            db.session.commit()
        return redirect(url_for('get_all_cafes'))
    return render_template('add.html', form=form)

# HTTP PUT/PATCH - Update Record


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    with app.app_context():
        try:
            cafe = db.get_or_404(Cafe, cafe_id)
        except werkzeug.exceptions.NotFound:
            return jsonify(response={"error": "Sorry a cafe with that id is not in the database"})

        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
    return jsonify(response={"success": "Successfully updated the price."})


# HTTP DELETE - Delete Record


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE", 'GET'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == os.getenv('api_key'):
        try:
            cafe = db.get_or_404(Cafe, cafe_id)
        except werkzeug.exceptions.NotFound:
            return jsonify(response={"error": "Sorry a cafe with that id is not in the database"})
        else:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted cafe from database."})
    else:
        return jsonify(response={"error": "Sorry, that's the incorrect api-key"})


if __name__ == '__main__':
    app.run(debug=True)
