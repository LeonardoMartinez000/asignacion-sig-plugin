# Asignación SIG - Plugin QGIS

[![License: GPL v2](https://img.shields.io/badge/License-GPLv2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![QGIS Version](https://img.shields.io/badge/QGIS-3.0%2B-green.svg)](https://qgis.org)
[![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org)

Herramienta profesional para gestionar permisos de usuarios en bases de datos PostgreSQL directamente desde QGIS.

## 🎯 Características Principales

- ✅ **Asignación de Permisos**: Asigna permisos (SELECT, INSERT, UPDATE, DELETE) a múltiples usuarios simultáneamente
- ✅ **Gestión de Permisos**: Visualiza y edita permisos por tabla y esquema
- ✅ **Revocación de Permisos**: Revoca todos los permisos de un usuario con un clic
- ✅ **Auditoría Completa**: Registro de todas las operaciones en archivo local
- ✅ **Logging en BD**: Registro centralizado en base de datos `00_LogGestionUsuarios`
- ✅ **Interfaz Intuitiva**: Diseño elegante con dos pestañas principales
- ✅ **Progreso en Tiempo Real**: Visualiza el progreso de cada operación paso a paso
- ✅ **Validación de Usuarios**: Verifica existencia de usuarios antes de operar
- ✅ **Manejo de Errores**: Muestra errores detallados sin interrumpir el proceso
- ✅ **Actualizaciones Automáticas**: Recibe actualizaciones directamente desde GitHub

## 📋 Requisitos

- **QGIS**: 3.0 o superior
- **PostgreSQL**: 10 o superior
- **Python**: 3.6 o superior
- **Base de datos**: `00_LogGestionUsuarios` con tabla `log_usuarios` (ver instalación)

## 🚀 Instalación

### Opción 1: Desde Repositorio QGIS (Recomendado)

1. Abrir QGIS
2. Ir a: **Complementos** → **Administrar e instalar complementos**
3. Buscar: `Asignación SIG`
4. Hacer clic en **Instalar complemento**
5. Reiniciar QGIS

### Opción 2: Desde GitHub

1. Descargar ZIP desde: [Releases](https://github.com/LeonardoMartinez000/asignacion-sig-plugin/releases)
2. Extraer en la carpeta de plugins:
   - **Windows**: `C:\Users\[usuario]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Renombrar carpeta a: `asignacion_sig`
4. Reiniciar QGIS
5. Activar en: **Complementos** → **Administrar e instalar complementos**

### Opción 3: Instalación Manual desde URL

1. Abrir QGIS
2. Ir a: **Complementos** → **Administrar e instalar complementos**
3. Click en **Configuración**
4. Agregar repositorio personalizado:
   - **Nombre**: `Asignación SIG`
   - **URL**: `https://github.com/LeonardoMartinez000/asignacion-sig-plugin/main/plugin.xml`
5. Aceptar
6. Buscar `Asignación SIG`
7. Instalar

## 🔧 Configuración Inicial

### Crear Base de Datos de Auditoría

Ejecutar en PostgreSQL como superusuario:

```sql
-- Crear base de datos
CREATE DATABASE "00_LogGestionUsuarios" OWNER postgres;

-- Conectar a la base de datos
\c 00_LogGestionUsuarios

-- Crear tabla de logs
CREATE TABLE log_usuarios (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    usuario_gestion VARCHAR(255) NOT NULL,
    bd VARCHAR(255) NOT NULL,
    tipo_gestion VARCHAR(50) NOT NULL,
    usuario_gestionado VARCHAR(255) NOT NULL,
    permisos TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejor rendimiento
CREATE INDEX idx_fecha ON log_usuarios(fecha);
CREATE INDEX idx_usuario_gestion ON log_usuarios(usuario_gestion);
CREATE INDEX idx_bd ON log_usuarios(bd);
CREATE INDEX idx_tipo_gestion ON log_usuarios(tipo_gestion);
```

## 📖 Uso

### 1. Abrir el Plugin

- Ir a: **Complementos** → **Asignación SIG**

### 2. Ingresar Credenciales

- **Base de datos**: Nombre de la BD objetivo
- **Host**: IP o nombre del servidor PostgreSQL
- **Usuario**: Usuario administrador
- **Contraseña**: Contraseña del usuario

### 3. Validar Conexión

- Click en **🔗 Validar Conexión**
- Esperar confirmación

### 4. Asignar Permisos (Pestaña 1)

1. Ingresar usuarios (separados por comas)
2. Seleccionar permisos a asignar
3. Click en **✓ Asignar Permisos**
4. Revisar resumen del proceso

### 5. Gestionar Permisos (Pestaña 2)

1. Click en **🔄 Cargar Usuarios**
2. Seleccionar usuario de la lista
3. Modificar permisos en la tabla
4. Click en **💾 Actualizar Permisos**
5. O click en **🚫 Quitar Todos** para revocar todos

## 📊 Estructura de Logs

### Archivo Local
- Ubicación: `logs/permisos_audit_YYYYMMDD.log`
- Contiene: Todas las operaciones realizadas

### Base de Datos
- Base: `00_LogGestionUsuarios`
- Tabla: `log_usuarios`
- Campos:
  - `id`: Identificador único (SERIAL)
  - `fecha`: Fecha de la operación
  - `hora`: Hora de la operación
  - `usuario_gestion`: Usuario que ejecutó la operación
  - `bd`: Base de datos afectada
  - `tipo_gestion`: Tipo de operación (ASIGNACION PERMISOS, ACTUALIZACION PERMISOS, QUITAR PERMISOS)
  - `usuario_gestionado`: Usuario afectado
  - `permisos`: Permisos asignados/actualizados/quitados

## 🔐 Seguridad

- ✅ Todas las consultas SQL usan parámetros (previene SQL injection)
- ✅ Identifiers entrecomillados
- ✅ Validación de usuarios antes de operar
- ✅ Auditoría completa de todas las operaciones
- ✅ No se modifican datos, solo permisos
- ✅ Manejo seguro de credenciales

## 🐛 Troubleshooting

### Plugin no aparece en QGIS

```
Verificar:
1. Carpeta se llama "asignacion_sig" (sin espacios)
2. Archivo __init__.py existe
3. metadata.txt tiene formato correcto
4. Revisar: Ayuda → Consola Python (errores)
```

### Error de conexión a PostgreSQL

```
Verificar:
1. Host y puerto correctos
2. Usuario y contraseña válidos
3. Base de datos existe
4. Usuario tiene permisos suficientes
5. PostgreSQL está ejecutándose
```

### Base de datos 00_LogGestionUsuarios no encontrada

```
Solución:
1. Ejecutar script SQL de creación (ver Configuración Inicial)
2. Verificar que la base de datos existe
3. Verificar permisos del usuario
```

### Actualizaciones no se detectan

```
Verificar:
1. URL de plugin.xml es correcta
2. Versión en plugin.xml > versión instalada
3. Esperar 5-10 minutos para caché
4. Reiniciar QGIS
```

## 📝 Documentación

- [Guía de Instalación y Actualizaciones](GUIA_GITHUB_QGIS.md)
- [Guía de Uso](GUIA_USO_FASE_1.md)
- [Historial de Cambios](CHANGELOG.md)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia GNU General Public License v2.0. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autor

**Servinformación**
- Email: leonardo.martinez@servinformacion.com
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/LeonardoMartinez000/asignacion-sig-plugin/issues)
- **Email**: leonardo.martinez@servinformacion.com
- **Documentación**: Ver archivos .md en el repositorio

## 🙏 Agradecimientos

- QGIS Community
- PostgreSQL Community
- Servinformación

---

**Versión**: 4.0  
**Última actualización**: 16 de Marzo de 2026  
**Estado**: ✅ Producción
