from flask import render_template, request, redirect, url_for, session, flash
from models.usuario_model import UsuarioModel

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()

    def registro(self):
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password']

            if self.model.obtener_por_email(email):
                flash('El email ya está registrado', 'error')
                return redirect(url_for('registro'))

            self.model.crear_usuario(nombre, email, password)
            flash('Registro exitoso. ¡Inicia sesión!', 'success')
            return redirect(url_for('login'))

        return render_template('registro.html')

    def login(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            usuario = self.model.obtener_por_email(email)

            if usuario and self.model.verificar_password(usuario, password):
                session['usuario_id'] = usuario[0]
                session['usuario_nombre'] = usuario[1]
                return redirect(url_for('mostrar_clase'))
            
            flash('Credenciales incorrectas', 'error')
        
        return render_template('login.html')

    def logout(self):
        session.clear()
        return redirect(url_for('login'))