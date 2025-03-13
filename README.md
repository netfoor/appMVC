# POO para Todos

Esta aplicación es una plataforma educativa para aprender los conceptos de Programación Orientada a Objetos (POO) de manera interactiva y sencilla.

## Estructura del Proyecto


## Instalación del Entorno

Para instalar y ejecutar la aplicación en tu entorno local, sigue estos pasos:

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Construye y levanta los contenedores de Docker:
    ```sh
    docker-compose up --build
    ```

3. La aplicación estará disponible en `http://localhost:5000`.

## Uso
### Rutas Disponibles

- `/clase`: Muestra la explicación de qué es una clase en POO.
- `/objeto`: Muestra la explicación de qué es un objeto en POO.

### Ejemplo de Uso

Para ver la explicación de qué es una clase, navega a `http://localhost:5000/clase`.

## Estructura de Archivos

### Controladores

- `clase_controller.py`: Controlador para manejar la lógica de la explicación de clases.
- `objeto_controller.py`: Controlador para manejar la lógica de la explicación de objetos.
- `theory_controller.py`: Controlador para manejar la lógica de las lecciones teóricas.

### Modelos

- `clase_model.py`: Modelo para manejar los datos relacionados con las clases.
- `objeto_model.py`: Modelo para manejar los datos relacionados con los objetos.
- `theory_model.py`: Modelo para manejar los datos relacionados con las lecciones teóricas.

### Servicios

- `interactivity_service.py`: Servicio para manejar la validación de ejercicios interactivos.

### Plantillas

- `clase.html`: Plantilla para la explicación de clases.
- `theory/`: Directorio que contiene las plantillas para las lecciones teóricas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.