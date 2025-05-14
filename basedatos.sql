-- Habilitar el uso de claves foráneas (recomendado ejecutar al inicio de la conexión)
PRAGMA foreign_keys = ON;

-- Tabla: Deudores
-- Descripción: Almacena información de las personas que tienen deudas o realizan abonos.
CREATE TABLE Deudores (
    deu_ide INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único del deudor (Clave Primaria)
    deu_nom TEXT NOT NULL,                     -- Nombre completo del deudor
    deu_ced TEXT UNIQUE,                       -- Cédula de identidad del deudor (debe ser única si se usa)
    deu_tel TEXT,                              -- Número de teléfono de contacto del deudor
    deu_dir TEXT,                              -- Dirección de habitación del deudor
    deu_fec TEXT NOT NULL,                     -- Fecha de registro del deudor en el sistema (Formato ISO8601 YYYY-MM-DD HH:MM:SS)
    deu_est CHAR(1) NOT NULL DEFAULT 'A'       -- Estatus del deudor (A: Activo, I: Inactivo). CHECK constraint abajo.
    CHECK (deu_est IN ('A', 'I'))
);

-- Tabla: Monedas
-- Descripción: Define las diferentes monedas que el sistema aceptará para las transacciones.
CREATE TABLE Monedas (
    mon_ide INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la moneda (Clave Primaria)
    mon_cod TEXT UNIQUE NOT NULL,              -- Código de la moneda (ej: 'USD', 'COP', 'VES')
    mon_nom TEXT NOT NULL,                     -- Nombre descriptivo de la moneda (ej: 'Dólar Americano')
    mon_sim TEXT,                              -- Símbolo de la moneda (ej: '$', 'Bs.')
    mon_est CHAR(1) NOT NULL DEFAULT 'A'       -- Estatus de la moneda (A: Activa, I: Inactiva). CHECK constraint abajo.
    CHECK (mon_est IN ('A', 'I'))
);

-- Tabla: TasasCambio
-- Descripción: Registra las tasas de cambio diarias entre pares de monedas, ingresadas manualmente.
CREATE TABLE TasasCambio (
    tas_ide INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la tasa de cambio (Clave Primaria)
    tas_mon_ori INTEGER NOT NULL,              -- ID de la moneda origen (FK a Monedas.mon_ide)
    tas_mon_des INTEGER NOT NULL,              -- ID de la moneda destino (FK a Monedas.mon_ide), usualmente la moneda local de referencia
    tas_val REAL NOT NULL,                     -- Valor de la tasa (ej: cuántas 'mon_des' equivalen a una 'mon_ori')
    tas_fec TEXT NOT NULL,                     -- Fecha de vigencia para esta tasa (Formato ISO8601 YYYY-MM-DD)
    tas_est CHAR(1) NOT NULL DEFAULT 'A'       -- Estatus de la tasa (A: Aplicada/Válida, X: Anulada/Corregida). CHECK constraint abajo.
    CHECK (tas_est IN ('A', 'X')),
    FOREIGN KEY (tas_mon_ori) REFERENCES Monedas(mon_ide),
    FOREIGN KEY (tas_mon_des) REFERENCES Monedas(mon_ide),
    UNIQUE (tas_mon_ori, tas_mon_des, tas_fec) -- Asegura que solo hay una tasa por par de monedas por día (válida)
);

-- Tabla: Transacciones
-- Descripción: Almacena cada operación de deuda o abono realizada por un deudor.
CREATE TABLE Transacciones (
    tra_ide INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la transacción (Clave Primaria)
    tra_deu_ide INTEGER NOT NULL,              -- ID del deudor asociado a la transacción (FK a Deudores.deu_ide)
    tra_mon_ide INTEGER NOT NULL,              -- ID de la moneda en que se realizó la transacción (FK a Monedas.mon_ide)
    tra_tip TEXT NOT NULL,                     -- Tipo de transacción ('DEUDA' para un nuevo fiao, 'ABONO' para un pago) CHECK (tra_tip IN ('DEUDA', 'ABONO'))
    tra_mto REAL NOT NULL,                     -- Monto de la transacción en la moneda especificada en 'tra_mon_ide'
    tra_fec_hra TEXT NOT NULL,                 -- Fecha y hora exactas de la transacción (Formato ISO8601 YYYY-MM-DD HH:MM:SS)
    tra_des TEXT,                              -- Descripción adicional o nota sobre la transacción (opcional)
    tra_usu_ide INTEGER,                       -- ID del usuario que registró la transacción (FK a Usuarios.usu_ide, opcional si no hay login detallado)
    tra_est CHAR(1) NOT NULL DEFAULT 'V'       -- Estatus de la transacción (V: Válida, N: Anulada). CHECK constraint abajo.
    CHECK (tra_est IN ('V', 'N')),
    FOREIGN KEY (tra_deu_ide) REFERENCES Deudores(deu_ide),
    FOREIGN KEY (tra_mon_ide) REFERENCES Monedas(mon_ide),
    FOREIGN KEY (tra_usu_ide) REFERENCES Usuarios(usu_ide)
);

-- Tabla: Usuarios
-- Descripción: Gestiona los usuarios del sistema (inicialmente, el propietario).
CREATE TABLE Usuarios (
    usu_ide INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único del usuario (Clave Primaria)
    usu_nom TEXT UNIQUE NOT NULL,              -- Nombre de usuario para login (debe ser único)
    usu_cla TEXT NOT NULL,                     -- Contraseña del usuario (se debe almacenar un HASH, no la clave en texto plano)
    usu_rol TEXT NOT NULL,                     -- Rol del usuario (ej: 'propietario', 'administrador')
    usu_est CHAR(1) NOT NULL DEFAULT 'A'       -- Estatus del usuario (A: Activo, I: Inactivo). CHECK constraint abajo.
    CHECK (usu_est IN ('A', 'I'))
);

-- Tabla: Configuracion
-- Descripción: Almacena parámetros y configuraciones generales del sistema.
CREATE TABLE Configuracion (
    con_cla TEXT PRIMARY KEY,                  -- Clave única para el parámetro de configuración (ej: 'moneda_referencia_id')
    con_val TEXT,                              -- Valor asociado a la clave de configuración
    con_est CHAR(1) NOT NULL DEFAULT 'A'       -- Estatus del parámetro (A: Activo, I: Inactivo). CHECK constraint abajo.
    CHECK (con_est IN ('A', 'I'))
);

-- (Los ejemplos de INSERT se mantienen igual, pero ahora las tablas tienen la columna de estatus con su valor por defecto 'A' o 'V')
INSERT INTO Monedas (mon_cod, mon_nom, mon_sim) VALUES
('VES', 'Bolívar Soberano', 'BsS'),
('COP', 'Peso Colombiano', 'COP'),
('USD', 'Dólar Americano', '$');

INSERT INTO Configuracion (con_cla, con_val) VALUES
('moneda_referencia_id', (SELECT mon_ide FROM Monedas WHERE mon_cod = 'VES'));