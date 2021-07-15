from controllers import datosCursosControllers, registroUserControllers, LoginUserControllers, actualizardatosUserControllers, editarvcdatosUserControllers, datosUserControllers, inputidiomaControllers, datosidiomaControllers, deteleidiomaControllers, inputconocimientosControllers, datosconocimientosControllers, inputhojadevidaControllers,datoshojadevidaControllers, registroEmpresaControllers, LoginEmpresaControllers, inputAnuncioControllers, datosEmpresaControllers, actualizardatosEmpresaControllers, datosAnunciosControllers, deteleAnuncioControllers, datosAnunciosAllControllers, consultaAnunciosControllers, generarcorreoUserControllers, VconlineControllers, VconlineidiomaControllers, VconlineconocimientosControllers

user = {

    "datos_cursos": "/api/v01/user/cursos", "datos_cursos_controllers": datosCursosControllers.as_view("Cursos_api"),

    "registro_user": "/api/v01/user/registro", "registro_user_controllers": registroUserControllers.as_view("registro_api"),
    "login_user": "/api/v01/user/login", "login_user_controllers": LoginUserControllers.as_view("login_api"),
    "actualizar_datos": "/api/v01/user/actualizar", "actualizar_datos_user_controllers": actualizardatosUserControllers.as_view("actualizar_api"),

    "editar_vc": "/api/v01/user/editarvc", "editar_vc_user_controllers": editarvcdatosUserControllers.as_view("editar_api"),
    "datos_user": "/api/v01/user/datos", "datos_user_controllers": datosUserControllers.as_view("datos_api"),

    "input_idioma": "/api/v01/user/inputidioma", "input_idioma_controllers": inputidiomaControllers.as_view("input_idioma_api"),
    "datos_idioma": "/api/v01/user/datosidioma", "datos_idioma_controllers": datosidiomaControllers.as_view("datos_idioma_api"),
    "borrar_idioma": "/api/v01/user/borraridioma", "borrar_idioma_controllers": deteleidiomaControllers.as_view("borrar_idioma_api"),

    "input_conocimientos": "/api/v01/user/inputconocimientos", "input_conocimientos_controllers": inputconocimientosControllers.as_view("input_conocimientos_api"),
    "datos_conocimientos": "/api/v01/user/datosconocimientos", "datos_conocimientos_controllers": datosconocimientosControllers.as_view("datos_conocimientos_api"),

    "input_hojadevida": "/api/v01/user/inputhojadevida", "input_hojadevida_controllers": inputhojadevidaControllers.as_view("input_hojadevida_api"),
    "datos_hojadevida": "/api/v01/user/datoshojadevida", "datos_hojadevida_controllers": datoshojadevidaControllers.as_view("datos_hojadevida_api"),

    "generar_correo_user": "/api/v01/user/generarcorreo", "generar_correo_user_controllers": generarcorreoUserControllers.as_view("generar_correo_user_api"),

    "vc_online": "/api/v01/user/vconline", "vc_online_controllers": VconlineControllers.as_view("vc_online_api"),

    "vc_online_idioma": "/api/v01/user/vconlineidioma", "vc_online_idioma_controllers": VconlineidiomaControllers.as_view("vc_online_idioma_api"),

    "vc_online_conocimientos": "/api/v01/user/vconlineconocimientos", "vc_online_conocimientos_controllers": VconlineconocimientosControllers.as_view("vc_online_conocimientos_api"),

    #
    # ------------------------------ Empresa --------------------------------------- #
    #

    "registro_empresa": "/api/v01/empresa/registro", "registro_empresa_controllers": registroEmpresaControllers.as_view("registro_empresa_api"),
    "login_empresa": "/api/v01/empresa/login", "login_empresa_controllers": LoginEmpresaControllers.as_view("login_empresa_api"),

    "datos_empresa": "/api/v01/datos/empresa", "datos_empresa_controllers": datosEmpresaControllers.as_view("datos_empresa_api"),
    "actualizar_datos_empresa": "/api/v01/actualizar/datos/empresa", "actualizar_datos_empresa_controllers": actualizardatosEmpresaControllers.as_view("actualizar_datos_api"),

    #
    # ------------------------------ Empresa --------------------------------------- #
    #

    "input_anuncio": "/api/v01/input/anuncio", "input_anuncio_controllers": inputAnuncioControllers.as_view("input_anuncio_api"),
    "datos_anuncios_all": "/api/v01/datos/anuncios/all", "datos_anuncios_all_controllers": datosAnunciosAllControllers.as_view("datos_anuncios_all_api"),
    "detele_anuncio": "/api/v01/detele/anuncio", "detele_anuncio_controllers": deteleAnuncioControllers.as_view("detele_anuncio_api"),
    "datos_anuncios": "/api/v01/datos/anuncios", "datos_anuncios_controllers": datosAnunciosControllers.as_view("datos_anuncios_api"),
    "consulta_anuncios": "/api/v01/consulta/anuncios", "consulta_anuncios_controllers": consultaAnunciosControllers.as_view("consulta_anuncios_api"),
    
}

