"""
ITKAP Intelligence Suite - Sistema Configurable de Análisis de Competencias HR
Versión: 2.0 - Con Panel de Configuración y Exportación Múltiple
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import io
import base64
from pathlib import Path
import zipfile
from pptx_generator import generar_presentacion

# Configuración de la página
st.set_page_config(
    page_title="ITKAP Intelligence Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stDownloadButton button {
        background-color: #10b981;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES AUXILIARES ====================

def load_configuration():
    """Carga la configuración guardada o retorna valores por defecto"""
    default_config = {
        "orden_heatmap": "Promedio (mayor a menor)",
        "mostrar_valores_heatmap": True,
        "esquema_colores": "RdYlGn",
        "umbral_bajo": 3.0,
        "umbral_alto": 4.0,
        "graficos_incluir": {
            "heatmap": True,
            "top10": True,
            "distribucion": True,
            "barras_competencias": True,
            "radar": False
        },
        "formato_exportacion": ["PDF", "PowerPoint", "Excel", "Imágenes"],
        "nombre_empresa": "",
        "mostrar_promedios": True
    }
    
    if 'config' not in st.session_state:
        st.session_state.config = default_config
    
    return st.session_state.config

def save_configuration(config):
    """Guarda la configuración en session_state"""
    st.session_state.config = config
    st.success("✅ Configuración guardada correctamente")

def process_data(df, nombre_col='Nombre'):
    """Procesa los datos y calcula métricas"""
    # Identificar columnas de competencias (numéricas)
    competencias_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Crear DataFrame de competencias
    df_competencias = df[competencias_cols].copy()
    df_info = df[[nombre_col]].copy()
    
    # Calcular promedio por empleado
    df_info['Promedio'] = df_competencias.mean(axis=1)
    
    # Calcular estadísticas por competencia
    stats_competencias = pd.DataFrame({
        'Competencia': competencias_cols,
        'Promedio': df_competencias.mean().values,
        'Mediana': df_competencias.median().values,
        'Mínimo': df_competencias.min().values,
        'Máximo': df_competencias.max().values,
        'Desv_Std': df_competencias.std().values
    })
    
    return df_competencias, df_info, stats_competencias, competencias_cols

def detectar_grupos_competencias(competencias_nombres):
    """Detecta automáticamente grupos de competencias basados en nombres comunes"""
    # Intentar cargar configuración personalizada
    try:
        from config_grupos import GRUPOS_COMPETENCIAS
        grupos = GRUPOS_COMPETENCIAS
    except ImportError:
        # Usar configuración por defecto
        grupos = {
            'Operaciones Administrativas e Intelectuales': {
                'color': '#6495ED',  # Azul
                'keywords': ['Análisis', 'Aprendizaje', 'Control', 'Enfoque', 'Organización', 
                            'Perseverancia', 'Pensamiento', 'Planificación', 'Orientación',
                            'Estratégico', 'Resultados', 'Administrativo', 'Problemas']
            },
            'Orientadas a las Relaciones': {
                'color': '#DC143C',  # Rojo
                'keywords': ['Comunicación', 'Relación', 'Interacción', 'Trabajo en Equipo',
                            'Persuasión', 'Negociación', 'Colaboración', 'Influencia',
                            'Efectiva', 'Interpersonal']
            },
            'Orientadas a Sí Mismo': {
                'color': '#32CD32',  # Verde
                'keywords': ['Delegación', 'Liderazgo', 'Autocontrol', 'Iniciativa',
                            'Responsabilidad', 'Autonomía', 'Desarrollo', 'Personal']
            }
        }
    
    # Asignar cada competencia a un grupo
    competencias_grupos = {}
    for competencia in competencias_nombres:
        asignado = False
        for grupo_nombre, grupo_info in grupos.items():
            for keyword in grupo_info['keywords']:
                if keyword.lower() in competencia.lower():
                    competencias_grupos[competencia] = {
                        'grupo': grupo_nombre,
                        'color': grupo_info['color']
                    }
                    asignado = True
                    break
            if asignado:
                break
        
        # Si no se asignó, va al primer grupo por defecto
        if not asignado:
            primer_grupo = list(grupos.keys())[0]
            competencias_grupos[competencia] = {
                'grupo': primer_grupo,
                'color': grupos[primer_grupo]['color']
            }
    
    return competencias_grupos

def crear_heatmap(df_competencias, df_info, config):
    """Crea el mapa de calor ordenado según configuración con grupos de competencias"""
    # Combinar datos
    df_viz = df_info.copy()
    df_viz = pd.concat([df_viz, df_competencias], axis=1)
    
    # Ordenar según configuración
    orden = config.get("orden_heatmap", "Promedio (mayor a menor)")
    
    if orden == "Promedio (mayor a menor)":
        df_viz = df_viz.sort_values('Promedio', ascending=False)
    elif orden == "Promedio (menor a mayor)":
        df_viz = df_viz.sort_values('Promedio', ascending=True)
    elif orden == "Alfabético":
        df_viz = df_viz.sort_values('Nombre')
    
    # Preparar datos para heatmap
    nombres = df_viz['Nombre'].values
    promedios = df_viz['Promedio'].values
    competencias_data = df_viz.drop(['Nombre', 'Promedio'], axis=1).values
    competencias_nombres = df_viz.drop(['Nombre', 'Promedio'], axis=1).columns.tolist()
    
    # Detectar grupos de competencias
    grupos_comp = detectar_grupos_competencias(competencias_nombres)
    
    # Crear heatmap
    esquema = config.get("esquema_colores", "RdYlGn")
    
    fig = go.Figure(data=go.Heatmap(
        z=competencias_data,
        x=competencias_nombres,
        y=[f"{nombre} ({prom:.2f})" for nombre, prom in zip(nombres, promedios)],
        colorscale=esquema,
        text=competencias_data if config.get("mostrar_valores_heatmap", True) else None,
        texttemplate='%{text:.2f}' if config.get("mostrar_valores_heatmap", True) else None,
        textfont={"size": 10},
        colorbar=dict(title="Nivel", thickness=15)
    ))
    
    # Agregar colores de fondo para grupos en el eje X
    shapes = []
    annotations = []
    
    # Organizar competencias por grupo
    grupos_ordenados = {}
    for i, comp in enumerate(competencias_nombres):
        grupo_nombre = grupos_comp[comp]['grupo']
        if grupo_nombre not in grupos_ordenados:
            grupos_ordenados[grupo_nombre] = []
        grupos_ordenados[grupo_nombre].append((i, comp, grupos_comp[comp]['color']))
    
    # Agregar rectángulos y anotaciones para cada grupo
    y_pos = len(nombres) + 0.5
    for grupo_nombre, items in grupos_ordenados.items():
        if items:
            x_start = min([item[0] for item in items]) - 0.5
            x_end = max([item[0] for item in items]) + 0.5
            color = items[0][2]
            
            # Rectángulo de fondo
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="y",
                x0=x_start,
                y0=y_pos - 0.3,
                x1=x_end,
                y1=y_pos + 0.3,
                fillcolor=color,
                opacity=0.3,
                layer="below",
                line_width=0,
            ))
            
            # Anotación del nombre del grupo
            annotations.append(dict(
                x=(x_start + x_end) / 2,
                y=y_pos,
                text=grupo_nombre,
                showarrow=False,
                font=dict(size=9, color="black", family="Arial Black"),
                xanchor="center",
                yanchor="middle"
            ))
    
    fig.update_layout(
        title="Mapa de Calor de Competencias por Colaborador (Ordenado por Promedio)",
        xaxis_title="Competencias",
        yaxis_title="Colaboradores",
        height=max(650, len(nombres) * 30),
        font=dict(size=11),
        margin=dict(l=200, r=50, t=100, b=150),
        xaxis=dict(tickangle=-45),
        shapes=shapes,
        annotations=annotations
    )
    
    return fig

def crear_heatmap_promedios(df_competencias):
    """Crea un mapa de calor con solo el promedio de cada competencia"""
    # Calcular promedio por competencia
    promedios = df_competencias.mean().values
    competencias_nombres = df_competencias.columns.tolist()
    
    # Detectar grupos
    grupos_comp = detectar_grupos_competencias(competencias_nombres)
    
    # Crear heatmap de una sola fila
    fig = go.Figure(data=go.Heatmap(
        z=[promedios],
        x=competencias_nombres,
        y=['Promedio Organizacional'],
        colorscale='RdYlGn',
        text=[promedios],
        texttemplate='%{text:.2f}',
        textfont={"size": 12, "color": "black"},
        colorbar=dict(title="Nivel", thickness=15),
        zmin=1,
        zmax=5
    ))
    
    # Agregar colores de fondo para grupos
    shapes = []
    annotations = []
    
    grupos_ordenados = {}
    for i, comp in enumerate(competencias_nombres):
        grupo_nombre = grupos_comp[comp]['grupo']
        if grupo_nombre not in grupos_ordenados:
            grupos_ordenados[grupo_nombre] = []
        grupos_ordenados[grupo_nombre].append((i, comp, grupos_comp[comp]['color']))
    
    # Agregar rectángulos y anotaciones
    for grupo_nombre, items in grupos_ordenados.items():
        if items:
            x_start = min([item[0] for item in items]) - 0.5
            x_end = max([item[0] for item in items]) + 0.5
            color = items[0][2]
            
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=x_start,
                y0=1.02,
                x1=x_end,
                y1=1.15,
                fillcolor=color,
                opacity=0.4,
                layer="below",
                line_width=1,
            ))
            
            annotations.append(dict(
                x=(x_start + x_end) / 2,
                y=1.085,
                yref="paper",
                text=f"<b>{grupo_nombre}</b>",
                showarrow=False,
                font=dict(size=10, color="black"),
                xanchor="center"
            ))
    
    fig.update_layout(
        title="Mapa de Calor - Promedio Organizacional por Competencia",
        xaxis_title="Competencias",
        height=250,
        font=dict(size=11),
        margin=dict(l=150, r=50, t=120, b=150),
        xaxis=dict(tickangle=-45),
        shapes=shapes,
        annotations=annotations,
        yaxis=dict(showticklabels=True)
    )
    
    return fig

def crear_top10(df_info):
    """Crea gráfico de top 10 colaboradores"""
    top10 = df_info.nlargest(10, 'Promedio')
    
    fig = go.Figure(data=[
        go.Bar(
            x=top10['Promedio'],
            y=top10['Nombre'],
            orientation='h',
            marker=dict(
                color=top10['Promedio'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Promedio")
            ),
            text=top10['Promedio'].round(2),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Top 10 Colaboradores por Promedio de Competencias",
        xaxis_title="Promedio",
        yaxis_title="Colaborador",
        height=500,
        showlegend=False
    )
    
    return fig

def crear_barras_competencias(stats_competencias):
    """Crea gráfico de barras de competencias organizacionales (estilo imagen)"""
    # Ordenar por promedio descendente
    stats_ordenadas = stats_competencias.sort_values('Promedio', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(
            x=stats_ordenadas['Competencia'],
            y=stats_ordenadas['Promedio'],
            marker=dict(color='#e91e63'),  # Color rosa/magenta como en la imagen
            text=stats_ordenadas['Promedio'].round(1),
            textposition='outside',
            textfont=dict(size=12, color='black')
        )
    ])
    
    fig.update_layout(
        title="Análisis de Competencias Organizacionales",
        xaxis_title="",
        yaxis_title="Nivel (0-5)",
        height=500,
        showlegend=False,
        yaxis=dict(range=[0, 5]),
        xaxis=dict(tickangle=-45),
        font=dict(size=10),
        margin=dict(b=150)
    )
    
    return fig

def crear_distribucion(df_info, config):
    """Crea gráfico de distribución de promedios"""
    umbral_bajo = config.get("umbral_bajo", 3.0)
    umbral_alto = config.get("umbral_alto", 4.0)
    
    # Clasificar colaboradores
    df_info['Categoria'] = pd.cut(
        df_info['Promedio'],
        bins=[0, umbral_bajo, umbral_alto, 5],
        labels=['Bajo', 'Medio', 'Alto']
    )
    
    conteo = df_info['Categoria'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=conteo.index,
            y=conteo.values,
            marker=dict(
                color=['#ef4444', '#f59e0b', '#10b981'],
            ),
            text=conteo.values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Distribución de Colaboradores por Nivel de Desempeño",
        xaxis_title="Categoría",
        yaxis_title="Cantidad de Colaboradores",
        height=400,
        showlegend=False
    )
    
    return fig

def exportar_a_excel(df, df_competencias, df_info, stats_competencias, nombre_empresa):
    """Exporta datos a Excel con múltiples hojas"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Hoja 1: Datos completos
        df.to_excel(writer, sheet_name='Datos Completos', index=False)
        
        # Hoja 2: Competencias con promedios
        df_export = pd.concat([df_info, df_competencias], axis=1)
        df_export = df_export.sort_values('Promedio', ascending=False)
        df_export.to_excel(writer, sheet_name='Competencias Ordenadas', index=False)
        
        # Hoja 3: Estadísticas
        stats_competencias.to_excel(writer, sheet_name='Estadísticas', index=False)
        
        # Hoja 4: Resumen Ejecutivo
        resumen = pd.DataFrame({
            'Métrica': [
                'Total Colaboradores',
                'Total Competencias Evaluadas',
                'Promedio General',
                'Mejor Colaborador',
                'Peor Colaborador'
            ],
            'Valor': [
                len(df_info),
                len(stats_competencias),
                f"{df_info['Promedio'].mean():.2f}",
                df_info.loc[df_info['Promedio'].idxmax(), 'Nombre'],
                df_info.loc[df_info['Promedio'].idxmin(), 'Nombre']
            ]
        })
        resumen.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
    
    output.seek(0)
    return output

def crear_zip_imagenes(figuras_dict):
    """Crea un ZIP con todas las imágenes de los gráficos"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for nombre, fig in figuras_dict.items():
            # Convertir a PNG
            img_bytes = fig.to_image(format="png", width=1920, height=1080, scale=2)
            zip_file.writestr(f"{nombre}.png", img_bytes)
    
    zip_buffer.seek(0)
    return zip_buffer

# ==================== PANEL DE CONFIGURACIÓN ====================

def panel_configuracion():
    """Panel de configuración lateral"""
    st.sidebar.title("⚙️ Panel de Configuración")
    
    config = load_configuration()
    
    # Sección 1: Ordenamiento
    st.sidebar.subheader("📊 Visualización del Heatmap")
    orden = st.sidebar.selectbox(
        "Ordenar colaboradores por:",
        ["Promedio (mayor a menor)", "Promedio (menor a mayor)", "Alfabético"],
        index=["Promedio (mayor a menor)", "Promedio (menor a mayor)", "Alfabético"].index(
            config.get("orden_heatmap", "Promedio (mayor a menor)")
        )
    )
    config["orden_heatmap"] = orden
    
    mostrar_valores = st.sidebar.checkbox(
        "Mostrar valores en celdas",
        value=config.get("mostrar_valores_heatmap", True)
    )
    config["mostrar_valores_heatmap"] = mostrar_valores
    
    # Sección 2: Esquema de colores
    esquema_colores = st.sidebar.selectbox(
        "Esquema de colores:",
        ["RdYlGn", "Viridis", "Blues", "RdBu", "Spectral"],
        index=["RdYlGn", "Viridis", "Blues", "RdBu", "Spectral"].index(
            config.get("esquema_colores", "RdYlGn")
        )
    )
    config["esquema_colores"] = esquema_colores
    
    # Sección 3: Umbrales
    st.sidebar.subheader("🎯 Umbrales de Evaluación")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        umbral_bajo = st.number_input(
            "Bajo (<)",
            min_value=0.0,
            max_value=5.0,
            value=config.get("umbral_bajo", 3.0),
            step=0.1
        )
        config["umbral_bajo"] = umbral_bajo
    with col2:
        umbral_alto = st.number_input(
            "Alto (>)",
            min_value=0.0,
            max_value=5.0,
            value=config.get("umbral_alto", 4.0),
            step=0.1
        )
        config["umbral_alto"] = umbral_alto
    
    # Sección 4: Gráficos a incluir
    st.sidebar.subheader("📈 Gráficos a Incluir")
    graficos = config.get("graficos_incluir", {})
    graficos["heatmap"] = st.sidebar.checkbox("Mapa de Calor", value=True)
    graficos["top10"] = st.sidebar.checkbox("Top 10 Colaboradores", value=True)
    graficos["barras_competencias"] = st.sidebar.checkbox("Barras de Competencias", value=True)
    graficos["distribucion"] = st.sidebar.checkbox("Distribución", value=True)
    graficos["radar"] = st.sidebar.checkbox("Gráfico Radar", value=False)
    config["graficos_incluir"] = graficos
    
    # Sección 5: Personalización
    st.sidebar.subheader("🎨 Personalización")
    nombre_empresa = st.sidebar.text_input(
        "Nombre de la empresa:",
        value=config.get("nombre_empresa", ""),
        placeholder="Ej: Empresa ABC"
    )
    config["nombre_empresa"] = nombre_empresa
    
    # Guardar configuración
    if st.sidebar.button("💾 Guardar Configuración", use_container_width=True):
        save_configuration(config)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Configuración Actual")
    st.sidebar.json({
        "Orden": config["orden_heatmap"],
        "Colores": config["esquema_colores"],
        "Umbrales": f"{config['umbral_bajo']} - {config['umbral_alto']}"
    })
    
    return config

# ==================== APLICACIÓN PRINCIPAL ====================

def main():
    # Header
    st.markdown('<h1 class="main-header">ITKAP Intelligence Suite</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema Configurable de Análisis de Competencias HR v2.0</p>', unsafe_allow_html=True)
    
    # Panel de configuración
    config = panel_configuracion()
    
    # Upload de archivo
    st.markdown("### 📁 Cargar Datos")
    uploaded_file = st.file_uploader(
        "Sube tu archivo Excel con evaluaciones de competencias",
        type=['xlsx', 'xls'],
        help="El archivo debe contener una columna 'Nombre' y columnas numéricas con las competencias"
    )
    
    if uploaded_file:
        try:
            # Cargar datos
            df = pd.read_excel(uploaded_file)
            
            # Procesar datos
            df_competencias, df_info, stats_competencias, competencias_cols = process_data(df)
            
            # Métricas principales
            st.markdown("---")
            st.markdown("### 📊 Métricas Generales")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Colaboradores", len(df_info))
            with col2:
                st.metric("Competencias Evaluadas", len(competencias_cols))
            with col3:
                st.metric("Promedio General", f"{df_info['Promedio'].mean():.2f}")
            with col4:
                mejor = df_info.loc[df_info['Promedio'].idxmax(), 'Nombre']
                st.metric("Mejor Colaborador", mejor)
            
            # Crear visualizaciones según configuración
            figuras = {}
            
            st.markdown("---")
            st.markdown("### 📈 Visualizaciones")
            
            # Heatmap
            if config["graficos_incluir"].get("heatmap", True):
                st.markdown("#### Mapa de Calor de Competencias por Colaborador")
                fig_heatmap = crear_heatmap(df_competencias, df_info, config)
                st.plotly_chart(fig_heatmap, use_container_width=True)
                figuras["01_Mapa_de_Calor_Colaboradores"] = fig_heatmap
                
                # Mapa de calor de promedios organizacionales
                st.markdown("#### Mapa de Calor - Promedio Organizacional")
                fig_heatmap_prom = crear_heatmap_promedios(df_competencias)
                st.plotly_chart(fig_heatmap_prom, use_container_width=True)
                figuras["01b_Mapa_Calor_Promedios"] = fig_heatmap_prom
            
            col1, col2 = st.columns(2)
            
            # Top 10
            if config["graficos_incluir"].get("top10", True):
                with col1:
                    st.markdown("#### Top 10 Colaboradores")
                    fig_top10 = crear_top10(df_info)
                    st.plotly_chart(fig_top10, use_container_width=True)
                    figuras["02_Top_10_Colaboradores"] = fig_top10
            
            # Distribución
            if config["graficos_incluir"].get("distribucion", True):
                with col2:
                    st.markdown("#### Distribución por Nivel")
                    fig_dist = crear_distribucion(df_info, config)
                    st.plotly_chart(fig_dist, use_container_width=True)
                    figuras["03_Distribucion"] = fig_dist
            
            # Barras de Competencias
            if config["graficos_incluir"].get("barras_competencias", True):
                st.markdown("#### Análisis de Competencias Organizacionales")
                fig_barras = crear_barras_competencias(stats_competencias)
                st.plotly_chart(fig_barras, use_container_width=True)
                figuras["04_Competencias_Organizacionales"] = fig_barras
            
            # Sección de Exportación
            st.markdown("---")
            st.markdown("### 💾 Exportar Reportes")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Excel
            with col1:
                excel_data = exportar_a_excel(
                    df, df_competencias, df_info, stats_competencias,
                    config.get("nombre_empresa", "Empresa")
                )
                st.download_button(
                    label="📊 Descargar Excel",
                    data=excel_data,
                    file_name=f"Reporte_Competencias_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            # PowerPoint
            with col2:
                # Preparar estadísticas para PowerPoint
                stats_pptx = {
                    'total_colaboradores': len(df_info),
                    'total_competencias': len(competencias_cols),
                    'promedio_general': df_info['Promedio'].mean(),
                    'mejor_colaborador': df_info.loc[df_info['Promedio'].idxmax(), 'Nombre'],
                    'mejor_promedio': df_info['Promedio'].max(),
                    'nivel_alto': len(df_info[df_info['Promedio'] >= config.get('umbral_alto', 4.0)]),
                    'nivel_medio': len(df_info[(df_info['Promedio'] >= config.get('umbral_bajo', 3.0)) & (df_info['Promedio'] < config.get('umbral_alto', 4.0))]),
                    'nivel_bajo': len(df_info[df_info['Promedio'] < config.get('umbral_bajo', 3.0)]),
                    'porcentaje_alto': (len(df_info[df_info['Promedio'] >= config.get('umbral_alto', 4.0)]) / len(df_info)) * 100,
                    'porcentaje_medio': (len(df_info[(df_info['Promedio'] >= config.get('umbral_bajo', 3.0)) & (df_info['Promedio'] < config.get('umbral_alto', 4.0))]) / len(df_info)) * 100,
                    'porcentaje_bajo': (len(df_info[df_info['Promedio'] < config.get('umbral_bajo', 3.0)]) / len(df_info)) * 100
                }
                
                pptx_data = generar_presentacion(
                    figuras,
                    df_info,  # df_empleados
                    df_competencias,  # df_competencias
                    stats_pptx,  # stats
                    config  # config
                )
                
                st.download_button(
                    label="📽️ Descargar PowerPoint",
                    data=pptx_data,
                    file_name=f"Presentacion_Competencias_{datetime.now().strftime('%Y%m%d')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
            
            # ZIP de imágenes
            with col3:
                if figuras:
                    zip_data = crear_zip_imagenes(figuras)
                    st.download_button(
                        label="🖼️ Descargar Imágenes",
                        data=zip_data,
                        file_name=f"Graficos_{datetime.now().strftime('%Y%m%d')}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
            
            # Datos raw
            with col4:
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Descargar CSV",
                    data=csv_data,
                    file_name=f"Datos_Raw_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Tabla de datos
            st.markdown("---")
            st.markdown("### 📋 Vista de Datos")
            tab1, tab2 = st.tabs(["Datos Completos", "Estadísticas de Competencias"])
            
            with tab1:
                df_display = pd.concat([df_info, df_competencias], axis=1)
                df_display = df_display.sort_values('Promedio', ascending=False)
                st.dataframe(df_display, use_container_width=True, height=400)
            
            with tab2:
                st.dataframe(stats_competencias, use_container_width=True, height=400)
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            st.exception(e)
    else:
        # Instrucciones
        st.info("""
        ### 📖 Instrucciones de Uso
        
        1. **Sube tu archivo Excel** con las evaluaciones de competencias
        2. **Configura** los parámetros en el panel lateral
        3. **Visualiza** los gráficos generados automáticamente
        4. **Exporta** los reportes en múltiples formatos
        
        #### Formato del archivo:
        - Columna "Nombre" con los nombres de colaboradores
        - Columnas numéricas con cada competencia evaluada (escala 1-5)
        - Sin espacios en blanco o valores nulos
        """)

if __name__ == "__main__":
    main()
