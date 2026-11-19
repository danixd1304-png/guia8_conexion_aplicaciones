-- =====================================================================
-- practica8_procedimientos.sql
-- Guía 8 - Procedimientos almacenados que se llaman desde Python (Actividad 3).
-- Base de datos: mydb (la misma de las prácticas anteriores).
--
-- 1) RegistrarMatricula: es el procedimiento de la Práctica 5, SIN cambios.
--    (Si ya lo tienes creado en tu servidor, esta parte solo lo recrea igual.)
-- 2) sp_promedio_estudiante y sp_historial_estudiante: adicionales de esta
--    práctica para mostrar otro parámetro OUT y un SELECT dentro de un SP.
-- =====================================================================
SET NAMES utf8mb4;
USE mydb;

DROP PROCEDURE IF EXISTS RegistrarMatricula;
DROP PROCEDURE IF EXISTS sp_promedio_estudiante;
DROP PROCEDURE IF EXISTS sp_historial_estudiante;

DELIMITER //

-- ---------- Práctica 5 (sin cambios) ----------
CREATE PROCEDURE RegistrarMatricula(
    IN p_id_estudiante INT,
    IN p_id_curso INT,
    OUT p_mensaje VARCHAR(200)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Estudiante
        WHERE idEstudiante = p_id_estudiante
    ) THEN
        SET p_mensaje = 'Error: el estudiante no existe';

    ELSEIF NOT EXISTS (
        SELECT 1 FROM curso
        WHERE idcurso = p_id_curso
    ) THEN
        SET p_mensaje = 'Error: el curso no existe';

    ELSE
        INSERT INTO Matricula (
            fecha_matricula,
            periodo,
            estado,
            id_estudiante,
            costo_matricula
        )
        VALUES (
            CURDATE(),
            '2026-2',
            'Activa',
            p_id_estudiante,
            5000000
        );

        SET @id_matricula = LAST_INSERT_ID();

        INSERT INTO Detalle_Matricula (
            id_matricula,
            id_curso,
            nota_final
        )
        VALUES (
            @id_matricula,
            p_id_curso,
            NULL
        );

        SET p_mensaje = 'Éxito: matrícula registrada correctamente';
    END IF;
END //

-- ---------- Adicionales de la Práctica 8 ----------
-- Promedio de notas de un estudiante (ignora las notas NULL).
--   IN  p_id_estudiante : id del estudiante
--   OUT p_promedio      : promedio de nota_final (NULL si no tiene notas)
CREATE PROCEDURE sp_promedio_estudiante(
    IN  p_id_estudiante INT,
    OUT p_promedio DECIMAL(3,2)
)
BEGIN
    SELECT AVG(d.nota_final)
      INTO p_promedio
      FROM Matricula m
      JOIN Detalle_Matricula d ON d.id_matricula = m.idMatricula
     WHERE m.id_estudiante = p_id_estudiante
       AND d.nota_final IS NOT NULL;
END //

-- Historial académico: devuelve un conjunto de resultados (SELECT).
CREATE PROCEDURE sp_historial_estudiante(IN p_id_estudiante INT)
BEGIN
    SELECT m.periodo, c.nombre AS curso, c.creditos, d.nota_final
      FROM Matricula m
      JOIN Detalle_Matricula d ON d.id_matricula = m.idMatricula
      JOIN curso c             ON c.idcurso = d.id_curso
     WHERE m.id_estudiante = p_id_estudiante
     ORDER BY m.periodo, c.nombre;
END //

DELIMITER ;
