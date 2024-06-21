# proyecto de gestion de instrumentos

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

Las contribuciones son bienvenidas. Por favor, abre un issue o haz un pull request con tus cambios.

# Licencia

este proyecto esta licenciado -
