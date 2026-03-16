# Guía: Publicar Plugin en GitHub e Instalar en QGIS

## 📋 Tabla de Contenidos
1. [Preparación del Proyecto](#preparación-del-proyecto)
2. [Crear Repositorio en GitHub](#crear-repositorio-en-github)
3. [Configurar Actualizaciones Automáticas](#configurar-actualizaciones-automáticas)
4. [Instalar Plugin en QGIS](#instalar-plugin-en-qgis)
5. [Actualizar Plugin](#actualizar-plugin)

---

## 1. Preparación del Proyecto

### 1.1 Estructura de Carpetas Recomendada

```
asignacion-sig-plugin/
├── asignacion_sig/                    # Carpeta principal del plugin
│   ├── __init__.py
│   ├── permisos.py
│   ├── validaciones.py
│   ├── validaciones_dialog.py
│   ├── resources.py
│   ├── resources.qrc
│   ├── metadata.txt                   # IMPORTANTE: Versión aquí
│   ├── icon.png
│   ├── credentials.ui
│   ├── Validaciones Servinfomacion_dialog_base.ui
│   ├── help/
│   ├── i18n/
│   ├── logs/
│   ├── scripts/
│   ├── test/
│   └── .gitignore
├── .github/
│   └── workflows/
│       └── release.yml                # Automatizar releases
├── README.md                          # Documentación principal
├── CHANGELOG.md                       # Historial de cambios
├── LICENSE                            # Licencia (GPL v2)
└── plugin.xml                         # Archivo de actualización (generado)
```

### 1.2 Archivos Necesarios

#### A. .gitignore
```
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
*.zip
.DS_Store
logs/
```

#### B. LICENSE (GPL v2)
```
GNU GENERAL PUBLIC LICENSE
Version 2, June 1991

[Copiar contenido de: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt]
```

#### C. README.md
```markdown
# Asignación SIG - Plugin QGIS

Herramienta para gestionar permisos de usuarios en bases de datos PostgreSQL desde QGIS.

## Características

- ✅ Asignación de permisos a múltiples usuarios
- ✅ Gestión de permisos por tabla y esquema
- ✅ Auditoría completa de operaciones
- ✅ Logging en base de datos 00_LogGestionUsuarios
- ✅ Interfaz intuitiva con pestañas

## Requisitos

- QGIS 3.0 o superior
- PostgreSQL 10 o superior
- Python 3.6+

## Instalación

### Desde GitHub (Recomendado)

1. Abrir QGIS
2. Ir a: Complementos → Administrar e instalar complementos
3. Buscar: "Asignación SIG"
4. Hacer clic en "Instalar complemento"

### Instalación Manual

1. Descargar: https://github.com/tu-usuario/asignacion-sig-plugin/releases
2. Extraer en: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. Reiniciar QGIS

## Uso

1. Abrir el plugin desde: Complementos → Asignación SIG
2. Ingresar credenciales de PostgreSQL
3. Validar conexión
4. Seleccionar usuarios y permisos
5. Ejecutar operación

## Documentación

Ver [GUIA_USO_FASE_1.md](GUIA_USO_FASE_1.md) para instrucciones detalladas.

## Soporte

- Email: leonardo.martinez@servinformacion.com
- Issues: https://github.com/tu-usuario/asignacion-sig-plugin/issues

## Licencia

GNU General Public License v2.0
```

#### D. CHANGELOG.md
```markdown
# Historial de Cambios

## [4.0] - 2026-03-16

### Agregado
- Logging en base de datos 00_LogGestionUsuarios
- Registro de asignación, actualización y revocación de permisos
- Interfaz mejorada con títulos de pestañas ajustados
- Soporte para actualizaciones automáticas desde GitHub

### Mejorado
- Paleta de colores elegante y profesional
- Panel de resumen en ambas pestañas
- Scroll funcional en paneles
- Progreso en tiempo real

### Corregido
- Eliminación de archivos innecesarios
- Optimización de código

## [3.3] - 2026-03-13

### Agregado
- Ajustes visuales fase 2
- Panel de resumen mejorado

## [1.0.1] - 2026-03-09

### Inicial
- Versión inicial del plugin
```

---

## 2. Crear Repositorio en GitHub

### 2.1 Pasos en GitHub

1. **Crear cuenta en GitHub** (si no tienes): https://github.com/signup

2. **Crear nuevo repositorio**:
   - Ir a: https://github.com/new
   - Nombre: `asignacion-sig-plugin`
   - Descripción: "Plugin QGIS para gestión de permisos PostgreSQL"
   - Visibilidad: Public
   - Agregar README.md: ✓
   - Agregar .gitignore: Python
   - Agregar licencia: GNU General Public License v2.0
   - Crear repositorio

3. **Clonar repositorio localmente**:
```bash
git clone https://github.com/LeonardoMartinez000/asignacion-sig-plugin.git
cd asignacion-sig-plugin
```

### 2.2 Estructura de Carpetas en Git

```bash
# Crear estructura
mkdir -p asignacion_sig
mkdir -p .github/workflows

# Copiar archivos del plugin a asignacion_sig/
cp -r /ruta/actual/plugin/* asignacion_sig/

# Crear archivos de configuración
touch README.md CHANGELOG.md LICENSE .gitignore
```

### 2.3 Primer Commit

```bash
git add .
git commit -m "Initial commit: Plugin Asignación SIG v4.0"
git push origin main
```

---

## 3. Configurar Actualizaciones Automáticas

### 3.1 Archivo plugin.xml (Repositorio de Plugins QGIS)

Crear archivo `plugin.xml` en la raíz del repositorio:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plugins>
  <pyqgis_plugin name="Asignación SIG" version="4.0">
    <description>Herramienta para gestionar permisos de usuarios en PostgreSQL</description>
    <version>4.0</version>
    <qgis_minimum_version>3.0</qgis_minimum_version>
    <qgis_maximum_version>3.99</qgis_maximum_version>
    <homepage>https://github.com/LeonardoMartinez000/asignacion-sig-plugin</homepage>
    <file_name>asignacion-sig-plugin-4.0.zip</file_name>
    <icon>https://raw.githubusercontent.com/LeonardoMartinez000/asignacion-sig-plugin/main/asignacion_sig/icon.png</icon>
    <author_name>Servinformación</author_name>
    <download_url>https://github.com/LeonardoMartinez000/asignacion-sig-plugin/releases/download/v4.0/asignacion-sig-plugin-4.0.zip</download_url>
    <uploaded_by>LeonardoMartinez000</uploaded_by>
    <create_date>2026-03-16</create_date>
    <update_date>2026-03-16</update_date>
    <experimental>False</experimental>
    <deprecated>False</deprecated>
    <tracker>https://github.com/LeonardoMartinez000/asignacion-sig-plugin/issues</tracker>
    <repository>https://github.com/LeonardoMartinez000/asignacion-sig-plugin</repository>
    <tags>postgresql,permissions,database,qgis</tags>
  </pyqgis_plugin>
</plugins>
```

### 3.2 Crear Release en GitHub

1. **Preparar versión**:
```bash
# Actualizar versión en metadata.txt
# Cambiar: version=4.0 → version=4.1 (si hay cambios)

# Crear tag
git tag -a v4.0 -m "Release version 4.0"
git push origin v4.0
```

2. **Crear Release en GitHub**:
   - Ir a: https://github.com/LeonardoMartinez000/asignacion-sig-plugin/releases
   - Click en "Create a new release"
   - Tag: v4.0
   - Title: "Asignación SIG v4.0"
   - Description: (copiar de CHANGELOG.md)
   - Adjuntar archivo ZIP del plugin
   - Publish release

3. **Generar ZIP del plugin**:
```bash
# Desde la raíz del repositorio
zip -r asignacion-sig-plugin-4.0.zip asignacion_sig/ -x "*.pyc" "__pycache__/*" "*.log"
```

---

## 4. Instalar Plugin en QGIS

### 4.1 Instalación desde Repositorio Oficial QGIS

**Nota**: Para que aparezca en el repositorio oficial de QGIS, debes:

1. Registrar el plugin en: https://plugins.qgis.org/
2. Subir el archivo ZIP
3. Esperar aprobación (24-48 horas)

### 4.2 Instalación desde GitHub (Método Alternativo)

**Opción A: Instalación Manual**

1. Descargar ZIP desde: https://github.com/LeonardoMartinez000/asignacion-sig-plugin/releases
2. Extraer en:
   - **Windows**: `C:\Users\[usuario]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Renombrar carpeta a: `asignacion_sig`
4. Reiniciar QGIS
5. Activar en: Complementos → Administrar e instalar complementos

**Opción B: Instalación desde URL (QGIS 3.14+)**

1. Abrir QGIS
2. Ir a: Complementos → Administrar e instalar complementos
3. Click en "Configuración"
4. Agregar repositorio personalizado:
   - Nombre: "Asignación SIG"
   - URL: `https://raw.githubusercontent.com/LeonardoMartinez000/asignacion-sig-plugin/main/plugin.xml`
5. Aceptar
6. Buscar "Asignación SIG"
7. Instalar

---

## 5. Actualizar Plugin

### 5.1 Flujo de Actualización

```
Cambios en código
    ↓
Actualizar versión en metadata.txt
    ↓
Commit y push a GitHub
    ↓
Crear tag y release
    ↓
Adjuntar ZIP a release
    ↓
QGIS detecta actualización automáticamente
    ↓
Usuario instala actualización
```

### 5.2 Pasos para Actualizar

1. **Hacer cambios en el código**:
```bash
# Editar archivos
git add .
git commit -m "Descripción de cambios"
```

2. **Actualizar versión**:
```bash
# Editar metadata.txt
# version=4.0 → version=4.1

git add metadata.txt
git commit -m "Bump version to 4.1"
```

3. **Crear release**:
```bash
git tag -a v4.1 -m "Release version 4.1"
git push origin main
git push origin v4.1
```

4. **Crear ZIP y subir a GitHub**:
```bash
zip -r asignacion-sig-plugin-4.1.zip asignacion_sig/ -x "*.pyc" "__pycache__/*" "*.log"
```

5. **Crear release en GitHub**:
   - Ir a Releases
   - New release
   - Tag: v4.1
   - Adjuntar ZIP
   - Publish

6. **Actualizar plugin.xml**:
   - Cambiar versión
   - Cambiar download_url
   - Cambiar update_date
   - Commit y push

### 5.3 En los Equipos con Plugin Instalado

1. Abrir QGIS
2. Ir a: Complementos → Administrar e instalar complementos
3. Buscar "Asignación SIG"
4. Si hay actualización disponible, aparecerá botón "Actualizar"
5. Click en "Actualizar"
6. Reiniciar QGIS

---

## 6. Automatizar Releases con GitHub Actions

### 6.1 Crear Workflow Automático

Crear archivo: `.github/workflows/release.yml`

```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Create ZIP
        run: |
          zip -r asignacion-sig-plugin-${{ github.ref_name }}.zip asignacion_sig/ \
            -x "*.pyc" "__pycache__/*" "*.log"
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Asignación SIG ${{ github.ref_name }}
          draft: false
          prerelease: false
      
      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./asignacion-sig-plugin-${{ github.ref_name }}.zip
          asset_name: asignacion-sig-plugin-${{ github.ref_name }}.zip
          asset_content_type: application/zip
```

---

## 7. Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Archivos subidos (README.md, CHANGELOG.md, LICENSE, .gitignore)
- [ ] metadata.txt con versión correcta
- [ ] plugin.xml creado y actualizado
- [ ] Primera release creada (v4.0)
- [ ] ZIP del plugin adjunto a release
- [ ] Plugin instalable desde GitHub
- [ ] Actualizaciones automáticas funcionando
- [ ] Documentación completa

---

## 8. Troubleshooting

### Problema: Plugin no aparece en QGIS
**Solución**:
- Verificar que la carpeta se llama `asignacion_sig` (sin espacios)
- Verificar que `__init__.py` existe
- Verificar que `metadata.txt` tiene formato correcto
- Revisar logs de QGIS: Ayuda → Consola Python

### Problema: Actualizaciones no se detectan
**Solución**:
- Verificar que plugin.xml está en la raíz del repositorio
- Verificar que versión en plugin.xml es mayor que versión instalada
- Verificar que download_url es accesible
- Esperar 5-10 minutos para que QGIS actualice caché

### Problema: Error al instalar desde URL
**Solución**:
- Verificar que URL de plugin.xml es correcta
- Verificar que repositorio es público
- Probar con URL directa en navegador

---

## 9. Recursos Útiles

- [Documentación oficial QGIS Plugins](https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/plugins/index.html)
- [Repositorio oficial de plugins QGIS](https://plugins.qgis.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Versión**: 1.0  
**Fecha**: 16 de Marzo de 2026  
**Autor**: Servinformación
