CREATE TABLE Usuario(
id SERIAL PRIMARY KEY,
username VARCHAR(1024) NOT NULL,
password VARCHAR(32) NOT NULL,
residencia VARCHAR(100),
sexo VARCHAR(20),
edad int
);

CREATE TABLE Registros(
id SERIAL,
id_user int,
distancia decimal(4,2),
tiempo time,
tipo_carrera VARCHAR(30),
fecha date,
PRIMARY KEY (id,id_user)
);

Alter table Registros ADD CONSTRAINT
FK_Registros FOREIGN KEY (id_user) REFERENCES Usuario (id);

INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Ivan','password','Estado de Mexico','Hombre',22);
INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Monica','moniquinha26','Ciudad de Mexico','Mujer',22);
INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Elizabeth','qwerty12','Toronto','Mujer',31);
INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Paul','543210','Atlanta','Hombre',44);
INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Gabriel','aphelios23','Guadalajara','Hombre',26);
INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('Maite','sirenita','Cancun','Mujer',49);

INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (2,2.2,'01:30:59','Fondo','2019/09/16');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (2,5.64,'4:41:12','Medio-Fondo','2019/12/06');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (4,1.25,'00:30:16','Caminata','2018/07/29');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (1,8.0,'07:41:47','Medio-Fondo','2019/11/03');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (6,4.51,'03:34:30','Fondo','2020/02/12');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (3,2.3,'01:06:16','Caminata','2020/01/25');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (5,1.9,'02:22:27','Caminata','2020/04/30');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (5,3.3,'02:11:43','Medio-Fondo','2019/10/01');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (4,5.46,'04:36:09','Medio-Fondo','2019/10/21');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (1,4.21,'04:57:59','Fondo','2019/12/13');
INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values (6,2.2,'01:30:36','Caminata','2020/03/10');