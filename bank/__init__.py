from flask import Flask

app = Flask(__name__)

from bank.api.routes import banks
from bank.api.routes import api_obj
from bank.api.routes import Bank

#register blueprint with app
app.register_blueprint(api.routes.banks, url_prefix='/api')
