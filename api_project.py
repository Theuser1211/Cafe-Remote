import sqlalchemy
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
app = Flask(__name__)
SECRET_API_KEY=os.environ['SECRET_API_KEY']
secret_api_key=SECRET_API_KEY
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dictionary(self):
        # Method 1.
        dictionary = {}


        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

@app.route("/",methods=['GET'])
def home():
    return render_template("index_api.html")

@app.route("/add", methods=["POST"])
def post_new_cafe():
    data = request.json  # Assuming the data is sent as JSON in the request body

    # Extract the required data from the request
    name = data.get("name")
    map_url = data.get("map_url")
    img_url = data.get("img_url")
    location = data.get("location")
    has_sockets = data.get("has_sockets")
    has_toilet = data.get("has_toilet")
    has_wifi = data.get("has_wifi")
    can_take_calls = data.get("can_take_calls")
    seats = data.get("seats")
    coffee_price = data.get("coffee_price")
    try:
           new_cafe = Cafe(
               name=name,
               map_url=map_url,
               img_url=img_url,
               location=location,
               has_sockets=has_sockets,
               has_toilet=has_toilet,
               has_wifi=has_wifi,
               can_take_calls=can_take_calls,
               seats=seats,
               coffee_price=coffee_price,
           )
           with app.app_context():
               db.session.add(new_cafe)
               db.session.commit()
           return jsonify(response={"success": "Successfully added the new cafe."})
    except sqlalchemy.exc.IntegrityError:

           return jsonify(response={"Error": "Already Existing!."})

@app.route("/random",methods=['GET'])
def random_cafes():
    with app.app_context():
        cafes=db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe=random.choice(cafes)
        return jsonify(random_cafe.to_dictionary())


@app.route("/all",methods=['GET'])
def all_cafes():
    with app.app_context():
        all_cafe_list=[]
        cafes=db.session.execute(db.select(Cafe)).scalars().all()
        for i in cafes:
            all_cafe_list.append(i.to_dictionary())
        all_cafe_dict={"cafes":all_cafe_list}
        return jsonify(all_cafe_dict)


@app.route("/search",methods=['GET'])
def search_cafe():
    all_cafe_list=[]
    location_entered_in_the_url=request.args.get("loc")
    print(location_entered_in_the_url)
    with app.app_context():
        cafes_in_a_particular_location=db.session.execute(db.select(Cafe).filter_by(location=location_entered_in_the_url)).scalars().all()
    print(cafes_in_a_particular_location)
    for i in cafes_in_a_particular_location:
        all_cafe_list.append(i.to_dictionary())
    if len(all_cafe_list)==0:
        all_cafe_dict={"error":{"Not Found":"Sorry,we don't have a cafe at that location."}}
    else:
        all_cafe_dict = {"cafes": all_cafe_list}
    return jsonify(all_cafe_dict)

@app.route("/update-price/<int:id>",methods=['PATCH'])
def update_price(id):
    new_price = request.args.get("new_price")
    with app.app_context():
        try:
            cafe_to_update = db.session.execute(db.select(Cafe).filter_by(id=id)).scalar_one()
            cafe_to_update.coffee_price = new_price
            db.session.commit()
            message={"Success":"New price has been updated."}
            error_code=None
        except:
            message={"Error":"No such ID Exits. Please check the id."}
            error_code=404
    return jsonify(message),error_code

@app.route("/report-closed/<int:id>",methods=['DELETE','GET'])
def delete_cafe(id):
    api_key=request.args.get("api-key")
    if api_key==secret_api_key:
        with app.app_context():
            try:
                cafe_to_delete = db.session.execute(db.select(Cafe).filter_by(id=id)).scalar_one()
                db.session.delete(cafe_to_delete)
                db.session.commit()
                message={"Success":"Cafe has been deleted."}
                error_code=None
            except:
                message = {"Error": "No such ID Exits. Please check the id."}
                error_code = 404
    else:
        message = {"Error": "That's not allowed.Make sure you have the correct api_key"}
        error_code = 403
    return jsonify(message),error_code

if __name__ == '__main__':
    app.run(debug=True,port=5000)
