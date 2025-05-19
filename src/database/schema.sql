-- Habilitar el uso de claves foráneas
PRAGMA foreign_keys = ON;
-- Standard para la creación de tablas: 3 primeras letras del nombre de la tabla seguido de "_" + 3 letras del nombre del campo
-- Tabla: Deudores
-- Descripción: Almacena información de las personas que tienen deudas o realizan abonos.
CREATE TABLE IF NOT EXISTS Deudores (
    ide_deu INTEGER PRIMARY KEY AUTOINCREMENT, -- id_deudor. Identificador único del deudor
    nom_deu TEXT NOT NULL,                     -- nombre_completo. Nombre completo del deudor
    ced_deu TEXT UNIQUE,                       -- cedula_identidad. Cédula de identidad del deudor
    tel_deu TEXT,                              -- telefono_contacto. Número de teléfono de contacto
    dir_deu TEXT,                              -- direccion_habitacion. Dirección de habitación
    fec_reg_deu TEXT NOT NULL,                 -- fecha_registro. Fecha de registro (Formato ISO8601)
    est_deu CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_deudor. Estatus (A: Activo, I: Inactivo)
    CHECK (est_deu IN ('A', 'I'))
);

-- Tabla: Monedas
-- Descripción: Define las diferentes monedas que el sistema aceptará para las transacciones.
CREATE TABLE IF NOT EXISTS Monedas (
    ide_mon INTEGER PRIMARY KEY AUTOINCREMENT, -- id_moneda. Identificador único de la moneda
    cod_mon TEXT UNIQUE NOT NULL,              -- codigo_moneda. Código (ej: 'USD', 'COP', 'VES')
    nom_mon TEXT NOT NULL,                     -- nombre_moneda. Nombre descriptivo de la moneda
    sim_mon TEXT,                              -- simbolo_moneda. Símbolo (ej: '$', 'Bs.')
    est_mon CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_moneda. Estatus (A: Activa, I: Inactiva)
    CHECK (est_mon IN ('A', 'I'))
);

-- Tabla: TasasCambio
-- Descripción: Registra las tasas de cambio diarias entre pares de monedas.
CREATE TABLE IF NOT EXISTS TasasCambio (
    ide_tas INTEGER PRIMARY KEY AUTOINCREMENT, -- id_tasa. Identificador único de la tasa
    mon_ori_tas INTEGER NOT NULL,              -- moneda_origen_id. FK a Monedas(ide_mon)
    mon_des_tas INTEGER NOT NULL,              -- moneda_destino_id. FK a Monedas(ide_mon)
    val_tas REAL NOT NULL,                     -- valor_tasa. Valor de la tasa
    fec_tas TEXT NOT NULL,                     -- fecha_tasa. Fecha de vigencia (Formato ISO8601)
    est_tas CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_tasa. Estatus (A: Aplicada, X: Anulada)
    CHECK (est_tas IN ('A', 'X')),
    FOREIGN KEY (mon_ori_tas) REFERENCES Monedas(ide_mon),
    FOREIGN KEY (mon_des_tas) REFERENCES Monedas(ide_mon),
    UNIQUE (mon_ori_tas, mon_des_tas, fec_tas) -- Unicidad por par de monedas y fecha
);

-- Tabla: MetodosPago
-- Descripción: Define los diferentes métodos de pago.
CREATE TABLE IF NOT EXISTS MetodosPago (
    ide_met INTEGER PRIMARY KEY AUTOINCREMENT, -- id_metodo. Identificador único del método de pago
    nom_met TEXT UNIQUE NOT NULL,              -- nombre_metodo. Nombre del método de pago
    des_met TEXT,                              -- descripcion_metodo. Descripción adicional
    est_met CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_metodo. Estatus (A: Activo, I: Inactivo)
    CHECK (est_met IN ('A', 'I'))
);

-- Tabla: Transacciones
-- Descripción: Almacena cada operación de deuda o abono.
CREATE TABLE IF NOT EXISTS Transacciones (
    ide_tra INTEGER PRIMARY KEY AUTOINCREMENT, -- id_transaccion. Identificador único
    deu_ide_tra INTEGER NOT NULL,              -- deudor_id. FK a Deudores(ide_deu)
    mon_ide_tra INTEGER NOT NULL,              -- moneda_id. FK a Monedas(ide_mon)
    tip_tra TEXT NOT NULL CHECK (tip_tra IN ('DEUDA', 'ABONO')), -- tipo_transaccion. ('DEUDA' o 'ABONO')
    mto_tra REAL NOT NULL,                     -- monto_transaccion. Monto en su moneda
    fec_hra_tra TEXT NOT NULL,                 -- fecha_hora_transaccion. Fecha y hora (Formato ISO8601)
    des_tra TEXT,                              -- descripcion_transaccion. Descripción adicional
    usu_ide_tra INTEGER,                       -- usuario_id. FK a Usuarios(ide_usu)
    met_ide_tra INTEGER,                       -- metodo_pago_id. FK a MetodosPago(ide_met), si es 'ABONO'
    est_tra CHAR(1) NOT NULL DEFAULT 'V'       -- estatus_transaccion. Estatus (V: Válida, N: Anulada)
    CHECK (est_tra IN ('V', 'N')),
    FOREIGN KEY (deu_ide_tra) REFERENCES Deudores(ide_deu),
    FOREIGN KEY (mon_ide_tra) REFERENCES Monedas(ide_mon),
    FOREIGN KEY (usu_ide_tra) REFERENCES Usuarios(ide_usu),
    FOREIGN KEY (met_ide_tra) REFERENCES MetodosPago(ide_met)
);

-- Tabla: Usuarios
-- Descripción: Gestiona los usuarios del sistema.
CREATE TABLE IF NOT EXISTS Usuarios (
    ide_usu INTEGER PRIMARY KEY AUTOINCREMENT, -- id_usuario. Identificador único del usuario
    nom_usu TEXT UNIQUE NOT NULL,              -- nombre_usuario. Nombre de usuario para login
    cla_usu TEXT NOT NULL,                     -- clave_usuario. Contraseña HASHED
    rol_usu TEXT NOT NULL,                     -- rol_usuario. Rol del usuario
    est_usu CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_usuario. Estatus (A: Activo, I: Inactivo)
    CHECK (est_usu IN ('A', 'I'))
);

-- Tabla: Configuracion
-- Descripción: Almacena parámetros generales del sistema.
CREATE TABLE IF NOT EXISTS Configuracion (
    cla_con TEXT PRIMARY KEY,                  -- clave_configuracion. Clave única del parámetro
    val_con TEXT,                              -- valor_configuracion. Valor del parámetro
    est_con CHAR(1) NOT NULL DEFAULT 'A'       -- estatus_configuracion. Estatus (A: Activo, I: Inactivo)
    CHECK (est_con IN ('A', 'I'))
);

-- Inserción de datos semilla
INSERT OR IGNORE INTO Monedas (cod_mon, nom_mon, sim_mon, est_mon) VALUES
('VES', 'Bolívar Soberano', 'BsS', 'A'),
('COP', 'Peso Colombiano', 'COP', 'A'),
('USD', 'Dólar Americano', '$', 'A');

INSERT OR IGNORE INTO MetodosPago (nom_met, des_met, est_met) VALUES
('Efectivo', 'Pago realizado en dinero físico', 'A'),
('Pago Móvil', 'Pago realizado mediante plataforma de pago móvil interbancario', 'A'),
('Transferencia', 'Transferencia bancaria directa', 'A');

INSERT OR IGNORE INTO Configuracion (cla_con, val_con, est_con) VALUES
('moneda_referencia_id', (SELECT ide_mon FROM Monedas WHERE cod_mon = 'VES'), 'A');