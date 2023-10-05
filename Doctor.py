from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'
cnx = mysql.connector.connect(user='root', password='Lotus@123', host='localhost', database='vivek')
cursor = cnx.cursor()
admin_pass = 'manager'
admin_key = 'system'

db_config = {
    'user': 'root',
    'password': 'Lotus@123',
    'host': 'localhost',
    'database': 'vivek'
}

def get_db():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route("/")
def Home():
    return render_template("Home.html")

@app.route("/Admin_Login", methods=['GET'])
def Admin_Login1():
    return render_template("Admin_Login.html")

@app.route("/Admin_Login", methods=['POST'])
def Admin_Login2():
    username = request.form['username']
    password = request.form['password']
    if username == admin_key and password == admin_pass:
        return redirect("/Administration")
    return render_template("Admin_Login.html", msg='Invalid Credentials!!')

@app.route("/History")
def History():
    return render_template("History.html")

@app.route("/Reach_Us")
def Reach_Us():
    return render_template("Reach_Us.html")

@app.route("/Administration")
def Administration():
    return render_template("Administration.html")

@app.route("/DoctorHome")
def DoctorHome():
    return render_template("DoctorHome.html")

@app.route("/Zookeeper", methods=['GET'])
def Zookeeper():
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT animal_name,name,year_of_join from zookeepers INNER JOIN animals ON zookeepers.animal_id = animals.animal_id"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("Zookeeper.html", data = result)

@app.route("/Zookeeper", methods=['POST'])
def Zookeeper1():
    conn = get_db()
    cursor = conn.cursor()
    oldkeeper = request.form['keeperold']
    newkeeper = request.form['keepernew']
    id = request.form['id']
    date = request.form['date']
    query = "UPDATE zookeepers SET name=%s, id=%s, year_of_join=%s WHERE name=%s"
    cursor.execute(query, (newkeeper, id, date, oldkeeper))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("Zookeeper.html", msg=True)

@app.route("/Animal_Info")
def Animal_Info():
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT image_path,animal_name from user_view"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("Animal_Info.html", data=result)

@app.route("/Animal_Add", methods=['GET'])
def Animal_Add1():
    return render_template("Animal_Add.html")

@app.route("/Animal_Add", methods=['POST'])
def Animal_Add2():
    conn = get_db()
    cursor = conn.cursor()
    animal_name = request.form['animal-name']
    image_store = "E:\\VIVEK TCE COLLEGE\\Second Year\\4th Semester\\Database Management Systems\\Application - Zookeeping\\static\\images\\"
    animal_image = request.files['animal-image']
    animal_image.save(image_store+'upload'+animal_image.filename)
    file_path = 'upload'+animal_image.filename
    cage_no = request.form['cage-number']
    breed = request.form['breed']
    desc = request.form['description']
    query = 'INSERT INTO animals VALUES (%s,%s,%s,%s,%s,%s)'
    values = (animal_name, file_path, cage_no, breed, desc, '21AN31')
    cursor.execute(query,values)
    conn.commit()
    cursor.close()
    conn.close()
    msg = True
    return redirect(url_for("Animal_Add1",msg=msg))

@app.route("/Animal_Remove", methods=['GET'])
def Remove1():
    return render_template("Animal_Remove.html")

@app.route("/Animal_Remove", methods=['POST'])
def Remove2():
    conn = get_db()
    cursor = conn.cursor()
    animal_name2 = request.form['animal-name2']
    query = "SELECT * FROM admin_view where animal_name=%s"
    cursor.execute(query,(animal_name2,))
    out = cursor.fetchone()
    if out:
        query = "DELETE FROM admin_view where animal_name=%s"
        cursor.execute(query,(animal_name2,))
        msg1 = animal_name2+" has been removed"
    else:
        msg1 = animal_name2+" Not Found"
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("Animal_Remove.html", msg1=msg1)

@app.route("/Reports", methods = ['GET'])
def Reports():
    return render_template("Reports.html")

@app.route("/Reports", methods =['POST'])
def Reports1():
    conn = get_db()
    cursor = conn.cursor()
    query1 = 'SELECT COUNT(doctor_id) FROM doctor_details'
    cursor.execute(query1)
    result1 = cursor.fetchall()
    query2 = 'SELECT COUNT(*) FROM zookeepers'
    cursor.execute(query2)
    result2 = cursor.fetchall()[0]
    query3 = 'SELECT COUNT(*) FROM animals'
    cursor.execute(query3)
    result3 = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return render_template("Reports.html", data1 = result1,data2 = result2,data3 = result3)

@app.route("/Doctor_Info")
def Doctor_Info1():
    return render_template("Doctor_Info.html")

@app.route("/Doctor_Info", methods=['POST'])
def Doctor_Info():
    conn = get_db()
    cursor = conn.cursor()
    animal = request.form['animal']
    query = "SELECT name,email,username,animal1,animal2,animal3 FROM doctor_details WHERE animal1 = %s OR animal2 = %s OR animal3 = %s"
    cursor.execute(query,(animal,animal,animal,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("Doctor_Info.html", data=result)

@app.route("/Doctor_Login", methods = ['GET'])
def Doctor_Login():
    return render_template("Doctor_Login.html")

@app.route("/Doctor_Login", methods = ['POST'])
def Login():
    conn = get_db()
    cursor = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    query = "SELECT * FROM doctor_details WHERE username=%s and password=%s"
    cursor.execute(query, (username,password,))
    result = cursor.fetchone()
    if result:
        return redirect(url_for("Appointments", username=username))
    
    msg = 'Invalid username or Password!'
    cursor.close()
    conn.close()
    return render_template('Doctor_Login.html', msg=msg)

@app.route("/Appointments", methods=['GET'])
def Appointments():
    conn = get_db()
    cursor = conn.cursor()
    username = request.args.get('username')
    query = "SELECT * FROM appointments WHERE doctor_id=(SELECT doctor_id FROM doctor_details WHERE username =%s)"
    cursor.execute(query,(username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("Appointments.html", data=result)

@app.route("/Doctor_Register", methods = ['GET'])
def Doctor_Register():
    return render_template("Doctor_Register.html")

@app.route("/Doctor_ContactUs")
def Doctor_ContactUs():
    return render_template("Doctor_ContactUs.html")

@app.route("/Doctor_Register", methods = ['POST'])
def Submit():
    # Create a new database connection
    conn = get_db()
    cursor = conn.cursor()
    name = request.form['name']
    animal1 = request.form['animal1']
    animal2 = request.form['animal2']
    animal3 = request.form['animal3']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    # Check if username already exists
    query = "SELECT * FROM doctor_details WHERE username=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        msg = 'Username already exists. Please choose a different username.'
        return render_template('Doctor_Register.html', msg=msg, out=username)

    msg = 'User Registered Successfully'
    # Insert the new doctor into the database
    query = 'INSERT INTO doctor_details(name, animal1, animal2, animal3, email, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    values = (name, animal1, animal2, animal3, email, username, password)
    cursor.execute(query, values)
    
    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()
    
    # Redirect the user to the login page
    return redirect("/Success1")

@app.route("/Success1")
def Success1():
    return render_template("Success1.html")

@app.route("/AdoptionHome")
def AdoptionHome():
    return render_template("AdoptionHome.html")

@app.route("/AnimalsCost")
def AnimalsCost():
    return render_template("/AnimalsCost.html")

@app.route("/AdoptLogin")
def AdoptLogin():
    return render_template("/AdoptLogin.html")

@app.route("/AdoptReg")
def AdoptReg():
    return render_template("/AdoptReg.html")

if __name__ == "__main__":
    app.run(debug = True)