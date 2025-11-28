# 🔧 PARCHES DE CORRECCIÓN - ISSUES DE ALTA SEVERIDAD

## Correcciones para ITKAP Intelligence Suite v3.0.1 → v3.0.2

**Fecha:** Enero 26, 2025  
**Issues Corregidos:** HIGH-01, HIGH-02, HIGH-03  
**Tiempo Estimado:** 4 horas de implementación

---

## 🔴 HIGH-01: Missing import in config.py

### Problema
`AppState` usa `st.session_state` sin import de Streamlit en `config.py`

### Solución: Mover AppState a app.py

#### **ARCHIVO: config.py (MODIFICAR)**

**ELIMINAR** (líneas 187-213):
```python
class AppState:
    """Gestión centralizada del estado de la aplicación"""
    
    @staticmethod
    def initialize_session_state():
        """Inicializa las variables de sesión necesarias"""
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'cols_rend' not in st.session_state:
            st.session_state.cols_rend = None
        if 'processed_data' not in st.session_state:
            st.session_state.processed_data = None
        if 'upload_timestamp' not in st.session_state:
            st.session_state.upload_timestamp = None
    
    @staticmethod
    def clear_cache():
        """Limpia el caché de datos"""
        st.session_state.data = None
        st.session_state.cols_rend = None
        st.session_state.processed_data = None
        st.session_state.upload_timestamp = None
    
    @staticmethod
    def has_data() -> bool:
        """Verifica si hay datos cargados"""
        return st.session_state.data is not None
```

#### **ARCHIVO: app.py (MODIFICAR)**

**CAMBIAR** (línea 30):
```python
# ANTES
from config import CONFIG, COLORS, MESSAGES, AppState

# DESPUÉS
from config import CONFIG, COLORS, MESSAGES
```

**AGREGAR** (después de línea 48, antes de configuración de página):
```python
# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

class AppState:
    """Gestión centralizada del estado de la aplicación"""
    
    @staticmethod
    def initialize_session_state():
        """Inicializa las variables de sesión necesarias"""
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'cols_rend' not in st.session_state:
            st.session_state.cols_rend = None
        if 'processed_data' not in st.session_state:
            st.session_state.processed_data = None
        if 'upload_timestamp' not in st.session_state:
            st.session_state.upload_timestamp = None
    
    @staticmethod
    def clear_cache():
        """Limpia el caché de datos"""
        st.session_state.data = None
        st.session_state.cols_rend = None
        st.session_state.processed_data = None
        st.session_state.upload_timestamp = None
    
    @staticmethod
    def has_data() -> bool:
        """Verifica si hay datos cargados"""
        return st.session_state.data is not None


# Configure logging (mantener como está)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

---

## 🔴 HIGH-02: Falta validación de tamaño de archivo

### Problema
No se valida el tamaño del archivo antes de procesar, permitiendo DoS con archivos masivos

### Solución: Agregar validación de tamaño

#### **ARCHIVO: data_service.py (MODIFICAR)**

**MODIFICAR** el método `process_excel_file` (línea 183):

```python
def process_excel_file(self, uploaded_file: BytesIO) -> ProcessingResult:
    """
    Procesa un archivo Excel de evaluación de competencias
    
    Args:
        uploaded_file: Archivo cargado en formato BytesIO
        
    Returns:
        ProcessingResult con datos procesados o mensaje de error
    """
    try:
        logger.info("Iniciando procesamiento de archivo Excel")
        
        # ═══════════════════════════════════════════════════════════════
        # NUEVO: Validar tamaño del archivo
        # ═══════════════════════════════════════════════════════════════
        uploaded_file.seek(0, 2)  # Ir al final del archivo
        file_size_bytes = uploaded_file.tell()
        uploaded_file.seek(0)  # Volver al inicio
        
        file_size_mb = file_size_bytes / (1024 * 1024)
        max_size_mb = CONFIG.MAX_UPLOAD_SIZE_MB
        
        logger.info(f"Tamaño del archivo: {file_size_mb:.2f} MB")
        
        if file_size_bytes > (max_size_mb * 1024 * 1024):
            error_msg = (
                f"⚠️ Archivo demasiado grande ({file_size_mb:.1f} MB). "
                f"Tamaño máximo permitido: {max_size_mb} MB"
            )
            logger.warning(error_msg)
            return ProcessingResult(success=False, error_message=error_msg)
        # ═══════════════════════════════════════════════════════════════
        
        # Paso 1: Lectura inicial del archivo
        df_raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
        
        # ... resto del código sin cambios
```

#### **TAMBIÉN AGREGAR** (después de línea 47 en DataValidator):

```python
@staticmethod
def validate_file_size(file_size_bytes: int, max_size_mb: int = 50) -> Tuple[bool, str]:
    """
    Valida el tamaño del archivo
    
    Args:
        file_size_bytes: Tamaño en bytes
        max_size_mb: Tamaño máximo permitido en MB
        
    Returns:
        Tuple (is_valid, error_message)
    """
    file_size_mb = file_size_bytes / (1024 * 1024)
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file_size_bytes > max_size_bytes:
        return False, (
            f"Archivo demasiado grande ({file_size_mb:.1f} MB). "
            f"Máximo permitido: {max_size_mb} MB"
        )
    
    return True, ""
```

---

## 🔴 HIGH-03: Falta sanitización de HTML en reportes (XSS)

### Problema
Nombres de empleados y competencias se insertan en HTML sin escapar, permitiendo XSS

### Solución: Sanitizar todo contenido dinámico

#### **ARCHIVO: report_generator.py (MODIFICAR)**

**AGREGAR** al inicio (después de imports, línea 14):

```python
import pandas as pd
import plotly.io as pio
from datetime import datetime
from typing import Dict, Optional
import html  # ← AGREGAR ESTE IMPORT

from config import COLORS, CONFIG
```

**AGREGAR** nueva función (después de __init__, línea ~30):

```python
class HTMLReportGenerator:
    """Generador de reportes HTML profesionales"""
    
    def __init__(self):
        self.colors = COLORS
        self.config = CONFIG
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        Escapa caracteres HTML peligrosos para prevenir XSS
        
        Args:
            text: Texto a sanitizar
            
        Returns:
            Texto con caracteres HTML escapados
        """
        if text is None:
            return ""
        return html.escape(str(text))
    
    def generate_executive_report(
        self,
        df_plot: pd.DataFrame,
        avg_score: float,
        total_employees: int,
        total_competencies: int
    ) -> str:
        """
        Genera un reporte ejecutivo completo en HTML
        
        ... (docstring sin cambios)
        """
        # Calcular métricas adicionales
        best_comp = df_plot.mean().idxmax()
        best_val = df_plot.mean().max()
        worst_comp = df_plot.mean().idxmin()
        worst_val = df_plot.mean().min()
        
        # ═══════════════════════════════════════════════════════════════
        # NUEVO: Sanitizar todas las variables que van al HTML
        # ═══════════════════════════════════════════════════════════════
        best_comp_safe = self.sanitize_html(best_comp)
        worst_comp_safe = self.sanitize_html(worst_comp)
        
        # También sanitizar nombres de empleados en el DataFrame
        df_plot_safe = df_plot.copy()
        df_plot_safe.index = [self.sanitize_html(name) for name in df_plot_safe.index]
        df_plot_safe.columns = [self.sanitize_html(col) for col in df_plot_safe.columns]
        # ═══════════════════════════════════════════════════════════════
        
        # Generar gráficos (usar df_plot_safe en lugar de df_plot)
        fig_dist = create_histogram(df_plot_safe.mean(axis=1))
        html_dist = pio.to_html(fig_dist, include_plotlyjs='cdn', config={'displayModeBar': False})
        
        fig_top = create_ranking_chart(df_plot_safe.mean(axis=1), n=10, mode='top')
        html_top = pio.to_html(fig_top, include_plotlyjs=False, config={'displayModeBar': False})
        
        fig_bottom = create_ranking_chart(df_plot_safe.mean(axis=1), n=10, mode='bottom')
        html_bottom = pio.to_html(fig_bottom, include_plotlyjs=False, config={'displayModeBar': False})
        
        fig_heatmap = create_heatmap(df_plot_safe)
        html_heatmap = pio.to_html(fig_heatmap, include_plotlyjs=False, config={'displayModeBar': False})
        
        # Estadísticas por competencia (usar df_plot_safe)
        stats_comp = pd.DataFrame({
            'Promedio': df_plot_safe.mean(),
            'Máximo': df_plot_safe.max(),
            'Mínimo': df_plot_safe.min(),
            'Desv. Est.': df_plot_safe.std()
        }).sort_values('Promedio', ascending=False)
        
        tabla_stats = stats_comp.to_html(
            classes='table-stats',
            float_format=lambda x: f'{x:.1f}',
            border=0,
            escape=True  # ← IMPORTANTE: Forzar escape en pandas
        )
        
        # ... resto del código
```

**MODIFICAR** en _get_html_template (donde se usan las variables):

**CAMBIAR** todas las ocurrencias de variables dinámicas:

```python
# ANTES (línea ~120)
<p>
    La evaluación organizacional muestra un promedio general de <strong>{kwargs['avg_score']:.1f}%</strong> 
    en las competencias evaluadas. La competencia con mejor desempeño es 
    <strong>{kwargs['best_comp']}</strong> ({kwargs['best_val']:.1f}%), mientras que 
    <strong>{kwargs['worst_comp']}</strong> ({kwargs['worst_val']:.1f}%) ...
</p>

# DESPUÉS
<p>
    La evaluación organizacional muestra un promedio general de <strong>{kwargs['avg_score']:.1f}%</strong> 
    en las competencias evaluadas. La competencia con mejor desempeño es 
    <strong>{kwargs['best_comp_safe']}</strong> ({kwargs['best_val']:.1f}%), mientras que 
    <strong>{kwargs['worst_comp_safe']}</strong> ({kwargs['worst_val']:.1f}%) ...
</p>
```

**ACTUALIZAR** llamada a _get_html_template:

```python
html_content = self._get_html_template(
    timestamp=timestamp,
    total_employees=total_employees,
    avg_score=avg_score,
    total_competencies=total_competencies,
    best_val=best_val,
    best_comp=best_comp_safe,      # ← Usar sanitizado
    best_comp_safe=best_comp_safe, # ← AGREGAR
    worst_comp=worst_comp_safe,    # ← Usar sanitizado
    worst_comp_safe=worst_comp_safe, # ← AGREGAR
    worst_val=worst_val,
    html_dist=html_dist,
    html_top=html_top,
    html_bottom=html_bottom,
    html_heatmap=html_heatmap,
    tabla_stats=tabla_stats
)
```

---

## 🧪 TESTING DE CORRECCIONES

### Test 1: HIGH-01 (AppState)

```python
# Test manual
python -c "import config; print('Config loads OK')"
# Debe funcionar sin errores
```

### Test 2: HIGH-02 (Validación de tamaño)

```python
# Crear archivo de prueba >50MB
import pandas as pd
import numpy as np

# Generar DataFrame grande
df = pd.DataFrame(np.random.rand(50000, 50))
df.to_excel('test_large.xlsx', index=False)

# Cargar en la app → Debe mostrar error de tamaño
```

### Test 3: HIGH-03 (XSS)

```python
# Crear Excel con nombre malicioso
df = pd.DataFrame({
    'NOMBRE': ['<script>alert("XSS")</script>', 'Juan Pérez'],
    'Comp1': [85, 90]
})
df.to_excel('test_xss.xlsx', index=False)

# Generar reporte HTML
# Abrir en navegador
# ANTES: Script se ejecuta ❌
# DESPUÉS: Muestra texto escapado ✅
```

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Antes de Aplicar Parches

- [ ] Backup de archivos originales
- [ ] Crear branch `hotfix/high-severity-fixes`
- [ ] Commit inicial: "Pre-fixes snapshot"

### Aplicar Correcciones

- [ ] **HIGH-01**: Mover AppState a app.py
  - [ ] Eliminar de config.py
  - [ ] Agregar a app.py
  - [ ] Actualizar import
  - [ ] Test: `python -c "import config"`

- [ ] **HIGH-02**: Validación de tamaño
  - [ ] Agregar validación en process_excel_file
  - [ ] Agregar método en DataValidator
  - [ ] Test con archivo >50MB

- [ ] **HIGH-03**: Sanitización HTML
  - [ ] Import html module
  - [ ] Agregar sanitize_html()
  - [ ] Sanitizar todas las variables dinámicas
  - [ ] Actualizar llamadas a template
  - [ ] Test con nombres maliciosos

### Testing Post-Correcciones

- [ ] Test suite básica (5 pruebas funcionales)
- [ ] Test manual de cada corrección
- [ ] Verificación de no-regresión (features existentes)

### Deploy

- [ ] Commit: "Fix HIGH-01, HIGH-02, HIGH-03"
- [ ] Push a repositorio
- [ ] Deploy a staging
- [ ] Verificación en staging
- [ ] Deploy a producción

---

## 📊 IMPACTO DE LAS CORRECCIONES

| Corrección | Líneas Modificadas | Archivos | Riesgo de Regresión |
|------------|-------------------|----------|---------------------|
| HIGH-01 | ~30 | 2 | 🟢 Bajo |
| HIGH-02 | ~25 | 1 | 🟢 Bajo |
| HIGH-03 | ~40 | 1 | 🟡 Medio |

**Total:** ~95 líneas en 3 archivos

---

## ⏱️ TIEMPO ESTIMADO

| Tarea | Tiempo |
|-------|--------|
| Implementación | 2.5 horas |
| Testing | 1 hora |
| Deploy + Verificación | 0.5 horas |
| **TOTAL** | **4 horas** |

---

## ✅ VERIFICACIÓN FINAL

Después de aplicar todos los parches:

```bash
# 1. Verificar imports
python -c "from config import CONFIG, COLORS, MESSAGES; print('✓ config.py OK')"

# 2. Ejecutar app
streamlit run app.py

# 3. Realizar pruebas manuales:
#    - Cargar archivo normal (debe funcionar)
#    - Cargar archivo >50MB (debe rechazar)
#    - Generar reporte con nombre <script> (debe escapar)

# 4. Revisar logs
#    - No debe haber errores
#    - Debe mostrar "Tamaño del archivo: X MB"
```

---

## 📞 SOPORTE

Si encuentras problemas al aplicar estos parches:

**Email:** soporte@itkap.com  
**Ref:** HOTFIX-HIGH-SEVERITY-v3.0.2

---

**FIN DE LOS PARCHES DE CORRECCIÓN**

*Versión: 3.0.1 → 3.0.2*  
*Fecha: Enero 26, 2025*
