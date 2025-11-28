"""
ITKAP Intelligence Suite - Data Service Module
Version: 3.2.4 (Fixed: Forward Fill for Competencias)
"""
import pandas as pd
import numpy as np
import logging
from io import BytesIO
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from config import CONFIG, MESSAGES

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    success: bool
    data: Optional[pd.DataFrame] = None
    competency_map: Optional[Dict[str, Dict[str, str]]] = None 
    row_count: int = 0
    column_count: int = 0
    error_message: Optional[str] = None

class DataValidator:
    @staticmethod
    def validate_file_size(file_obj: BytesIO) -> Tuple[bool, str]:
        file_obj.seek(0, 2)
        size_bytes = file_obj.tell()
        file_obj.seek(0)
        limit_bytes = CONFIG.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if size_bytes > limit_bytes:
            return False, f"Archivo demasiado grande ({size_bytes / 1024 / 1024:.1f}MB). Máximo: {CONFIG.MAX_UPLOAD_SIZE_MB}MB"
        return True, ""

    @staticmethod
    def validate_structure(df_raw: pd.DataFrame) -> Tuple[bool, str]:
        if df_raw.shape[0] < CONFIG.MIN_ROWS_REQUIRED:
            return False, MESSAGES.ERROR_INVALID_FORMAT
        return True, ""

class DataService:
    def __init__(self):
        self.validator = DataValidator()

    def process_excel_file(self, uploaded_file: BytesIO) -> ProcessingResult:
        try:
            # 1. Validación de Seguridad
            is_valid_size, size_error = self.validator.validate_file_size(uploaded_file)
            if not is_valid_size:
                return ProcessingResult(success=False, error_message=size_error)

            # 2. Lectura Inicial
            df_raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
            
            # 3. Validación de Estructura
            is_valid_struct, struct_error = self.validator.validate_structure(df_raw)
            if not is_valid_struct:
                return ProcessingResult(success=False, error_message=struct_error)

            # 4. Parsing de Encabezados (3 niveles)
            # La estructura real tiene 3 filas de headers:
            # 1. Categorías (fila 9 Excel, índice 8) - celdas combinadas
            # 2. Competencias específicas (fila 10 Excel, índice 9)
            # 3. Columnas fijas + Métricas (fila 11 Excel, índice 10)
            
            idx_categoria = CONFIG.CATEGORY_ROW - 1      # Fila 9 Excel = índice 8
            idx_competencia = CONFIG.COMPETENCE_ROW - 1  # Fila 10 Excel = índice 9
            idx_metrica = CONFIG.METRIC_ROW - 1          # Fila 11 Excel = índice 10
            
            logger.info(f"Leyendo categorías desde índice {idx_categoria} (Fila {CONFIG.CATEGORY_ROW} Excel)")
            logger.info(f"Leyendo competencias desde índice {idx_competencia} (Fila {CONFIG.COMPETENCE_ROW} Excel)")
            logger.info(f"Leyendo métricas desde índice {idx_metrica} (Fila {CONFIG.METRIC_ROW} Excel)")

            # Extraer las 3 filas de headers
            categoria_series = df_raw.iloc[idx_categoria].ffill()  # Forward fill para celdas combinadas
            competencia_series = df_raw.iloc[idx_competencia].ffill()  # Forward fill TAMBIÉN para competencias
            metrica_series = df_raw.iloc[idx_metrica].copy()
            
            # Mapeo de competencias
            competency_map = {}
            
            # Primero, identificar dónde terminan las columnas fijas
            fixed_cols_end = 0
            for i in range(len(metrica_series)):
                metrica_val = metrica_series.iloc[i]
                metrica_str = str(metrica_val).strip() if pd.notna(metrica_val) else ""
                if metrica_str in CONFIG.REQUIRED_COLUMNS:
                    fixed_cols_end = i + 1
            
            logger.info(f"Columnas fijas detectadas: {fixed_cols_end} columnas")
            
            # Procesar columnas de competencias (después de las columnas fijas)
            for i in range(fixed_cols_end, len(metrica_series)):
                categoria_val = categoria_series.iloc[i]
                competencia_val = competencia_series.iloc[i]
                metrica_val = metrica_series.iloc[i]
                
                categoria = str(categoria_val).strip() if pd.notna(categoria_val) else ""
                competencia = str(competencia_val).strip() if pd.notna(competencia_val) else ""
                metrica = str(metrica_val).strip() if pd.notna(metrica_val) else ""
                
                # Ignorar si no hay datos válidos
                if not competencia or not metrica:
                    continue
                
                # Limpiar nombres (quitar espacios extras)
                competencia = ' '.join(competencia.split())
                
                # Nombre completo de columna
                col_name = f"{competencia} - {metrica}"
                
                # Inicializar competencia en el mapa si no existe
                if competencia not in competency_map:
                    competency_map[competencia] = {'Rango': None, 'Pct': None}
                
                # Detectar tipo de métrica con patrones mejorados
                metrica_lower = metrica.lower()
                
                # LOG: Imprimir métricas para debug
                if i < 70:  # Solo las primeras 70 columnas
                    logger.info(f"  Col {i}: Métrica='{metrica}' | Competencia='{competencia}'")
                
                # Detección de RANGO
                if any(keyword in metrica_lower for keyword in ['rango', 'range']):
                    competency_map[competencia]['Rango'] = col_name
                    logger.debug(f"    → Detectado como RANGO")
                # Detección de PORCENTAJE/RENDIMIENTO
                elif any(keyword in metrica_lower for keyword in ['rend', '%', 'percent', 'porcentaje', 'pct']):
                    competency_map[competencia]['Pct'] = col_name
                    logger.debug(f"    → Detectado como PCT")
                else:
                    logger.warning(f"    → NO DETECTADO (ni Rango ni Pct): '{metrica}'")
            
            logger.info(f"Competencias mapeadas: {len(competency_map)}")

            # 5. Recarga de Datos con headers correctos
            uploaded_file.seek(0)
            df_data_raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
            
            # Extraer datos desde la fila correcta
            start_row = CONFIG.DATA_START_ROW  # Fila 11 Excel = índice 10
            df_data = df_data_raw.iloc[start_row:].copy()
            
            logger.info(f"Datos extraídos desde fila {start_row} (Fila {CONFIG.DATA_START_ROW+1} Excel)")
            logger.info(f"Forma de datos: {df_data.shape}")
            
            # 6. Reconstrucción de nombres de columnas
            final_columns = []
            for i in range(df_data_raw.shape[1]):
                metrica_val = metrica_series.iloc[i] if i < len(metrica_series) else None
                metrica_str = str(metrica_val).strip() if pd.notna(metrica_val) else ""
                
                # Si es columna fija, usar nombre directo
                if metrica_str in CONFIG.REQUIRED_COLUMNS:
                    final_columns.append(metrica_str)
                else:
                    # Es columna de competencia
                    comp_val = competencia_series.iloc[i] if i < len(competencia_series) else None
                    comp_str = str(comp_val).strip() if pd.notna(comp_val) else ""
                    
                    if comp_str and metrica_str:
                        comp_str = ' '.join(comp_str.split())  # Limpiar espacios
                        final_columns.append(f"{comp_str} - {metrica_str}")
                    else:
                        # Columna sin nombre válido
                        final_columns.append(f"Col_{i}")
            
            # Ajustar longitud
            if len(final_columns) > len(df_data.columns):
                final_columns = final_columns[:len(df_data.columns)]
            elif len(df_data.columns) > len(final_columns):
                df_data = df_data.iloc[:, :len(final_columns)]
            
            df_data.columns = final_columns
            
            logger.info(f"Columnas finales: {list(df_data.columns[:10])}")  # Primeras 10
            
            # 7. LIMPIEZA CRÍTICA
            # Eliminar filas completamente vacías
            df_data = df_data.dropna(how='all')
            
            if 'NOMBRE' in df_data.columns:
                # Filtrar por NOMBRE válido
                df_data = df_data[df_data['NOMBRE'].notna()].copy()
                df_data['NOMBRE'] = df_data['NOMBRE'].astype(str).str.strip()
                
                # Eliminar headers repetidos y filas de totales
                df_data = df_data[~df_data['NOMBRE'].str.upper().isin(['NOMBRE', 'PROMEDIO', 'TOTAL', ''])]
                df_data = df_data[df_data['NOMBRE'] != '']
                
                # Validar CLAVE si existe
                if 'CLAVE' in df_data.columns:
                    df_data = df_data[df_data['CLAVE'].notna()].copy()
                    df_data = df_data[df_data['CLAVE'].astype(str).str.strip() != '']
            
            # Reset index
            df_data = df_data.reset_index(drop=True)
            
            logger.info(f"Datos finales: {len(df_data)} empleados x {len(competency_map)} competencias")
            
            return ProcessingResult(
                success=True,
                data=df_data,
                competency_map=competency_map,
                row_count=len(df_data),
                column_count=len(competency_map)
            )

        except Exception as e:
            logger.error(f"Error procesando archivo: {str(e)}", exc_info=True)
            return ProcessingResult(success=False, error_message=f"{MESSAGES.ERROR_PROCESSING}: {str(e)}")

    def prepare_visualization_data(self, df: pd.DataFrame, selected_cols: List[str]) -> pd.DataFrame:
        valid_cols = [c for c in selected_cols if c in df.columns]
        if not valid_cols: return pd.DataFrame()
            
        df_plot = df[['NOMBRE'] + valid_cols].copy()
        new_col_names = []
        for c in df_plot.columns:
            if c == 'NOMBRE': new_col_names.append(c)
            else:
                clean_name = c.split(' - ')[0].strip()
                new_col_names.append(clean_name)
        
        df_plot.columns = new_col_names
        df_plot.set_index('NOMBRE', inplace=True)
        return df_plot.apply(pd.to_numeric, errors='coerce')

class MetricsCalculator:
    def calculate_organizational_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {'avg_overall': 0.0, 'total_employees': 0, 'total_competencies': 0}
        return {
            'avg_overall': df.mean().mean() or 0.0,
            'total_employees': len(df),
            'total_competencies': len(df.columns)
        }

    def calculate_competency_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        stats = pd.DataFrame({
            'Promedio': df.mean(), 'Mediana': df.median(),
            'Máximo': df.max(), 'Mínimo': df.min(), 'Desv. Est.': df.std()
        })
        mean_safe = df.mean().replace(0, np.nan)
        stats['Coef. Var.'] = (df.std() / mean_safe * 100).fillna(0)
        return stats.sort_values('Promedio', ascending=False)

data_service = DataService()
metrics_calculator = MetricsCalculator()