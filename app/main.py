from app import app
#from contacts import contacts
from cliente import clientes
from vendedor import vendedores
from producto import productos
from almacen import almacen
from venta import ventas
from carrito import carritos
#from producto_carrito import productos_carrito

#app.register_blueprint(contacts)
app.register_blueprint(clientes)
app.register_blueprint(vendedores)
app.register_blueprint(productos)
app.register_blueprint(almacen)
app.register_blueprint(ventas)
app.register_blueprint(carritos)
#app.register_blueprint(productos_carrito)

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)