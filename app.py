from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from routes import *
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'evenhome'

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "*"}})

app.add_url_rule(user["datos_cursos"], view_func=user["datos_cursos_controllers"])
app.add_url_rule(user["registro_user"], view_func=user["registro_user_controllers"])
app.add_url_rule(user["login_user"], view_func=user["login_user_controllers"])
app.add_url_rule(user["datos_user"], view_func=user["datos_user_controllers"])
app.add_url_rule(user["actualizar_datos"], view_func=user["actualizar_datos_user_controllers"])
app.add_url_rule(user["editar_vc"], view_func=user["editar_vc_user_controllers"])

app.add_url_rule(user["input_idioma"], view_func=user["input_idioma_controllers"])
app.add_url_rule(user["datos_idioma"], view_func=user["datos_idioma_controllers"])

app.add_url_rule(user["registro_empresa"], view_func=user["registro_empresa_controllers"])
app.add_url_rule(user["login_empresa"], view_func=user["login_empresa_controllers"])

app.add_url_rule(user["input_anuncio"], view_func=user["input_anuncio_controllers"])
app.add_url_rule(user["datos_empresa"], view_func=user["datos_empresa_controllers"])
app.add_url_rule(user["actualizar_datos_empresa"], view_func=user["actualizar_datos_empresa_controllers"])


#
# ------------------------------ Empresa --------------------------------------- #
#
