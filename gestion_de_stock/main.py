from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models.models import *
from dotenv import load_dotenv
# from datetime import timedelta
import os

load_dotenv('/home/mauro/Escritorio/Practica/Gestion-de-Stock/.env')

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestor_stock.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    # esto es para contralar el tiempo de las sessiones por default esta 30min, esto va con el: session.permanent = True, en el login
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db.init_app(app)

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db_user = Usuario.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password_hash, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            print("contrasenia incorrecta")
            return render_template('login.html') 
        
    else:
        return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'user' in session:
 
        # session.permanent = True
        return render_template('dashboard.html', user=session['user'])
    else:
        print("Sesión no activa, redirigiendo a login...")
        return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all() 
            print("Base de datos y tablas creadas.")
            
            # esto es la verificacion de las credenciales de admin, ademas de la creacion si no es existente 
            admin = Usuario.query.filter_by(username='admin').first()
            print(admin) 
            if not admin:
                admin = Usuario(username='admin')
                admin.set_password('admin123')  
            
                db.session.add(admin)
                db.session.commit()
                print("Usuario admin creado.")
        except Exception as e:
            print(f"Error al crear BD {e}")
    
    app.run(debug=True)
