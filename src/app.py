from flask import Flask, request, session, url_for, render_template, flash, redirect
from flask_jwt_extended import JWTManager, create_access_token
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import os, requests
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
app = Flask(__name__)
app.config["MYSQL_USER"] = os.environ.get("user")
app.config["MYSQL_HOST"]= os.environ.get("host")
app.config["MYSQL_PASSWORD"]= os.environ.get("password")
app.config["MYSQL_DB"]= os.environ.get("base_d")
app.config["SECRET_KEY"]= os.environ.get("SECRET_KEY")
app.config["MYSQL_CURSORCLASS"]= "DictCursor"

conexion = MySQL(app)
app.secret_key="asfaeefwef"
jwt = JWTManager(app)


@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.errorhandler(404)
def inicio(error):
    return render_template("error.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))

@app.route("/register")
def do_register():
    return render_template("register.html")
@app.route("/favoritos")
def do_favoritos():
    return render_template("favoritos.html")

@app.route("/login")
def do_login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    cursor = conexion.connection.cursor()
    query = "SELECT nombre, fecha_registro, ultimo_login FROM users WHERE id=%s"
    cursor.execute(query,(session["id"],))
    resultado = cursor.fetchone()
    cursor.close()
    
    nombre = resultado["nombre"]
    fecha = resultado["fecha_registro"]

    

    
        
    
    return render_template("dashboard.html", dato=nombre, dato_1= fecha)

@app.route("/register", methods=["POST"])
def register():
    cursor=None
    try:
        cursor = conexion.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        nombre = request.form.get("nombre")
        
        if not email or not password or not nombre:
            flash("Rellena los campos")
            return redirect(url_for("do_register"))
    
        query = "SELECT email FROM users WHERE email=%s"
        cursor.execute(query,(email,))
        respuesta = cursor.fetchone()
        password_hash = generate_password_hash(password)
        
        if respuesta:
            flash("Ya estas registrado")
            return redirect(url_for("do_register"))
        
        
        else:
            query = "INSERT INTO users(nombre, email, password_hash) VALUES(%s,%s, %s)"
            cursor.execute(query,(nombre, email, password_hash))
            conexion.connection.commit()  
            token = create_access_token(identity=email)
            session["token"] = token
            return redirect(url_for("do_favoritos"))
        
      

       
    except Exception as e:
        print(e)
        return redirect(url_for("inicio"))
    finally:
        if cursor:
            cursor.close()
            
@app.route("/login", methods=["POST"])
def login():
    cursor=None
    try:
        cursor = conexion.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
       
        
        if not email or not password:
            flash("Rellena los campos")
            return redirect(url_for("do_login"))
    
        query = "SELECT password_hash FROM users WHERE email=%s"
        cursor.execute(query,(email,))
        respuesta = cursor.fetchone()
        contrasena = check_password_hash(respuesta["password_hash"], password)
        
        if not respuesta:
            flash("No estas registrado")
            return redirect(url_for("do_register"))
        
        elif not contrasena:
            flash("No estas registrado")
            return redirect(url_for("do_login"))
        
        else:
            tiempo = datetime.now()
            
            print(str(tiempo))
            query = "UPDATE users SET ultimo_login=%s WHERE email =%s"
            cursor.execute(query,(tiempo, email))
            
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query,(email,))
            usuario_completo = cursor.fetchone()
            
            token = create_access_token(identity=email)
            session["token"] = token
            session["id"] = usuario_completo["id"]
            return redirect(url_for("dashboard"))
           
      
     
      

       
    except Exception as e:
        print(e)
        return redirect(url_for("inicio"))
    finally:
        if cursor:
            cursor.close()          


    
if __name__ == "__main__":
    app.run(debug=True)