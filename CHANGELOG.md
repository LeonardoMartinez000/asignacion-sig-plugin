# Historial de Cambios

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [4.0] - 2026-03-16

### ✨ Agregado

- **Logging en Base de Datos**: Registro centralizado en `00_LogGestionUsuarios`
  - Tabla `log_usuarios` con campos: id, fecha, hora, usuario_gestion, bd, tipo_gestion, usuario_gestionado, permisos
  - Función `registrarLogGestion()` en permisos.py
  - Integración en asignación, actualización y revocación de permisos

- **Soporte para Actualizaciones Automáticas**
  - Archivo `plugin.xml` para repositorio de plugins
  - Configuración de versiones en metadata.txt
  - Soporte para GitHub Releases

- **Mejoras de Interfaz**
  - Títulos de pestañas ajustados (9pt)
  - Textos de usuarios aumentados (11px)
  - Checkboxes de permisos aumentados (13px)
  - Iconos de botones aumentados (24px)

- **Documentación Completa**
  - GUIA_GITHUB_QGIS.md: Guía completa de publicación
  - README.md mejorado con instrucciones detalladas
  - CHANGELOG.md: Este archivo

### 🔧 Mejorado

- Paleta de colores elegante y profesional
  - Fondo: #f8f9fa (gris muy claro)
  - Paneles: #f5f7fa (azul muy claro)
  - Acentos: #2196F3 (azul vibrante)

- Panel de resumen en ambas pestañas
  - Pestaña 1: `mostrarProceso`
  - Pestaña 2: `mostrarProcesoPermisos`

- Scroll funcional en paneles
  - Scroll bars elegantes
  - Auto-scroll al final
  - Colores coordinados

- Progreso en tiempo real
  - Validación de usuarios línea por línea
  - Cada GRANT/REVOKE mostrado inmediatamente
  - Errores mostrados con detalles

### 🗑️ Eliminado

- 18 archivos innecesarios de documentación histórica
- Archivos de configuración obsoletos
- README antiguos

### 🐛 Corregido

- Optimización de código
- Eliminación de archivos redundantes
- Mejora de estructura del proyecto

### 🔒 Seguridad

- Todas las consultas SQL usan parámetros
- Identifiers entrecomillados
- Validación de usuarios antes de operar
- Manejo seguro de credenciales

---

## [3.3] - 2026-03-13

### ✨ Agregado

- Ajustes visuales fase 2
- Panel de resumen mejorado en ambas pestañas
- Scroll funcional en paneles

### 🔧 Mejorado

- Interfaz más elegante
- Mejor visibilidad de errores
- Progreso visible en tiempo real
- Colores armoniosos

### 🐛 Corregido

- Tamaño de fuentes inconsistente
- Scroll no funcional
- Errores no mostrados

---

## [1.0.1] - 2026-03-09

### ✨ Agregado

- Versión inicial del plugin
- Funciones básicas de gestión de permisos
- Interfaz con dos pestañas
- Auditoría local en archivos

### 🔧 Mejorado

- Implementación de Phase 1 Critical Corrections
  - SQL injection eliminado (queries parametrizadas)
  - Auditoría implementada
  - Validación de usuarios
  - Gestión de conexiones

### 🔒 Seguridad

- Reemplazo de f-strings con queries parametrizadas
- Context managers para conexiones
- Validación de usuarios antes de GRANT

---

## Notas de Versión

### Cómo Actualizar

1. **Desde QGIS**:
   - Ir a: Complementos → Administrar e instalar complementos
   - Buscar "Asignación SIG"
   - Si hay actualización, aparecerá botón "Actualizar"
   - Click en "Actualizar"
   - Reiniciar QGIS

2. **Manual**:
   - Descargar ZIP desde [Releases](https://github.com/tu-usuario/asignacion-sig-plugin/releases)
   - Extraer en carpeta de plugins
   - Reiniciar QGIS

### Compatibilidad

| Versión | QGIS | PostgreSQL | Python | Estado |
|---------|------|------------|--------|--------|
| 4.0 | 3.0+ | 10+ | 3.6+ | ✅ Actual |
| 3.3 | 3.0+ | 10+ | 3.6+ | ⚠️ Anterior |
| 1.0.1 | 3.0+ | 10+ | 3.6+ | ⚠️ Anterior |

### Requisitos Especiales

#### Versión 4.0
- Base de datos `00_LogGestionUsuarios` con tabla `log_usuarios`
- Script SQL de creación disponible en README.md

#### Versión 3.3
- Sin requisitos especiales

#### Versión 1.0.1
- Sin requisitos especiales

---

## Roadmap Futuro

### Fase 3: Optimizaciones Futuras
- [ ] Barra de progreso visual
- [ ] Cancelación de operaciones en curso
- [ ] Exportación de logs a CSV/PDF
- [ ] Historial de operaciones con filtros
- [ ] Soporte para roles de PostgreSQL
- [ ] Backup/Restore de permisos
- [ ] Comparación de permisos entre usuarios
- [ ] Plantillas de permisos predefinidas

### Fase 4: Integraciones
- [ ] Integración con LDAP/Active Directory
- [ ] Sincronización automática de usuarios
- [ ] Webhooks para eventos
- [ ] API REST para automatización

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama para tu feature
3. Commit cambios
4. Push a la rama
5. Abrir Pull Request

---

## Licencia

GNU General Public License v2.0 - Ver [LICENSE](LICENSE)

---

**Última actualización**: 16 de Marzo de 2026  
**Mantenedor**: Servinformación
