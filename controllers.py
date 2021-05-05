from flask.views import MethodView
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from config import KEY_TOKEN_AUTH
import datetime
import time
import bcrypt
import jwt
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'refugio'

mysql = MySQL(app)
       
cursos = [{"id": 1, "img": "https://th.bing.com/th/id/Ra3c3156d499577b15081cf292edcee4a?rik=N84HtXVTkzcntg&pid=ImgRaw",
                 "nombre": "KhanAcademy", "descripcion": "Es una organización sin fines de lucro con la misión de proporcionar una educación gratuita, aprenda gratis sobre matemáticas, arte, programación informática, economía, historia y más."},
             {"id": 2, "img": "https://online.columbia.edu/files/2017/01/logo-edx-2lx489l.png",
                 "nombre": "edX", "descripcion": "Es una plataforma de cursos abiertos masivos en línea, basada en software de código abierto. Ofrece cursos de nivel universitario sin costes que promueven la investigación y el aprendizaje."},
             {"id": 3, "img": "https://th.bing.com/th/id/R7a24ffba14e0694152f96bcd0f1c37ca?rik=%2bjUkZUW34CcG4A&pid=ImgRaw",
                 "nombre": "Memrise", "descripcion": "Es una plataforma ofrece de manera gratuita técnicas de enseñanza para dominar más de 200 idiomas y dialectos. Te ofrece recordatorios, pruebas e incluso competiciones con los demás usuarios."},
             {"id": 4, "img": "https://cdn.freebiesupply.com/logos/thumbs/2x/udacity-logo.png",
                 "nombre": "Udacity", "descripcion": "Es una organización educativa con ánimo de lucro fundada por Sebastian Thrun, David Stavens y Mike Sokolsky que ofrece cursos en línea masivos y abiertos (MOOCs). Según Thrun, el origen del nombre Udacity proviene del deseo de la compañía de ser audaz para ti,"},
             {"id": 5, "img": "https://th.bing.com/th/id/OIP.PgSrriHOvKAvVGwdUda6PgAAAA?pid=ImgDet&rs=1",
                 "nombre": "Google Actívate", "descripcion": "Cursos gratuitos de Google para que te conviertas en un experto en tecnología digital Cursos de marketing online gratuitos - Google Actívate Herramientas, formación y tecnología para ayudar a que tu carrera profesional o tu negocio se fortalezcan."},
             {"id": 6, "img": "https://static.wixstatic.com/media/b73e04_edbd2b7697354d30881413f79c60f5b6~mv2_d_3864_3422_s_4_2.jpg/v1/fit/w_2500,h_1330,al_c/b73e04_edbd2b7697354d30881413f79c60f5b6~mv2_d_3864_3422_s_4_2.jpg",
                 "nombre": "Duolingo", "descripcion": "En Duolingo puedes aprender el idioma que prefieras. Aprovechan el aprendizaje que hacen unas personas para un proyecto de gran magnitud: traducir Internet. A medida que un estudiante progresa y hace sus ejercicios está contribuyendo a esta tarea, por lo que se ve recompensado."},
             {"id": 7, "img": "https://th.bing.com/th/id/OIP._X9GGpXnboE8GCldjkPeEgAAAA?pid=ImgDet&rs=1",
                 "nombre": "Open Culture", "descripcion": "Desde el sitio de Open Culture se puede acceder a un buen número de cursos online gratuitos. No es una plataforma formativa al uso, pero alberga multitud de enlaces, clasificados en base al campo al que pertenece la materia que se imparte en ellos."},
             {"id": 8, "img": "https://btcces.com/web/wp-content/uploads/2020/02/mooc.jpg",
                 "nombre": "Mooc", "descripcion": "Los Mooc son Cursos Online Gratis de las mejores universidades del mundo y que puedes cursar para mejorar en tu trabajo. Su potencial reside en su capacidad para conectar el conocimiento de los participantes."}
             ]

class datosCursosControllers(MethodView):
    """
        datos
    """
    def get(self):
        return jsonify({"data": cursos}), 200


class registroUserControllers(MethodView):
    """
        Registro
    """
    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(1)
        content = request.get_json()
        nombre = content.get("nombre")
        apellido = content.get("apellido")
        correo = content.get("correo")
        telefono = content.get("telefono")
        contraseña = content.get("contraseña")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(contraseña), encoding= 'utf-8'), salt)
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre, apellido, correo, telefono, contraseña) VALUES (%s,%s,%s,%s,%s)",
                    (nombre, apellido, correo, telefono, hash_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"registro ok": True, "nombre": nombre,  "apellido": apellido}), 200
       


class LoginUserControllers(MethodView):
    """
        Login 
    """
    def post(self):
        time.sleep(1)
        content = request.get_json()
        email = content.get("correo")
        password = content.get("contraseña")
        # creamos comandos sql para verificar que la informacion que ingresamos sea correcta
        curl = mysql.connection.cursor()
        curl.execute("SELECT nombre, apellido, correo, contraseña FROM usuario WHERE correo=%s", ([email]))
        user = curl.fetchall()
        user = user[0]
        correo = user[2] 
        clave = user[3]
        usuario = {}
        usuario[correo] = {"contraseña":clave} 
        curl.close()
        # creamos diversos caminos que el sofware puede coger
        if len(user) > 0:
        
            passwordb = usuario[correo]["contraseña"]

            if bcrypt.checkpw(bytes(str(password), encoding= 'utf-8'), passwordb.encode('utf-8')):

               encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15), 'correo': correo}, KEY_TOKEN_AUTH , algorithm='HS256')   
               
               return jsonify({"auth": True, "nombre": user[0], "token": encoded_jwt}), 200  
               
            else:
                return jsonify({"auth": False,}), 403
        else:
            return jsonify({"auth": False,}), 401


class datosUserControllers(MethodView):
    """
         adopcion
     """
    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(1)
        content = request.get_json()
        nombres = content.get("nombre")
        apellidos = content.get("apellido")
        documento = content.get("documento")
        fechanacimineto = content.get("fechanaci")
        telefono = content.get("telefono")
        sexo = content.get("sexo")
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre2, apellido2, documento, fechanaci, cel, sexo) VALUES (%s,%s,%s,%s,%s,%s)",
                    (nombres, apellidos, documento, fechanacimineto, telefono, sexo))
        mysql.connection.commit()
        cur.close()
        return jsonify({"datos ok": True}), 200


