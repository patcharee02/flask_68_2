from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "flower_db"

app.config['SECRET_KEY'] = 'loksbisjobuthsohtbsuohborhb'

@app.route('/home', methods=['GET'])
def home():
    name = "Anya"
    age = 7
    my_dict = {"name": "Yor", "age": 26}
    return render_template('home.html', name=name, age=age, my_dict=my_dict)


@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')


@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        flower_name = request.form['flower_name']
        flower_price = request.form['flower_price']
        flower_place = request.form['flower_place']
        flower_description = request.form['flower_description']
        print('store.html', flower_name, flower_price, flower_place, flower_description)

        my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
        )

        my_cursor = my_db.cursor(dictionary=True)
        sql = "INSERT INTO flowers (flower_name, flower_price, flower_place, flower_description) VALUES (%s, %s, %s, %s)"
        val = (flower_name, flower_price, flower_place, flower_description)
        my_cursor.execute(sql, val)
        my_db.commit()
        my_db.close()

        session['alert_status'] = "success"
        session['alert_message'] = "Flower added successfully!"
        return redirect('/')
    else:

        session['alert_status'] = "danger"
        session['alert_message'] = "Failed to add flower."  
        return redirect('/')

@app.route('/', methods=['GET'])
def index():
    my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
        )
    my_cursor = my_db.cursor(dictionary=True)

    sql = "SELECT * FROM flowers"
    my_cursor.execute(sql)
    flowers = my_cursor.fetchall()
    my_db.close()

    if 'alert_status' in session and 'alert_message' in session:
        alert_message = {
            'status': session['alert_status'],
            'message': session['alert_message']
        }
        del session['alert_status']
        del session['alert_message']
    else:
        alert_message = {
            'status' : None,
            'message' : None
        }

    return render_template('index.html', flowers=flowers, alert_message=alert_message)

@app.route('/edit/<int:flower_id>', methods=['GET'])
def edit(flower_id):
    my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    my_cursor = my_db.cursor(dictionary=True)

    sql = "SELECT * FROM flowers WHERE id = %s"
    val = (flower_id,)
    my_cursor.execute(sql, val)
    flower = my_cursor.fetchall()
    my_db.close()

    return render_template('edit.html', flower=flower)

@app.route('/update/<int:flower_id>', methods=['POST'])
def update(flower_id):
    if request.method == 'POST':
        flower_name = request.form['flower_name']
        flower_price = request.form['flower_price']
        flower_place = request.form['flower_place']
        flower_description = request.form['flower_description']
        print('UPDATE INPUT:', flower_id, flower_price, flower_place, flower_description)

        my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
        )

        my_cursor = my_db.cursor(dictionary=True)
        sql = "UPDATE flowers SET flower_name = %s, flower_price = %s, flower_place = %s, flower_description = %s WHERE id = %s"
        val = (flower_name, flower_price, flower_place, flower_description, flower_id)
        my_cursor.execute(sql, val)
        my_db.commit()
        my_db.close()

        session['alert_status'] = "success"
        session['alert_message'] = "Flower updated successfully!"
        return redirect('/')
    else:

        session['alert_status'] = "danger"
        session['alert_message'] = "Failed to update flower."
        return redirect('/')
    
@app.route('/delete/<int:flower_id>', methods=['GET'])
def delete(flower_id):
    my_db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,   
        password=DB_PASS,
        database=DB_NAME
    )
    my_cursor = my_db.cursor(dictionary=True)

    sql = "DELETE FROM flowers WHERE id = %s"
    val = (flower_id,)
    my_cursor.execute(sql, val)
    my_db.commit()
    my_db.close()

    session['alert_status'] = "success"
    session['alert_message'] = "Flower deleted successfully!"
    return redirect('/')

    
if __name__ == '__main__':
    # app.run()# production mode
    app.run(debug=True)  # development mode