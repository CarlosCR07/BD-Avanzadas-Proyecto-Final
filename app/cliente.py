from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

clientes = Blueprint('clientes', __name__, template_folder='app/templates')

@clientes.route('/')
def index():
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM Cliente')
    cliente_data = cur.fetchall()

    cur.execute('SELECT * FROM Producto')
    productos_data = cur.fetchall()

    cur.execute('SELECT * FROM Vendedor')
    vendedores_data = cur.fetchall()

    cur.execute('SELECT * FROM Almacen')
    almacenes_data = cur.fetchall()

    cur.execute('SELECT * FROM Venta')
    ventas_data = cur.fetchall()

    cur.execute('SELECT * FROM Carrito_Compras')
    carritos_data = cur.fetchall()

    cur.close()
    return render_template('index.html', clientes=cliente_data, productos=productos_data, vendedores=vendedores_data, almacen=almacenes_data, ventas=ventas_data, carritos=carritos_data)
    #return render_template('index.html', clientes=cliente_data)

@clientes.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Cliente (Nombre, Apellido, Direccion, Telefono, Correo_Electronico) VALUES (%s,%s,%s,%s,%s)",
                (nombre, apellido, direccion, telefono, correo_electronico)
            )
            mysql.connection.commit()
            #flash('Cliente agregado exitosamente')
            return redirect(url_for('clientes.index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('clientes.index'))

@clientes.route('/edit_cliente/<id>', methods=['POST', 'GET'])
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE id = %s', (id))
    cliente_data = cur.fetchall()
    cur.close()
    print(cliente_data[0])
    return render_template('edit-cliente.html', cliente=cliente_data[0])

@clientes.route('/update_cliente/<id>', methods=['POST'])
def update_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Cliente
            SET Nombre = %s,
                Apellido = %s,
                Direccion = %s,
                Telefono = %s,
                Correo_Electronico = %s
            WHERE ID = %s
        """, (nombre, apellido, direccion, telefono, correo_electronico, id))
        #flash('Cliente actualizado exitosamente')
        mysql.connection.commit()
        return redirect(url_for('clientes.index'))

@clientes.route('/delete_cliente/<int:id>', methods=['POST', 'GET'])
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Cliente WHERE ID = %s', (id,))
    mysql.connection.commit()
    #flash('Cliente eliminado exitosamente')
    return redirect(url_for('clientes.index'))
