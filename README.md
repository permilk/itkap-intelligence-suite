# 🔷 ITKAP Intelligence Suite v3.0

> **Enterprise-Grade Competency Analysis Platform**  
> Clean Architecture • Professional Design • Production-Ready

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características-principales)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación-rápida)
- [Uso](#-uso)
- [Módulos](#-módulos-del-sistema)
- [Documentación](#-documentación)
- [Soporte](#-soporte)

---

## 🎯 Descripción

**ITKAP Intelligence Suite** es una plataforma empresarial de análisis de competencias organizacionales, diseñada con arquitectura de software profesional para maximizar escalabilidad, mantenibilidad y rendimiento.

### Ideal para:

- 🏢 Departamentos de Recursos Humanos
- 📊 Consultoras de Capital Humano
- 🎯 Empresas con evaluaciones periódicas
- 📈 Organizaciones enfocadas en desarrollo de talento

---

## ✨ Características Principales

### 🏗️ Arquitectura Enterprise

- **Clean Architecture** - Separación clara de responsabilidades
- **Service Layer Pattern** - Lógica de negocio encapsulada
- **Component-Based UI** - Componentes reutilizables
- **Type Safety** - Type hints y dataclasses
- **Professional Logging** - Sistema de logging robusto

### 📊 Funcionalidades

- ✅ **Dashboard Organizacional** - Vista panorámica con KPIs
- ✅ **Análisis Individual** - Perfiles detallados por colaborador
- ✅ **Rankings Dinámicos** - Top performers y áreas de oportunidad
- ✅ **Matriz de Calor** - Visualización completa de competencias
- ✅ **Reportes Ejecutivos** - HTML descargables y profesionales
- ✅ **Validación Robusta** - Multi-capa con mensajes claros

### 🎨 Diseño Profesional

- 🎨 Paleta corporativa ITKAP
- 📱 Interfaz responsive
- ⚡ Animaciones suaves
- 🖼️ Visualizaciones interactivas con Plotly
- 🎯 UX optimizada para decisiones ejecutivas

---

## 🏛️ Arquitectura

```
┌────────────────────────────────────┐
│     Presentation Layer             │
│  (app.py + ui_components.py)      │
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│    Business Logic Layer            │
│ (data_service.py + charts.py)     │
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│      Data Access Layer             │
│    (pandas + openpyxl)             │
└────────────────────────────────────┘
```

**Ver:** [Documentación Técnica Completa](ARQUITECTURA_TECNICA.md)

---

## 🚀 Instalación Rápida

### Requisitos

- Python 3.8+
- pip 21.0+

### Pasos

```bash
# 1. Clonar/descargar proyecto
git clone [URL] itkap-suite
cd itkap-suite

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
streamlit run app.py
```

### Acceso

Abre tu navegador en: **http://localhost:8501**

---

## 💼 Uso

### 1. Cargar Datos

1. Ve a la sección **"Inicio"**
2. Arrastra tu archivo Excel (.xlsx o .xlsm)
3. El sistema valida y procesa automáticamente

### 2. Explorar Análisis

Usa el menú lateral para navegar por:

- **Dashboard General** - Métricas organizacionales
- **Análisis Individual** - Perfiles por colaborador
- **Rankings** - Top 10 mejores y áreas de mejora
- **Matriz de Calor** - Vista completa de competencias

### 3. Generar Reportes

1. Ve a **"Reporte General"** o **"Dashboard General"**
2. Haz clic en **"Descargar Reporte"**
3. Obtén un HTML profesional listo para presentar

---

## 📦 Módulos del Sistema

| Módulo | Propósito | LOC |
|--------|-----------|-----|
| `config.py` | Configuración centralizada | ~200 |
| `data_service.py` | Lógica de negocio y validación | ~400 |
| `charts.py` | Componentes de visualización | ~500 |
| `ui_components.py` | Componentes UI reutilizables | ~450 |
| `report_generator.py` | Generación de reportes HTML | ~300 |
| `app.py` | Aplicación principal | ~350 |

**Total:** ~2,200 líneas de código limpio y documentado

---

## 📚 Documentación

### Guías Disponibles

- 📘 [Arquitectura Técnica](ARQUITECTURA_TECNICA.md) - Diseño del sistema
- 📗 [Guía de Usuario](GUIA_USUARIO.md) - Manual de uso
- 📙 [Guía de Desarrollo](ARQUITECTURA_TECNICA.md#guía-de-desarrollo) - Para desarrolladores
- 📕 [Propuesta Comercial](PROPUESTA_COMERCIAL.md) - Documento de ventas

### Documentación en Código

Todos los módulos incluyen:
- ✅ Docstrings completos
- ✅ Type hints
- ✅ Comentarios explicativos
- ✅ Examples de uso

---

## 🛠️ Stack Tecnológico

### Core

- **Python 3.8+** - Lenguaje base
- **Streamlit 1.30+** - Framework web
- **Pandas 2.1+** - Procesamiento de datos
- **Plotly 5.18+** - Visualizaciones interactivas
- **NumPy 1.24+** - Operaciones numéricas

### Herramientas

- **OpenPyXL** - Lectura de Excel
- **Dataclasses** - Estructuras de datos
- **Logging** - Sistema de logs
- **Type Hints** - Seguridad de tipos

---

## 📊 Métricas de Calidad

| Métrica | Valor |
|---------|-------|
| Módulos | 7 |
| Clases | 25+ |
| Funciones | 60+ |
| Cobertura de tipos | 90% |
| Tiempo de carga | <2s |
| Procesamiento (10MB) | <3s |

---

## 🆘 Soporte

### Contacto

- **Email:** soporte@itkap.com
- **Web:** www.itkap.com
- **Desarrollador:** Kenneth - ITKAP Development Team

### Reportar Issues

Para reportar bugs o solicitar features:
1. Describe el problema claramente
2. Incluye pasos para reproducir
3. Adjunta screenshots si aplica
4. Especifica versión de Python y OS

---

## 📝 Changelog

### v3.0.0 (2025-01-26)
- ✨ **NEW:** Arquitectura completamente refactorizada
- ✨ **NEW:** Clean Architecture + Service Layer Pattern
- ✨ **NEW:** Component-based UI system
- ✨ **NEW:** Professional error handling
- ✨ **NEW:** Enterprise logging
- ⚡ **IMPROVED:** Performance optimizations
- 🐛 **FIXED:** All previous bugs resolved

### v2.5.1 (2025-01-26)
- 🐛 Fixed NameError in report generation
- 🐛 Fixed KeyError in dashboard metrics

---

## 📄 Licencia

© 2025 ITKAP Consulting - Todos los derechos reservados

**Licencia Propietaria** - Uso exclusivo para clientes de ITKAP Consulting

---

## 🙏 Créditos

**Desarrollado por:**  
ITKAP Development Team  
Kenneth - Senior Full-Stack Developer

**Empresa:**  
ITKAP Consulting  
www.itkap.com

---

<div align="center">

**Construido con ❤️ por ITKAP Consulting**

[Documentación](ARQUITECTURA_TECNICA.md) • [Soporte](mailto:soporte@itkap.com) • [Web](https://www.itkap.com)

</div>

