CREATE TABLE IF NOT EXISTS pacientes (
	id_paciente SERIAL PRIMARY KEY,
	nombre_paciente VARCHAR(100) NOT NULL
);

	-- Tabla de sensores vinculados a pacientes
CREATE TABLE IF NOT EXISTS sensores (
	id_sensor SERIAL PRIMARY KEY,
	id_paciente INTEGER NOT NULL,
	tipo_sensor VARCHAR(50) NOT NULL,
	unidad VARCHAR(10) NOT NULL,
	CONSTRAINT fk_paciente
		FOREIGN KEY(id_paciente)
		REFERENCES pacientes(id_paciente)
		ON DELETE CASCADE
);

				-- Tabla de logs de sensores (valores registrados)
CREATE TABLE IF NOT EXISTS log_sensores (
	id SERIAL PRIMARY KEY,
	id_sensor INTEGER NOT NULL,
	valor FLOAT NOT NULL,
	time TIMESTAMP NOT NULL DEFAULT NOW(),
	CONSTRAINT fk_sensor
		FOREIGN KEY(id_sensor)
		REFERENCES sensores(id_sensor)
		ON DELETE CASCADE
);

				-- (Opcional) Ejemplo de datos iniciales
INSERT INTO pacientes (nombre_paciente) VALUES ('Paciente 1'), ('Paciente 2');

INSERT INTO sensores (id_sensor, id_paciente, tipo_sensor, unidad) VALUES 
    (1, 1, 'Temperatura corporal', '°C'),
    (2, 1, 'Ritmo cardiaco', 'BPM'),
    (3, 2, 'Presion arterial', 'mmHg');
