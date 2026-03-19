# TFG-Auditra 
**Detector de Audio Generado por IA** - Aplicación de escritorio para detectar y analizar audio sintético/generado artificialmente a partir de sus metadatos y posibles patrones

---

## 📋 Tabla de contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
  - [Modo desarrollo](#modo-desarrollo)
  - [Compilación a .exe](#compilación-a-exe)
  - [Ejecución del .exe](#ejecución-del-exe)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías utilizadas](#tecnologías-utilizadas)

---

## 📝 Descripción

**TFG-Auditra** es una herramienta forense de audio diseñada para **detectar y analizar audio generado mediante inteligencia artificial** (deepfakes, síntesis de voz, etc.). La aplicación proporciona un análisis detallado de las características de audio para identificar patrones anómalos típicos del audio sintético.

### ¿Por qué es importante?

El audio generado con IA (deepfakes de audio, síntesis de voz) representa un riesgo significativo en la sociedad moderna:
- 🎭 **Suplantación de identidad** - Robo y clonación de identidad vocal
- 📰 **Desinformación** - Contenido falso que se viraliza rápidamente
- 💰 **Fraude de voz** - Estafas telefónicas y suplantaciones avanzadas

**TFG-Auditra** proporciona herramientas forenses profesionales para identificar y autenticar la autenticidad del contenido de audio, siendo especialmente útil para investigadores, forenses digitales y profesionales de seguridad.

---

## ✨ Características

- ✅ **Carga de archivos de audio** - Soporta múltiples formatos (MP3, WAV, etc.)
- ✅ **Análisis IA en tiempo real** - Detecta características de audio generado
- ✅ **Análisis metadata** - Extrae información forense del archivo
- ✅ **Reportes detallados** - Genera análisis comprensivos del audio
- ✅ **Interfaz moderna** - Dashboard intuitivo y responsivo
- ✅ **Internacionalización** - Soporte multi-idioma (ES/EN)
- ✅ **Aplicación nativa** - Experiencia de escritorio con webview
- ✅ **Portátil** - Un único ejecutable sin dependencias externas

---

## ⚙️ Requisitos previos

### Para Windows:

**Backend:**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

**Frontend:**
- Node.js (v16+)
- npm o yarn

**Para compilar a .exe:**
- PyInstaller
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

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Backend** | Python | 3.8+ |
| | FastAPI | Latest |
| | Uvicorn | - |
| | PyWebView | - |
| **Frontend** | React | 18+ |
| | Vite | - |
| | CSS Modules | - |
| | i18n (Internacionalización) | - |
| **Deployment** | PyInstaller | - |
| **Package Manager** | pip (Python) / npm (Node.js) | - |

---

## 🔧 Configuración

### Puertos y URLs (centralizados en `backend/app/core/config.py`)

```python
Config.BACKEND_HOST = "127.0.0.1"
Config.BACKEND_PORT = 8000
Config.FRONTEND_DEV_PORT = 5173
Config.FRONTEND_DEV_URL = "http://localhost:5173"
```

Para cambiar estos valores, edita `backend/app/core/config.py`

---

## � Estrategias de análisis

La aplicación implementa múltiples estrategias para detectar audio generado por IA:

- **Metadata Analysis** - Análisis de metadatos del archivo
- **Pattern Detection** - Detección de patrones anómalos en la señal
- **Spectral Analysis** - Análisis del espectrograma
- **Feature Extraction** - Extracción de características acústicas

---

## �📝 Notas importantes

- **Desarrollo**: Backend y frontend se ejecutan en procesos separados con hot-reload
- **Producción (.exe)**: Todo se ejecuta en un único proceso con interfaz integrada
- **Primera ejecución**: La aplicación creará automáticamente directorios necesarios
- **Encoding**: Soporta caracteres Unicode y acentos sin problemas
- **Limpieza**: Los archivos subidos se almacenan temporalmente en `backend/uploads/`
- **Detección**: Las estrategias de análisis se pueden extender con nuevos modelos IA

---

## 📄 Licencia
Este proyecto es parte de un TFG (Trabajo de Fin de Grado)

---

## 👤 Autora
Claudia Nistal García - Detector de Audio IA (TFG)
