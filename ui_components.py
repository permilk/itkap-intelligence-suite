"""
ITKAP Intelligence Suite - UI Components
Version: 3.0.4
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from config import CONFIG, COLORS

class UIComponents:
    def render_page_header(self, title: str, subtitle: str = None, icon: str = None):
        """Renderiza el encabezado de página"""
        if icon:
            st.markdown(f"<h1 style='text-align: center;'>{icon} {title}</h1>", unsafe_allow_html=True)
        else:
            st.title(title)
        
        if subtitle:
            st.markdown(f"<p style='text-align: center; color: {COLORS.GRAY_TEXT}; font-size: 1.1rem;'>{subtitle}</p>", unsafe_allow_html=True)
        st.markdown("---")

    def render_info_card(self, title: str, content: str, icon: str = "ℹ️", card_type: str = "default"):
        """Renderiza una tarjeta de información estilizada"""
        # Define colores según tipo
        border_color = COLORS.GRAY_LIGHT
        left_border = COLORS.SECONDARY
        if card_type == "success": left_border = COLORS.SUCCESS
        if card_type == "warning": left_border = COLORS.WARNING
        if card_type == "info": left_border = COLORS.INFO
        
        st.markdown(f"""
            <div style='
                background-color: white;
                padding: 1.25rem;
                border: 1px solid {border_color};
                border-left: 4px solid {left_border};
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                margin-bottom: 1rem;
            '>
                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.25rem; margin-right: 0.5rem;'>{icon}</span>
                    <h4 style='margin: 0; color: {COLORS.PRIMARY};'>{title}</h4>
                </div>
                <div style='color: {COLORS.GRAY_TEXT}; font-size: 0.95rem; line-height: 1.5;'>
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)

    def render_success_message(self, message: str):
        st.success(message)

    def render_error_message(self, message: str):
        st.error(message)
    
    def render_info_message(self, message: str):
        st.info(message)

    def render_empty_state(self, title: str, message: str, icon: str = "🔍"):
        st.markdown(f"""
            <div style='text-align: center; padding: 4rem 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>{icon}</div>
                <h3 style='color: {COLORS.PRIMARY};'>{title}</h3>
                <p style='color: {COLORS.GRAY_TEXT};'>{message}</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_divider(self):
        st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

class StatsDisplay:
    def render_kpi_row(self, metrics: List[Dict[str, Any]]):
        """Renderiza una fila de KPIs"""
        cols = st.columns(len(metrics))
        for idx, metric in enumerate(metrics):
            with cols[idx]:
                st.metric(
                    label=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta', None),
                    help=metric.get('help', None)
                )

class TableRenderer:
    def render_styled_dataframe(self, df: Any, use_gradient: bool = True, height: int = 400):
        """
        Fix BUG #1: Maneja correctamente objetos Styler para evitar AttributeError
        """
        # Si ya es un Styler, no llamamos a .style de nuevo
        if isinstance(df, pd.io.formats.style.Styler):
            st.dataframe(df, use_container_width=True, height=height)
        else:
            # Si es DataFrame puro, aplicamos estilo básico
            styler = df.style.format("{:.1f}")
            if use_gradient:
                styler = styler.background_gradient(cmap='RdYlGn', vmin=0, vmax=100)
            st.dataframe(styler, use_container_width=True, height=height)

    def render_comparison_table(self, emp_data, org_data, show_difference=True):
        """Renderiza tabla comparativa detallada"""
        df_comp = pd.DataFrame({
            'Colaborador': emp_data,
            'Promedio Org.': org_data
        })
        
        if show_difference:
            df_comp['Diferencia'] = df_comp['Colaborador'] - df_comp['Promedio Org.']
            
        st.dataframe(
            df_comp.style.background_gradient(subset=['Colaborador'], cmap='Blues', vmin=0, vmax=100)
                   .format("{:.1f}"),
            use_container_width=True
        )

class Navigation:
    def render_sidebar_header(self):
        st.markdown(f"""
            <div style='text-align: center; padding: 2rem 0 1rem 0;'>
                <h1 style='color: {COLORS.SECONDARY}; font-size: 2rem; font-weight: 800; margin: 0;'>ITKAP</h1>
                <p style='color: {COLORS.GRAY_LIGHT}; font-size: 0.9rem; margin: 0;'>Intelligence Suite v{CONFIG.APP_VERSION}</p>
            </div>
        """, unsafe_allow_html=True)

    def render_sidebar_footer(self, has_data: bool):
        st.markdown("---")
        status_color = COLORS.SUCCESS if has_data else COLORS.GRAY_LIGHT
        status_text = "Sistema Activo" if has_data else "Esperando datos"
        
        st.markdown(f"""
            <div style='display: flex; align-items: center; justify-content: center; gap: 8px;'>
                <div style='width: 10px; height: 10px; border-radius: 50%; background-color: {status_color};'></div>
                <span style='color: {COLORS.WHITE}; font-size: 0.85rem;'>{status_text}</span>
            </div>
            <div style='text-align: center; margin-top: 1rem;'>
                <small style='color: rgba(255,255,255,0.5);'>© 2025 ITKAP Consulting</small>
            </div>
        """, unsafe_allow_html=True)

class FileUploader:
    def render_upload_area(self):
        return st.file_uploader(
            "Cargar archivo Excel",
            type=['xlsx', 'xlsm'],
            label_visibility="collapsed"
        )

class ActionButton:
    def render_download_button(self, label, data, file_name, icon="📥", button_type="primary"):
        st.download_button(
            label=f"{icon} {label}",
            data=data,
            file_name=file_name,
            mime="text/html",
            use_container_width=True,
            type=button_type
        )

# Instancias
ui = UIComponents()
nav = Navigation()
uploader = FileUploader()
table = TableRenderer()
button = ActionButton()
stats = StatsDisplay()