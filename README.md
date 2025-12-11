# ITKAP Intelligence Suite v2.0

## Sistema Configurable de Análisis de Competencias HR

Sistema profesional para análisis y visualización de evaluaciones de competencias organizacionales, con panel de configuración avanzado y exportación múltiple.

---

## 🚀 Características Principales

### ✅ Panel de Configuración Avanzado
- **Ordenamiento Flexible**: Colaboradores por promedio (mayor/menor) o alfabético
- **Esquemas de Colores**: 5 paletas profesionales (RdYlGn, Viridis, Blues, RdBu, Spectral)
- **Umbrales Personalizables**: Define tus propios niveles de Bajo/Medio/Alto
- **Selección de Gráficos**: Activa/desactiva visualizaciones según necesites
- **White Label**: Personaliza con el nombre de tu empresa cliente

### 📊 Visualizaciones Incluidas

1. **Mapa de Calor de Competencias**
   - Ordenado automáticamente por promedio de colaboradores
   - Valores visibles en cada celda
   - Colores configurables según tus preferencias

2. **Top 10 Colaboradores**
   - Ranking de los mejores evaluados
   - Visualización horizontal con código de colores

3. **Gráfico de Barras de Competencias Organizacionales**
   - Análisis de cada competencia a nivel empresa
   - Estilo profesional (rosa/magenta)
   - Valores mostrados sobre cada barra

4. **Distribución por Nivel de Desempeño**
   - Categorización en Bajo/Medio/Alto
   - Conteo de colaboradores por nivel
   - Semáforo visual (Rojo/Amarillo/Verde)

5. **Gráfico Radar** (opcional)
   - Vista radial de competencias
   - Comparativas visuales

### 💾 Exportación Múltiple

1. **Excel Completo**
   - Hoja "Datos Completos": Información raw
   - Hoja "Competencias Ordenadas": Ranking por promedio
   - Hoja "Estadísticas": Métricas por competencia
   - Hoja "Resumen Ejecutivo": KPIs principales

2. **PowerPoint Ejecutivo**
   - Portada con branding personalizado
   - Resumen ejecutivo con métricas clave
   - Todos los gráficos en slides individuales
   - Recomendaciones estratégicas
   - Slide de cierre profesional

3. **Paquete de Imágenes (ZIP)**
   - Cada gráfico en PNG de alta resolución (1920x1080)
   - Listo para usar en emails, documentos, etc.
   - Nombrado consistente y ordenado

4. **CSV Raw Data**
   - Datos sin procesar
   - Compatible con cualquier herramienta

---

## 📋 Requisitos del Sistema

### Software Necesario
```bash
Python 3.8 o superior
pip (gestor de paquetes de Python)
```

### Dependencias
Todas las dependencias están en `requirements.txt`:
- streamlit (interfaz web)
- pandas (procesamiento de datos)
- plotly (gráficos interactivos)
- openpyxl (generación de Excel)
- python-pptx (generación de PowerPoint)
- kaleido (exportación de imágenes)

---

## 🔧 Instalación

### Opción 1: Instalación Manual

1. **Descargar el código**
```bash
# Si tienes el código en un ZIP, descomprímelo
# O clona desde el repositorio
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

5. **Abrir en el navegador**
```
La aplicación se abrirá automáticamente en:
http://localhost:8501
```

### Opción 2: Instalación Rápida (Una Línea)

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && streamlit run app.py
```

---

## 📖 Modo de Uso

### 1. Preparar tu archivo Excel

Tu archivo debe tener la siguiente estructura:

| Nombre | Competencia 1 | Competencia 2 | Competencia 3 | ... |
|--------|---------------|---------------|---------------|-----|
| Juan Pérez | 4.5 | 3.8 | 4.2 | ... |
| María López | 3.9 | 4.1 | 3.7 | ... |
| ... | ... | ... | ... | ... |

**Requisitos:**
- ✅ Columna "Nombre" con los colaboradores
- ✅ Columnas numéricas para cada competencia
- ✅ Valores entre 1-5 (escala típica)
- ✅ Sin celdas vacías
- ✅ Formato `.xlsx` o `.xls`

### 2. Configurar el Sistema

En el **Panel de Configuración** (barra lateral):

1. **Visualización del Heatmap**
   - Elegir orden de colaboradores
   - Activar/desactivar valores en celdas
   - Seleccionar esquema de colores

2. **Umbrales de Evaluación**
   - Definir umbral bajo (ej: 3.0)
   - Definir umbral alto (ej: 4.0)

3. **Gráficos a Incluir**
   - Seleccionar qué visualizaciones mostrar
   - Todos activos por defecto

4. **Personalización**
   - Ingresar nombre de la empresa cliente
   - Esto aparecerá en la portada del PowerPoint

5. **Guardar Configuración**
   - Click en "💾 Guardar Configuración"
   - La config se mantiene durante la sesión

### 3. Cargar Datos

1. Click en "Browse files" o arrastra tu archivo
2. El sistema procesará automáticamente
3. Verás las métricas principales en 4 cards

### 4. Revisar Visualizaciones

Todas las gráficas se generan automáticamente:
- Mapa de calor (ordenado por promedio)
- Top 10 colaboradores
- Barras de competencias organizacionales
- Distribución por nivel

### 5. Exportar Reportes

En la sección "💾 Exportar Reportes":

| Botón | Descripción | Formato |
|-------|-------------|---------|
| 📊 Descargar Excel | Archivo Excel con 4 hojas | .xlsx |
| 📽️ Descargar PowerPoint | Presentación ejecutiva completa | .pptx |
| 🖼️ Descargar Imágenes | ZIP con todos los gráficos | .zip |
| 📄 Descargar CSV | Datos sin procesar | .csv |

---

## 🎨 Personalización Avanzada

### Esquemas de Colores Disponibles

1. **RdYlGn** (Rojo-Amarillo-Verde) ⭐ Recomendado
   - Semáforo visual intuitivo
   - Verde = Alto, Amarillo = Medio, Rojo = Bajo

2. **Viridis** (Profesional)
   - Escala de azul a amarillo
   - Accesible para daltónicos

3. **Blues** (Corporativo)
   - Escala de azules
   - Look profesional y sobrio

4. **RdBu** (Divergente)
   - Rojo a Azul
   - Ideal para comparativas

5. **Spectral** (Multicolor)
   - Arcoíris completo
   - Máxima diferenciación visual

### Umbrales Personalizables

**Ejemplo 1: Evaluación Estricta**
```
Umbral Bajo: 3.5
Umbral Alto: 4.5
```

**Ejemplo 2: Evaluación Estándar**
```
Umbral Bajo: 3.0
Umbral Alto: 4.0
```

**Ejemplo 3: Evaluación Flexible**
```
Umbral Bajo: 2.5
Umbral Alto: 3.5
```

---

## 📂 Estructura del Proyecto

```
itkap_hr_suite/
│
├── app.py                      # Aplicación principal Streamlit
├── pptx_generator.py           # Generador de PowerPoint
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
├── ejemplo_datos.xlsx          # Archivo de ejemplo
└── ejemplo_datos.csv           # Datos de ejemplo en CSV
```

---

## 💡 Casos de Uso

### Para Consultores HR
- ✅ Analizar múltiples empresas clientes
- ✅ Generar reportes profesionales en minutos
- ✅ Personalizar con logo/nombre del cliente
- ✅ Exportar en formatos cliente-ready

### Para Departamentos de RRHH
- ✅ Evaluaciones periódicas de competencias
- ✅ Seguimiento de desarrollo organizacional
- ✅ Identificación de brechas de talento
- ✅ Reportes ejecutivos para dirección

### Para Instituciones Educativas
- ✅ Evaluación de competencias docentes
- ✅ Análisis de programas de formación
- ✅ Reportes para acreditaciones
- ✅ Seguimiento de desarrollo profesoral

---

## 🔒 Seguridad y Privacidad

- ✅ **Datos locales**: Todo se procesa en tu computadora
- ✅ **Sin cloud**: No se suben datos a servidores externos
- ✅ **Sin registro**: No requiere cuenta ni login
- ✅ **Confidencialidad**: Tus datos nunca salen de tu control

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de haber activado el entorno virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Port 8501 already in use"
```bash
# Usa otro puerto
streamlit run app.py --server.port 8502
```

### Error al generar PowerPoint
```bash
# Instala/actualiza kaleido
pip install -U kaleido
```

### Gráficos no se ven correctamente
```bash
# Actualiza plotly
pip install -U plotly
```

---

## 📝 Notas de la Versión

### v2.0 (Actual)
- ✅ Panel de configuración completo
- ✅ Exportación a PowerPoint automática
- ✅ Mapa de calor ordenado por ranking
- ✅ Gráfico de barras de competencias
- ✅ Exportación de paquete de imágenes
- ✅ Múltiples esquemas de colores
- ✅ Umbrales configurables
- ✅ White label personalizable

### v1.0
- Visualización básica de competencias
- Exportación a Excel simple
- Gráficos fijos

---

## 🆘 Soporte

Para soporte técnico o consultas:
- **Email**: [tu_email@itkap.com]
- **WhatsApp**: [tu_numero]
- **Web**: www.itkap.com

---

## 📜 Licencia

**Licencia Perpetua - Uso Comercial**

Este software es propiedad de **ITKAP Consulting**.

### Derechos Otorgados:
- ✅ Uso comercial ilimitado
- ✅ Modificación del código fuente
- ✅ Uso con todos tus clientes
- ✅ White label completo

### Restricciones:
- ❌ No revender el código fuente
- ❌ No sublicenciar a terceros
- ❌ No crear productos competidores

---

## 🙏 Créditos

**Desarrollado por**: ITKAP Consulting  
**Versión**: 2.0  
**Última actualización**: Diciembre 2024

---

## 📞 Contacto

**ITKAP Consulting**  
Transformación Digital y Analytics  
www.itkap.com

---

*Sistema diseñado específicamente para consultores HR y departamentos de Recursos Humanos que requieren análisis profesional de competencias organizacionales.*
