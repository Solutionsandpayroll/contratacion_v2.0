# Cómo ejecutar y entender el proyecto

## 1. Introducción breve

Este proyecto es una aplicación web desarrollada en Django 6.0.5 para gestionar procesos de contratación y administración de empleados. Su flujo principal permite:

- registrar y completar datos de empleados,
- cargar información masiva desde archivos Excel,
- generar documentos de contratación y fichas de ingreso en formato Word/Excel,
- consultar beneficios,
- enviar correos a empleados mediante Microsoft Graph,
- y administrar referencias auxiliares como ciudades, centros de costos y subclientes.

La aplicación está organizada en dos apps principales dentro del proyecto Django:

- `iniciar_sesion`: autenticación del usuario de negocio y manejo de sesión.
- `regitrar_empleados`: módulo principal de empleados, formularios, lógica de negocio, generación de documentos y envío de correos.

Además, el proyecto incluye:

- `api/`: punto de entrada para despliegue en Vercel.
- `app/templates/`: plantillas HTML usadas por las vistas.
- `app/media/`: plantillas de Word/Excel y archivos de soporte.

---

## 2. Funcionamiento

El flujo real de la aplicación, tal como está implementado en el código, es el siguiente:

1. La petición llega a Django a través del archivo de URLs raíz, [app/app/urls.py](app/app/urls.py).
   - La ruta raíz (`/`) se deriva a las URLs de `iniciar_sesion`.
   - La ruta `empleados/` se deriva a las URLs de `regitrar_empleados`.

2. Las peticiones de autenticación se manejan en [app/iniciar_sesion/views.py](app/iniciar_sesion/views.py).
   - `login_view` recibe el formulario de login, valida las credenciales contra el modelo `Usuario` y, si son correctas, guarda `id_usuario` y `usuario` en la sesión.
   - Luego redirige al panel administrativo.
   - El decorador `login_requerido` protege las vistas sensibles y redirige al login si no existe sesión activa.

3. La vista principal de empleados, [app/regitrar_empleados/views.py](app/regitrar_empleados/views.py), procesa el módulo de gestión de personal.
   - En un GET, consulta todos los empleados, arma los formularios y renderiza la plantilla [app/templates/empleados.html](app/templates/empleados.html).
   - En un POST, puede ejecutar distintas acciones según el campo `accion`:
     - `cargar_excel`: lee un archivo Excel con `pandas`, transforma las columnas relevantes y crea registros de `Empleado`.
     - `crear`: crea un empleado nuevo a partir del formulario básico.
     - `editar_basico`: actualiza los datos básicos del empleado.
     - `completar`: guarda la información extendida del empleado con `EmpleadoCompletoForm`.
     - `eliminar`: elimina el registro del empleado.

4. La lógica de negocio para documentos está centralizada en [app/regitrar_empleados/utils.py](app/regitrar_empleados/utils.py).
   - El proceso toma los datos del empleado, construye un contexto enriquecido y selecciona la plantilla Word adecuada según el tipo de contrato.
   - Luego genera un archivo ZIP en memoria con los documentos listos para descargar.
   - También genera archivos Excel de fichas de ingreso a partir de una plantilla base almacenada en la carpeta de media.

5. La generación de documentos no se hace directamente en la vista, sino que utiliza `docxtpl` sobre plantillas Word ubicadas en [app/media](app/media).
   - La vista `generar_documentos_empleado` recibe valores del formulario, arma el contexto y devuelve el ZIP al navegador como respuesta de descarga.

6. La generación de fichas de ingreso se realiza en `generar_ficha_empleados`.
   - Filtra empleados por mes a partir del parámetro `mes` en la URL.
   - Revisa la plantilla Excel en `media/` y devuelve un archivo `.xlsx` listo para descargar.

7. La creación rápida de ciudades, centros de costos y subclientes utiliza endpoints AJAX.
   - Las vistas `crear_ciudad_ajax`, `crear_centro_costo_ajax` y `crear_subcliente_ajax` reciben datos por POST, validan el formulario y devuelven `JsonResponse` con el resultado.

8. El envío de correos está implementado con Microsoft Graph en [app/regitrar_empleados/graph.py](app/regitrar_empleados/graph.py).
   - La vista `enviar_correo` recibe el asunto, el cuerpo HTML y los adjuntos, reemplaza el marcador `{nombre}` y llama a Graph para enviar el mensaje.
   - La respuesta se devuelve al usuario mediante mensajes flash en la interfaz.

---

## 3. Estructura técnica

| Archivo o carpeta | Rol |
|---|---|
| [app](app) | Directorio raíz del proyecto Django. Contiene la configuración, las apps y los recursos estáticos/templatos. |
| [app/app/settings.py](app/app/settings.py) | Configuración principal de Django: apps instaladas, middleware, rutas de templates, base de datos, archivos estáticos y variables externas. |
| [app/app/urls.py](app/app/urls.py) | Archivo de URLs raíz del proyecto; enruta las peticiones a las apps `iniciar_sesion` y `regitrar_empleados`. |
| [app/app/wsgi.py](app/app/wsgi.py) | Punto de entrada WSGI usado por Django y por Vercel. |
| [app/manage.py](app/manage.py) | Script de administración de Django para ejecutar migraciones, levantar el servidor y otros comandos. |
| [app/iniciar_sesion](app/iniciar_sesion) | App de autenticación y sesiones. |
| [app/iniciar_sesion/views.py](app/iniciar_sesion/views.py) | Implementa `login_view` y `cerrar_sesion`. |
| [app/iniciar_sesion/models.py](app/iniciar_sesion/models.py) | Modelo `Usuario` usado para el login del sistema. |
| [app/iniciar_sesion/decorators.py](app/iniciar_sesion/decorators.py) | Decorador `login_requerido` que protege vistas. |
| [app/regitrar_empleados](app/regitrar_empleados) | App principal del negocio: empleados, formularios, utilidades, documentos y correos. |
| [app/regitrar_empleados/views.py](app/regitrar_empleados/views.py) | Contiene las vistas para panel, creación/edición de empleados, generación de documentos, fichas, beneficios, AJAX y envío de correos. |
| [app/regitrar_empleados/models.py](app/regitrar_empleados/models.py) | Modelos `Empleado`, `Ciudad`, `CentroCosto` y `Subcliente`. |
| [app/regitrar_empleados/forms.py](app/regitrar_empleados/forms.py) | Formularios Django para datos básicos y completos de empleados, así como formularios rápidos para referencias auxiliares. |
| [app/regitrar_empleados/utils.py](app/regitrar_empleados/utils.py) | Lógica para generar ZIP de documentos Word, construir contextos para plantillas y preparar datos para la generación de contratos. |
| [app/regitrar_empleados/graph.py](app/regitrar_empleados/graph.py) | Integración con Microsoft Graph para envío de correos. |
| [app/regitrar_empleados/management/commands/cargar_ciudades.py](app/regitrar_empleados/management/commands/cargar_ciudades.py) | Comando de administración para cargar ciudades iniciales. |
| [app/templates](app/templates) | Plantillas HTML usadas por las vistas: login, panel, empleados, fichas, beneficios, modal de correo. |
| [app/media](app/media) | Archivos de soporte: plantillas Word/Excel y recursos estáticos de negocio. |
| [app/static](app/static) | Archivos estáticos del proyecto. |
| [requirements.txt](requirements.txt) | Dependencias Python del proyecto. |
| [build_files.sh](build_files.sh) | Script de instalación y preparación para despliegue. |
| [vercel.json](vercel.json) | Configuración de despliegue para Vercel. |
| [api/index.py](api/index.py) | Punto de entrada WSGI para el despliegue en Vercel. |

---

## 4. Endpoints principales

| Ruta | Función | Propósito |
|---|---|---|
| `/` | `login_view` | Muestra la pantalla de login y autentica al usuario. |
| `/cerrar-sesion/` | `cerrar_sesion` | Cierra la sesión del usuario y redirige al login. |
| `/admin/` | `admin.site.urls` | Panel administrativo de Django. |
| `/empleados/panel/` | `panel_admin_view` | Muestra el panel principal del módulo de empleados. |
| `/empleados/registrar-empleado/` | `empleados_view` | Gestión CRUD de empleados, carga de Excel y completado de formularios. |
| `/empleados/<id_empleado>/generar-documentos/` | `generar_documentos_empleado` | Genera un ZIP con documentos Word para un empleado. |
| `/empleados/generar-ficha/` | `generar_ficha_empleados` | Genera una ficha de ingreso en Excel para un conjunto de empleados. |
| `/empleados/beneficios/` | `lista_beneficios_empleados` | Muestra la vista de beneficios. |
| `/empleados/ajax/ciudad/crear/` | `crear_ciudad_ajax` | Crea una ciudad mediante petición AJAX. |
| `/empleados/ajax/centro-costo/crear/` | `crear_centro_costo_ajax` | Crea un centro de costo mediante petición AJAX. |
| `/empleados/ajax/subcliente/crear/` | `crear_subcliente_ajax` | Crea un subcliente mediante petición AJAX. |
| `/empleados/enviar/` | `enviar_correo` | Envía un correo electrónico a un empleado usando Microsoft Graph. |

---

## 5. Requisitos

### Lenguaje y runtime

- Python: se ha validado en este entorno con Python 3.14.5.
- No existe configuración de Node.js en este proyecto.
- Framework base: Django 6.0.5.

### Dependencias principales

El proyecto declara estas dependencias en [requirements.txt](requirements.txt):

- Django 6.0.5
- dj-database-url 3.1.2
- whitenoise 6.12.0
- psycopg2-binary 2.9.12
- pandas 3.0.3
- openpyxl 3.1.5
- docxtpl 0.20.2
- python-docx 1.2.0
- requests 2.34.2
- xlrd 2.0.2

### Base de datos

La configuración de base de datos se define en [app/app/settings.py](app/app/settings.py) mediante `dj_database_url` y la variable de entorno `DATABASE_URL`.

El proyecto también incluye un archivo [app/db.sqlite3](app/db.sqlite3), por lo que una ejecución local sencilla puede apuntar a SQLite.

### Servicios externos

- Microsoft Graph para envío de correos.
  - Se esperan las variables de entorno `GRAPH_TENANT_ID`, `GRAPH_CLIENT_ID` y `GRAPH_CLIENT_SECRET`.
  - El remitente está fijado en [app/regitrar_empleados/graph.py](app/regitrar_empleados/graph.py) como `vachury@solutionsandpayroll.com`.
- Power Automate URL: se define en [app/app/settings.py](app/app/settings.py) como `POWER_AUTOMATE_URL`, aunque en la lógica actual el flujo real usa Graph.

---

## 6. Estructura recomendada de ejecución en Windows con PowerShell

Ejecuta los pasos desde la raíz del proyecto:

1. Crear y activar un entorno virtual:

   ```powershell
   cd c:\PROYECTO\contratacion_v2.0
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instalar dependencias:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Definir variables de entorno necesarias para la ejecución local:

   ```powershell
   $env:SECRET_KEY = "dev-secret-key"
   $env:DATABASE_URL = "sqlite:///db.sqlite3"
   $env:GRAPH_TENANT_ID = "<tu-tenant-id>"
   $env:GRAPH_CLIENT_ID = "<tu-client-id>"
   $env:GRAPH_CLIENT_SECRET = "<tu-client-secret>"
   ```

   > El proyecto usa `SECRET_KEY` y `DATABASE_URL` desde [app/app/settings.py](app/app/settings.py). Para el envío de correos, también debe existir la configuración de Graph.

4. Entrar al directorio del proyecto Django:

   ```powershell
   cd app
   ```

5. Ejecutar migraciones:

   ```powershell
   python manage.py migrate
   ```

6. Crear un superusuario si deseas usar el panel de administración:

   ```powershell
   python manage.py createsuperuser
   ```

7. Si necesitas cargar datos base de ciudades, ejecutar el comando incluido:

   ```powershell
   python manage.py cargar_ciudades
   ```

8. Recoger archivos estáticos:

   ```powershell
   python manage.py collectstatic --noinput
   ```

9. Levantar el servidor:

   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```

10. Abrir en el navegador:
   - Login: `http://127.0.0.1:8000/`
   - Panel de empleados: `http://127.0.0.1:8000/empleados/panel/`
   - Admin: `http://127.0.0.1:8000/admin/`

---

## 7. Opción con script

Existe un script de preparación para despliegue en [build_files.sh](build_files.sh). Su comportamiento real es el siguiente:

1. Instala todas las dependencias listadas en [requirements.txt](requirements.txt).
2. Entra al directorio `app`.
3. Ejecuta `collectstatic` para recopilar archivos estáticos.
4. Ejecuta `makemigrations` para preparar migraciones.
5. Ejecuta `migrate` para aplicar las migraciones a la base de datos.

Ejemplo de ejecución:

```bash
bash build_files.sh
```

> En el entorno actual, el script está pensado para despliegue o preparación de ambiente, no para reemplazar el flujo de ejecución manual local.

---

## 8. Notas finales

- El proyecto está pensado como una herramienta operativa para RRHH y contratación, no como un servicio API tradicional.
- La autenticación de negocio no usa el modelo de usuarios estándar de Django para las vistas principales; usa el modelo `Usuario` de [app/iniciar_sesion/models.py](app/iniciar_sesion/models.py) y la sesión de Django.
- El envío de correos real está ligado a Microsoft Graph; sin las variables de entorno correspondientes, esa parte no funcionará.
- La generación de documentos depende de las plantillas Word y Excel almacenadas en [app/media](app/media).
- Para despliegues en Vercel, la configuración está en [vercel.json](vercel.json) y [api/index.py](api/index.py), apuntando al WSGI del proyecto Django.
- El proyecto está preparado para funcionar con `whitenoise` en el manejo de estáticos.
