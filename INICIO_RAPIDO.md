# ⚡ GUÍA DE INICIO RÁPIDO

## ITKAP Intelligence Suite v3.0 - 5 Minutos a la Productividad

---

## 🚀 INSTALACIÓN EN 3 PASOS

### Paso 1: Preparar Ambiente

```bash
# Crear carpeta del proyecto
mkdir itkap-suite
cd itkap-suite

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

✅ **Resultado:** Ambiente aislado listo

---

### Paso 2: Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

**Tiempo:** ~2 minutos

✅ **Resultado:** Todas las librerías instaladas

---

### Paso 3: Ejecutar Aplicación

```bash
# Iniciar la aplicación
streamlit run app.py
```

**Tiempo:** ~5 segundos

✅ **Resultado:** App corriendo en http://localhost:8501

---

## 📁 PRIMER USO

### 1. Abrir la Aplicación

```
http://localhost:8501
```

Verás la pantalla de **"Inicio"**

---

### 2. Cargar tu Archivo

1. **Arrastra** tu archivo Excel a la zona de carga  
   O  
2. **Haz clic** en "Browse files"

**Formato soportado:** .xlsx o .xlsm

---

### 3. Esperar Procesamiento

```
🔄 Procesando datos...
```

**Tiempo:** ~3 segundos

✅ Verás mensaje de **éxito**

---

### 4. Explorar Análisis

Usa el menú lateral para navegar:

```
📂 Inicio              ← Estás aquí
📊 Dashboard General   ← Ve aquí
👤 Análisis Individual
🏆 Rankings
🔥 Matriz de Calor
📄 Reporte General
```

---

## 📊 NAVEGACIÓN RÁPIDA

### Dashboard General

**Qué verás:**
- 4 KPIs principales
- Histograma de distribución
- Top 5 mejores
- Top 5 a desarrollar

**Acción:** Haz clic en **"📄 Descargar Reporte"**

---

### Análisis Individual

**Qué verás:**
- Selector de empleado
- 3 métricas individuales
- Gráfico comparativo
- Tabla detallada

**Acción:** Explora diferentes empleados

---

### Rankings

**Qué verás:**
- Control deslizante (3-20 personas)
- Top performers
- Áreas de oportunidad
- Ranking completo

**Acción:** Ajusta cantidad con slider

---

### Matriz de Calor

**Qué verás:**
- Heatmap completo
- Colores: Verde (alto), Amarillo (medio), Rojo (bajo)
- Estadísticas por competencia

**Acción:** Identifica patrones visuales

---

### Reporte General

**Qué verás:**
- Información del reporte
- Botón de descarga
- Vista previa

**Acción:** Descarga reporte HTML ejecutivo

---

## 💡 TIPS RÁPIDOS

### Para Mejores Resultados

✅ **Archivo Excel:**
- Formato estándar de evaluaciones
- Filas 9-10 con encabezados
- Columnas: NOMBRE, CLAVE, EDAD, NIVEL, PERFIL, ÁREA

✅ **Navegación:**
- Usa menú lateral para cambiar secciones
- Todos los gráficos son interactivos
- Pasa el mouse sobre gráficos para info

✅ **Reportes:**
- HTML se abre en cualquier navegador
- Convertible a PDF (Ctrl+P → Guardar como PDF)
- Listo para presentar a dirección

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error al iniciar app

```bash
# Verificar instalación
python verificar_app.py
```

### Error al cargar archivo

**Verificar:**
- ✅ Archivo .xlsx o .xlsm
- ✅ Tiene datos en filas 9+
- ✅ Columna NOMBRE existe

### App muy lenta

**Solución:**
- Cerrar otros procesos
- Verificar tamaño de archivo (<50MB)
- Reiniciar la app

---

## 📞 AYUDA RÁPIDA

### Documentación Completa

📘 **README.md** - Guía general  
📗 **ARQUITECTURA_TECNICA.md** - Guía técnica  
📙 **PROPUESTA_COMERCIAL.md** - Info comercial  
📕 **INDICE_MAESTRO.md** - Índice de archivos

### Contacto

📧 soporte@itkap.com  
🌐 www.itkap.com  

---

## ⏱️ TIMELINE TÍPICO

```
Minuto 0:  Descargar archivos
Minuto 1:  Crear ambiente
Minuto 2:  Instalar dependencias (automático)
Minuto 3:  Iniciar app
Minuto 4:  Cargar primer archivo
Minuto 5:  Explorando dashboards ✅
```

**Total:** 5 minutos a productividad completa

---

## ✅ CHECKLIST PRIMERA VEZ

- [ ] Python 3.8+ instalado
- [ ] Archivos del proyecto descargados
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] App ejecutándose
- [ ] Archivo Excel listo
- [ ] Datos cargados exitosamente
- [ ] Explorado todas las secciones
- [ ] Generado primer reporte

---

## 🎯 PRÓXIMOS PASOS

### Después del Primer Uso

1. **Explorar todas las secciones** - Familiarízate con cada módulo
2. **Generar reportes** - Prueba descarga HTML
3. **Probar con datos reales** - Usa tus evaluaciones
4. **Compartir con equipo** - Muestra los dashboards
5. **Leer documentación** - Profundiza en features

### Para Producción

1. **Configurar servidor** - Deploy en ambiente productivo
2. **Capacitar usuarios** - Sesión de 2-4 horas
3. **Establecer proceso** - Flujo regular de uso
4. **Monitorear uso** - Verificar adopción
5. **Solicitar feedback** - Mejoras continuas

---

## 📊 EJEMPLOS DE USO

### Caso 1: Evaluación Anual

```
1. Cargar Excel de evaluaciones
2. Ir a Dashboard General
3. Revisar KPIs y distribución
4. Descargar reporte ejecutivo
5. Presentar a dirección
```

**Tiempo:** 10 minutos

---

### Caso 2: 1-on-1 con Empleado

```
1. Cargar datos actualizados
2. Ir a Análisis Individual
3. Seleccionar empleado
4. Revisar gráfico comparativo
5. Discutir fortalezas/áreas
```

**Tiempo:** 5 minutos por empleado

---

### Caso 3: Identificar Talento

```
1. Cargar evaluaciones
2. Ir a Rankings
3. Ajustar a Top 10
4. Identificar top performers
5. Revisar en Análisis Individual
```

**Tiempo:** 15 minutos

---

## 🎨 PERSONALIZACIÓN RÁPIDA

### Cambiar Colores

Editar `config.py`:

```python
@dataclass(frozen=True)
class ColorPalette:
    PRIMARY: str = "#0E1B2E"      # ← Tu color primario
    SECONDARY: str = "#F27200"    # ← Tu color secundario
```

**Reiniciar app para ver cambios**

---

## 🏆 CARACTERÍSTICAS CLAVE

### Lo que hace único a ITKAP Suite

✨ **Arquitectura Enterprise** - Clean code, fácil mantener  
⚡ **Velocidad** - Procesamiento en segundos  
🎨 **Diseño Profesional** - Listo para presentar  
📊 **Análisis Completo** - 6 tipos de visualizaciones  
📄 **Reportes Ejecutivos** - HTML profesionales  
🔒 **Seguro** - Datos locales, sin cloud  

---

<div align="center">

## 🎉 ¡Listo para Comenzar!

**¿Dudas?** → soporte@itkap.com  
**¿Demo personalizada?** → ventas@itkap.com  
**¿Más info?** → Leer README.md

---

**ITKAP Intelligence Suite v3.0**  
*5 Minutos a la Productividad*

© 2025 ITKAP Consulting

</div>
