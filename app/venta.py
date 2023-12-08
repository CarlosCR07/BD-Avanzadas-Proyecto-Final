from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

ventas = Blueprint('ventas', __name__, template_folder='app/templates')

@ventas.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Venta')
    data_venta = cur.fetchall()
    cur.close()
    return render_template('index.html', ventas=data_venta)

@ventas.route('/add_venta', methods=['POST'])
def add_venta():
    if request.method == 'POST':
        fecha_venta = request.form['fecha_venta']      
        total_venta = request.form['total_venta']
        metodo_pago = request.form['metodo_pago']
        cliente_id = request.form['cliente_id']
        vendedor_id = request.form['vendedor_id']
        carrito_id =  request.form['carrito_id']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Venta (Fecha_Venta, Total_Venta, Metodo_Pago, Cliente_ID, Vendedor_ID, Carrito_ID) VALUES (%s,%s,%s,%s,%s,%s)",
                (fecha_venta, total_venta, metodo_pago, cliente_id, vendedor_id, carrito_id)
            )
            mysql.connection.commit()
            #flash('Venta agregada exitosamente')
            return redirect(url_for('ventas.index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('ventas.index'))

@ventas.route('/edit_venta/<id>', methods=['POST', 'GET'])
def get_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Venta WHERE ID = %s', (id,))
    data_venta = cur.fetchall()
    cur.close()
    print(data_venta[0])
    return render_template('edit-venta.html', venta=data_venta[0])

@ventas.route('/update_venta/<id>', methods=['POST'])
def update_venta(id):
    if request.method == 'POST':
        fecha_venta = request.form['fecha_venta']
        total_venta = request.form['total_venta']
        metodo_pago = request.form['metodo_pago']
        cliente_id = request.form['cliente_id']
        vendedor_id = request.form['vendedor_id']
        carrito_id =  request.form['carrito_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Venta
            SET Fecha_Venta = %s,
                Total_Venta = %s,
                Metodo_Pago = %s,
                Cliente_ID = %s,
                Vendedor_ID = %s,
                Carrito_ID = %s
            WHERE ID = %s
        """, (fecha_venta, total_venta, metodo_pago, cliente_id, vendedor_id, carrito_id, id))
        #flash('Venta actualizada exitosamente')
        mysql.connection.commit()
        return redirect(url_for('ventas.index'))

@ventas.route('/delete_venta/<int:id>', methods=['POST', 'GET'])
def delete_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Venta WHERE ID = %s', (id,))
    mysql.connection.commit()
    #flash('Venta eliminada exitosamente')
    return redirect(url_for('ventas.index'))
