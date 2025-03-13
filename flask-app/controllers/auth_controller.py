from flask import render_template, request, redirect, url_for, flash, session
from models.usuario_model import UsuarioModel
import re
import logging

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        logging.basicConfig(level=logging.DEBUG)

    def registro(self):
        # Inicializar errores
        errors = {}

        if request.method == 'POST':
            nombre = request.form.get('nombre', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

            # Validaciones del lado del servidor
            if not nombre:
                errors['nombre'] = 'El nombre es obligatorio'
            
            # Validar formato de email
            email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
            if not email or not email_pattern.match(email):
                errors['email'] = 'Introduce un correo electrónico válido'

            # Validar longitud de contraseña
            if len(password) < 6:
                errors['password'] = 'La contraseña debe tener al menos 6 caracteres'

            # Verificar si el email ya está registrado
            if not errors and self.model.obtener_por_email(email):
                flash('El correo electrónico ya está registrado. Por favor, utiliza otro o inicia sesión.', 'error')
                return render_template('registro.html', errors=errors)

            # Si no hay errores, crear el usuario
            if not errors:
                try:
                    self.model.crear_usuario(nombre, email, password)
                    flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
                    logging.debug(f"Usuario registrado: {email}")
                    return redirect(url_for('login'))
                except Exception as e:
                    logging.error(f"Error al registrar usuario: {e}")
                    flash('Ha ocurrido un error al registrar tu cuenta. Por favor, inténtalo más tarde.', 'error')

        # Si hay errores o es una petición GET, mostrar el formulario
        return render_template('registro.html', errors=errors)

    def login(self):
        errors = {}

        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')

            # Validaciones básicas
            if not email:
                errors['email'] = 'El email es obligatorio'
            
            if not password:
                errors['password'] = 'La contraseña es obligatoria'

            if not errors:
                # Buscar usuario
                usuario = self.model.obtener_por_email(email)
                
                if not usuario:
                    flash('No existe ninguna cuenta con este correo electrónico', 'error')
                elif not self.model.verificar_password(usuario, password):
                    flash('La contraseña es incorrecta', 'error')
                else:
                    # Login exitoso - guardar datos en sesión
                    session['usuario_id'] = usuario[0]
                    session['usuario_nombre'] = usuario[1]
                    logging.debug(f"Usuario autenticado: {email}")
                    
                    # Redireccionar según el caso de uso
                    if 'next' in request.args:
                        return redirect(request.args['next'])
                    else:
                        return redirect(url_for('mostrar_clase'))
        
        return render_template('login.html', errors=errors)

    def logout(self):
        # Limpiar datos de sesión
        session.pop('usuario_id', None)
        session.pop('usuario_nombre', None)
        flash('Has cerrado sesión correctamente', 'success')
        return redirect(url_for('login'))