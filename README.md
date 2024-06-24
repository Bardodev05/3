# proyecto de gestion de instrumentos


Proyecto de Gestión de Instrumentos

Este proyecto es una aplicación desarrollada con FastAPI, SQLAlchemy y Pydantic, diseñada para gestionar usuarios e instrumentos musicales. La aplicación permite registrar, actualizar, eliminar, crear y consultar información sobre usuarios e instrumentos.

## Características

- Autenticación JWT para proteger rutas sensibles.
- Registro y gestión de usuarios.
- Gestión de instrumentos musicales (CRUD).
- Relación muchos a muchos entre usuarios e instrumentos.

## Tecnologías Utilizadas

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite (puede cambiarse a cualquier otra base de datos soportada por SQLAlchemy)
- Passlib (para hashing de contraseñas)
- Python-JOSE (para JWT)

## Requisitos Previos

- Python 3.7+
- PIP (Python Package Installer)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

</code></div></div><monica-code-tools></monica-code-tools></pre>

2. Crea y activa un entorno virtual:
   En Windows usa `env\Scripts\activate`
   </code></div></div><monica-code-tools></monica-code-tools></pre>
3. Instala las dependencias:
   pip install -r requirements.txt
   </code></div></div><monica-code-tools></monica-code-tools></pre>

## Uso

1. Inicia el servidor FastAPI:
   uvicorn main:app --reload
   </code></div></div><monica-code-tools></monica-code-tools></pre>
2. Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para ver la documentación interactiva de la API generada por Swagger.

## Endpoints Principales

### Autenticación

* **POST**`/jwtauth/login` - Inicio de sesión para obtener un token JWT.
* **POST**`/jwtauth/register` - Registro de nuevos usuarios.
* **GET**`/jwtauth/users/me` - Obtener información del usuario autenticado.
* **DELETE**`/jwtauth/users/{username}` - Eliminar un usuario.
* **PATCH**`/jwtauth/users/{username}` - Actualizar un usuario.

### Gestión de Instrumentos

* **GET**`/instrumentos` - Obtener una lista de todos los instrumentos.
* **GET**`/instrumentos/{instrumento_id}` - Obtener un instrumento por ID.
* **POST**`/instrumentos` - Crear un nuevo instrumento.
* **PUT**`/instrumentos/{instrumento_id}` - Actualizar un instrumento.
* **DELETE**`/instrumentos/{instrumento_id}` - Eliminar un instrumento.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un "issue" para reportar bugs o sugerir nuevas funcionalidades. También puedes abrir un "pull request" con tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

este proyecto es una aplicacion desarollada por fastapi,sqlalchemy y pydatic diseñada para gestionar usuarios e instrumentos musicales. la aplicacion permite hacer un registro,actulizar ,eliminar, crear y consultar informacion sobre usuarios e instrumentos.

# caracteristicas

-autentificacion JWT para proteger rutas sencibles.

-registro y gestion de usuarios.

-gestion de instrumentos musicales(crud).

-uso de sqlalchemy para insteractual con la base de datos sqlite

-validacion de modelos con pydantic

# requisitos

antes de instalar las dependecias,asegurate de tener python instalado en el sistemas,para verificar si esta instalado en la termnar ejecuta "python --version" o "py --version"

Instala las dependecias usando pip:

"pip download -r requirements.txt"

## configuracion

la aplicacion usa como base de datos sqlite local por defecto Si deseas cambiar a otra base de datos**,** modifica la variable **\`DATABASE\_URL\`** en **\`models/modelsdb.py\`**.

# uso

Para iniciar la aplicación ejecuta:

py -m uvicorn main:app --reload

Esto iniciará la aplicación en modo de desarrollo con recarga automática.

# Autenticación

-POST /jwtauth/login Iniciar sesión y obtener token de acceso.

-GET /jwtauth/users/me Obtener detalles del usuario actualmente autenticado.

# Usuarios

-POST /register Registrar un nuevo usuario.

-DELETE /users/{username} Eliminar un usuario.

-PATCH /users/{username} Actualizar detalles del usuario.

# Instrumentos

- GET /instrumentos/{instrumento\_id} Obtener detalles de un instrumento por ID.

-GET /instrumentos Obtener todos los instrumentos.

-POST /instrumento :Registrar un nuevo instrumento.

-PUT /instrumentos/{instrumento\_id}: Actualizar un instrumento.

- DELETE /instrumento/{instrumento\_id}: Eliminar un instrumento.

# Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un "issue" para reportar bugs o sugerir nuevas funcionalidades. También puedes abrir un "pull request" con tus cambios.Las contribuciones son bienvenidas. Por favor, abre un issue o haz un pull request con tus cambios.

# Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.este proyecto esta licenciado -
