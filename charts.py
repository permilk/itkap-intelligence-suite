"""
ITKAP Intelligence Suite - Visualization Module
Professional chart components with Plotly
Author: ITKAP Development Team
Version: 3.1.7 (Heatmap - Values Inside Cells, Optimized Format)
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple
from abc import ABC, abstractmethod

from config import COLORS, CHART_CONFIG, CONFIG, ChartType, get_chart_layout_config


class BaseChart(ABC):
    """Clase base abstracta para todos los gráficos"""
    
    def __init__(self):
        self.colors = COLORS
        self.config = CHART_CONFIG
        self.fig = None
    
    @abstractmethod
    def create(self, *args, **kwargs) -> go.Figure:
        """Método abstracto para crear el gráfico"""
        pass
    
    def _detect_scale(self, *data_sources) -> Dict:
        """
        Detecta automáticamente la escala de los datos
        
        Args:
            *data_sources: Series o DataFrames con datos numéricos
            
        Returns:
            Dict con información de escala: {
                'max': valor máximo del eje,
                'format': formato de números,
                'suffix': sufijo ('' o '%'),
                'title': título del eje Y,
                'hover_format': formato para hover
            }
        """
        # Encontrar el valor máximo entre todas las fuentes de datos
        max_val = 0
        for data in data_sources:
            if data is not None:
                try:
                    current_max = float(data.max().max() if isinstance(data, pd.DataFrame) else data.max())
                    max_val = max(max_val, current_max)
                except:
                    pass
        
        # Detectar escala basándose en el valor máximo
        if max_val <= 5.5:
            return {
                'max': 5,
                'format': '.2f',
                'suffix': '',
                'title': 'Nivel (0-5)',
                'hover_format': '{:.2f}'
            }
        elif max_val <= 10.5:
            return {
                'max': 10,
                'format': '.1f',
                'suffix': '',
                'title': 'Puntaje (0-10)',
                'hover_format': '{:.1f}'
            }
        else:
            return {
                'max': 100,
                'format': '.1f',
                'suffix': '%',
                'title': 'Nivel (%)',
                'hover_format': '{:.1f}%'
            }
    
    def _apply_base_layout(self, fig: go.Figure, title: str = None, height: int = None) -> go.Figure:
        """Aplica configuración base de layout"""
        layout_config = get_chart_layout_config()
        
        if height:
            layout_config['height'] = height
        
        if title:
            layout_config['title'] = {
                'text': title,
                'font': {
                    'color': self.colors.PRIMARY,
                    'size': self.config.FONT_SIZE_TITLE,
                    'family': self.config.FONT_FAMILY
                },
                'x': 0.5,
                'xanchor': 'center'
            }
        
        fig.update_layout(**layout_config)
        return fig
    
    def get_figure(self) -> go.Figure:
        """Retorna la figura creada"""
        return self.fig


class RadarChart(BaseChart):
    """Gráfico radar para comparación de competencias"""
    
    def create(
        self,
        employee_data: pd.Series,
        org_average: pd.Series,
        employee_name: str,
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Crea un gráfico radar comparativo
        
        Args:
            employee_data: Series con datos del empleado
            org_average: Series con promedio organizacional
            employee_name: Nombre del empleado
            title: Título opcional del gráfico
        """
        categories = employee_data.index.tolist()
        
        # Detectar escala automáticamente
        scale = self._detect_scale(employee_data, org_average)
        fmt, suffix = scale["format"], scale["suffix"]
        
        # Cerrar el polígono
        values_emp = employee_data.values.tolist() + [employee_data.values[0]]
        values_org = org_average.values.tolist() + [org_average.values[0]]
        categories_plot = categories + [categories[0]]
        
        fig = go.Figure()
        
        # Traza del promedio organizacional
        fig.add_trace(go.Scatterpolar(
            r=values_org,
            theta=categories_plot,
            fill='toself',
            name='Promedio Organizacional',
            line=dict(
                color=self.colors.PRIMARY,
                width=2,
                dash='dot'
            ),
            fillcolor=self.colors.PRIMARY_ALPHA_10,
            hovertemplate=f"<b>Promedio Org.</b><br>%{{theta}}<br>%{{r:{fmt}}}{suffix}<extra></extra>"
        ))
        
        # Traza del empleado
        fig.add_trace(go.Scatterpolar(
            r=values_emp,
            theta=categories_plot,
            fill='toself',
            name=employee_name,
            line=dict(
                color=self.colors.SECONDARY,
                width=3
            ),
            fillcolor=self.colors.SECONDARY_ALPHA_15,
            hovertemplate=f"<b>{employee_name}</b><br>%{{theta}}<br>%{{r:{fmt}}}{suffix}<extra></extra>"
        ))
        
        # Configuración específica del radar
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, scale['max']],
                    showline=False,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=self.config.FONT_SIZE_SMALL)
                ),
                angularaxis=dict(
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=self.config.FONT_SIZE_SMALL)
                )
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=self.config.FONT_SIZE_NORMAL)
            ),
            height=CONFIG.CHART_HEIGHT_BASE + 50
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class ComparisonBarChart(BaseChart):
    """Gráfico de barras comparativo agrupado"""
    
    def create(
        self,
        employee_data: pd.Series,
        org_average: pd.Series,
        employee_name: str,
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Crea un gráfico de barras comparativo
        
        Args:
            employee_data: Series con datos del empleado
            org_average: Series con promedio organizacional
            employee_name: Nombre del empleado
            title: Título opcional
        """
        # Detectar escala automáticamente
        scale = self._detect_scale(employee_data, org_average)
        fmt, suffix = scale["format"], scale["suffix"]
        
        categories = employee_data.index.tolist()
        
        # Detectar escala automáticamente
        scale = self._detect_scale(employee_data, org_average)
        fmt, suffix = scale["format"], scale["suffix"]
        
        fig = go.Figure()
        
        # Barras del empleado
        fig.add_trace(go.Bar(
            x=categories,
            y=employee_data.values,
            name=employee_name,
            marker_color=self.colors.PRIMARY,
            text=[f"{v:.1f}{suffix}" for v in employee_data.values],
            textposition='outside',
            textangle=0,
            textfont=dict(
                size=self.config.FONT_SIZE_SMALL,
                color=self.colors.PRIMARY,
                family=self.config.FONT_FAMILY,
                weight='bold'
            ),
            hovertemplate=f"<b>%{{x}}</b><br>{employee_name}: %{{y:{fmt}}}{suffix}<extra></extra>"
        ))
        
        # Barras del promedio organizacional
        fig.add_trace(go.Bar(
            x=categories,
            y=org_average.values,
            name='Promedio Organizacional',
            marker_color='#E91E63',
            text=[f"{v:.1f}{suffix}" for v in org_average.values],
            textposition='outside',
            textangle=0,
            textfont=dict(
                size=self.config.FONT_SIZE_SMALL,
                color='#E91E63',
                family=self.config.FONT_FAMILY,
                weight='bold'
            ),
            hovertemplate=f"<b>%{{x}}</b><br>Promedio Org.: %{{y:{fmt}}}{suffix}<extra></extra>"
        ))
        
        fig.update_layout(
            barmode='group',
            xaxis=dict(
                tickangle=-45,
                gridcolor='rgba(0,0,0,0.1)',
                title="",
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                range=[0, scale['max'] * 1.1],  # +10% espacio arriba
                gridcolor='rgba(0,0,0,0.1)',
                title=scale['title']
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.15,  # Arriba del gráfico
                xanchor="center",
                x=0.5,
                font=dict(size=self.config.FONT_SIZE_NORMAL)
            ),
            height=CONFIG.CHART_HEIGHT_BASE + 100,
            margin=dict(b=150, l=60, r=40, t=100)  # Más espacio arriba para leyenda
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class GapAnalysisChart(BaseChart):
    """Gráfico de análisis de brechas horizontal"""
    
    def create(
        self,
        employee_data: pd.Series,
        org_average: pd.Series,
        title: Optional[str] = "Análisis de Brechas"
    ) -> go.Figure:
        """
        Crea un gráfico de análisis de brechas
        
        Args:
            employee_data: Series con datos del empleado
            org_average: Series con promedio organizacional
            title: Título del gráfico
        """
        # Detectar escala automáticamente
        scale = self._detect_scale(employee_data, org_average)
        fmt, suffix = scale["format"], scale["suffix"]
        
        difference = employee_data - org_average
        
        df_gap = pd.DataFrame({
            'Competencia': employee_data.index,
            'Brecha': difference.values,
            'Puntaje': employee_data.values
        }).sort_values('Brecha')
        
        # Colorear según sea positivo o negativo
        colors = [
            self.colors.DANGER if x < 0 else self.colors.SUCCESS 
            for x in df_gap['Brecha']
        ]
        
        fig = go.Figure(go.Bar(
            y=df_gap['Competencia'],
            x=df_gap['Brecha'],
            orientation='h',
            marker_color=colors,
            text=df_gap['Brecha'].apply(lambda x: f"{x:+.1f}{suffix}"),
            textposition='outside',
            textfont=dict(
                size=self.config.FONT_SIZE_SMALL,
                family=self.config.FONT_FAMILY,
                weight='bold'
            ),
            customdata=df_gap['Puntaje'],
            hovertemplate=f"<b>%{{y}}</b><br>Desviación: %{{x:+{fmt}}}{suffix}<br>Puntaje: %{{customdata:{fmt}}}{suffix}<extra></extra>"
        ))
        
        fig.update_layout(
            xaxis=dict(
                title=f"Desviación del Promedio ({scale['suffix'] if scale['suffix'] else 'puntos'})",
                gridcolor='rgba(0,0,0,0.1)',
                zerolinecolor='rgba(0,0,0,0.3)',
                zerolinewidth=2
            ),
            yaxis=dict(
                title="",
                gridcolor='rgba(0,0,0,0.05)'
            ),
            height=max(CONFIG.CHART_HEIGHT_BASE, len(df_gap) * 40)
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class RankingChart(BaseChart):
    """Gráfico de ranking horizontal"""
    
    def create(
        self,
        data: pd.Series,
        n: int = 5,
        mode: str = 'top',
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Crea un gráfico de ranking
        
        Args:
            data: Series con promedios por empleado
            n: Cantidad de registros a mostrar
            mode: 'top' o 'bottom'
            title: Título del gráfico
        """
        sorted_data = data.sort_values(ascending=(mode == 'top'))
        
        # Detectar escala automáticamente
        scale = self._detect_scale(data)
        fmt, suffix = scale["format"], scale["suffix"]
        display_data = sorted_data.tail(n) if mode == 'top' else sorted_data.head(n)
        
        color = self.colors.SECONDARY if mode == 'top' else self.colors.DANGER
        
        if not title:
            title = f"Top {n} Mejor Desempeño" if mode == 'top' else f"Top {n} Requiere Atención"
        
        fig = go.Figure(go.Bar(
            x=display_data.values,
            y=display_data.index,
            orientation='h',
            marker_color=color,
            text=[f"{v:.1f}{suffix}" for v in display_data.values],
            textposition='inside',
            textfont=dict(
                size=self.config.FONT_SIZE_NORMAL,
                color='white',
                family=self.config.FONT_FAMILY,
                weight='bold'
            ),
            hovertemplate=f"<b>%{{y}}</b><br>Promedio: %{{x:{fmt}}}{suffix}<extra></extra>"
        ))
        
        fig.update_layout(
            xaxis=dict(
                range=[0, scale['max'] * 1.05],
                gridcolor='rgba(0,0,0,0.1)',
                title=""
            ),
            yaxis=dict(
                title="",
                automargin=True
            ),
            height=max(350, n * 45)
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class HeatmapChart(BaseChart):
    """Matriz de calor organizacional"""
    
    def create(
        self,
        df: pd.DataFrame,
        title: Optional[str] = "Matriz de Competencias Organizacional"
    ) -> go.Figure:
        """
        Crea un heatmap de competencias
        
        Args:
            df: DataFrame con datos de competencias
            title: Título del gráfico
        """
        # Detectar escala automáticamente
        scale = self._detect_scale(df)
        fmt, suffix = scale["format"], scale["suffix"]
        
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale=[
                [0, self.colors.DANGER],
                [0.5, self.colors.WARNING],
                [1, self.colors.SUCCESS]
            ],
            zmin=0,
            zmax=scale['max'],
            # Texto dentro de celdas con formato dinámico
            text=[[f"{v:.1f}" if scale['max'] <= 10 else f"{v:.0f}" for v in row] for row in df.values],
            texttemplate='%{text}',
            textfont=dict(
                size=7,  # Fuente pequeña para caber en celdas
                color='white',
                family=self.config.FONT_FAMILY,
                weight='bold'
            ),
            # Hover con información completa
            hovertemplate=f"<b>Empleado:</b> %{{y}}<br><b>Competencia:</b> %{{x}}<br><b>Nivel:</b> %{{z:{fmt}}}{suffix}<extra></extra>",
            colorbar=dict(
                title=scale['title'],
                tickvals=[0, scale['max']*0.25, scale['max']*0.5, scale['max']*0.75, scale['max']],
                ticktext=[f"0{suffix}", 
                         f"{scale['max']*0.25:.0f}{scale['suffix']}", 
                         f"{scale['max']*0.5:.0f}{scale['suffix']}", 
                         f"{scale['max']*0.75:.0f}{scale['suffix']}", 
                         f"{scale['max']:.0f}{scale['suffix']}"],
                len=0.7
            )
        ))
        
        fig.update_layout(
            xaxis=dict(
                tickangle=-90,  # Vertical
                side='bottom',
                tickfont=dict(size=9),
                tickmode='linear',
                automargin=True
            ),
            yaxis=dict(
                tickfont=dict(size=10),
                autorange='reversed',
                automargin=True,
                tickmode='linear'
            ),
            height=max(650, len(df) * 45),  # Más altura para acomodar texto
            width=None,  # Auto width
            margin=dict(b=180, l=220, r=100, t=60)
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class DistributionHistogram(BaseChart):
    """Histograma de distribución"""
    
    def create(
        self,
        data: pd.Series,
        nbins: int = 15,
        title: Optional[str] = "Distribución de Desempeño"
    ) -> go.Figure:
        """
        Crea un histograma de distribución
        
        Args:
            data: Series con datos a distribuir
            nbins: Número de bins
            title: Título del gráfico
        """
        # Detectar escala automáticamente
        scale = self._detect_scale(data)
        fmt, suffix = scale["format"], scale["suffix"]
        
        fig = go.Figure(data=[go.Histogram(
            x=data,
            marker_color=self.colors.PRIMARY,
            nbinsx=nbins,
            hovertemplate=f"Rango: %{{x:{fmt}}}{suffix}<br>Empleados: %{{y}}<extra></extra>",
            opacity=0.85
        )])
        
        # Agregar línea de promedio
        mean_val = data.mean()
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color=self.colors.SECONDARY,
            annotation_text=f"Promedio: {mean_val:{fmt}}{suffix}",
            annotation_position="top right",
            annotation_font=dict(
                size=self.config.FONT_SIZE_NORMAL,
                color=self.colors.SECONDARY
            )
        )
        
        fig.update_layout(
            xaxis=dict(
                title=scale["title"],
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                title="Número de Empleados",
                gridcolor='rgba(0,0,0,0.1)'
            ),
            height=400,
            bargap=0.1
        )
        
        self.fig = self._apply_base_layout(fig, title)
        return self.fig


class ChartFactory:
    """Factory para crear gráficos de forma consistente"""
    
    _chart_classes = {
        ChartType.RADAR: RadarChart,
        ChartType.BAR: RankingChart,
        ChartType.HEATMAP: HeatmapChart,
        ChartType.HISTOGRAM: DistributionHistogram,
        ChartType.COMPARISON: ComparisonBarChart
    }
    
    @classmethod
    def create_chart(cls, chart_type: ChartType) -> BaseChart:
        """
        Crea una instancia de gráfico según el tipo
        
        Args:
            chart_type: Tipo de gráfico a crear
            
        Returns:
            Instancia de BaseChart
        """
        chart_class = cls._chart_classes.get(chart_type)
        if not chart_class:
            raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")
        
        return chart_class()


# Funciones de conveniencia para uso directo
def create_radar_chart(employee_data, org_avg, employee_name, title=None):
    """Función de conveniencia para crear radar chart"""
    chart = ChartFactory.create_chart(ChartType.RADAR)
    return chart.create(employee_data, org_avg, employee_name, title)


def create_comparison_chart(employee_data, org_avg, employee_name, title=None):
    """Función de conveniencia para crear comparison chart"""
    chart = ChartFactory.create_chart(ChartType.COMPARISON)
    return chart.create(employee_data, org_avg, employee_name, title)


def create_gap_chart(employee_data, org_avg, title=None):
    """Función de conveniencia para crear gap analysis chart"""
    chart = GapAnalysisChart()
    return chart.create(employee_data, org_avg, title)


def create_ranking_chart(data, n=5, mode='top', title=None):
    """Función de conveniencia para crear ranking chart"""
    chart = ChartFactory.create_chart(ChartType.BAR)
    return chart.create(data, n, mode, title)


def create_heatmap(df, title=None):
    """Función de conveniencia para crear heatmap"""
    chart = ChartFactory.create_chart(ChartType.HEATMAP)
    return chart.create(df, title)


def create_histogram(data, nbins=15, title=None):
    """Función de conveniencia para crear histograma"""
    chart = ChartFactory.create_chart(ChartType.HISTOGRAM)
    return chart.create(data, nbins, title)


if __name__ == "__main__":
    print("Visualization Module loaded ✓")
    print(f"Available chart types: {[ct.value for ct in ChartType]}")
    print(f"Chart factory ready with {len(ChartFactory._chart_classes)} chart types")
