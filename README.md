# MyDeepTrade - Aplicación Django

Aplicación web de trading con Django que incluye autenticación de usuarios y dashboard.

## Características

- 🏠 **Home**: Página principal con presentación de la plataforma
- 🔐 **Login**: Sistema de inicio de sesión
- 📝 **Register**: Registro de nuevos usuarios
- 📊 **Dashboard**: Panel de control personalizado para usuarios autenticados
- 🎨 **Diseño Moderno**: Interfaz con Tailwind CSS y efectos visuales

## Requisitos

- Python 3.8+
- Django 6.0

## Instalación

1. Activa el entorno virtual:
```bash
source venv/bin/activate
```

2. Las dependencias ya están instaladas (Django 6.0)

3. Las migraciones ya están aplicadas

## Ejecutar la Aplicación

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

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
