# MyDeepTrade - AI Trading Platform

Plataforma de trading automatizado con IA que incluye gestión de modelos, agentes, órdenes de trabajo y transacciones.

## 🚀 Características

- 🔐 **Autenticación**: Sistema completo de login, registro y perfiles de usuario
- 📊 **Dashboard**: Panel de control con KPIs en tiempo real
- 💼 **Transacciones**: Gestión de compras y ventas con cálculo automático
- 📋 **Work Orders**: Sistema de órdenes de trabajo programadas con ejecución automática
- 🤖 **Agentes**: Agentes de IA con periodicidad y horarios configurables
- 🧠 **Modelos AI**: Integración con ChatGPT y Ollama
- 👤 **Perfiles**: Gestión de perfiles con avatares y cambio de contraseña
- 🐳 **Docker**: Contenedorizado con worker para tareas programadas

## 📦 Requisitos

- Docker & Docker Compose (recomendado)
- O Python 3.14+ para desarrollo local

## 🐳 Instalación con Docker (Recomendado)

### 1. Construir y ejecutar los contenedores

```bash
# Construir las imágenes
docker-compose build

# Iniciar los servicios
docker-compose up -d

# Ver los logs
docker-compose logs -f
```

### 2. Acceder a la aplicación

La aplicación estará disponible en: `http://localhost:8000/`

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Servicios Docker

El proyecto incluye 3 servicios:

- **web**: Aplicación Django (puerto 8000)
- **db**: Base de datos PostgreSQL (puerto 5432)
- **worker**: Ejecutor de órdenes de trabajo programadas

### 4. Comandos útiles

```bash
# Detener los servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs del worker
docker-compose logs -f worker

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario adicional
docker-compose exec web python manage.py createsuperuser

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

## 💻 Instalación Local (Desarrollo)

### 1. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

### 6. Ejecutar worker (en otra terminal)

```bash
python manage.py run_workorders
```

## 📂 Estructura del Proyecto

```
MyDeepTrade/
├── core/                          # Aplicación principal
│   ├── management/
│   │   └── commands/
│   │       └── run_workorders.py  # Worker para ejecutar órdenes
│   ├── models.py                  # Modelos (Agent, Model, Transaction, WorkOrder)
│   ├── views.py                   # Vistas del sistema
│   └── urls.py                    # URLs de la aplicación
├── templates/                     # Templates HTML
│   ├── dashboard.html             # Dashboard con KPIs
│   ├── workorders/                # Templates de órdenes de trabajo
│   ├── agents/                    # Templates de agentes
│   ├── models/                    # Templates de modelos AI
│   ├── transactions/              # Templates de transacciones
│   └── users/                     # Templates de usuarios
├── mydeeptrade/                   # Configuración del proyecto
│   ├── settings.py                # Configuración (SQLite/PostgreSQL)
│   └── urls.py                    # URLs principales
├── media/                         # Archivos subidos (avatars)
├── Dockerfile                     # Imagen Docker para web
├── Dockerfile.worker              # Imagen Docker para worker
├── docker-compose.yml             # Orquestación de servicios
├── entrypoint.sh                  # Script de inicio web
├── worker.sh                      # Script de inicio worker
└── requirements.txt               # Dependencias Python
```

## 🤖 Sistema de Work Orders

Las órdenes de trabajo se ejecutan automáticamente basándose en:

1. **Horario de la orden**: start_time y end_time
2. **Horario del agente**: start_time y end_time del agente
3. **Periodicidad del agente**: Cada X minutos/horas/días
4. **Estado del agente**: Solo si está activo

El worker verifica cada 30 segundos qué órdenes deben ejecutarse y las procesa automáticamente.

## 🔧 Configuración de Modelos AI

### ChatGPT
1. Ve a Models → Create Model
2. Selecciona tipo "ChatGPT"
3. Ingresa tu API key de OpenAI
4. Prueba la conexión con el botón "Test"

### Ollama (Local)
1. Instala Ollama en tu máquina
2. Ejecuta un modelo: `ollama run llama2`
3. Crea un modelo tipo "Ollama" en la aplicación

## 📊 Funcionalidades Principales

### Dashboard
- Contador de agentes (activos/inactivos)
- Contador de modelos AI configurados
- Contador de transacciones totales

### Work Orders
- Secuencia automática (OT-000001, OT-000002...)
- Estados: Draft, Working, Completed
- Ejecución automática por el worker
- Horarios configurables

### Agentes
- Asociados a un modelo AI
- Periodicidad configurable (minutos/horas/días)
- Horario de trabajo (ej: 08:00 - 20:00)
- Sistema prompt personalizable

### Transacciones
- Tipo: Buy/Sell
- Cálculo automático de importe (cantidad × precio)
- Historial completo de operaciones

## 🔒 Seguridad

- Autenticación requerida para todas las funcionalidades
- Gestión de perfiles con avatares
- Cambio de contraseña seguro
- Validación de formularios
- CSRF protection

## 🐛 Troubleshooting

### El worker no ejecuta órdenes

1. Verifica que el worker esté corriendo:
   ```bash
   docker-compose logs worker
   ```

2. Verifica que:
   - La orden esté en estado "draft" o "working"
   - El agente esté activo
   - La hora actual esté dentro del horario de la orden
   - La hora actual esté dentro del horario del agente

### Error de conexión a PostgreSQL

```bash
# Reiniciar servicios
docker-compose restart db web worker
```

### Limpiar y reiniciar todo

```bash
# Detener y eliminar todo
docker-compose down -v

# Reconstruir y arrancar
docker-compose up -d --build
```

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Estructura del Proyecto

```
MyDeepTrade/
├── mydeeptrade/          # Configuración del proyecto
│   ├── settings.py       # Configuraciones
│   └── urls.py           # URLs principales
├── core/                 # Aplicación principal
│   ├── views.py          # Vistas (home, login, register, dashboard)
│   └── urls.py           # URLs de la app
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── home.html         # Página de inicio
│   ├── login.html        # Inicio de sesión
│   ├── register.html     # Registro
│   └── dashboard.html    # Panel de control
└── manage.py             # Script de administración
```

## URLs Disponibles

- `/` - Página de inicio
- `/login/` - Iniciar sesión
- `/register/` - Registrarse
- `/dashboard/` - Dashboard (requiere autenticación)
- `/logout/` - Cerrar sesión
- `/admin/` - Panel de administración

## Crear Superusuario

Para acceder al panel de administración:

```bash
python manage.py createsuperuser
```

## Tecnologías Utilizadas

- **Backend**: Django 6.0
- **Frontend**: HTML5, Tailwind CSS (via CDN)
- **Base de Datos**: SQLite (desarrollo)
- **Autenticación**: Sistema de autenticación de Django

## Características del Diseño

- Gradientes modernos (azul a púrpura)
- Efectos de hover y transiciones suaves
- Diseño responsive
- Backdrop blur effects
- Animaciones fade-in
- Mensajes flash estilizados
- Navbar sticky con backdrop blur

## Próximos Pasos

1. Implementar funcionalidad de trading real
2. Agregar gráficos de mercado en tiempo real
3. Integrar APIs de trading
4. Implementar sistema de notificaciones
5. Agregar más análisis y estadísticas

## Licencia

© 2026 MyDeepTrade. Todos los derechos reservados.
