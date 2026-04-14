-- DocuMind - Base de datos principal
-- Servidor: lenovoserver (100.68.201.68)
-- Base: documind_db · Usuario: sergio

CREATE TABLE IF NOT EXISTS documentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    fuente VARCHAR(50) NOT NULL,
    fecha_ingesta TIMESTAMP DEFAULT NOW(),
    estado VARCHAR(50) DEFAULT 'PROCESADO',
    qdrant_collection VARCHAR(100) DEFAULT 'documind',
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS sugerencias (
    id SERIAL PRIMARY KEY,
    fuente VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    titulo VARCHAR(500) NOT NULL,
    texto TEXT NOT NULL,
    url VARCHAR(1000),
    fecha_generacion TIMESTAMP DEFAULT NOW(),
    estado VARCHAR(50) DEFAULT 'PENDIENTE',
    leida BOOLEAN DEFAULT FALSE,
    enviada_correo BOOLEAN DEFAULT FALSE,
    enviada_telegram BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS consultas (
    id SERIAL PRIMARY KEY,
    pregunta TEXT NOT NULL,
    categoria_detectada VARCHAR(100),
    respuesta TEXT,
    chunks_usados INT,
    fecha TIMESTAMP DEFAULT NOW(),
    canal VARCHAR(50)
);
