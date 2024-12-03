from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
from models.models import *
from dotenv import load_dotenv
from functools import wraps
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




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db_user = Usuario.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password_hash, password):
            session['user'] = username      
            return redirect('/dashboard')
        else:
            print("contrasenia incorrecta")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')



# Ruta para el logout
@app.route('/logout')
def logout():
    # Eliminar la sesión actual
    session.pop('user', None)
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('login'))  # Redirige al login después de cerrar sesión



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:  
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function




# Rutas protegidas

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])

@app.route('/productos')
@login_required
def productos():
    return render_template('productos.html', user=session['user'])

@app.route('/')
@login_required
def home():
    return redirect(url_for('login'))



# Ruta que sirve los productos en formato JSON (API)
@app.route('/api/productos', methods=['GET'])
@login_required
def listar_productos():
    productos = Producto.query.all()
    productos_json = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "cantidad": p.cantidad,
            "categoria": p.categoria.nombre if p.categoria else "Sin Categoría"
        }
        for p in productos
    ]
    return jsonify(productos_json)



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
                # print("Usuario admin creado.")
        except Exception as e:
            print(f"Error al crear BD {e}")
    

    app.run(debug=True)
    print(app.url_map)