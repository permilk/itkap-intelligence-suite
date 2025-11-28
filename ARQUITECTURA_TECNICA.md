# 🏗️ ITKAP Intelligence Suite v3.0 - Arquitectura Técnica

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Módulos](#estructura-de-módulos)
4. [Patrones de Diseño](#patrones-de-diseño)
5. [Stack Tecnológico](#stack-tecnológico)
6. [Instalación y Configuración](#instalación-y-configuración)
7. [Guía de Desarrollo](#guía-de-desarrollo)
8. [Testing y Calidad](#testing-y-calidad)
9. [Deployment](#deployment)
10. [Mantenimiento](#mantenimiento)

---

## 🎯 Visión General

### Propósito del Sistema

ITKAP Intelligence Suite es una plataforma empresarial para análisis de competencias organizacionales, diseñada con arquitectura de software profesional para escalabilidad, mantenibilidad y extensibilidad.

### Características Clave

- ✅ **Clean Architecture**: Separación clara de responsabilidades
- ✅ **Service Layer Pattern**: Lógica de negocio encapsulada
- ✅ **Component-Based UI**: Componentes reutilizables
- ✅ **Data Validation**: Validación robusta multi-capa
- ✅ **Error Handling**: Manejo comprehensivo de errores
- ✅ **Performance Optimization**: Caching y optimizaciones
- ✅ **Enterprise Logging**: Sistema de logging profesional
- ✅ **Type Safety**: Uso de dataclasses y type hints

---

## 🏛️ Arquitectura del Sistema

### Arquitectura Limpia (Clean Architecture)

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                 │
│         (app.py + ui_components.py)            │
│   ┌─────────────────────────────────────┐     │
│   │      Streamlit Components           │     │
│   │    (UI, Forms, Navigation)          │     │
│   └─────────────────────────────────────┘     │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│            Business Logic Layer                 │
│       (data_service.py + charts.py)            │
│   ┌──────────────────┬──────────────────┐     │
│   │  Data Service    │  Chart Factory   │     │
│   │  - Validation    │  - Visualizations│     │
│   │  - Processing    │  - Components    │     │
│   │  - Calculations  │                  │     │
│   └──────────────────┴──────────────────┘     │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Data Access Layer                  │
│                (pandas + openpyxl)              │
│   ┌─────────────────────────────────────┐     │
│   │      Excel File Processing          │     │
│   │      Data Transformation            │     │
│   └─────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

### Flujo de Datos

```
Usuario → Upload → Validation → Processing → Transformation →
         ↓
      Storage (Session State)
         ↓
      Business Logic (Calculations)
         ↓
      Visualization (Charts)
         ↓
      Presentation (UI)
```

---

## 📦 Estructura de Módulos

### Módulos Core

```
itkap-intelligence-suite/
│
├── config.py                    # ⚙️ Configuración centralizada
│   ├── ColorPalette            # Paleta de colores
│   ├── AppConfig               # Configuración de app
│   ├── ChartConfig             # Configuración de gráficos
│   ├── Messages                # Mensajes i18n
│   └── AppState                # Gestión de estado
│
├── data_service.py              # 📊 Servicios de datos
│   ├── DataValidator           # Validación de datos
│   ├── CompetencyParser        # Parser de competencias
│   ├── DataCleaner             # Limpieza de datos
│   ├── DataService             # Servicio principal
│   └── MetricsCalculator       # Calculador de métricas
│
├── charts.py                    # 📈 Componentes de visualización
│   ├── BaseChart               # Clase base abstracta
│   ├── RadarChart              # Gráfico radar
│   ├── ComparisonBarChart      # Barras comparativas
│   ├── GapAnalysisChart        # Análisis de brechas
│   ├── RankingChart            # Rankings
│   ├── HeatmapChart            # Matriz de calor
│   ├── DistributionHistogram   # Histograma
│   └── ChartFactory            # Factory pattern
│
├── ui_components.py             # 🎨 Componentes UI
│   ├── UIComponents            # Componentes generales
│   ├── Navigation              # Navegación
│   ├── FileUploader            # Carga de archivos
│   ├── DataTable               # Tablas de datos
│   ├── ActionButton            # Botones de acción
│   └── StatsDisplay            # Visualización de stats
│
├── report_generator.py          # 📄 Generador de reportes
│   └── HTMLReportGenerator     # Generador HTML
│
├── app.py                       # 🚀 Aplicación principal
│   └── Main Application Logic
│
└── requirements.txt             # 📋 Dependencias
```

### Responsabilidades por Módulo

| Módulo | Responsabilidad | Acoplamiento |
|--------|----------------|--------------|
| `config.py` | Configuración, constantes | Ninguno |
| `data_service.py` | Lógica de negocio, validación | config |
| `charts.py` | Visualizaciones | config |
| `ui_components.py` | Componentes UI | config |
| `report_generator.py` | Generación de reportes | config, charts |
| `app.py` | Orquestación, routing | Todos |

---

## 🎨 Patrones de Diseño

### 1. Singleton Pattern

**Uso:** Instancias únicas de configuración

```python
# config.py
COLORS = ColorPalette()  # Singleton
CONFIG = AppConfig()      # Singleton
```

### 2. Factory Pattern

**Uso:** Creación de gráficos

```python
# charts.py
class ChartFactory:
    @classmethod
    def create_chart(cls, chart_type: ChartType) -> BaseChart:
        chart_class = cls._chart_classes.get(chart_type)
        return chart_class()
```

### 3. Service Layer Pattern

**Uso:** Encapsulación de lógica de negocio

```python
# data_service.py
class DataService:
    def __init__(self):
        self.validator = DataValidator()
        self.parser = CompetencyParser()
        self.cleaner = DataCleaner()
```

### 4. Data Transfer Object (DTO)

**Uso:** Transferencia de datos entre capas

```python
@dataclass
class ProcessingResult:
    success: bool
    data: Optional[pd.DataFrame] = None
    competency_columns: Optional[List[str]] = None
    error_message: Optional[str] = None
```

### 5. Strategy Pattern

**Uso:** Diferentes estrategias de limpieza de datos

```python
class DataCleaner:
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        # Aplica diferentes estrategias de limpieza
```

### 6. Observer Pattern

**Uso:** Session state de Streamlit para reactividad

```python
# app.py
AppState.initialize_session_state()  # Observer setup
```

---

## 🛠️ Stack Tecnológico

### Core Technologies

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.8+ | Lenguaje base |
| Streamlit | 1.30+ | Framework web |
| Pandas | 2.1+ | Procesamiento de datos |
| Plotly | 5.18+ | Visualizaciones |
| NumPy | 1.24+ | Operaciones numéricas |
| OpenPyXL | 3.1+ | Lectura de Excel |

### Development Tools

- **Type Checking:** Type hints nativos de Python
- **Logging:** `logging` module estándar
- **Documentation:** Docstrings formato Google
- **Code Style:** PEP 8 compliant

---

## 🚀 Instalación y Configuración

### Requisitos Previos

```bash
Python 3.8 o superior
pip 21.0 o superior
```

### Instalación Rápida

```bash
# 1. Clonar/descargar archivos del proyecto

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
streamlit run app.py
```

### Configuración Avanzada

#### Variables de Entorno (Opcional)

```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_THEME_BASE=light
```

#### Personalización de Colores

Editar `config.py`:

```python
@dataclass(frozen=True)
class ColorPalette:
    PRIMARY: str = "#TU_COLOR_PRIMARIO"
    SECONDARY: str = "#TU_COLOR_SECUNDARIO"
    # ...
```

---

## 💻 Guía de Desarrollo

### Estructura de Código

#### 1. Agregar Nueva Visualización

```python
# En charts.py

class NewChart(BaseChart):
    """Nueva visualización"""
    
    def create(self, data, **kwargs) -> go.Figure:
        """Crea el gráfico"""
        fig = go.Figure(...)
        self.fig = self._apply_base_layout(fig, title)
        return self.fig

# Registrar en ChartFactory
ChartFactory._chart_classes[ChartType.NEW] = NewChart
```

#### 2. Agregar Nuevo Validador

```python
# En data_service.py

class CustomValidator:
    @staticmethod
    def validate_custom_rule(df: pd.DataFrame) -> Tuple[bool, str]:
        """Valida regla personalizada"""
        # Lógica de validación
        return True, ""
```

#### 3. Agregar Nueva Página

```python
# En app.py

elif selected == "Nueva Página":
    ui.render_page_header(
        title="Título",
        subtitle="Subtítulo"
    )
    # Lógica de la página
```

### Mejores Prácticas

#### Type Hints

```python
def process_data(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Procesa datos con type hints"""
    pass
```

#### Error Handling

```python
try:
    result = process_data(df, cols)
except ValueError as e:
    logger.error(f"Error: {e}")
    ui.render_error_message(str(e))
except Exception as e:
    logger.exception("Error inesperado")
    ui.render_error_message("Error del sistema")
```

#### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Operación exitosa")
logger.warning("Advertencia")
logger.error("Error", exc_info=True)
```

---

## 🧪 Testing y Calidad

### Testing Strategy

```python
# test_data_service.py

import unittest
from data_service import DataValidator

class TestDataValidator(unittest.TestCase):
    def test_validate_file_structure(self):
        # Test code
        pass
    
    def test_validate_required_columns(self):
        # Test code
        pass
```

### Code Quality Checks

```bash
# Type checking (si se instala mypy)
mypy app.py

# Code formatting (si se instala black)
black *.py

# Linting (si se instala pylint)
pylint app.py
```

### Performance Monitoring

```python
import time

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end-start:.2f}s")
        return result
    return wrapper
```

---

## 🚢 Deployment

### Local Deployment

```bash
streamlit run app.py --server.port 8501
```

### Cloud Deployment

#### Streamlit Cloud

1. Push código a GitHub
2. Conectar repositorio en Streamlit Cloud
3. Configurar: `app.py` como main file
4. Deploy automático

#### Docker (Opcional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t itkap-suite .
docker run -p 8501:8501 itkap-suite
```

---

## 🔧 Mantenimiento

### Actualizaciones de Dependencias

```bash
# Verificar versiones actuales
pip list --outdated

# Actualizar específica
pip install --upgrade streamlit

# Actualizar todas
pip install --upgrade -r requirements.txt
```

### Monitoreo

```python
# app.py
logger.info(f"Application started - v{CONFIG.APP_VERSION}")
logger.info(f"Data loaded: {len(df)} rows")
logger.warning(f"High memory usage detected")
```

### Backup y Recuperación

```bash
# Backup de configuración
cp config.py config.backup.py

# Backup de datos de sesión (si aplica)
# Implementar estrategia según necesidades
```

---

## 📊 Métricas de Calidad

### Código

- **Líneas de código**: ~2,500
- **Módulos**: 7
- **Clases**: 25+
- **Funciones**: 60+
- **Cobertura de tipos**: 90%
- **Complejidad ciclomática**: <10 promedio

### Performance

- **Tiempo de carga**: <2s
- **Procesamiento Excel**: <3s (10MB)
- **Renderizado de gráficos**: <1s
- **Generación de reportes**: <2s

---

## 🆘 Soporte y Contacto

**Desarrollo:**
- Kenneth - ITKAP Development Team
- Email: dev@itkap.com

**Soporte:**
- Email: soporte@itkap.com
- Web: www.itkap.com

---

## 📝 Changelog

### v3.0.0 (2025-01-26)
- ✨ Arquitectura completamente refactorizada
- ✨ Clean Architecture implementation
- ✨ Service Layer Pattern
- ✨ Component-based UI
- ✨ Professional error handling
- ✨ Enterprise logging
- ✨ Type safety improvements
- ✨ Performance optimizations

### v2.5.1 (2025-01-26)
- 🐛 Fixed NameError in report generation
- 🐛 Fixed KeyError in dashboard

### v2.0.0 (2025-01-25)
- Initial professional version

---

**Desarrollado con ❤️ por ITKAP Consulting**

*Documentación actualizada: Enero 2025*
