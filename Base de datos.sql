create schema evenhome;
use evenhome;

create table usuario(
id_user int primary key not null auto_increment,
correo varchar(50)  not null ,
contrasena varchar(256) not null,
nombre char(20) not null,
apellidos char(50) not null,
condiciones char(8),
genero char(9) not null,
cargo char(25) not null,
tipoidentificacion char(24) not null,
identificacion varchar(20) not null,
fechanacimiento date not null,
estadocivil char(11) not null,
telefono varchar(50) not null,
otrotelefono varchar(50) not null,
horadecontacto char(11) not null,
pais char(20) not null,
cuidad varchar(20) not null,
direccion varchar(100) not null,
empresa varchar(40) not null,
funcion_empresa varchar(50) not null,
area_empresa char(37) not null,
logros varchar(255),
id_idioma int not null,
centro_estudios varchar(40) not null,
nivel_estudios char(33) not null,
titulación varchar(50) not null,
estado char(21) not null,
conocimientos char(20) not null,
conocimientosescritos char(20) not null,
hoja_vida varchar(255) not null,
pdf_word blob,
foto blob,	/*ruta donde esta la imagen en el disco duro*/
UNIQUE INDEX (`correo` ASC)
);

create table idioma(
id_idioma  int primary key not null auto_increment,
idiomas char(14) not null,
nivel char(10) not null
);

create table empresa(
id_empresa int primary key not null auto_increment,
nombre char(20) not null,
apellidos char(50) not null,
correo varchar(50)  not null,
telefono varchar(50) not null,
contrasena varchar(256) not null,
nombrempresa varchar(40) not null,
Denominacionsocial varchar(40) not null,
tamañoempresa char(25),
actividadempresa char(37),
pais char(20) not null,
cuidad varchar(20) not null,
codigonif varchar(20) not null,
direccion varchar(100) not null,
telefonoempresa varchar(50) not null,
descripcion varchar(200) not null,
PáginaWeb char(255) not null,
UNIQUE INDEX (`correo` ASC)
);

create table anuncios(
id_anuncio int primary key auto_increment,
idempresa int not null,
titulo varchar(30) not null,
profesiones char(26) not null,
experiencia char(17) not null,
herramientas char(255) not null,
duracion char(16) not null,
nivel char(12) not null,
empleo char(15) not null,
salario char(15) not null,
descripcion char(255) not null
);

alter table idioma add foreign key(id_idioma) references usuario(id_idioma);
alter table anuncios add foreign key(idempresa) references empresas(idempresa);
