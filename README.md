```markdown
# POO para Todos

Esta aplicación es una plataforma educativa para aprender los conceptos de Programación Orientada a Objetos (POO) de manera interactiva y sencilla.

## Descripción del Proyecto

POO para Todos es una aplicación web desarrollada con Flask que ofrece lecciones interactivas sobre Programación Orientada a Objetos. El proyecto está diseñado para proporcionar una experiencia de aprendizaje intuitiva utilizando:

*   Explicaciones teóricas claras y concisas
*   Ejemplos prácticos interactivos
*   Ejercicios de codificación en tiempo real
*   Cuestionarios y exámenes para evaluar el progreso
*   Diseño responsivo y amigable para estudiantes de todos los niveles

## Arquitectura del Proyecto (MVC)

Este proyecto sigue el patrón Modelo-Vista-Controlador (MVC):

### Modelo (Model)

*   Ubicación: `models`
*   Responsabilidad: Gestión de datos y lógica de negocio
*   Componentes principales: `usuario_model.py`, `clase_model.py`, `quiz_model.py`, etc.

### Vista (View)

*   Ubicación: `templates`
*   Responsabilidad: Presentación de la información al usuario
*   Tecnologías: HTML, Tailwind CSS, Alpine.js, HTMX

### Controlador (Controller)

*   Ubicación: `controllers`
*   Responsabilidad: Manejo de las peticiones del usuario y coordinación entre modelos y vistas
*   Componentes principales: `theory_controller.py`, `clase_controller.py`, `auth_controller.py`, etc.

## Estructura del Proyecto

```
flask-app/
├── app.py                 
├── database.txt           
├── controllers/           
├── models/                
├── services/              
├── static/                
├── templates/             
│   └── theory/          
└── Dockerfile             
```

## Requisitos

*   Docker y Docker Compose
*   Python 3.10+ (para desarrollo local)
*   Navegador web moderno

## Instalación del Entorno

### Usando Docker (Recomendado)

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/tu-usuario/poo-para-todos.git
    cd poo-para-todos
    ```

2.  Crea un archivo `.env` en la raíz del proyecto (opcional):

    ```bash
    cp .env.example .env
    ```

3.  Construye y levanta los contenedores:

    ```bash
    docker-compose up --build
    ```

    La aplicación estará disponible en `http://localhost:5000`

### Instalación Local (Desarrollo)

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/tu-usuario/poo-para-todos.git
    cd poo-para-todos
    ```

2.  Crea un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  Instala las dependencias:

    ```bash
    cd flask-app
    pip install -r requirements.txt
    ```

4.  Ejecuta la aplicación:

    ```bash
    python app.py
    ```

    La aplicación estará disponible en `http://localhost:5000`

## Base de Datos

El proyecto utiliza una base de datos simple almacenada en `database.txt`.

### Acceso a la Base de Datos

Para acceder y manipular la base de datos:

Con el contenedor en ejecución:

```bash
docker exec -it clases-obj-flask-app-1 bash
```

Desde la terminal del contenedor, puedes manipular la base de datos:

```bash
cat database.txt          # Ver contenido
echo "..." >> database.txt # Añadir contenido
```

### Estructura de la Base de Datos

La base de datos contiene información sobre:

*   Usuarios
*   Progreso en las lecciones
*   Resultados de cuestionarios y exámenes

## Uso

### Rutas Principales

*   `/`: Página principal
*   `/theory/<lesson_id>`: Lecciones teóricas (ej: `/theory/1` para la primera lección)
*   `/clase`: Explicación del concepto de clases
*   `/objeto`: Explicación del concepto de objetos
*   `/quiz/<quiz_id>`: Cuestionarios interactivos
*   `/exam/<exam_id>`: Exámenes de evaluación
*   `/login`: Inicio de sesión
*   `/register`: Registro de usuario

### Características Interactivas

*   Editor de código en vivo: Prueba ejemplos de código Python directamente en el navegador
*   Ejercicios de arrastrar y soltar: Organiza conceptos de POO
*   Cuestionarios interactivos: Verifica tu comprensión

## Desarrollo

### Añadir Nuevas Lecciones

1.  Crea un archivo HTML en `theory`
2.  Actualiza el controlador en `theory_controller.py`
3.  Añade la ruta en `app.py` si es necesario

## Herramientas y Tecnologías

*   Backend: Flask (Python)
*   Frontend: HTML, Tailwind CSS, Alpine.js, HTMX
*   Editor de Código: CodeMirror
*   Contenerización: Docker
*   Estilos: Tailwind CSS

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1.  Haz un fork del repositorio
2.  Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3.  Haz commit de tus cambios (`git commit -m 'Añade nueva función'`)
4.  Haz push a la rama (`git push origin feature/nueva-funcion`)
5.  Abre un Pull Request

## Guía de Estilo

*   Python: Sigue PEP 8
*   HTML/CSS: Utiliza Tailwind CSS con clases semánticas
*   JavaScript: Prefiere funciones modernas y mantén el código limpio

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio o contacta al mantenedor del proyecto.

Desarrollado con ❤️ para hacer la Programación Orientada a Objetos accesible para todos.

Fortino Romero Mantilla
```