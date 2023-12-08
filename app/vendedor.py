from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

vendedores = Blueprint('vendedores', __name__, template_folder='app/templates')

@vendedores.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Vendedor')
    data_vendedor = cur.fetchall()
    cur.close()
    return render_template('index.html', vendedores=data_vendedor)

@vendedores.route('/add_vendedor', methods=['POST'])
def add_vendedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Vendedor (Nombre, Apellido, Telefono, Correo_Electronico) VALUES (%s,%s,%s,%s)",
                (nombre, apellido, telefono, correo_electronico)
            )
            mysql.connection.commit()
            #flash('Vendedor agregado exitosamente')
            return redirect(url_for('vendedores.index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('vendedores.index'))

@vendedores.route('/edit_vendedor/<id>', methods=['POST', 'GET'])
def get_vendedor(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Vendedor WHERE ID = %s', (id))
    data_vendedor = cur.fetchall()
    cur.close()
    print(data_vendedor[0])
    return render_template('edit-vendedor.html', vendedor=data_vendedor[0])

@vendedores.route('/update_vendedor/<id>', methods=['POST'])
def update_vendedor(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Vendedor
            SET Nombre = %s,
                Apellido = %s,
                Telefono = %s,
                Correo_Electronico = %s
            WHERE ID = %s
        """, (nombre, apellido, telefono, correo_electronico, id))
        #flash('Vendedor actualizado exitosamente')
        mysql.connection.commit()
        return redirect(url_for('vendedores.index'))

@vendedores.route('/delete_vendedor/<int:id>', methods=['POST', 'GET'])
def delete_vendedor(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Vendedor WHERE ID = %s', (id,))
    mysql.connection.commit()
    #flash('Vendedor eliminado exitosamente')
    return redirect(url_for('vendedores.index'))
