-- Tabla Cliente
CREATE TABLE Cliente (
    ID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Direccion VARCHAR(200),
    Telefono VARCHAR(20),
    Correo_Electronico VARCHAR(100)
);

-- Tabla Vendedor
CREATE TABLE Vendedor (
    ID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Telefono VARCHAR(20),
    Correo_Electronico VARCHAR(100)
);

-- Tabla Producto
CREATE TABLE Producto (
    ID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion VARCHAR(300),
    Precio DECIMAL(10,2),
    Stock INT
);

-- Tabla Almacén
CREATE TABLE Almacen (
    ID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Direccion VARCHAR(200),
    Telefono VARCHAR(20)
);

-- Tabla Venta
CREATE TABLE Venta (
    ID INT PRIMARY KEY,
    Fecha_Venta DATE,
    Total_Venta DECIMAL(10,2),
    Metodo_Pago VARCHAR(50),
    Cliente_ID INT,
    Vendedor_ID INT,
    CONSTRAINT fk_cliente FOREIGN KEY (Cliente_ID) REFERENCES Cliente(ID),
    CONSTRAINT fk_vendedor FOREIGN KEY (Vendedor_ID) REFERENCES Vendedor(ID)
);

-- Tabla Carrito de Compras
CREATE TABLE Carrito_Compras (
    ID INT PRIMARY KEY,
    Fecha_Creacion DATE,
    Estado VARCHAR(20)
);

-- Relaciones Many-to-Many (Producto - Carrito de Compras) y (Producto - Almacén)
-- Creación de tablas intermedias

-- Producto en Carrito de Compras
CREATE TABLE Producto_Carrito (
    Producto_ID INT,
    Carrito_ID INT,
    CONSTRAINT fk_producto_carrito_producto FOREIGN KEY (Producto_ID) REFERENCES Producto(ID),
    CONSTRAINT fk_producto_carrito_carrito FOREIGN KEY (Carrito_ID) REFERENCES Carrito_Compras(ID)
);

-- Producto en Almacén
CREATE TABLE Producto_Almacen (
    Producto_ID INT,
    Almacen_ID INT,
    -- otros atributos...
    CONSTRAINT fk_producto_almacen_producto FOREIGN KEY (Producto_ID) REFERENCES Producto(ID),
    CONSTRAINT fk_producto_almacen_almacen FOREIGN KEY (Almacen_ID) REFERENCES Almacen(ID)
);

-- Relación Uno a Uno (Venta - Carrito de Compras)
ALTER TABLE Venta ADD (
    Carrito_ID INT UNIQUE,
    CONSTRAINT fk_carrito_venta FOREIGN KEY (Carrito_ID) REFERENCES Carrito_Compras(ID)
);
