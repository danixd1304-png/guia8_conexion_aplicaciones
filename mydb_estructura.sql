-- Estructura de la base de datos mydb (tomada de quiz_en_clase_SQL.sql)
CREATE DATABASE mydb;
USE mydb;

CREATE TABLE Carrera (
    idCarrera INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    Facultad VARCHAR(100),
    Duracion_semestres varchar (100),
    modalidad VARCHAR(30)
);

CREATE TABLE Profesor (
    idProfesor INT PRIMARY KEY AUTO_INCREMENT,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    titulo VARCHAR(100) NOT NULL
);

CREATE TABLE Estudiante (
    idEstudiante INT PRIMARY KEY AUTO_INCREMENT,
    documento VARCHAR(20) NOT NULL,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    correo VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(150),
    id_carrera INT,
    FOREIGN KEY (id_carrera) REFERENCES Carrera(idCarrera)
);

CREATE TABLE curso (
    idcurso INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    creditos INT,
    semestre INT,
    id_profesor INT,
    FOREIGN KEY (id_profesor) REFERENCES Profesor(idProfesor)
);

CREATE TABLE Matricula (
    idMatricula INT PRIMARY KEY AUTO_INCREMENT,
    fecha_matricula DATE,
    periodo VARCHAR(10),
    estado VARCHAR(20),
    id_estudiante INT,
    costo_matricula DECIMAL(10,2),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiante(idEstudiante)
);

CREATE TABLE Detalle_Matricula (
    idDetalle INT PRIMARY KEY AUTO_INCREMENT,
    id_matricula INT,
    id_curso INT,
    nota_final DECIMAL(3,2),
    FOREIGN KEY (id_matricula) REFERENCES Matricula(idMatricula),
    FOREIGN KEY (id_curso) REFERENCES curso(idcurso)
);
