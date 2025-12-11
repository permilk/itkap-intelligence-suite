"""
ITKAP INTELLIGENCE SUITE - MAIN APPLICATION
Version: 3.3.9 (Navigation Fixed - Two Independent Blocks)
"""
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import logging

from config import CONFIG, COLORS, MESSAGES
from data_service import data_service, metrics_calculator
from charts import (
    create_comparison_chart, create_ranking_chart, 
    create_heatmap, create_histogram, create_radar_chart
)
from ui_components import ui, nav, uploader, table, button, stats
from report_generator import report_generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════
class AppState:
    @staticmethod
    def initialize_session_state():
        if 'data' not in st.session_state: st.session_state.data = None
        if 'competency_map' not in st.session_state: st.session_state.competency_map = None
        if 'upload_timestamp' not in st.session_state: st.session_state.upload_timestamp = None
        if 'current_page' not in st.session_state: st.session_state.current_page = "Inicio"
    
    @staticmethod
    def has_data() -> bool:
        return st.session_state.data is not None
    
    @staticmethod
    def set_page(page: str):
        st.session_state.current_page = page
    
    @staticmethod
    def get_page() -> str:
        return st.session_state.get('current_page', 'Inicio')
    
    @staticmethod
    def get_scale_info(df_plot) -> dict:
        """Detecta automáticamente la escala de los datos y devuelve info de formato"""
        if df_plot.empty:
            return {'type': 'rango', 'format': '{:.2f}', 'suffix': '', 'max': 5}
        
        max_val = df_plot.max().max()
        
        if max_val <= 5.5:
            return {
                'type': 'rango',
                'format': '{:.2f}',
                'suffix': '',
                'max': 5,
                'label': 'Rango (0-5)'
            }
        elif max_val <= 10.5:
            return {
                'type': 'puntos',
                'format': '{:.1f}',
                'suffix': '',
                'max': 10,
                'label': 'Puntos (0-10)'
            }
        else:
            return {
                'type': 'porcentaje',
                'format': '{:.1f}',
                'suffix': '%',
                'max': 100,
                'label': 'Porcentaje (%)'
            }

st.set_page_config(
    page_title=CONFIG.APP_NAME,
    page_icon=CONFIG.APP_ICON,
    layout=CONFIG.LAYOUT,
    initial_sidebar_state=CONFIG.SIDEBAR_STATE
)

# Inject CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {COLORS.BACKGROUND}; }}
    section[data-testid="stSidebar"] {{ background: {COLORS.PRIMARY}; }}
    h1, h2, h3 {{ color: {COLORS.PRIMARY}; }}
    div[data-testid="metric-container"] {{
        background-color: white; border: 1px solid {COLORS.GRAY_LIGHT};
        border-left: 4px solid {COLORS.SECONDARY}; padding: 15px; border-radius: 8px;
    }}
    [data-testid='stFileUploader'] section {{ background-color: white; border: 2px dashed {COLORS.SECONDARY}; }}
    .stRadio > label {{ color: white !important; font-weight: 600; }}
    .stRadio div[role='radiogroup'] > label {{ color: white !important; }}
    </style>
""", unsafe_allow_html=True)

AppState.initialize_session_state()

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    nav.render_sidebar_header()
    
    # --- CONTROL DE ESCALA (FILTRO) ---
    scale_mode = "Rango (0-5)" # Default
    if AppState.has_data():
        st.markdown("---")
        st.markdown("<h4 style='color:white; margin:0;'>⚙️ Configuración</h4>", unsafe_allow_html=True)
        
        # CSS para hacer visible el texto del radio Y los botones
        st.markdown("""
        <style>
        /* Título del radio */
        div[data-testid="stRadio"] > label {
            color: white !important;
            font-weight: 500;
        }
        /* Opciones del radio */
        div[data-testid="stRadio"] label[data-baseweb="radio"] {
            color: white !important;
        }
        div[data-testid="stRadio"] label[data-baseweb="radio"] span {
            color: white !important;
        }
        /* Texto dentro del radio */
        div[data-testid="stRadio"] label[data-baseweb="radio"] > div {
            color: white !important;
        }
        /* Radio buttons visibles - círculos */
        div[data-testid="stRadio"] input[type="radio"] {
            accent-color: #ff6b35 !important;
            width: 18px !important;
            height: 18px !important;
            cursor: pointer !important;
        }
        /* Radio button container */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: rgba(255, 255, 255, 0.05) !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            margin: 4px 0 !important;
            cursor: pointer !important;
        }
        /* Radio button cuando está seleccionado */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            background-color: rgba(255, 107, 53, 0.2) !important;
            border: 1px solid #ff6b35 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        scale_mode = st.radio(
            "Escala de Visualización",
            ["Rango (0-5)", "Porcentaje (0-100)"],
            index=0,
            help="Elige si ver los datos en escala de 0 a 5 o en porcentaje."
        )
    # ----------------------------------

    # CSS GLOBAL para eliminar fondos del option_menu
    st.markdown("""
    <style>
    /* Eliminar todos los fondos del menú */
    nav[data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }
    div[data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }
    /* Forzar que el contenedor del option_menu sea transparente */
    .css-17lntkn, .css-pkbazv {
        background-color: transparent !important;
    }
    /* Eliminar todos los fondos de divs en sidebar */
    section[data-testid="stSidebar"] div {
        background-color: transparent !important;
    }
    /* Específicamente para nav-menu */
    nav.css-1544g2n {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Dashboard General", "Análisis Individual", "Rankings", "Matriz de Calor", "Reporte General"],
        icons=["house-fill", "graph-up", "person-circle", "trophy-fill", "grid-3x3-gap-fill", "file-earmark-text-fill"],
        menu_icon="cast", 
        default_index=0,
        key="main_navigation",
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "transparent",
                "border": "none"
            },
            "icon": {
                "color": "#1e3a5f",  # Azul oscuro para íconos no seleccionados
                "font-size": "20px"  # Íconos más grandes
            },
            "nav-link": {
                "font-size": "15px",  # Texto un poco más grande
                "margin": "3px 0", 
                "padding": "12px 16px",  # Más espacio (antes 8px 12px)
                "color": "#1e3a5f",
                "background-color": "transparent",
                "border": "none",
                "border-radius": "6px"
            },
            "nav-link-selected": {
                "background-color": COLORS.SECONDARY,
                "color": "#ffffff",
                "font-weight": "600"
            },
        }
    )
    
    # CSS adicional para hacer íconos blancos cuando está seleccionado
    st.markdown("""
    <style>
    /* Íconos blancos en item seleccionado */
    nav[data-testid="stSidebarNav"] a[aria-current="page"] svg {
        color: white !important;
        fill: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    nav.render_sidebar_footer(AppState.has_data())


# ═══════════════════════════════════════════════════════════════════════════
# LOGIC
# ═══════════════════════════════════════════════════════════════════════════

if selected == "Inicio":
    ui.render_page_header(CONFIG.APP_NAME, "Sistema Profesional de Análisis de Competencias")
    
    col1, col2, col3 = st.columns(3)
    with col1: ui.render_info_card("1. Carga", "Sube el archivo Excel exportado desde PsycoSource.", "📁", "info")
    with col2: ui.render_info_card("2. Proceso", "Validación automática de estructura y datos.", "⚙️", "success")
    with col3: ui.render_info_card("3. Análisis", "Dashboards interactivos y reportes ejecutivos.", "📊", "default")
    
    uploaded_file = uploader.render_upload_area()
    
    if uploaded_file:
        with st.spinner(MESSAGES.INFO_LOADING):
            result = data_service.process_excel_file(uploaded_file)
            if result.success:
                st.session_state.data = result.data
                st.session_state.competency_map = result.competency_map
                st.session_state.upload_timestamp = datetime.now()
                st.balloons()
                ui.render_success_message(MESSAGES.SUCCESS_UPLOAD)
                
                metrics = [
                    {'label': 'Empleados', 'value': str(result.row_count)},
                    {'label': 'Competencias', 'value': str(len(result.competency_map))}
                ]
                stats.render_kpi_row(metrics)
                ui.render_info_message("👈 Selecciona 'Dashboard General' en el menú lateral")
            else:
                ui.render_error_message(result.error_message)

if selected != "Inicio" and not AppState.has_data():
    ui.render_empty_state(MESSAGES.ERROR_NO_DATA, "Carga un archivo en Inicio para comenzar.")
    st.stop()

if AppState.has_data() and selected != "Inicio":
    # --- PREPARACIÓN DE DATOS CON VALIDACIÓN ---
    df = st.session_state.data
    comp_map = st.session_state.competency_map
    
    target_key = 'Rango' if scale_mode == "Rango (0-5)" else 'Pct'
    
    # DEBUG: Mostrar estructura del competency_map
    import streamlit as st
#     with st.expander("🔍 DEBUG: Estructura de Competencias", expanded=False):
#         st.write(f"**Buscando columnas tipo:** `{target_key}`")
#         st.write(f"**Total competencias:** {len(comp_map)}")
#         
#         # Contar cuántas tienen cada tipo
#         count_rango = sum(1 for m in comp_map.values() if m.get('Rango'))
#         count_pct = sum(1 for m in comp_map.values() if m.get('Pct'))
#         
#         st.write(f"- Competencias con **Rango**: {count_rango}")
#         st.write(f"- Competencias con **Pct**: {count_pct}")
#         
#         # Mostrar primeras 5 competencias con nombres de columnas completos
#         st.write("**Primeras 5 competencias:**")
#         for i, (comp, metrics) in enumerate(list(comp_map.items())[:5]):
#             rango_col = metrics.get('Rango', 'N/A')
#             pct_col = metrics.get('Pct', 'N/A')
#             st.write(f"{i+1}. **{comp}**")
#             st.write(f"   - Rango: `{rango_col}`")
#             st.write(f"   - Pct: `{pct_col}`")
#         
#         # NUEVO: Mostrar TODAS las columnas del DataFrame original
#         st.write("---")
#         st.write("**🔍 ANÁLISIS: Columnas disponibles en el archivo**")
#         all_cols = list(df.columns)
#         st.write(f"Total columnas: {len(all_cols)}")
#         
#         # Mostrar todas las columnas en grupos
#         st.write("**TODAS LAS COLUMNAS DEL ARCHIVO:**")
#         
#         # Primeras 10 columnas
#         st.write("**Primeras 10 columnas:**")
#         for i, col in enumerate(all_cols[:10], 1):
#             st.code(f"{i}. {col}", language=None)
#         
#         # Últimas 10 columnas
#         if len(all_cols) > 10:
#             st.write("**Últimas 10 columnas:**")
#             for i, col in enumerate(all_cols[-10:], len(all_cols)-9):
#                 st.code(f"{i}. {col}", language=None)
#         
#         # Buscar columnas que NO son solo "Rango"
#         non_rango_cols = [col for col in all_cols if 'Rango' not in col and 'CLAVE' not in col and 'NOMBRE' not in col and 'EDAD' not in col]
#         if non_rango_cols:
#             st.write(f"**Columnas que NO son 'Rango' ni fijas: {len(non_rango_cols)}**")
#             for col in non_rango_cols[:10]:
#                 st.code(col, language=None)
    
    # Construir lista de columnas seleccionadas
    selected_cols = []
    for comp, metrics in comp_map.items():
        # Priorizar la columna del tipo seleccionado
        if metrics.get(target_key):
            selected_cols.append(metrics[target_key])
        # Si no existe, usar la otra columna disponible (fallback)
        elif target_key == 'Rango' and metrics.get('Pct'):
            selected_cols.append(metrics['Pct'])
        elif target_key == 'Pct' and metrics.get('Rango'):
            selected_cols.append(metrics['Rango'])
    
    # DEBUG: Mostrar columnas seleccionadas
#     with st.expander("🔍 DEBUG: Columnas Seleccionadas", expanded=False):
#         st.write(f"**Columnas encontradas:** {len(selected_cols)}")
#         if selected_cols:
#             st.write("**Primeras 5 columnas:**")
#             for i, col in enumerate(selected_cols[:5]):
#                 st.write(f"{i+1}. `{col}`")

    df_plot = data_service.prepare_visualization_data(df, selected_cols)
    
    # === CORRECCIÓN DE CRASH: VALIDAR SI HAY DATOS ===
    if df_plot.empty or df_plot.shape[1] == 0:
        ui.render_error_message(f"⚠️ **Atención:** No se encontraron datos para la escala seleccionada ({scale_mode}).")
        st.info("Por favor, cambia la opción en 'Escala de Visualización' en el menú lateral (ej. cambia de Rango a Porcentaje).")
        st.stop()
    # ================================================

    # NOTA: org_metrics se calcula dentro de cada página que lo necesita
    
    if selected == "Dashboard General":
        # Calcular métricas organizacionales
        org_metrics = metrics_calculator.calculate_organizational_metrics(df_plot)
        
        # Detectar escala automáticamente
        scale_info = AppState.get_scale_info(df_plot)
        
        ui.render_page_header("Dashboard Organizacional", f"Vista panorámica ({scale_info['label']})")
        
        col_l, col_r = st.columns([3,1])
        with col_r:
            html_rep = report_generator.generate_executive_report(df_plot, org_metrics['avg_overall'], org_metrics['total_employees'], org_metrics['total_competencies'])
            button.render_download_button("Descargar Reporte", html_rep, f"Reporte_{datetime.now().strftime('%Y%m%d')}.html")
        
        best_comp = df_plot.mean().idxmax()
        metrics = [
            {'label': MESSAGES.LABEL_EMPLOYEE_COUNT, 'value': str(org_metrics['total_employees'])},
            {'label': MESSAGES.LABEL_AVG_SCORE, 'value': scale_info['format'].format(org_metrics['avg_overall']) + scale_info['suffix']},
            {'label': MESSAGES.LABEL_BEST_COMPETENCY, 'value': scale_info['format'].format(df_plot.mean().max()) + scale_info['suffix'], 'delta': str(best_comp)[:15]+"..."}
        ]
        stats.render_kpi_row(metrics)
        ui.render_divider()
        
        st.plotly_chart(create_histogram(df_plot.mean(axis=1)), use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(create_ranking_chart(df_plot.mean(axis=1), 5, 'top'), use_container_width=True)
        with c2: st.plotly_chart(create_ranking_chart(df_plot.mean(axis=1), 5, 'bottom'), use_container_width=True)
    
    elif selected == "Análisis Individual":
        # Calcular métricas organizacionales
        org_metrics = metrics_calculator.calculate_organizational_metrics(df_plot)
        
        # Detectar escala automáticamente
        scale_info = AppState.get_scale_info(df_plot)
        
        ui.render_page_header("Análisis Individual", f"Perfil detallado ({scale_info['label']})")
        empleado = st.selectbox("Seleccionar Colaborador", df_plot.index.sort_values())
        
        ind_avg = df_plot.loc[empleado].mean()
        diff = ind_avg - org_metrics['avg_overall']
        
        metrics = [
            {'label': 'Promedio Individual', 'value': scale_info['format'].format(ind_avg) + scale_info['suffix']},
            {'label': 'vs Organización', 'value': f"{diff:+.2f}" + scale_info['suffix'], 'delta': "Diferencia"},
            {'label': 'Fortaleza', 'value': df_plot.loc[empleado].idxmax()}
        ]
        stats.render_kpi_row(metrics)
        ui.render_divider()
        
        # Gráficas
        st.plotly_chart(create_comparison_chart(df_plot.loc[empleado], df_plot.mean(), empleado), use_container_width=True)
        st.plotly_chart(create_radar_chart(df_plot.loc[empleado], df_plot.mean(), empleado), use_container_width=True)
        # Aquí se usa automáticamente el GapAnalysisChart actualizado (semáforo)
        from charts import create_gap_chart 
        st.plotly_chart(create_gap_chart(df_plot.loc[empleado], df_plot.mean(), "Semáforo de Brechas"), use_container_width=True)
        
        table.render_comparison_table(df_plot.loc[empleado], df_plot.mean())
    
    elif selected == "Rankings":
        # Detectar escala automáticamente
        scale_info = AppState.get_scale_info(df_plot)
        
        ui.render_page_header("Rankings de Desempeño", f"Talento clave en escala {scale_info['label']}")
        n_val = st.slider("Cantidad", 3, 20, 8)
        
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(create_ranking_chart(df_plot.mean(axis=1), n_val, 'top'), use_container_width=True)
        with c2: st.plotly_chart(create_ranking_chart(df_plot.mean(axis=1), n_val, 'bottom'), use_container_width=True)
        
        # Crear DataFrame de ranking
        rank_df = df_plot.mean(axis=1).sort_values(ascending=False).to_frame('Promedio')
        rank_df.insert(0, 'Posición', range(1, len(rank_df)+1))
        
        # Aplicar estilizado personalizado
        # Determinar vmin y vmax según la escala
        if scale_info['max'] <= 5:
            # Escala 0-5
            vmin, vmax = 0, 5
        elif scale_info['max'] <= 10:
            # Escala 0-10
            vmin, vmax = 0, 10
        else:
            # Escala 0-100
            vmin, vmax = 0, 100
        
        # Estilizar solo la columna "Promedio" con semáforo
        styled_rank = rank_df.style.background_gradient(
            subset=['Promedio'],
            cmap='RdYlGn',
            vmin=vmin,
            vmax=vmax
        ).format({'Promedio': '{:.1f}', 'Posición': '{:.0f}'})
        
        # Renderizar con estilo personalizado
        st.dataframe(styled_rank, use_container_width=True, height=500)
    
    elif selected == "Matriz de Calor":
        # Detectar escala automáticamente
        scale_info = AppState.get_scale_info(df_plot)
        
        ui.render_page_header("Matriz de Calor", f"Mapa global ({scale_info['label']})")
        st.plotly_chart(create_heatmap(df_plot), use_container_width=True)
        
        stats_df = metrics_calculator.calculate_competency_stats(df_plot)
        table.render_styled_dataframe(stats_df)
    
    elif selected == "Reporte General":
        # Calcular métricas organizacionales
        org_metrics = metrics_calculator.calculate_organizational_metrics(df_plot)
        
        ui.render_page_header("Generador de Reportes", "Exportación ejecutiva")
        if st.button("Generar Reporte"):
            st.success("Reporte generado")
        
        html_rep = report_generator.generate_executive_report(df_plot, org_metrics['avg_overall'], org_metrics['total_employees'], org_metrics['total_competencies'])
        button.render_download_button("Descargar HTML", html_rep, f"Reporte_{datetime.now().strftime('%Y%m%d')}.html")
    
# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color: #aaa;'>{CONFIG.APP_NAME} v{CONFIG.APP_VERSION} © 2025</div>", unsafe_allow_html=True)