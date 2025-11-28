"""
ITKAP Intelligence Suite - Configuration Module
Enterprise-grade configuration management
Version: 3.0.9 (Row Index Fix)
"""

from typing import Dict, Tuple, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class ChartType(Enum):
    RADAR = "radar"
    BAR = "bar"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    COMPARISON = "comparison"

class MetricType(Enum):
    PERCENTAGE = "percentage"
    COUNT = "count"
    TEXT = "text"

@dataclass(frozen=True)
class ColorPalette:
    PRIMARY: str = "#0E1B2E"
    SECONDARY: str = "#F27200"
    BACKGROUND: str = "#F8FAFC"
    WHITE: str = "#FFFFFF"
    GRAY_LIGHT: str = "#E2E8F0"
    GRAY_TEXT: str = "#64748B"
    SUCCESS: str = "#10B981"
    WARNING: str = "#F59E0B"
    DANGER: str = "#EF4444"
    INFO: str = "#3B82F6"
    
    PRIMARY_ALPHA_10: str = "rgba(14, 27, 46, 0.1)"
    PRIMARY_ALPHA_20: str = "rgba(14, 27, 46, 0.2)"
    SECONDARY_ALPHA_15: str = "rgba(242, 114, 0, 0.15)"
    SECONDARY_ALPHA_20: str = "rgba(242, 114, 0, 0.2)"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'primary': self.PRIMARY,
            'secondary': self.SECONDARY,
            'background': self.BACKGROUND,
            'white': self.WHITE,
            'gray_light': self.GRAY_LIGHT,
            'gray_text': self.GRAY_TEXT,
            'success': self.SUCCESS,
            'warning': self.WARNING,
            'danger': self.DANGER,
            'info': self.INFO
        }

@dataclass(frozen=True)
class AppConfig:
    APP_NAME: str = "ITKAP Intelligence Suite"
    APP_VERSION: str = "3.3.6"
    APP_ICON: str = "🔷"
    COMPANY_NAME: str = "ITKAP Consulting"
    
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    
    MIN_ROWS_REQUIRED: int = 10 # Reducido por flexibilidad
    MAX_UPLOAD_SIZE_MB: int = 50
    
    REQUIRED_COLUMNS: Tuple[str, ...] = ('NOMBRE', 'CLAVE', 'EDAD', 'NIVEL', 'PERFIL', 'ÁREA')
    
    # === CONFIGURACIÓN DE ESTRUCTURA DEL ARCHIVO ===
    # Basado en análisis real del Excel de PsycoSource:
    # Fila 9 Excel (índice 8) = Categorías de competencias (celdas combinadas)
    # Fila 10 Excel (índice 9) = Nombres específicos de competencias
    # Fila 11 Excel (índice 10) = Columnas fijas (CLAVE, NOMBRE, etc.) + Métricas (Rango/Rend %)
    # Fila 12 Excel (índice 11) = Primera fila de datos de empleados
    CATEGORY_ROW: int = 9         # Fila 9 Excel = índice 8 (Categorías)
    COMPETENCE_ROW: int = 10      # Fila 10 Excel = índice 9 (Competencias)
    METRIC_ROW: int = 11          # Fila 11 Excel = índice 10 (Métricas)
    DATA_START_ROW: int = 11      # Fila 12 Excel = índice 11 (Datos)
    
    CACHE_TTL: int = 3600
    
    CHART_MIN_SCORE: int = 0
    CHART_MAX_SCORE: int = 100
    CHART_HEIGHT_BASE: int = 450
    
    DEFAULT_TOP_N: int = 5
    MIN_TOP_N: int = 3
    MAX_TOP_N: int = 20

@dataclass
class ChartConfig:
    PLOTLY_CONFIG: Dict = field(default_factory=dict)
    MARGIN_DEFAULT: Dict[str, int] = field(default_factory=dict)
    MARGIN_COMPACT: Dict[str, int] = field(default_factory=dict)
    GAP_CRITICAL_THRESHOLD: float = -5.0
    
    FONT_FAMILY: str = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    FONT_SIZE_SMALL: int = 10
    FONT_SIZE_NORMAL: int = 12
    FONT_SIZE_LARGE: int = 14
    FONT_SIZE_TITLE: int = 16

    def __post_init__(self):
        if not self.PLOTLY_CONFIG:
            self.PLOTLY_CONFIG = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'toImageButtonOptions': {'format': 'png', 'filename': 'itkap_chart', 'height': 800, 'width': 1200, 'scale': 2}
            }
        if not self.MARGIN_DEFAULT: self.MARGIN_DEFAULT = {'l': 50, 'r': 50, 't': 80, 'b': 80}
        if not self.MARGIN_COMPACT: self.MARGIN_COMPACT = {'l': 20, 'r': 20, 't': 40, 'b': 40}

    @staticmethod
    def get_scale_params(max_value: float) -> Dict[str, Any]:
        if max_value <= 5.5: return {'max': 5, 'dtick': 1, 'title': 'Nivel (0-5)', 'format': '.2f', 'is_percent': False}
        elif max_value <= 10.5: return {'max': 10, 'dtick': 1, 'title': 'Puntaje (0-10)', 'format': '.1f', 'is_percent': False}
        else: return {'max': 100, 'dtick': 10, 'title': 'Nivel (%)', 'format': '.1f', 'is_percent': True}

@dataclass(frozen=True)
class Messages:
    SUCCESS_UPLOAD: str = "✅ Archivo procesado exitosamente"
    SUCCESS_REPORT: str = "✅ Reporte generado correctamente"
    ERROR_NO_DATA: str = "⚠️ No hay datos disponibles"
    ERROR_INVALID_FORMAT: str = "❌ Formato de archivo no válido"
    ERROR_MISSING_COLUMNS: str = "❌ Faltan columnas requeridas en el archivo"
    ERROR_PROCESSING: str = "❌ Error al procesar el archivo"
    ERROR_EMPTY_FILE: str = "❌ El archivo está vacío o no tiene datos válidos"
    ERROR_SIZE_LIMIT: str = "⚠️ El archivo excede el límite de tamaño permitido"
    INFO_UPLOAD: str = "📂 Arrastra tu archivo Excel aquí o haz clic para seleccionar"
    INFO_LOADING: str = "🔄 Procesando datos..."
    LABEL_EMPLOYEE_COUNT: str = "Total Empleados"
    LABEL_AVG_SCORE: str = "Promedio General"
    LABEL_COMPETENCIES: str = "Competencias"
    LABEL_BEST_COMPETENCY: str = "Mejor Competencia"

COLORS = ColorPalette()
CONFIG = AppConfig()
CHART_CONFIG = ChartConfig()
MESSAGES = Messages()

def get_chart_layout_config() -> Dict:
    return {'font': {'family': CHART_CONFIG.FONT_FAMILY}, 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)', 'margin': CHART_CONFIG.MARGIN_DEFAULT, 'hovermode': 'closest'}