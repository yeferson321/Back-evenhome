from controllers import datosCursosControllers, registroUserControllers, LoginUserControllers, actualizardatosUserControllers, editarvcdatosUserControllers, datosUserControllers, inputidiomaControllers, datosidiomaControllers, registroEmpresaControllers, LoginEmpresaControllers, inputAnuncioControllers,  datosEmpresaControllers, actualizardatosEmpresaControllers

user = {

    "datos_cursos": "/api/v01/user/cursos", "datos_cursos_controllers": datosCursosControllers.as_view("Cursos_api"),
    "registro_user": "/api/v01/user/registro", "registro_user_controllers": registroUserControllers.as_view("registro_api"),
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "actualizar_datos": "/api/v01/user/actualizar", "actualizar_datos_user_controllers": actualizardatosUserControllers.as_view("actualizar_api"),
    "editar_vc": "/api/v01/user/editarvc", "editar_vc_user_controllers": editarvcdatosUserControllers.as_view("editar_api"),
    "datos_user": "/api/v01/user/datos", "datos_user_controllers": datosUserControllers.as_view("datos_api"),

    "input_idioma": "/api/v01/user/inputidioma", "input_idioma_controllers": inputidiomaControllers.as_view("input_idioma_api"),
    "datos_idioma": "/api/v01/user/datosidioma", "datos_idioma_controllers": datosidiomaControllers.as_view("datos_idioma_api"),

    #
    # ------------------------------ Empresa --------------------------------------- #
    #

    "registro_empresa": "/api/v01/empresa/registro", "registro_empresa_controllers": registroEmpresaControllers.as_view("registro_empresa_api"),
    "login_empresa": "/api/v01/empresa/login", "login_empresa_controllers": LoginEmpresaControllers.as_view("login_empresa_api"),

    "input_anuncio": "/api/v01/input/anuncio", "input_anuncio_controllers": inputAnuncioControllers.as_view("input_anuncio_api"),

    "datos_empresa": "/api/v01/datos/empresa", "datos_empresa_controllers": datosEmpresaControllers.as_view("datos_empresa_api"),

    "actualizar_datos_empresa": "/api/v01/actualizar/datos/empresa", "actualizar_datos_empresa_controllers": actualizardatosEmpresaControllers.as_view("actualizar_datos_api"),


}

