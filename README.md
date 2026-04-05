# Auditra 
**Detector de Audio Generado por IA** - Herramienta forense de escritorio para detectar y analizar audio sintético mediante análisis de metadatos y patrones visuales

## 📝 Descripción

**Auditra** es una herramienta forense de audio diseñada para **detectar y analizar audio generado mediante inteligencia artificial** (deepfakes, síntesis de voz, etc.). La aplicación proporciona un análisis detallado de las características de audio mediante múltiples métodos forenses para identificar patrones anómalos típicos del audio sintético.

## 🔬 Módulos de análisis

Auditra proporciona **3 módulos independientes y complementarios** para un análisis integral:

### 1️⃣ **Cargar Audio** (Ingesta)
- Carga segura de archivos WAV, MP3, M4A (máx 2GB)
- Validación de formato y tamaño
- Cálculo de hash SHA-256 para integridad de cadena de custodia
- Cola de procesamiento (un archivo a la vez para garantizar integridad)
- Punto de entrada para los otros dos módulos

### 2️⃣ **Análisis de Metadatos**
**Extrae información técnica completa** del archivo usando herramientas forenses avanzadas:

- **Campos extraídos:**
  - Información básica: título, artista, álbum, género, duración
  - Codificación: codec, bitrate, sample rate, canales
  - Contenedor: formato, tamaño, timestamps
  - Librerías de codificación: software usado originalmente
  - Histogramas de distribución

- **Indicadores de manipulación:**
  - Discrepancias de bitrate (re-codificación)
  - Inconsistencias en metadatos (síntesis de voz)
  - Rastros de software de terceros (editores, herramientas IA)
  - Anomalías en arquitectura del contenedor

### 3️⃣ **Análisis de Patrones**
**Visualización de estructura interna** mediante bitmap de bytes y análisis de bordes:

**Dos pestañas complementarias:**

- **Autosimilitud (Mapa de Contenido)**
  - Cada píxel = un byte (escala de grises 0x00-0xFF)
  - Audio natural: transiciones graduales y variadas
  - Audio sintético: patrones regulares, repetitivos, bloques uniformes
  - Ajusta resolución (128-2048 bytes/fila) para diferentes escalas

- **Relleno (Análisis de Bordes)**
  - Examina primeros y últimos 1024 bytes
  - Detecta bytes repetidos (0x00, 0xFF) que indican:
    - Re-codificación incompleta
    - Exportación con relleno de IA
    - Manipulación posterior
  - Hexdump formateado para análisis detallado

---

## ⚙️ Requisitos previos

### Para Windows:

**Backend:**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- ExifTool (incluido en `/backend/bin/exiftool_files/`)

**Frontend:**
- Node.js (v16+)
- npm o yarn

**Para compilar a .exe:**
- PyInstaller (`pip install pyinstaller`)
- Todo lo anterior

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/claudianistal/TFG-Auditra.git
cd TFG-Auditra
```

### 2. Instalar dependencias del backend
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Instalar dependencias del frontend
```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Ejecución

### Modo Desarrollo

En modo desarrollo, el backend y frontend se ejecutan de forma independiente, permitiendo hot-reload y debugging más fácil.

#### Terminal 1 - Ejecutar Backend + Webview
```bash
cd backend
python -m app.main
```
- El backend inicia en `http://localhost:8000`
- El webview intentará conectar con el frontend en `http://localhost:5173`

#### Terminal 2 - Ejecutar Frontend (Vite dev server)
```bash
cd frontend
npm run dev
```
- El frontend se sirve en `http://localhost:5173` con hot-reload

**Resultado:** La aplicación se abrirá en una ventana de escritorio con el frontend en modo desarrollo.

---

### Compilación a .exe

Para crear un ejecutable Windows de distribución:

```bash
python build.py
```

**Qué hace el script:**
1. Compila el frontend React a archivos estáticos
2. Empaqueta todo con PyInstaller
3. Genera un único archivo `Auditra.exe` en la carpeta `dist/`

**Requisitos:**
- PyInstaller instalado (`pip install pyinstaller`)
- Frontend compilado: `cd frontend && npm run build`

> **Nota:** El script `build.py` ya hace la compilación de frontend automáticamente si es necesario.

---

### Ejecución del .exe

Una vez compilado, simplemente ejecuta:

```bash
dist/Auditra.exe
```

**Comportamiento en modo .exe:**
- El backend se inicia automáticamente en `http://localhost:8000`
- El frontend se sirve desde `http://localhost:8000` (archivos estáticos compilados)
- Se abre directamente una ventana de escritorio sin necesidad de terminal


## 🛠️ Tecnologías utilizadas

| Capa | Tecnología | Propósito |
|------|-----------|----------|
| **Backend** | Python 3.8+ | Lenguaje principal |
| | FastAPI | Framework API REST |
| | Uvicorn | Servidor ASGI |
| | PyWebView | Ventana de escritorio integrada |
| | Mutagen | Extracción de metadatos (MP3, M4A) |
| | Wave | Extracción de metadatos (WAV) |
| | ExifTool | Herramienta forense de metadatos |
| | FFprobe | Análisis multimedia avanzado |
| | Pillow | Generación de imágenes (bitmap) |
| | NumPy | Procesamiento de datos numéricos |
| **Frontend** | React 18+ | Framework UI |
| | Vite | Build tool y dev server |
| | i18next | Internacionalización (ES/EN) |
| | CSS3 | Estilos (variables, grid, flexbox) |
| **Deployment** | PyInstaller | Compilación a .exe |
| **Package Managers** | pip | Dependencias Python |
| | npm | Dependencias Node.js |

## 🔍 Métodos de análisis forense

### 1. Análisis de Metadatos
**Investigadores:** Mutagen, Wave, ExifTool, FFprobe
- Extrae información de cabeceras y contenedores
- Identifica herramientas de creación original
- Detecta discrepancias en bitrate y re-codificación

### 2. Análisis de Patrones Visuales
**Método de bitmap (autosimilitud):**
- Visualiza estructura de bytes como imagen
- Audio natural: transiciones graduales
- Audio sintético: patrones regulares y bloques uniformes

### 3. Análisis de Bordes (Padding)
**Detección de relleno:**
- Examina primeros y últimos 1024 bytes
- Audio sintético a menudo contiene relleno (0x00, 0xFF)
- Indica re-codificación incompleta o manipulación

---

## 📝 Notas importantes

- **Desarrollo**: Backend y frontend se ejecutan en procesos separados con hot-reload activo
- **Producción (.exe)**: Todo se ejecuta en un único proceso con interfaz integrada y sin consola visible
- **Primera ejecución**: La aplicación crea automáticamente la carpeta de uploads en Documentos
- **Encoding**: Soporta caracteres Unicode y acentos sin problemas (español, caracteres especiales)
- **Almacenamiento temporal**: Los archivos subidos se almacenan en `C:\Users\[Usuario]\Documents\TFG_Auditra_Uploads\`
- **Integridad**: Cada archivo recibe un UUID único para garantizar cadena de custodia
- **Extensibilidad**: Las estrategias de análisis se pueden extender con nuevos modelos IA o librerías de análisis

---

## 📄 Licencia
Este proyecto es parte de un TFG (Trabajo de Fin de Grado)

---

## 👤 Autora
Claudia Nistal Martínez - Detector de Audio IA (TFG)
