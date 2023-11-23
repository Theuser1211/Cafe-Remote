from flask import Flask, render_template,request,redirect,url_for,abort,jsonify
from flask_bootstrap import Bootstrap
import requests,pprint
from forms import NewCafeForm
from json import JSONDecodeError
import os,time

SECRET_KEY=os.environ["SECRET_KEY_APP"]
# all_cafes = requests.get("http://127.0.0.1:5000/all").json()
# cafe_list=list(all_cafes['cafes'])
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

def loop():
    while True:
        all_cafes = requests.get("http://127.0.0.1:5000/all").json()
        cafe_list = list(all_cafes['cafes'])
        time.sleep(2)
        return cafe_list

@app.route("/",methods=['GET','POST'])
def home():
    cafe_list=loop()
    return render_template("index.html",cafe_list=cafe_list)

@app.route("/search", methods=['GET', 'POST'])
def search():

    if request.method == "POST":
        search_query = request.form.get("search")
        search_query=search_query.title()
        print(search_query)
        # search_request= requests.get(f"http://127.0.0.1:5000/search?loc={search_query}").json()
        # print(search_request.raise_for_status())

        try:
            search_request = requests.get(f"http://127.0.0.1:5000/search?loc={search_query}").json()
            print(search_request)
            if "error" in search_request:
                error_message = search_request["error"]["Not Found"]
                # print(error_message)
                return render_template("error.html", error_response=error_message)

            search_request_list=list(search_request['cafes'])
            return render_template("search.html", search_loc_list=search_request_list,place=search_query.title())
        except JSONDecodeError as e:
            # Handle the JSONDecodeError here
            print(f"JSONDecodeError: {e}")
            # return render_template("error.html", error_response="Invalid JSON response from the server.")

        # if "error" in search_request:
        #     error_message = search_request["error"]["Not Found"]
        #     # print(error_message)
        #     return render_template("error.html", error_response=error_message)
        #
        # search_request_list=list(search_request['cafes'])
        # return render_template("search.html", search_loc_list=search_request_list,place=search_query.title())

@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    add_form=NewCafeForm()

    if add_form.validate_on_submit():

        name = add_form.name.data
        map_url = add_form.map_url.data
        img_url = add_form.img_url.data
        location = add_form.location.data
        has_sockets = add_form.has_sockets.data
        has_toilet = add_form.has_toilet.data
        has_wifi = add_form.has_wifi.data
        can_take_calls = add_form.can_take_calls.data
        seats = add_form.seats.data
        coffee_price = add_form.coffee_price.data
        name=name.title()
        location=location.title()
        if has_sockets=="Yes":
            has_sockets=True
        else:
            has_sockets=False
        if has_toilet=="Yes":
            has_toilet=True
        else:
            has_toilet=False
        if has_wifi=="Yes":
            has_wifi=True
        else:
            has_wifi=False
        if can_take_calls=="Yes":
            can_take_calls=True
        else:
            can_take_calls=False
        coffee_price="£"+coffee_price

        add_url="http://127.0.0.1:5000/add"
        data={
            "name": name,
            "map_url": map_url,
            "img_url": img_url,
            "location":location,
            "has_sockets":has_sockets,
            "has_toilet":has_toilet,
            "has_wifi":has_wifi,
            "can_take_calls":can_take_calls,
            "seats":seats,
            "coffee_price":coffee_price

        }

        add_url_response=requests.post(add_url, json=data)

        if "success" in add_url_response.text:
            success_message = "You have successfully added the new cafe into the database"
            # success_message=add_url_response.text
            return render_template("success.html", success_response=success_message)
        else:
            error_message="Cafe Already Existing"
            return render_template("error.html",error_response=error_message)

    return render_template("add_cafe.html",form=add_form)
@app.route("/update/<id>",methods=['GET','POST'])
def update_price(id):
    print(id)
    if request.method == "POST":
        new_price=request.form.get("update")
        print(new_price,id)
        update_price_url=f"http://127.0.0.1:5000/update-price/{id}?new_price=£{new_price}"
        update_price_response=requests.patch(url=update_price_url)
        print(update_price_response)
        if "Success" in update_price_response.text:
            success_message="Price has been updated"
            return render_template("success.html",success_response=success_message)
        else:
            return render_template("error.html",error_response=update_price_response.text)

    return render_template("update_details.html",id=id)
@app.route("/delete/<id>",methods=['GET','POST'])
def delete(id):
    print(id)
    if request.method == "POST":
        api_key=request.form.get("delete")
        print(api_key,id)
        delete_cafe_url=f"http://127.0.0.1:5000/report-closed/{id}?api-key={api_key}"

        delete_cafe_response=requests.delete(url=delete_cafe_url)
        print(delete_cafe_response)
        if "Success" in delete_cafe_response.text:
            success_message="Cafe has been deleted from the database"
            return render_template("success.html",success_response=success_message)
        else:
            if "api_key" in delete_cafe_response.text:
                error_message="The api_key provided is incorrect.Please try again!"
            else:
                error_message="No such cafe exists!"

            return render_template("error.html",error_response=error_message)
    return render_template("delete_cafe.html",id=id)

if __name__ == '__main__':

    app.run(debug=True,port=5001)
