from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

carritos = Blueprint('carritos', __name__, template_folder='app/templates')

@carritos.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Carrito_Compras')
    data_carrito = cur.fetchall()
    cur.close()
    return render_template('index_carrito.html', carritos=data_carrito)

@carritos.route('/add_carrito', methods=['POST'])
def add_carrito():
    if request.method == 'POST':
        fecha_creacion = request.form['fecha_creacion']
        estado = request.form['estado']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Carrito_Compras (Fecha_Creacion, Estado) VALUES (%s,%s)",
                (fecha_creacion, estado)
            )
            mysql.connection.commit()
            return redirect(url_for('carritos.index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('carritos.index'))

@carritos.route('/edit_carrito/<id>', methods=['POST', 'GET'])
def get_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Carrito_Compras WHERE ID = %s', (id,))
    data_carrito = cur.fetchall()
    cur.close()
    return render_template('edit-carrito.html', carrito=data_carrito[0])

@carritos.route('/update_carrito/<id>', methods=['POST'])
def update_carrito(id):
    if request.method == 'POST':
        fecha_creacion = request.form['fecha_creacion']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Carrito_Compras
            SET Fecha_Creacion = %s,
                Estado = %s
            WHERE ID = %s
        """, (fecha_creacion, estado, id))
        mysql.connection.commit()
        return redirect(url_for('carritos.index'))

@carritos.route('/delete_carrito/<int:id>', methods=['POST', 'GET'])
def delete_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Carrito_Compras WHERE ID = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('carritos.index'))
