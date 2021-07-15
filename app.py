from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from routes import *
from flask_cors import CORS
from collections import UserDict

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
app.add_url_rule(user["borrar_idioma"], view_func=user["borrar_idioma_controllers"])

app.add_url_rule(user["input_conocimientos"], view_func=user["input_conocimientos_controllers"])
app.add_url_rule(user["datos_conocimientos"], view_func=user["datos_conocimientos_controllers"])

app.add_url_rule(user["input_hojadevida"], view_func=user["input_hojadevida_controllers"])
app.add_url_rule(user["datos_hojadevida"], view_func=user["datos_hojadevida_controllers"])

app.add_url_rule(user["generar_correo_user"], view_func=user["generar_correo_user_controllers"])

app.add_url_rule(user["vc_online"], view_func=user["vc_online_controllers"])

app.add_url_rule(user["vc_online_idioma"], view_func=user["vc_online_idioma_controllers"])

app.add_url_rule(user["vc_online_conocimientos"], view_func=user["vc_online_conocimientos_controllers"])

#
# ------------------------------ Empresa --------------------------------------- #
#

app.add_url_rule(user["registro_empresa"], view_func=user["registro_empresa_controllers"])
app.add_url_rule(user["login_empresa"], view_func=user["login_empresa_controllers"])

app.add_url_rule(user["actualizar_datos_empresa"], view_func=user["actualizar_datos_empresa_controllers"])
app.add_url_rule(user["datos_empresa"], view_func=user["datos_empresa_controllers"])

#
# ------------------------------ Anuncios --------------------------------------- #
#

app.add_url_rule(user["datos_anuncios_all"], view_func=user["datos_anuncios_all_controllers"])
app.add_url_rule(user["input_anuncio"], view_func=user["input_anuncio_controllers"])
app.add_url_rule(user["detele_anuncio"], view_func=user["detele_anuncio_controllers"])
app.add_url_rule(user["datos_anuncios"], view_func=user["datos_anuncios_controllers"])
app.add_url_rule(user["consulta_anuncios"], view_func=user["consulta_anuncios_controllers"])
