from logging import exception
from django.shortcuts import render
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#instantiate  flask app
app = Flask(__name__)

#setting configurations
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instantiate db object
db = SQLAlchemy(app)

#creating marshmallow object
ma = Marshmallow(app)

#creating database
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_name = db.Column(db.String(200),default="General")
    description = db.Column(db.String(200))
    buy_price = db.Column(db.Integer, nullable=False)
    sell_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return self.id

#
#
#
#
@app.route('/',methods = ["GET","POST"])
def home():
    items = Shop.query.all()
    return render_template("home.html", items = items)
#
#
#


#create Shop schema
class ShopSchema(ma.Schema):
    class Meta:
        fields = ('id','name','category_name','description','buy_price','sell_price','quantity')

#create instance of schema
Shopitem_schema = ShopSchema(many=False)
Shopitems_schema = ShopSchema(many= True)

#create shop route
@app.route("/shop", methods=["POST"])
def add_item():
    try:
        name = request.json['name']
        category_name = request.json['category_name']
        description = request.json['description']
        buy_price = request.json['buy_price']
        sell_price = request.json['sell_price']

        new_item = Shop(name=name,category_name=category_name,description=description,buy_price=buy_price,sell_price=sell_price)

        db.session.add(new_item)
        db.session.commit()
        return Shopitem_schema.jsonify(new_item)
    except exception as e:
        return jsonify({"Error":"Invalid request."})

#get shop item
@app.route("/shop",methods = ["GET"])
def get_items():
    items = Shop.query.all()
    result_set = Shopitems_schema.dump(items)
    return jsonify(result_set)

@app.route("/shop/<int:id>", methods = ["GET"])
def get_item(id):
    item = Shop.query.get_or_404(int(id))
    return Shopitem_schema.jsonify(item)

#update an item details
@app.route("/shop/<int:id>", methods=["PUT"])
def update_item(id):
    item = Shop.query.get_or_404(int(id))

    name = request.json['name']
    category_name = request.json['category_name']
    description = request.json['description']
    buy_price = request.json['buy_price']
    sell_price = request.json['sell_price']

    item.name = name
    item.category_name = category_name
    item.description = description
    item.buy_price = buy_price
    item.sell_price = sell_price

    db.session.commit()

    return Shopitem_schema.jsonify(item)
    
#delete an item
@app.route("/shop/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = Shop.query.get_or_404(int(id))
    db.session.delete(item)
    db.session.commit()
    return jsonify({"Success":"Item deleted"})

if __name__ == "__main__":
    app.run(debug=True)