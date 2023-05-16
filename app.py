import os
from db import db
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "sometestsecretkey"
    jwt = JWTManager(app)

    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

# @app.get("/store")
# def get_stores():
#     return {"stores": list(stores.values())}
#
#
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found")
#
#
# @app.post("/store")
# def create_store():
#     store_data = request.get_json()
#     if "name" not in store_data:
#         abort(400, message="Bad request. Ensure 'name' is included in JSON payload.")
#     store_id = uuid.uuid4().hex
#     store = {**store_data, "store_id": store_id}
#     stores[store_id] = store
#     return store, 201
#
#
# @app.delete('/store/string:<store_id>')
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         abort(404, "Store not found")
#
#
# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}
#
#
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
#         abort(400, message="Ensure 'price', 'store_id', and 'name' are included in JSON payload")
#     for item in items.values():
#         if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
#             abort(400, message="Item already exists!")
#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found")
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item, 201
#
#
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found")
#
#
# @app.put('/item/<string:item_id>')
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(400, message="Bad request. Ensure 'price' and 'name' are included in JSON payload.")
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404, message="Item not found.")
#
#
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted."}
#     except KeyError:
#         abort(404, message="Item not found.")
