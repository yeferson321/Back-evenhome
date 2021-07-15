from flask.views import MethodView
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from config import KEY_TOKEN_AUTH
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json, _json
import datetime
import time
import bcrypt
import jwt
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'evenhome'

CORS(app, resources={r"/*": {"origins": "*"}})

mysql = MySQL(app)

cursos = [{"id": 1, "img": "https://th.bing.com/th/id/Ra3c3156d499577b15081cf292edcee4a?rik=N84HtXVTkzcntg&pid=ImgRaw",
           "nombre": "KhanAcademy", "descripcion": "Es una organización sin fines de lucro con la misión de proporcionar una educación gratuita, aprenda gratis sobre matemáticas, arte, programación informática, economía, historia y más.", "link": "https://es.khanacademy.org/"},
          {"id": 2, "img": "https://online.columbia.edu/files/2017/01/logo-edx-2lx489l.png",
           "nombre": "edX", "descripcion": "Es una plataforma de cursos abiertos masivos en línea, basada en software de código abierto. Ofrece cursos de nivel universitario sin costes que promueven la investigación y el aprendizaje.", "link": "https://www.edx.org/es"},
          {"id": 3, "img": "https://th.bing.com/th/id/R7a24ffba14e0694152f96bcd0f1c37ca?rik=%2bjUkZUW34CcG4A&pid=ImgRaw",
           "nombre": "Memrise", "descripcion": "Es una plataforma ofrece de manera gratuita técnicas de enseñanza para dominar más de 200 idiomas y dialectos. Te ofrece recordatorios, pruebas e incluso competiciones con los demás usuarios.", "link": "https://www.memrise.com/es/"},
          {"id": 4, "img": "https://cdn.freebiesupply.com/logos/thumbs/2x/udacity-logo.png",
           "nombre": "Udacity", "descripcion": "Es una organización educativa con ánimo de lucro fundada por Sebastian Thrun, David Stavens y Mike Sokolsky que ofrece cursos en línea masivos y abiertos (MOOCs). Según Thrun.", "link": "https://www.udacity.com/"},
          {"id": 5, "img": "https://media-exp1.licdn.com/dms/image/C4D0BAQGlBBVXCfSVag/company-logo_200_200/0?e=2159024400&v=beta&t=vts0NvBVAJyX3sOCv2Uj-7Lxlu1Uag3ydmxYgZIoLcg",
           "nombre": "Google Actívate", "descripcion": "Cursos gratuitos de Google para que te conviertas en un experto en tecnología digital Cursos de marketing online gratuitos - Google Actívate Herramientas, formación y tecnología para ayudar a que tu carrera profesional o tu negocio se fortalezcan.", "link": "https://learndigital.withgoogle.com/activate"},
          {"id": 6, "img": "https://static.wixstatic.com/media/b73e04_edbd2b7697354d30881413f79c60f5b6~mv2_d_3864_3422_s_4_2.jpg/v1/fit/w_2500,h_1330,al_c/b73e04_edbd2b7697354d30881413f79c60f5b6~mv2_d_3864_3422_s_4_2.jpg",
           "nombre": "Duolingo", "descripcion": "En Duolingo puedes aprender el idioma que prefieras. Aprovechan el aprendizaje que hacen unas personas para un proyecto de gran magnitud: traducir Internet. A medida que un estudiante progresa y hace sus ejercicios está contribuyendo a esta tarea, por lo que se ve recompensado.", "link": "https://es.duolingo.com/"},
          {"id": 7, "img": "https://yt3.ggpht.com/a-/AAuE7mAqNcah25ocnt8NLmBxdyNzVk3aorXCW4SEMA=s900-mo-c-c0xffffffff-rj-k-no",
           "nombre": "Open Culture", "descripcion": "Desde el sitio de Open Culture se puede acceder a un buen número de cursos online gratuitos. No es una plataforma formativa al uso, pero alberga multitud de enlaces, clasificados en base al campo al que pertenece la materia que se imparte en ellos.", "link": "https://www.openculture.com/"},
          {"id": 8, "img": "https://btcces.com/web/wp-content/uploads/2020/02/mooc.jpg",
           "nombre": "Mooc", "descripcion": "Los Mooc son Cursos Online Gratis de las mejores universidades del mundo y que puedes cursar para mejorar en tu trabajo. Su potencial reside en su capacidad para conectar el conocimiento de los participantes.", "link": "https://mooc.es/"}
          ]


class datosCursosControllers(MethodView):
    """
        datos
    """

    def get(self):
        return jsonify({"data": cursos}), 200


class registroUserControllers(MethodView):
    """
        datos
    """

    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(.500)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        correo = content.get("correo")
        contraseña = content.get("contraseña")
        condiciones = content.get("condiciones")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(
            bytes(str(contraseña), encoding='utf-8'), salt)
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()

        #hace la insercion
        cur.execute("INSERT INTO usuario (nombre, apellidos, correo, contrasena, condiciones) VALUES (%s,%s,%s,%s,%s)",
                    (nombre, apellidos, correo, hash_password, condiciones))
        mysql.connection.commit()

        #consulta
        cur.execute("SELECT id_user, nombre, apellidos, correo, contrasena FROM usuario WHERE correo=%s", ([correo]))
        user = cur.fetchall()
        user = user[0]
        id_user = user[0]
        correo = user[3]
        clave = user[4]
        
        cur.close()

        if bcrypt.hashpw(bytes(str(contraseña), encoding='utf-8'), salt):

            encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
                hours=10), 'correo': correo, 'id_user': id_user, 'tipo_user': 'usuario'}, KEY_TOKEN_AUTH, algorithm='HS256')

        return jsonify({"auth": True, 'id_user': user[0], "nombre": user[1], "apellidos": user[2], "correo": user[3], "token": encoded_jwt}), 200


class LoginUserControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        email = content.get("correo")
        password = content.get("contraseña")
        # creamos comandos sql para verificar que la informacion que ingresamos sea correcta
        curl = mysql.connection.cursor()
        curl.execute(
            "SELECT id_user, nombre, apellidos, correo, contrasena FROM usuario WHERE correo=%s", ([email]))
        user = curl.fetchall()
        user = user[0]
        id_user = user[0]
        correo = user[3]
        clave = user[4]
        usuario = {}
        usuario[correo] = {"contraseña": clave}
        curl.close()
        # creamos diversos caminos que el sofware puede coger
        if len(user) > 0:

            passwordb = usuario[correo]["contraseña"]

            if bcrypt.checkpw(bytes(str(password), encoding='utf-8'), passwordb.encode('utf-8')):

                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=10), 'correo': correo, 'id_user': id_user, 'tipo_user': 'usuario'}, KEY_TOKEN_AUTH, algorithm='HS256')

                return jsonify({"auth": True, 'id_user': user[0], "nombre": user[1], "apellidos": user[2], "correo": user[3], "token": encoded_jwt}), 200

        else:
            return jsonify({"auth": False, }), 403


class actualizardatosUserControllers(MethodView):
    """
        datos
    """

    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(.500)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        genero = content.get("genero")
        cargo = content.get("cargo")
        tipoidentificacion = content.get("tipoidentificacion")
        identificacion = content.get("identificacion")
        fechanacimiento = content.get("fechanacimiento")
        estadocivil = content.get("estadocivil")
        telefono = content.get("telefono")
        otrotelefono = content.get("otrotelefono")
        horadecontacto = content.get("horadecontacto")
        pais = content.get("pais")
        ciudad = content.get("ciudad")
        direccion = content.get("direccion")
        id_user = content.get('id')
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute(f'UPDATE usuario SET nombre= "{nombre}", apellidos= "{apellidos}", genero= "{genero}", cargo= "{cargo}", tipoidentificacion= "{tipoidentificacion}", identificacion= "{identificacion}", fechanacimiento= "{fechanacimiento}", estadocivil= "{estadocivil}", telefono= "{telefono}", otrotelefono= "{otrotelefono}", horadecontacto= "{horadecontacto}", pais= "{pais}", cuidad= "{ciudad}", direccion= "{direccion}" WHERE id_user = "{id_user}"')
        mysql.connection.commit()
        cur.close()
        return jsonify({"registro ok": True, "nombre": nombre, "apellidos": apellidos}), 200


class editarvcdatosUserControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        genero = content.get("genero")
        cargo = content.get("cargo")
        tipoidentificacion = content.get("tipoidentificacion")
        identificacion = content.get("identificacion")
        fechanacimiento = content.get("fechanacimiento")
        estadocivil = content.get("estadocivil")
        telefono = content.get("telefono")
        otrotelefono = content.get("otrotelefono")
        horadecontacto = content.get("horadecontacto")
        pais = content.get("pais")
        ciudad = content.get("ciudad")
        direccion = content.get("direccion")
        id_user = content.get('id')
        print("cme:", id_user)
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute(f'UPDATE usuario SET nombre = "{nombre}", apellidos = "{apellidos}", genero = "{genero}", cargo = "{cargo}", tipoidentificacion = "{tipoidentificacion}", identificacion = "{identificacion}", fechanacimiento = "{fechanacimiento}", estadocivil = "{estadocivil}", telefono = "{telefono}", otrotelefono = "{otrotelefono}", horadecontacto = "{horadecontacto}", pais = "{pais}", cuidad = "{ciudad}", direccion = "{direccion}" WHERE id_user = "{id_user}"')
        mysql.connection.commit()
        cur.close()
        return jsonify({"registro ok": True, "nombre": nombre, "apellidos": apellidos}), 200


class datosUserControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute(
                    "select nombre, apellidos, genero, cargo, tipoidentificacion, identificacion, fechanacimiento, estadocivil, telefono, otrotelefono, horadecontacto, pais, cuidad, direccion from usuario where correo=%s", ([correo]))
                dato = curl.fetchall()
                datos_user = dato
                #empresa, funcion_empresa, area_empresa, logros, idiomas, nivel, centro_estudios, nivel_estudios, titulación, estado, conocimientos, conocimientosescritos, hoja_vida

                return jsonify({"datos": datos_user}), 200

            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403



class inputidiomaControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        idioma = content.get("idioma")
        nivel = content.get("nivel")
        id = content.get("id")
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO idioma (idiomas, nivel, usuario_id) VALUES (%s,%s,%s)",
                    (idioma, nivel, id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"registro ok": True}), 200


class datosidiomaControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                id_user = request.args.get('id')
                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute("select id_idioma, idiomas, nivel, usuario_id from idioma where usuario_id=%s", ([id_user]))
                dato = curl.fetchall()
                curl.close()
                datos_user = dato

                data = []
                objeto = {}
                for value in dato:
                    objecto={'id_idioma':value[0], 'idiomas':value[1], 'nivel':value[2], 'usuario_id':value[3]}
                    data.append(objecto)
                    objecto = {}

                return jsonify({"data": data}), 200

            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


class deteleidiomaControllers(MethodView):
    """
        datos
    """

    def delete(self):
        id_user = request.args.get('id')
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute(f'delete from idioma where id_idioma = "{id_user}"')
        mysql.connection.commit()
        cur.close()

        return jsonify({"ok": True}), 200


class inputconocimientosControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        conocimientosescritos = content.get("conocimientosescritos")
        id = content.get("id")
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO conocimientos (conocimientosescritos, usuario_id) VALUES (%s,%s)", (conocimientosescritos, id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"registro ok": True}), 200


class datosconocimientosControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                id_user = request.args.get('id')
                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute("select conocimientosescritos from conocimientos where usuario_id=%s", ([id_user]))
                dato = curl.fetchall()
                curl.close()
                datos_user = dato

                return jsonify({"datos": datos_user}), 200

            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


class inputhojadevidaControllers(MethodView):
    """
        datos
    """
    def post(self):
        time.sleep(.500)
        hojavida = request.form.get("hojavida")
        id_user = request.form.get("id")
        f = request.files['pdfword']
        os.mkdir('archivos/'+'user_'+id_user)
        f.save(os.path.join('archivos/'+'user_'+id_user, secure_filename(id_user+"_documento.pdf")))
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        #conexion con el cursor para enviar datos, si se maneja curl con l todos la deben tener o si es cur solo todos deben ser cur 
        cur.execute(f'UPDATE usuario SET hoja_vida = "{hojavida}" WHERE id_user = "{id_user}"')
        mysql.connection.commit()
        cur.close()
        #cierre de la peticion a la bd
        return jsonify({"registro ok": True}), 200



class datoshojadevidaControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                id_user = request.args.get('id')
                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute("select hoja_vida, id_user from usuario where id_user=%s", ([id_user]))
                dato = curl.fetchall()
                curl.close()
                datos_user = dato

                return jsonify({"datos": datos_user}), 200


            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


#
#
# ------------------------------ Empresa --------------------------------------- #
#
#


class registroEmpresaControllers(MethodView):
    """
        datos
    """

    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(.500)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        telefono = content.get("telefono")
        correo = content.get("correo")
        contraseña = content.get("contraseña")
        nombrempresa = content.get("nombrempresa")
        denominacionsocial = content.get("denominacionsocial")
        pais = content.get("pais")
        tamañoempresa = content.get("tamañoempresa")
        ciudad = content.get("ciudad")
        codigo = content.get("codigo")
        direccion = content.get("direccion")
        telefonoempresa = content.get("telefonoempresa")
        actividad = content.get("actividad")
        descripcion = content.get("descripcion")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(
            bytes(str(contraseña), encoding='utf-8'), salt)
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empresa (nombre, apellidos, correo, telefono, contrasena, nombrempresa, Denominacionsocial, tamañoempresa, actividadempresa, pais, cuidad, codigonif, direccion, telefonoempresa, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (nombre, apellidos, correo, telefono, hash_password, nombrempresa, denominacionsocial, tamañoempresa, actividad, pais, ciudad, codigo, direccion, telefonoempresa, descripcion))
        mysql.connection.commit()

        #consulta
        cur.execute("SELECT id_empresa, nombrempresa, correo, contrasena FROM empresa WHERE correo=%s", ([correo]))
        user = cur.fetchall()
        user = user[0]
        id_user = user[0]
        correo = user[2]
        clave = user[3] 
        cur.close()

        if bcrypt.hashpw(bytes(str(contraseña), encoding='utf-8'), salt):

            encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=10), 'correo': correo, 'id_user': id_user, 'tipo_user': 'empresa'}, KEY_TOKEN_AUTH, algorithm='HS256')

        return jsonify({"auth": True, "nombre": user[1], "correo": user[2], "id_user": user[0], "token": encoded_jwt}), 200



class LoginEmpresaControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        email = content.get("correo")
        password = content.get("contraseña")
        # creamos comandos sql para verificar que la informacion que ingresamos sea correcta
        curl = mysql.connection.cursor()
        curl.execute(
            "SELECT id_empresa, nombrempresa, correo, contrasena FROM empresa WHERE correo=%s", ([email]))
        user = curl.fetchall()
        user = user[0]
        id_user = user[0]
        correo = user[2]
        clave = user[3]
        usuario = {}
        usuario[correo] = {"contraseña": clave}
        curl.close()
        # creamos diversos caminos que el sofware puede coger
        if len(user) > 0:

            passwordb = usuario[correo]["contraseña"]

            if bcrypt.checkpw(bytes(str(password), encoding='utf-8'), passwordb.encode('utf-8')):

                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=10), 'correo': correo, 'id_user': id_user, 'tipo_user': 'empresa'}, KEY_TOKEN_AUTH, algorithm='HS256')

                return jsonify({"auth": True, "id_user": user[0], "nombre": user[1], "correo": user[2], "token": encoded_jwt}), 200

        else:
            return jsonify({"auth": False, }), 403


class actualizardatosEmpresaControllers(MethodView):
    """
        datos
    """

    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(.500)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        telefono = content.get("telefono")
        nombrempresa = content.get("nombrempresa")
        denominacionsocial = content.get("denominacionsocial")
        pais = content.get("pais")
        tamañoempresa = content.get("tamañoempresa")
        ciudad = content.get("ciudad")
        codigo = content.get("codigo")
        direccion = content.get("direccion")
        telefonoempresa = content.get("telefonoempresa")
        actividad = content.get("actividad")
        descripcion = content.get("descripcion")
        id_user = content.get("id")
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute(f'UPDATE empresa SET nombre= "{nombre}", apellidos= "{apellidos}", telefono= "{telefono}", nombrempresa= "{nombrempresa}", Denominacionsocial= "{denominacionsocial}", tamañoempresa= "{tamañoempresa}", actividadempresa= "{actividad}", pais= "{pais}", cuidad= "{ciudad}", codigonif= "{codigo}", direccion= "{direccion}", telefonoempresa= "{telefonoempresa}", descripcion= "{descripcion}" WHERE id_empresa= "{id_user}"')
        mysql.connection.commit()
        cur.close()
        return jsonify({"registro ok": True,}), 200


class datosEmpresaControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute(
                    "select nombre, apellidos, correo, telefono, nombrempresa, Denominacionsocial, tamañoempresa, actividadempresa, pais, cuidad, codigonif, direccion, telefonoempresa, descripcion, PáginaWeb from empresa where correo=%s", ([correo]))
                dato = curl.fetchall()
                datos_user = dato

                return jsonify({"datos": datos_user}), 200

            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


class inputAnuncioControllers(MethodView):
    """
        datos
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        vacantes = content.get("vacantes")
        profesiones = content.get("profesiones")
        experiencia = content.get("experiencia")
        herramientas = content.get("herramientas")
        duracion = content.get("duracion")
        nivel = content.get("nivel")
        empleo = content.get("empleo")
        salario = content.get("salario")
        descripcion = content.get("descripcion")
        nombre = content.get("nombre")
        id_user = content.get("id")
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `anuncios` (`numerovacantes`, `profesiones`, `experiencia`, `herramientas`, `duracion`, `nivel`, `empleo`, `salario`, `descripcion`, `nombre`, `usuario_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (vacantes, profesiones, experiencia, herramientas, duracion, nivel, empleo, salario, descripcion, nombre, id_user))
        mysql.connection.commit()
        cur.close()

        return jsonify({"registro ok": True}), 200

class deteleAnuncioControllers(MethodView):
    """
        datos
    """

    def delete(self):
        id_user = request.args.get('id')
        # comandos sql para agregar infomacion a la tabla users
        cur = mysql.connection.cursor()
        cur.execute(f'delete from anuncios where id_anuncio = "{id_user}"')
        mysql.connection.commit()
        cur.close()

        return jsonify({"ok": True}), 200


class datosAnunciosControllers(MethodView):
    """
        datos
    """

    def get(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            # print("-----------------_", token[1])
            try:
                data = jwt.decode(
                    token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
                correo = data.get("correo")

                id_user = request.args.get('id')
                datos_user = ""
                curl = mysql.connection.cursor()
                curl.execute(
                    "select id_anuncio, titulo, profesiones, experiencia, herramientas, duracion, nivel, empleo, salario, descripcion from anuncios where usuario_id=%s", ([id_user]))
                dato = curl.fetchall()
                datos_anuncios = dato

                data = []
                objeto = {}
                for value in dato:
                    objecto={'id_anuncio':value[0], 'titulo':value[1], 'profesiones':value[2], 'experiencia':value[3], 'herramientas':value[4], 'duracion':value[5], 'nivel':value[6], 'empleo':value[7], 'salario':value[8], 'descripcion':value[9]}
                    data.append(objecto)
                    objecto = {}

                return jsonify({"data": data}), 200

            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


#
#
# ------------------------------ Anuncios --------------------------------------- #
#
#


class datosAnunciosAllControllers(MethodView):
    """
        datos
    """

    def get(self):

        datos_user = ""
        curl = mysql.connection.cursor()
        curl.execute("select id_anuncio, numerovacantes, profesiones, experiencia, herramientas, duracion, nivel, empleo, salario, descripcion, nombre, usuario_id, solicitudes from anuncios")
        dato = curl.fetchall()
        datos_anuncios = dato

        data = []
        objeto = {}
        for value in dato:
            objecto={'id_anuncio':value[0], 'numerovacantes':value[1], 'profesiones':value[2], 'experiencia':value[3], 'herramientas':value[4], 'duracion':value[5], 'nivel':value[6], 'empleo':value[7], 'salario':value[8], 'descripcion':value[9], 'nombre':value[10], 'usuario_id':value[11], 'solicitudes':value[12]}
            data.append(objecto)
            objecto = {} 

        return jsonify({"dato": data}), 200


class consultaAnunciosControllers(MethodView):
    """
        datos
    """

    def post(self):
        content = request.get_json()
        palabra = content.get('palabra')
        habilidad = content.get('habilidad')

        datos_user = ""
        curl = mysql.connection.cursor()
        curl.execute(f'SELECT id_anuncio, numerovacantes, profesiones, experiencia, herramientas, duracion, nivel, empleo, salario, descripcion, nombre, usuario_id, solicitudes FROM anuncios where profesiones like "%{palabra}%" and herramientas like "%{habilidad}%" ')
        dato = curl.fetchall()
        datos_anuncios = dato

        data = []
        objeto = {}
        for value in dato:
            objecto={'id_anuncio':value[0], 'numerovacantes':value[1], 'profesiones':value[2], 'experiencia':value[3], 'herramientas':value[4], 'duracion':value[5], 'nivel':value[6], 'empleo':value[7], 'salario':value[8], 'descripcion':value[9], 'nombre':value[10], 'usuario_id':value[11], 'solicitudes':value[12]}
            data.append(objecto)
            objecto = {} 

        return jsonify({"dato": data}), 200




class generarcorreoUserControllers(MethodView):
    def post(self):

        if (request.headers.get('Authorization')):
                token = request.headers.get('Authorization').split(" ")
                data= jwt.decode(token[1], KEY_TOKEN_AUTH , algorithms=['HS256'])
                correo = data.get("correo")

                content = request.get_json()
                id_anuncio = content.get('id_anuncio')
                usuario_id = content.get('usuario_id')
                profesiones = content.get('profesiones')
                nombre = content.get('nombre')

                curl = mysql.connection.cursor()
                curl.execute("select correo from empresa where id_empresa=%s", ([usuario_id]))
                user = curl.fetchone() 
                user = user[0]
                curl.close()

                curl = mysql.connection.cursor()
                curl.execute("select solicitudes from anuncios where id_anuncio=%s", ([id_anuncio]))
                num = curl.fetchone() 
                num = num[0]
                curl.close()

                cur = mysql.connection.cursor()
                cur.execute(f'UPDATE anuncios SET solicitudes = "{num + 1}" WHERE id_anuncio= "{id_anuncio}"')
                mysql.connection.commit()
                cur.close()

                #credenciales
                proveedor_correo = 'smtp.live.com: 587'
                remitente = 'evenhome90@gmail.com'
                password = 'flzqxbqmbfbplwxm'
                #conexion a servidor
                #servidor = smtplib.SMTP(proveedor_correo)
                servidor = smtplib.SMTP('smtp.gmail.com:587')
                servidor.starttls()
                servidor.ehlo()
                #autenticacion
                servidor.login(remitente, password)
                #mensaje 
               
                #envio correo al empresa
                mensaje_institucion = "<h2> <h2 style='text-align: center; color:  #1ed760; font-family: cursive;'>Evenhome<h2/> <br> <h2 style='text-align: center; color:  #1ed760;'>Se acaba de generar una nueva solicitud de empleo a tu anuncio '{}'<br> <h3 style='text-align: center; color: #000000;'>Tienes 3 dias para responder este mensaje, de no hacerlo perderas a uno de los mejores talentos<br>Puedes comunicarte con tu talento al siguiente correo: {}<br>Mira su Vc Online en Evenhome http://localhost:4200/vc_online_usuario<h3/> <br> <p style='text-align: center; color: #88898c;'>Recibes este email por estar registrado en Evenhome<p> <h2/>".format(profesiones,correo)
                msg = MIMEMultipart()
                msg.attach(MIMEText(mensaje_institucion, 'html'))
                #correo
                msg['From'] = remitente
                #correo destinatario
                msg['To'] = user
                msg['Subject'] = 'Nueva solicitud de empleo'
                servidor.sendmail(msg['From'] , msg['To'], msg.as_string())

                #envio correo al usuario
                mensaje_institucion = "<h2> <h2 style='text-align: center; color:  #1ed760; font-family: cursive;'>Evenhome<h2/> <br> <h2 style='text-align: center; color:  #1ed760;'>Se acaba de inscribir a la oferta remota '{}'<br> <h3 style='text-align: center; color: #000000;'>La empresa '{}' Tienes 3 dias para ponerse en contacto con tigo, de no hacerlo se cancelara el proceso<br><h3/> <br> <p style='text-align: center; color: #88898c;'>Recibes este email por estar registrado en Evenhome<p> <h2/>".format(profesiones,nombre)
                msg = MIMEMultipart()
                msg.attach(MIMEText(mensaje_institucion, 'html'))
                #correo
                msg['From'] = remitente
                #correo destinatario
                msg['To'] = correo
                msg['Subject'] = 'Inscripcion a oferta remota'
                servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
                
                return jsonify({"registro ok": True,}), 200
        return jsonify({"Status": "No ha enviado un token"}), 403


class VconlineControllers(MethodView):
    """
        datos
    """

    def get(self):
        content = request.get_json()

        id_user = 1

        curl = mysql.connection.cursor()
        curl.execute("select id_user, correo, nombre, apellidos, genero, cargo, tipoidentificacion, identificacion, fechanacimiento, estadocivil, telefono, otrotelefono, horadecontacto, pais, cuidad, direccion, hoja_vida from usuario where id_user=%s", ([id_user]))
        datosuser = curl.fetchall()
        curl.close()

        datosusuario = []
        objeto = {}
        for value in datosuser:
            objecto={'id_user':value[0], 'correo':value[1], 'nombre':value[2], 'apellidos':value[3], 'genero':value[4], 'cargo':value[5], 'tipoidentificacion':value[6], 'identificacion':value[7], 'fechanacimiento':value[8], 'estadocivil':value[9], 'telefono':value[10], 'otrotelefono':value[11], 'horadecontacto':value[12], 'pais':value[13], 'cuidad':value[14], 'direccion':value[15], 'hoja_vida':value[16]}
            datosusuario.append(objecto)
            objecto = {} 

        return jsonify({"datosusuario": datosusuario}), 200


class VconlineidiomaControllers(MethodView):
    """
        datos
    """

    def get(self):
        content = request.get_json()

        id_user = 1

        curl = mysql.connection.cursor()
        curl.execute("select id_idioma, idiomas, nivel, usuario_id from idioma where usuario_id=%s", ([id_user]))
        datos = curl.fetchall()
        curl.close()

        datosidioma = []
        objeto = {}
        for value in datos:
            objecto={'id_idioma':value[0], 'idiomas':value[1], 'nivel':value[2], 'usuario_id':value[3]}
            datosidioma.append(objecto)
            objecto = {} 

        return jsonify({"datosidioma": datosidioma}), 200


class VconlineconocimientosControllers(MethodView):
    """
        datos
    """

    def get(self):
        content = request.get_json()

        id_user = 1

        curl = mysql.connection.cursor()
        curl.execute("select id_conocimientos, conocimientosescritos, usuario_id from conocimientos where usuario_id=%s", ([id_user]))
        dato = curl.fetchall()
        curl.close()

        datosconocimientos = []
        objeto = {}
        for value in dato:
            objecto={'id_conocimientos':value[0], 'conocimientosescritos':value[1], 'usuario_id':value[2]}
            datosconocimientos.append(objecto)
            objecto = {} 

        return jsonify({"datosconocimientos": datosconocimientos}), 200
