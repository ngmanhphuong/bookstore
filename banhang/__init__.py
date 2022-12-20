from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = '@@#%@#@#@#&@#*$(*#^&*&%^&%%^&%%^&^%$%^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/banhang?charset=utf8mb4' % quote('Az123123123@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

cloudinary.config(cloud_name='dxxwcby8l',
                  api_key='448651448423589',
                  api_secret='ftGud0r1TTqp0CGp5tjwNmkAm-A',
                  api_proxy='http://proxy.server:3128')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'


