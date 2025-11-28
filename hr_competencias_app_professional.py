import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from io import BytesIO
from datetime import datetime
import plotly.io as pio

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ITKAP Intelligence Suite", 
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES CORPORATIVA ITKAP
# ═══════════════════════════════════════════════════════════════════════════

COLOR_NAVY = "#0E1B2E"
COLOR_ORANGE = "#F27200"
COLOR_BG_LIGHT = "#F8FAFC"
COLOR_WHITE = "#FFFFFF"
COLOR_GRAY_LIGHT = "#E2E8F0"
COLOR_GRAY_TEXT = "#64748B"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"

# ═══════════════════════════════════════════════════════════════════════════
# ESTILOS CSS PROFESIONALES
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ==== CONFIGURACIÓN GLOBAL ==== */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .stApp {{
        background-color: {COLOR_BG_LIGHT};
    }}
    
    /* ==== SIDEBAR ==== */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLOR_NAVY} 0%, #1a2942 100%);
        border-right: 1px solid rgba(242, 114, 0, 0.1);
    }}
    
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLOR_WHITE};
    }}
    
    /* ==== TIPOGRAFÍA ==== */
    h1 {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_NAVY};
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    h2 {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_NAVY};
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    
    h3 {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_NAVY};
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }}
    
    h4 {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_GRAY_TEXT};
        font-weight: 500;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}
    
    p, .stMarkdown {{
        color: {COLOR_GRAY_TEXT};
        line-height: 1.6;
    }}
    
    /* ==== FILE UPLOADER ==== */
    [data-testid='stFileUploader'] {{
        width: 100%;
    }}
    
    [data-testid='stFileUploader'] section {{
        padding: 3rem 2rem;
        background-color: {COLOR_WHITE};
        border: 2px dashed {COLOR_ORANGE};
        border-radius: 12px;
        transition: all 0.3s ease;
    }}
    
    [data-testid='stFileUploader'] section:hover {{
        border-color: {COLOR_NAVY};
        background-color: #fafafa;
    }}
    
    [data-testid='stFileUploader'] section > input + div {{
        display: none;
    }}
    
    [data-testid='stFileUploader'] section::after {{
        content: "📂 Arrastra tu archivo Excel aquí o haz clic para seleccionar";
        color: {COLOR_NAVY};
        font-weight: 500;
        font-size: 1.1rem;
        display: block;
        text-align: center;
        margin-top: 10px;
    }}
    
    /* ==== MÉTRICAS ==== */
    div[data-testid="metric-container"] {{
        background-color: {COLOR_WHITE};
        border: 1px solid {COLOR_GRAY_LIGHT};
        border-left: 4px solid {COLOR_ORANGE};
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        padding: 1.25rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }}
    
    div[data-testid="metric-container"]:hover {{
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }}
    
    div[data-testid="metric-container"] label {{
        color: {COLOR_GRAY_TEXT};
        font-weight: 500;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {COLOR_NAVY};
        font-weight: 700;
        font-size: 2rem;
    }}
    
    /* ==== BOTONES ==== */
    .stButton > button {{
        background-color: {COLOR_ORANGE};
        color: {COLOR_WHITE};
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(242, 114, 0, 0.2);
    }}
    
    .stButton > button:hover {{
        background-color: #d96300;
        box-shadow: 0 4px 12px rgba(242, 114, 0, 0.3);
        transform: translateY(-1px);
    }}
    
    /* ==== SELECTBOX ==== */
    .stSelectbox > div > div {{
        background-color: {COLOR_WHITE};
        border: 1px solid {COLOR_GRAY_LIGHT};
        border-radius: 8px;
        padding: 0.5rem;
    }}
    
    /* ==== ALERTS ==== */
    .stAlert {{
        border-radius: 8px;
        border-left-width: 4px;
    }}
    
    /* ==== DATAFRAME ==== */
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }}
    
    /* ==== SPINNER ==== */
    .stSpinner > div {{
        border-top-color: {COLOR_ORANGE};
    }}
    
    /* ==== TARJETAS PERSONALIZADAS ==== */
    .info-card {{
        background-color: {COLOR_WHITE};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLOR_GRAY_LIGHT};
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }}
    
    .info-card-header {{
        color: {COLOR_NAVY};
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .info-card-content {{
        color: {COLOR_GRAY_TEXT};
        line-height: 1.6;
    }}
    
    /* ==== DIVIDER ==== */
    hr {{
        border: none;
        border-top: 1px solid {COLOR_GRAY_LIGHT};
        margin: 2rem 0;
    }}
    
    /* ==== CAPTION ==== */
    .caption {{
        color: {COLOR_GRAY_TEXT};
        font-size: 0.875rem;
        font-weight: 400;
    }}
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# GESTIÓN DE ESTADO
# ═══════════════════════════════════════════════════════════════════════════

if 'data' not in st.session_state:
    st.session_state.data = None
if 'cols_rend' not in st.session_state:
    st.session_state.cols_rend = None

# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES DE PROCESAMIENTO
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def cargar_datos(uploaded_file):
    """
    Procesa archivos Excel de evaluación de competencias
    Retorna: (DataFrame, columnas_rendimiento, error_msg)
    """
    try:
        # Lectura inicial
        df_raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
        if df_raw.shape[0] < 12:
            return None, None, "Formato de archivo no válido (estructura incompleta)"
        
        # Extracción de encabezados
        competencia_row = df_raw.iloc[9]
        metrica_row = df_raw.iloc[10]
        
        # Construcción de nombres de columnas
        new_columns = []
        competencias_dict = {}
        current_competency = ""
        
        for i in range(len(metrica_row)):
            metrica = metrica_row.iloc[i]
            competencia = competencia_row.iloc[i]
            
            # Columnas estándar
            if pd.notna(metrica) and str(metrica).strip() in ['CLAVE', 'NOMBRE', 'EDAD', 'NIVEL', 'PERFIL', 'ÁREA']:
                new_columns.append(str(metrica).strip())
                current_competency = ""
            
            # Nueva competencia
            elif pd.notna(competencia):
                comp_clean = str(competencia).strip()
                current_competency = comp_clean
                if pd.notna(metrica):
                    metrica_clean = str(metrica).strip()
                    col_name = f"{comp_clean} - {metrica_clean}"
                    new_columns.append(col_name)
                    if 'Rend' in metrica_clean or '%' in metrica_clean:
                        competencias_dict[comp_clean] = col_name
                else:
                    new_columns.append(comp_clean)
            
            # Métricas adicionales
            elif current_competency and pd.notna(metrica):
                metrica_clean = str(metrica).strip()
                col_name = f"{current_competency} - {metrica_clean}"
                new_columns.append(col_name)
                if 'Rend' in metrica_clean or '%' in metrica_clean:
                    competencias_dict[current_competency] = col_name
            
            else:
                new_columns.append(f"Col_{i}")
        
        # Recarga con estructura correcta
        uploaded_file.seek(0)
        df_data = pd.read_excel(uploaded_file, sheet_name=0, header=10)
        
        if len(df_data.columns) <= len(new_columns):
            df_data.columns = new_columns[:len(df_data.columns)]
        
        # Limpieza de datos
        df_data = df_data.dropna(how='all')
        if 'NOMBRE' in df_data.columns:
            df_data = df_data[df_data['NOMBRE'].notna()]
            df_data = df_data[df_data['NOMBRE'].astype(str).str.strip() != '']
            df_data['NOMBRE'] = df_data['NOMBRE'].astype(str).str.strip()
        
        return df_data, list(competencias_dict.values()), None
        
    except Exception as e:
        return None, None, f"Error en el procesamiento: {str(e)}"

def generar_reporte_html(df_plot, promedio_org, total_empleados, total_competencias):
    """Genera un reporte HTML completo con todos los análisis"""
    
    # Obtener datos para el reporte
    mejor_competencia = df_plot.mean().idxmax()
    mejor_valor = df_plot.mean().max()
    peor_competencia = df_plot.mean().idxmin()
    peor_valor = df_plot.mean().min()
    
    # Top 10 empleados
    top_10 = df_plot.mean(axis=1).sort_values(ascending=False).head(10)
    bottom_10 = df_plot.mean(axis=1).sort_values(ascending=True).head(10)
    
    # Generar gráficos en HTML
    fig_dist = plot_distribution_histogram(df_plot.mean(axis=1))
    html_dist = pio.to_html(fig_dist, include_plotlyjs='cdn', config={'displayModeBar': False})
    
    fig_top = plot_top_performers(df_plot, n=10, mode='top')
    html_top = pio.to_html(fig_top, include_plotlyjs=False, config={'displayModeBar': False})
    
    fig_bottom = plot_top_performers(df_plot, n=10, mode='bottom')
    html_bottom = pio.to_html(fig_bottom, include_plotlyjs=False, config={'displayModeBar': False})
    
    fig_heatmap = plot_heatmap(df_plot)
    html_heatmap = pio.to_html(fig_heatmap, include_plotlyjs=False, config={'displayModeBar': False})
    
    # Estadísticas por competencia
    stats_comp = pd.DataFrame({
        'Promedio': df_plot.mean(),
        'Máximo': df_plot.max(),
        'Mínimo': df_plot.min(),
        'Desv. Est.': df_plot.std()
    }).sort_values('Promedio', ascending=False)
    
    tabla_stats = stats_comp.to_html(
        classes='table-stats',
        float_format=lambda x: f'{x:.1f}',
        border=0
    )
    
    # Crear HTML completo
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Competencias - ITKAP Intelligence Suite</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #F8FAFC;
                color: #0E1B2E;
                line-height: 1.6;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{
                text-align: center;
                border-bottom: 3px solid #F27200;
                padding-bottom: 30px;
                margin-bottom: 40px;
            }}
            
            .header h1 {{
                color: #0E1B2E;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }}
            
            .header .logo {{
                color: #F27200;
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}
            
            .header .subtitle {{
                color: #64748B;
                font-size: 1rem;
            }}
            
            .meta-info {{
                background-color: #F8FAFC;
                padding: 15px 20px;
                border-radius: 8px;
                margin-bottom: 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .meta-info .date {{
                color: #64748B;
                font-size: 0.9rem;
            }}
            
            .kpi-section {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .kpi-card {{
                background: linear-gradient(135deg, #0E1B2E 0%, #1a2942 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            }}
            
            .kpi-card .label {{
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                opacity: 0.8;
                margin-bottom: 10px;
            }}
            
            .kpi-card .value {{
                font-size: 2rem;
                font-weight: 700;
                color: #F27200;
            }}
            
            .section {{
                margin-bottom: 50px;
            }}
            
            .section-title {{
                font-size: 1.75rem;
                color: #0E1B2E;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #E2E8F0;
            }}
            
            .section-subtitle {{
                color: #64748B;
                font-size: 1rem;
                margin-bottom: 25px;
            }}
            
            .two-column {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            
            .chart-container {{
                background-color: #F8FAFC;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }}
            
            .table-stats {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            .table-stats th {{
                background-color: #0E1B2E;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                font-size: 0.9rem;
            }}
            
            .table-stats td {{
                padding: 10px 12px;
                border-bottom: 1px solid #E2E8F0;
                font-size: 0.9rem;
            }}
            
            .table-stats tr:hover {{
                background-color: #F8FAFC;
            }}
            
            .insight-box {{
                background-color: #FFF7ED;
                border-left: 4px solid #F27200;
                padding: 20px;
                border-radius: 8px;
                margin: 30px 0;
            }}
            
            .insight-box h4 {{
                color: #F27200;
                margin-bottom: 10px;
            }}
            
            .insight-box p {{
                color: #64748B;
                line-height: 1.8;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 60px;
                padding-top: 30px;
                border-top: 2px solid #E2E8F0;
                color: #64748B;
                font-size: 0.9rem;
            }}
            
            @media print {{
                body {{
                    padding: 0;
                }}
                .container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">ITKAP</div>
                <h1>Reporte de Competencias Organizacional</h1>
                <div class="subtitle">Intelligence Suite - Análisis Integral de Talento</div>
            </div>
            
            <div class="meta-info">
                <div class="date">📅 Fecha de generación: {fecha_actual}</div>
                <div class="date">📊 Reporte versión 2.5</div>
            </div>
            
            <div class="kpi-section">
                <div class="kpi-card">
                    <div class="label">Total Empleados</div>
                    <div class="value">{total_empleados}</div>
                </div>
                <div class="kpi-card">
                    <div class="label">Promedio General</div>
                    <div class="value">{promedio_org:.1f}%</div>
                </div>
                <div class="kpi-card">
                    <div class="label">Competencias</div>
                    <div class="value">{total_competencias}</div>
                </div>
                <div class="kpi-card">
                    <div class="label">Mejor Competencia</div>
                    <div class="value">{mejor_valor:.1f}%</div>
                </div>
            </div>
            
            <div class="insight-box">
                <h4>📊 Resumen Ejecutivo</h4>
                <p>
                    La evaluación organizacional muestra un promedio general de <strong>{promedio_org:.1f}%</strong> 
                    en las competencias evaluadas. La competencia con mejor desempeño es 
                    <strong>{mejor_competencia}</strong> ({mejor_valor:.1f}%), mientras que 
                    <strong>{peor_competencia}</strong> ({peor_valor:.1f}%) representa la mayor oportunidad de desarrollo.
                </p>
            </div>
            
            <div class="section">
                <h2 class="section-title">1. Distribución del Desempeño</h2>
                <p class="section-subtitle">Visualización de cómo se distribuyen los promedios de los colaboradores</p>
                <div class="chart-container">
                    {html_dist}
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">2. Rankings de Desempeño</h2>
                <p class="section-subtitle">Identificación de alto desempeño y oportunidades de desarrollo</p>
                <div class="two-column">
                    <div class="chart-container">
                        {html_top}
                    </div>
                    <div class="chart-container">
                        {html_bottom}
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">3. Matriz de Competencias Organizacional</h2>
                <p class="section-subtitle">Vista integral de todas las competencias por colaborador</p>
                <div class="chart-container">
                    {html_heatmap}
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">4. Estadísticas por Competencia</h2>
                <p class="section-subtitle">Análisis detallado del desempeño en cada competencia evaluada</p>
                {tabla_stats}
            </div>
            
            <div class="insight-box">
                <h4>💡 Recomendaciones Estratégicas</h4>
                <p>
                    1. <strong>Fortalezas Organizacionales:</strong> Capitalizar el alto desempeño en {mejor_competencia} 
                    como referencia para programas de mentoría interna.<br><br>
                    2. <strong>Áreas de Oportunidad:</strong> Implementar programas de desarrollo enfocados en 
                    {peor_competencia} para elevar el promedio organizacional.<br><br>
                    3. <strong>Gestión del Talento:</strong> Diseñar planes de carrera personalizados para los 
                    colaboradores del Top 10 para retención de talento clave.
                </p>
            </div>
            
            <div class="footer">
                <p><strong>ITKAP Consulting</strong> - Sistema de Inteligencia para la Gestión del Talento</p>
                <p>Este reporte fue generado automáticamente por ITKAP Intelligence Suite v2.5</p>
                <p>© 2025 ITKAP Consulting - Todos los derechos reservados</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def plot_radar_chart(df, empleado, promedio_gral):
    """Gráfico radar comparativo de competencias"""
    datos_emp = df.loc[empleado]
    categorias = df.columns.tolist()
    
    valores_emp = datos_emp.values.tolist() + [datos_emp.values[0]]
    valores_prom = promedio_gral.values.tolist() + [promedio_gral.values[0]]
    categorias_plot = categorias + [categorias[0]]

    fig = go.Figure()
    
    # Promedio organizacional
    fig.add_trace(go.Scatterpolar(
        r=valores_prom,
        theta=categorias_plot,
        fill='toself',
        name='Promedio Organizacional',
        line=dict(color=COLOR_NAVY, width=2, dash='dot'),
        fillcolor='rgba(14, 27, 46, 0.08)',
        hovertemplate='<b>Promedio Org.</b><br>%{theta}<br>%{r:.1f}%<extra></extra>'
    ))
    
    # Empleado seleccionado
    fig.add_trace(go.Scatterpolar(
        r=valores_emp,
        theta=categorias_plot,
        fill='toself',
        name=empleado,
        line=dict(color=COLOR_ORANGE, width=3),
        fillcolor='rgba(242, 114, 0, 0.15)',
        hovertemplate=f'<b>{empleado}</b><br>%{{theta}}<br>%{{r:.1f}}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(0,0,0,0.1)'
            )
        ),
        showlegend=True,
        margin=dict(t=40, b=40, l=80, r=80),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_competency_comparison(df, empleado, promedio_gral):
    """Gráfico de barras comparativo por competencia (empleado vs organización)"""
    datos_emp = df.loc[empleado]
    categorias = datos_emp.index.tolist()
    
    fig = go.Figure()
    
    # Barras del empleado (Navy)
    fig.add_trace(go.Bar(
        x=categorias,
        y=datos_emp.values,
        name=empleado,
        marker_color=COLOR_NAVY,
        text=datos_emp.values.round(1),
        textposition='outside',
        textfont=dict(size=10, color=COLOR_NAVY),
        hovertemplate='<b>%{x}</b><br>' + empleado + ': %{y:.1f}%<extra></extra>'
    ))
    
    # Barras del promedio organizacional (Rosa/Magenta)
    fig.add_trace(go.Bar(
        x=categorias,
        y=promedio_gral.values,
        name='Promedio Organizacional',
        marker_color='#E91E63',  # Rosa/magenta
        text=promedio_gral.values.round(1),
        textposition='outside',
        textfont=dict(size=10, color='#E91E63'),
        hovertemplate='<b>%{x}</b><br>Promedio Org.: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='group',
        height=450,
        margin=dict(l=50, r=30, t=40, b=120),
        xaxis=dict(
            tickangle=45,
            gridcolor='rgba(0,0,0,0.1)',
            title=""
        ),
        yaxis=dict(
            range=[0, 105],
            gridcolor='rgba(0,0,0,0.1)',
            title="Nivel (%)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_gap_analysis(df, empleado, promedio_gral):
    """Análisis de brechas vs promedio organizacional"""
    datos_emp = df.loc[empleado]
    diferencia = datos_emp - promedio_gral
    
    df_gap = pd.DataFrame({
        'Competencia': datos_emp.index,
        'Brecha': diferencia.values,
        'Real': datos_emp.values
    }).sort_values('Brecha')
    
    colores = [COLOR_DANGER if x < 0 else COLOR_SUCCESS for x in df_gap['Brecha']]
    
    fig = go.Figure(go.Bar(
        y=df_gap['Competencia'],
        x=df_gap['Brecha'],
        orientation='h',
        marker_color=colores,
        text=df_gap['Brecha'].apply(lambda x: f"{x:+.1f}%"),
        textposition='outside',
        customdata=df_gap['Real'],
        hovertemplate='<b>%{y}</b><br>Desviación: %{x:+.1f}%<br>Puntaje: %{customdata:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Análisis de Brechas",
            font=dict(color=COLOR_NAVY, size=16, family='Inter')
        ),
        xaxis_title="Desviación del Promedio (%)",
        height=max(450, len(df_gap)*40),
        margin=dict(l=20, r=60, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)', zerolinecolor='rgba(0,0,0,0.2)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    return fig

def plot_top_performers(df, n=5, mode='top'):
    """Ranking de mejores y menores desempeños"""
    promedios = df.mean(axis=1).sort_values(ascending=(mode=='top'))
    data = promedios.tail(n) if mode == 'top' else promedios.head(n)
    color = COLOR_ORANGE if mode == 'top' else COLOR_DANGER
    titulo = f"Top {n} Mejor Desempeño" if mode == 'top' else f"Top {n} Requiere Atención"
    
    fig = go.Figure(go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        marker_color=color,
        text=data.values.round(1),
        textposition='inside',
        textfont=dict(size=12, color='white', family='Inter', weight='bold'),
        hovertemplate='<b>%{y}</b><br>Promedio: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(color=COLOR_NAVY, size=16, family='Inter')
        ),
        height=max(350, n*45),
        margin=dict(l=20, r=40, t=60, b=40),
        xaxis=dict(
            range=[0, 105],
            gridcolor='rgba(0,0,0,0.1)',
            title=""
        ),
        yaxis=dict(title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_heatmap(df):
    """Matriz de calor organizacional completa"""
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
        colorscale=[
            [0, COLOR_DANGER],
            [0.5, COLOR_WARNING],
            [1, COLOR_SUCCESS]
        ],
        zmin=50,
        zmax=100,
        text=df.values.round(1),
        texttemplate='%{text}',
        textfont=dict(size=10, color='white', family='Inter', weight='bold'),
        hovertemplate='<b>%{y}</b><br>%{x}<br><b>Nivel:</b> %{z:.1f}%<extra></extra>',
        colorbar=dict(
            title="Nivel (%)",
            tickvals=[50, 65, 80, 100],
            ticktext=['50', '65', '80', '100']
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="Matriz de Competencias Organizacional",
            font=dict(color=COLOR_NAVY, size=16, family='Inter')
        ),
        height=max(600, len(df)*30),
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis=dict(tickangle=45),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_distribution_histogram(promedios):
    """Histograma de distribución de desempeño"""
    fig = go.Figure(data=[go.Histogram(
        x=promedios,
        marker_color=COLOR_NAVY,
        nbinsx=15,
        hovertemplate='Rango: %{x:.1f}%<br>Empleados: %{y}<extra></extra>',
        opacity=0.8
    )])
    
    fig.update_layout(
        title=dict(
            text="Distribución de Desempeño",
            font=dict(color=COLOR_NAVY, size=16, family='Inter')
        ),
        xaxis_title="Promedio General (%)",
        yaxis_title="Número de Empleados",
        height=400,
        margin=dict(l=50, r=30, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - NAVEGACIÓN
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo corporativo
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='color: {COLOR_ORANGE}; font-size: 2rem; font-weight: 700; margin: 0;'>ITKAP</h1>
            <p style='color: {COLOR_GRAY_LIGHT}; font-size: 0.875rem; margin: 0.25rem 0 0 0;'>Intelligence Suite</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Menú de navegación
    selected = option_menu(
        menu_title=None,
        options=[
            "Inicio",
            "Dashboard General",
            "Análisis Individual",
            "Rankings",
            "Matriz de Calor",
            "Reporte General"
        ],
        icons=[
            "house-fill",
            "graph-up",
            "person-circle",
            "trophy-fill",
            "grid-3x3-gap-fill",
            "file-earmark-text-fill"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent"
            },
            "icon": {
                "color": COLOR_WHITE,
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "12px 16px",
                "color": COLOR_WHITE,
                "border-radius": "8px",
                "font-weight": "500"
            },
            "nav-link-selected": {
                "background-color": COLOR_ORANGE,
                "color": COLOR_WHITE,
                "font-weight": "600"
            },
        }
    )
    
    # Estado del sistema
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.data is not None:
        st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem;'>
                <span style='color: {COLOR_SUCCESS}; font-size: 1.5rem;'>●</span>
                <p style='color: {COLOR_WHITE}; font-size: 0.875rem; margin: 0.25rem 0 0 0;'>Sistema Activo</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem;'>
                <span style='color: {COLOR_GRAY_LIGHT}; font-size: 1.5rem;'>●</span>
                <p style='color: {COLOR_GRAY_LIGHT}; font-size: 0.875rem; margin: 0.25rem 0 0 0;'>Sin datos cargados</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2025 ITKAP Consulting • v2.5")

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: INICIO / CARGA DE DATOS
# ═══════════════════════════════════════════════════════════════════════════

if selected == "Inicio":
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: {COLOR_NAVY}; font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;'>
                ITKAP Intelligence Suite
            </h1>
            <p style='color: {COLOR_GRAY_TEXT}; font-size: 1.25rem; margin: 0;'>
                Sistema Profesional de Análisis de Competencias
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tarjeta de instrucciones
    st.markdown(f"""
        <div class='info-card'>
            <div class='info-card-header'>
                📋 Instrucciones de Uso
            </div>
            <div class='info-card-content'>
                <ol style='margin: 0; padding-left: 1.5rem;'>
                    <li style='margin-bottom: 0.5rem;'>Carga tu archivo Excel de evaluación de competencias</li>
                    <li style='margin-bottom: 0.5rem;'>El sistema procesará automáticamente los datos</li>
                    <li style='margin-bottom: 0.5rem;'>Navega por las diferentes secciones usando el menú lateral</li>
                    <li>Visualiza dashboards, análisis individuales y reportes estratégicos</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Widget de carga
    uploaded_file = st.file_uploader(
        "Selecciona tu archivo",
        type=['xlsx', 'xlsm'],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner('🔄 Procesando datos...'):
            df, cols_rend, error = cargar_datos(uploaded_file)
            
            if error:
                st.error(f"❌ **Error:** {error}")
                st.info("💡 Verifica que el archivo tenga el formato correcto de PsycoSource.")
            else:
                st.session_state.data = df
                st.session_state.cols_rend = cols_rend
                
                st.success("✅ **Archivo procesado exitosamente**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Registros", f"{len(df)}")
                with col2:
                    st.metric("Competencias", f"{len(cols_rend)}")
                with col3:
                    st.metric("Columnas", f"{len(df.columns)}")
                
                st.info("👈 **Siguiente paso:** Selecciona 'Dashboard General' en el menú lateral")

# ═══════════════════════════════════════════════════════════════════════════
# VALIDACIÓN: BLOQUEO SI NO HAY DATOS
# ═══════════════════════════════════════════════════════════════════════════

if selected != "Inicio" and st.session_state.data is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='text-align: center; padding: 3rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>⚠️</div>
            <h2 style='color: {COLOR_NAVY};'>No hay datos disponibles</h2>
            <p style='color: {COLOR_GRAY_TEXT}; font-size: 1.1rem;'>
                Por favor, dirígete a <strong>Inicio</strong> y carga un archivo Excel para comenzar.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# PREPARACIÓN DE DATOS PARA VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════

if st.session_state.data is not None:
    df = st.session_state.data
    cols = st.session_state.cols_rend
    
    # DataFrame optimizado para gráficos
    df_plot = df[['NOMBRE'] + cols].copy()
    df_plot.columns = [c.split(' - ')[0].strip() for c in df_plot.columns]
    df_plot.set_index('NOMBRE', inplace=True)
    df_plot = df_plot.apply(pd.to_numeric, errors='coerce')

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: DASHBOARD GENERAL
# ═══════════════════════════════════════════════════════════════════════════

    if selected == "Dashboard General":
        # KPIs principales - CALCULAR PRIMERO
        promedio_org = df_plot.mean().mean()
        total_empleados = len(df_plot)
        total_competencias = len(df_plot.columns)
        mejor_competencia = df_plot.mean().idxmax()
        mejor_valor = df_plot.mean().max()
        
        # Header con botón de descarga
        col_title, col_button = st.columns([3, 1])
        with col_title:
            st.title("Dashboard Organizacional")
            st.markdown(f"<p style='color: {COLOR_GRAY_TEXT}; font-size: 1rem;'>Vista panorámica del desempeño de competencias</p>", unsafe_allow_html=True)
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)
            # Generar reporte HTML (ahora las variables ya existen)
            html_reporte = generar_reporte_html(df_plot, promedio_org, total_empleados, total_competencias)
            st.download_button(
                label="📄 Descargar Reporte",
                data=html_reporte,
                file_name=f"Reporte_Competencias_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Empleados",
                f"{total_empleados}",
                help="Número total de colaboradores evaluados"
            )
        
        with col2:
            st.metric(
                "Promedio General",
                f"{promedio_org:.1f}%",
                help="Promedio organizacional de todas las competencias"
            )
        
        with col3:
            st.metric(
                "Competencias",
                f"{total_competencias}",
                help="Número de competencias evaluadas"
            )
        
        with col4:
            st.metric(
                "Mejor Competencia",
                f"{mejor_valor:.1f}%",
                delta=mejor_competencia,
                help="Competencia con mejor desempeño promedio"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Distribución de desempeño
        st.markdown(f"<h3 style='color: {COLOR_NAVY};'>Distribución del Desempeño</h3>", unsafe_allow_html=True)
        st.caption("Visualización de cómo se distribuyen los promedios de los colaboradores")
        
        promedios_emp = df_plot.mean(axis=1)
        fig_dist = plot_distribution_histogram(promedios_emp)
        st.plotly_chart(fig_dist, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top performers resumido
        col_top, col_bottom = st.columns(2)
        
        with col_top:
            st.markdown(f"<h3 style='color: {COLOR_NAVY};'>🏆 Top Desempeño</h3>", unsafe_allow_html=True)
            st.plotly_chart(plot_top_performers(df_plot, n=5, mode='top'), use_container_width=True)
        
        with col_bottom:
            st.markdown(f"<h3 style='color: {COLOR_NAVY};'>⚠️ Requiere Atención</h3>", unsafe_allow_html=True)
            st.plotly_chart(plot_top_performers(df_plot, n=5, mode='bottom'), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: ANÁLISIS INDIVIDUAL
# ═══════════════════════════════════════════════════════════════════════════

    elif selected == "Análisis Individual":
        # Selector de empleado (primero para obtener el nombre)
        col_select, col_spacer = st.columns([2, 3])
        with col_select:
            empleado = st.selectbox(
                "Seleccionar Colaborador",
                options=df_plot.index.sort_values(),
                help="Elige un empleado para ver su análisis detallado"
            )
        
        # Título con nombre del colaborador
        st.title(f"Análisis Individual de Colaborador: {empleado}")
        st.markdown(f"<p style='color: {COLOR_GRAY_TEXT}; font-size: 1rem;'>Perfil detallado de competencias y brechas de desarrollo</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Métricas del empleado
        promedio_emp = df_plot.loc[empleado].mean()
        promedio_org = df_plot.mean().mean()
        diferencia = promedio_emp - promedio_org
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Promedio Individual",
                f"{promedio_emp:.1f}%",
                help="Promedio del colaborador en todas las competencias"
            )
        
        with col2:
            st.metric(
                "vs Organización",
                f"{diferencia:+.1f}%",
                delta=f"{diferencia:+.1f}%",
                help="Diferencia respecto al promedio organizacional"
            )
        
        with col3:
            mejor_comp = df_plot.loc[empleado].idxmax()
            mejor_val = df_plot.loc[empleado].max()
            st.metric(
                "Fortaleza Principal",
                mejor_comp,
                delta=f"{mejor_val:.1f}%",
                help="Competencia con mejor calificación"
            )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Gráfico de barras comparativo
        st.markdown(f"<h4 style='color: {COLOR_NAVY};'>Comparativa por Competencia</h4>", unsafe_allow_html=True)
        fig_comparison = plot_competency_comparison(df_plot, empleado, df_plot.mean())
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabla de resultados
        st.markdown(f"<h4 style='color: {COLOR_NAVY};'>Detalle de Competencias</h4>", unsafe_allow_html=True)
        
        tabla_empleado = df_plot.loc[empleado].to_frame(name="Puntaje (%)")
        tabla_empleado['Promedio Org.'] = df_plot.mean()
        tabla_empleado['Diferencia'] = tabla_empleado['Puntaje (%)'] - tabla_empleado['Promedio Org.']
        
        st.dataframe(
            tabla_empleado.style.background_gradient(
                subset=['Puntaje (%)'],
                cmap='RdYlGn',
                vmin=50,
                vmax=100
            ).format({
                'Puntaje (%)': '{:.1f}',
                'Promedio Org.': '{:.1f}',
                'Diferencia': '{:+.1f}'
            }),
            use_container_width=True,
            height=400
        )

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: RANKINGS
# ═══════════════════════════════════════════════════════════════════════════

    elif selected == "Rankings":
        st.title("Rankings de Desempeño")
        st.markdown(f"<p style='color: {COLOR_GRAY_TEXT}; font-size: 1rem;'>Identificación de alto desempeño y oportunidades de desarrollo</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Control de cantidad
        n_val = st.slider(
            "Número de colaboradores a mostrar",
            min_value=3,
            max_value=20,
            value=8,
            help="Ajusta cuántos empleados deseas visualizar en cada ranking"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Rankings comparativos
        col_top, col_bot = st.columns(2)
        
        with col_top:
            st.plotly_chart(
                plot_top_performers(df_plot, n=n_val, mode='top'),
                use_container_width=True
            )
        
        with col_bot:
            st.plotly_chart(
                plot_top_performers(df_plot, n=n_val, mode='bottom'),
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabla completa de rankings
        st.markdown(f"<h4 style='color: {COLOR_NAVY};'>Ranking Completo</h4>", unsafe_allow_html=True)
        
        ranking_completo = df_plot.mean(axis=1).sort_values(ascending=False).to_frame(name='Promedio (%)')
        ranking_completo['Posición'] = range(1, len(ranking_completo) + 1)
        ranking_completo = ranking_completo[['Posición', 'Promedio (%)']]
        
        st.dataframe(
            ranking_completo.style.background_gradient(
                subset=['Promedio (%)'],
                cmap='RdYlGn',
                vmin=50,
                vmax=100
            ).format({'Promedio (%)': '{:.1f}'}),
            use_container_width=True,
            height=500
        )

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: MATRIZ DE CALOR
# ═══════════════════════════════════════════════════════════════════════════

    elif selected == "Matriz de Calor":
        st.title("Matriz de Competencias Organizacional")
        st.markdown(f"<p style='color: {COLOR_GRAY_TEXT}; font-size: 1rem;'>Vista integral de todas las competencias por colaborador</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Información contextual
        st.info("💡 **Tip:** Los colores indican el nivel de desempeño - verde (alto), amarillo (medio), rojo (bajo)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Matriz completa
        fig_heatmap = plot_heatmap(df_plot)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Estadísticas por competencia
        st.markdown(f"<h4 style='color: {COLOR_NAVY};'>Estadísticas por Competencia</h4>", unsafe_allow_html=True)
        
        stats_comp = pd.DataFrame({
            'Promedio': df_plot.mean(),
            'Máximo': df_plot.max(),
            'Mínimo': df_plot.min(),
            'Desv. Est.': df_plot.std()
        }).sort_values('Promedio', ascending=False)
        
        st.dataframe(
            stats_comp.style.background_gradient(
                subset=['Promedio'],
                cmap='RdYlGn',
                vmin=50,
                vmax=100
            ).format({
                'Promedio': '{:.1f}',
                'Máximo': '{:.1f}',
                'Mínimo': '{:.1f}',
                'Desv. Est.': '{:.1f}'
            }),
            use_container_width=True,
            height=400
        )

# ═══════════════════════════════════════════════════════════════════════════
# PANTALLA: REPORTE GENERAL
# ═══════════════════════════════════════════════════════════════════════════

    elif selected == "Reporte General":
        st.title("Reporte General de Competencias")
        st.markdown(f"<p style='color: {COLOR_GRAY_TEXT}; font-size: 1rem;'>Genera un reporte ejecutivo completo en formato HTML</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Información del reporte
        st.markdown(f"""
            <div class='info-card'>
                <div class='info-card-header'>
                    📋 Contenido del Reporte
                </div>
                <div class='info-card-content'>
                    El reporte ejecutivo incluye:
                    <ul style='margin: 1rem 0 0 1.5rem; color: {COLOR_GRAY_TEXT};'>
                        <li style='margin-bottom: 0.5rem;'><strong>KPIs Organizacionales:</strong> Métricas clave de desempeño</li>
                        <li style='margin-bottom: 0.5rem;'><strong>Distribución de Desempeño:</strong> Histograma con análisis estadístico</li>
                        <li style='margin-bottom: 0.5rem;'><strong>Rankings:</strong> Top 10 mejores y áreas de oportunidad</li>
                        <li style='margin-bottom: 0.5rem;'><strong>Matriz de Calor:</strong> Vista completa de todas las competencias</li>
                        <li style='margin-bottom: 0.5rem;'><strong>Estadísticas Detalladas:</strong> Por cada competencia evaluada</li>
                        <li><strong>Recomendaciones Estratégicas:</strong> Insights accionables</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botones de acción
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            # Generar y descargar reporte
            html_reporte = generar_reporte_html(
                df_plot,
                df_plot.mean().mean(),
                len(df_plot),
                len(df_plot.columns)
            )
            
            st.download_button(
                label="📥 Descargar Reporte Ejecutivo",
                data=html_reporte,
                file_name=f"Reporte_Ejecutivo_ITKAP_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                use_container_width=True,
                type="primary"
            )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Preview del reporte
        st.markdown(f"<h3 style='color: {COLOR_NAVY};'>Vista Previa</h3>", unsafe_allow_html=True)
        st.info("💡 El reporte se descargará como archivo HTML que podrás abrir en cualquier navegador. También es compatible con conversión a PDF.")
        
        # Mostrar resumen ejecutivo
        promedio_org = df_plot.mean().mean()
        mejor_competencia = df_plot.mean().idxmax()
        mejor_valor = df_plot.mean().max()
        peor_competencia = df_plot.mean().idxmin()
        peor_valor = df_plot.mean().min()
        
        st.markdown(f"""
            <div class='info-card'>
                <div class='info-card-header'>
                    📊 Resumen Ejecutivo
                </div>
                <div class='info-card-content' style='line-height: 1.8;'>
                    La evaluación organizacional muestra un promedio general de <strong>{promedio_org:.1f}%</strong> 
                    en las competencias evaluadas. La competencia con mejor desempeño es 
                    <strong>{mejor_competencia}</strong> ({mejor_valor:.1f}%), mientras que 
                    <strong>{peor_competencia}</strong> ({peor_valor:.1f}%) representa la mayor oportunidad de desarrollo.
                    <br><br>
                    <strong>Total de colaboradores evaluados:</strong> {len(df_plot)}<br>
                    <strong>Competencias analizadas:</strong> {len(df_plot.columns)}
                </div>
            </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# FIN DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════════
