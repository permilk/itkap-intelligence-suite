"""
ITKAP Intelligence Suite - Report Generator
Version: 3.0.3 (Fix: Empty sequence safety)
"""
import pandas as pd
import plotly.io as pio
import html
from typing import List, Any
from datetime import datetime
from config import CONFIG, COLORS
from charts import create_histogram, create_ranking_chart, create_heatmap

class HTMLReportGenerator:
    
    @staticmethod
    def sanitize_html(text: Any) -> str:
        if text is None:
            return ""
        return html.escape(str(text))

    def generate_executive_report(self, df_plot: pd.DataFrame, avg_score: float, 
                                total_emp: int, total_comp: int) -> str:
        
        # FIX: Validación de seguridad por si el DataFrame llega vacío
        if df_plot.empty or df_plot.shape[1] == 0:
            return "<html><body><h1>Error: No hay datos suficientes para generar el reporte.</h1></body></html>"

        # Preparar datos sanitizados
        best_comp_raw = df_plot.mean().idxmax()
        worst_comp_raw = df_plot.mean().idxmin()
        
        best_comp = self.sanitize_html(best_comp_raw)
        worst_comp = self.sanitize_html(worst_comp_raw)
        best_val = df_plot.mean().max()
        worst_val = df_plot.mean().min()
        
        # Generar gráficos HTML
        fig_dist = create_histogram(df_plot.mean(axis=1))
        html_dist = pio.to_html(fig_dist, include_plotlyjs='cdn', full_html=False, config={'displayModeBar': False})
        
        fig_top = create_ranking_chart(df_plot.mean(axis=1), n=10, mode='top')
        html_top = pio.to_html(fig_top, include_plotlyjs=False, full_html=False, config={'displayModeBar': False})
        
        fig_bottom = create_ranking_chart(df_plot.mean(axis=1), n=10, mode='bottom')
        html_bottom = pio.to_html(fig_bottom, include_plotlyjs=False, full_html=False, config={'displayModeBar': False})
        
        fig_heatmap = create_heatmap(df_plot)
        html_heatmap = pio.to_html(fig_heatmap, include_plotlyjs=False, full_html=False, config={'displayModeBar': False})
        
        # Tabla de estadísticas
        stats_comp = pd.DataFrame({
            'Promedio': df_plot.mean(),
            'Máximo': df_plot.max(),
            'Mínimo': df_plot.min()
        }).sort_values('Promedio', ascending=False)
        
        tabla_stats = stats_comp.to_html(classes='table-stats', float_format=lambda x: f'{x:.1f}', border=0, escape=True)
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Template HTML seguro
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte Ejecutivo - {CONFIG.APP_NAME}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                body {{ font-family: 'Inter', sans-serif; background-color: {COLORS.BACKGROUND}; color: {COLORS.PRIMARY}; padding: 40px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid {COLORS.SECONDARY}; padding-bottom: 30px; margin-bottom: 40px; }}
                h1 {{ color: {COLORS.PRIMARY}; }}
                .logo {{ color: {COLORS.SECONDARY}; font-size: 2rem; font-weight: bold; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }}
                .kpi-card {{ background: {COLORS.PRIMARY}; color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .kpi-val {{ font-size: 2rem; font-weight: bold; color: {COLORS.SECONDARY}; }}
                .chart-box {{ background: #F8FAFC; padding: 20px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #E2E8F0; }}
                .table-stats {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .table-stats th {{ background: {COLORS.PRIMARY}; color: white; padding: 12px; text-align: left; }}
                .table-stats td {{ padding: 10px; border-bottom: 1px solid #E2E8F0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">ITKAP</div>
                    <h1>Reporte Ejecutivo de Competencias</h1>
                    <p>{fecha_actual} • Versión 3.0</p>
                </div>
                
                <div class="kpi-grid">
                    <div class="kpi-card"><div>Empleados</div><div class="kpi-val">{total_emp}</div></div>
                    <div class="kpi-card"><div>Promedio Global</div><div class="kpi-val">{avg_score:.1f}%</div></div>
                    <div class="kpi-card"><div>Competencias</div><div class="kpi-val">{total_comp}</div></div>
                    <div class="kpi-card"><div>Mejor Área</div><div class="kpi-val">{best_val:.1f}%</div></div>
                </div>
                
                <div style="background: #FFF7ED; border-left: 4px solid {COLORS.SECONDARY}; padding: 20px; border-radius: 8px; margin-bottom: 40px;">
                    <h3>💡 Insights Estratégicos</h3>
                    <p>La organización presenta un desempeño destacado en <strong>{best_comp}</strong> ({best_val:.1f}%), 
                    mientras que se identifica una oportunidad de mejora en <strong>{worst_comp}</strong> ({worst_val:.1f}%).</p>
                </div>
                
                <h2>1. Distribución del Desempeño</h2>
                <div class="chart-box">{html_dist}</div>
                
                <h2>2. Rankings de Talento</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="chart-box"><h3>Top Desempeño</h3>{html_top}</div>
                    <div class="chart-box"><h3>Requieren Atención</h3>{html_bottom}</div>
                </div>
                
                <h2>3. Mapa de Calor Organizacional</h2>
                <div class="chart-box">{html_heatmap}</div>
                
                <h2>4. Detalle Estadístico</h2>
                {tabla_stats}
                
                <div style="text-align: center; margin-top: 60px; color: #64748B; font-size: 0.9rem;">
                    Generado por ITKAP Intelligence Suite © 2025
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

report_generator = HTMLReportGenerator()