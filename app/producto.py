from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

productos = Blueprint('productos', __name__, template_folder='app/templates')

@productos.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Producto')
    vendedor_data = cur.fetchall()
    cur.close()
    return render_template('index.html', productos=vendedor_data)

@productos.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Producto (Nombre, Descripcion, Precio, Stock) VALUES (%s,%s,%s,%s)",
                (nombre, descripcion, precio, stock)
            )
            mysql.connection.commit()
            #flash('Producto agregado exitosamente')
            return redirect(url_for('productos.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('productos.Index'))

@productos.route('/edit_producto/<id>', methods=['POST', 'GET'])
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Producto WHERE ID = %s', (id,))
    vendedor_data = cur.fetchall()
    cur.close()
    print(vendedor_data[0])
    return render_template('edit-producto.html', producto=vendedor_data[0])

@productos.route('/update_producto/<id>', methods=['POST'])
def update_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Producto
            SET Nombre = %s,
                Descripcion = %s,
                Precio = %s,
                Stock = %s
            WHERE ID = %s
        """, (nombre, descripcion, precio, stock, id))
        #flash('Producto actualizado exitosamente')
        mysql.connection.commit()
        return redirect(url_for('productos.Index'))

@productos.route('/delete_producto/<int:id>', methods=['POST', 'GET'])
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Producto WHERE ID = %s', (id,))
    mysql.connection.commit()
    #flash('Producto eliminado exitosamente')
    return redirect(url_for('productos.Index'))
