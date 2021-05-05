from controllers import registroUserControllers, LoginUserControllers, datosCursosControllers, datosUserControllers

user = {

    "datos_cursos": "/api/v01/user/cursos", "datos_cursos_controllers": datosCursosControllers.as_view("Cursos_api"),
    "registro_user": "/api/v01/user/registro", "registro_user_controllers": registroUserControllers.as_view("registro_api"),
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "datos_user": "/api/v01/user/datos", "datos_user_controllers": datosUserControllers.as_view("datos_api")
}