from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

almacen = Blueprint('almacen', __name__, template_folder='app/templates')

@almacen.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Almacen')
    almacen_data = cur.fetchall()
    cur.close()
    return render_template('almacen_index.html', almacen=almacen_data)

@almacen.route('/add_almacen', methods=['POST'])
def add_almacen():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Almacen (Nombre, Direccion, Telefono) VALUES (%s,%s,%s)",
                (nombre, direccion, telefono)
            )
            mysql.connection.commit()
            #flash('Almacén agregado exitosamente')
            return redirect(url_for('almacen.index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('almacen.index'))

@almacen.route('/edit_almacen/<id>', methods=['POST', 'GET'])
def get_almacen(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Almacen WHERE ID = %s', (id,))
    almacen_data = cur.fetchall()
    cur.close()
    print(almacen_data[0])
    return render_template('edit-almacen.html', almacen=almacen_data[0])

@almacen.route('/update_almacen/<id>', methods=['POST'])
def update_almacen(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Almacen
            SET Nombre = %s,
                Direccion = %s,
                Telefono = %s
            WHERE ID = %s
        """, (nombre, direccion, telefono, id))
        #flash('Almacén actualizado exitosamente')
        mysql.connection.commit()
        return redirect(url_for('almacen.index'))

@almacen.route('/delete_almacen/<int:id>', methods=['POST', 'GET'])
def delete_almacen(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Almacen WHERE ID = %s', (id,))
    mysql.connection.commit()
    #flash('Almacén eliminado exitosamente')
    return redirect(url_for('almacen.index'))
