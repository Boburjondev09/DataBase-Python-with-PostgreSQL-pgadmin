from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #dastur nomi

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:your_password@localhost:5432/fastapitest' # database url manzilini kiritib qoydi
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #database ni ishga tushirdi

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True) # this is a method reference
    name = db.Column(db.String(100), nullable=False) # this is a method reference
    description = db.Column(db.Text) # this is a method reference

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description} # return orqali kiritilgan qiymatni qaytaradi

@app.route('/items', methods=['GET']) # objectga kiritgan reference larni oldi
def get_items():
    items = Item.query.all()
    return jsonify([i.to_dict() for i in items])

@app.route('/items/<int:item_id>', methods=['GET']) # object reference id reference orqali olish uchun
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    return jsonify({"message": "Item not found"}), 404 # Agar table ichida item mavjud bolmasa xatolik chiqadi


@app.route('/items', methods=['POST']) # kiritilgan item ning malumotlarini output ga chiqaradi
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Invalid item data"}), 400 # Agar item dagi malumot mos kelmasa error 404 not found xatolik beradi

    new_item = Item(name=data['name'], description=data.get('description')) # bu item ning nomi va tavsifi
    db.session.add(new_item) # yangi item kiritish uchun
    db.session.commit() # server ga yuborish uchun

    return jsonify(new_item.to_dict()), 201


@app.route('/items/<int:item_id>', methods=['PUT']) # item ning id sini kiritish uchun
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    data = request.get_json() # malumotni json file id va description olib beradi
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']

    db.session.commit()
    return jsonify(item.to_dict()) # server ga yuborilganda json file item ni dictionary ga convert qilib json file da saqlaydi


@app.route('/items/<int:item_id>', methods=['DELETE']) #item ni uchirish uchun method
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Item {item_id} deleted successfully"}) # item uchirilganda json dan avtomatik uni id si uchadi


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug=True)
