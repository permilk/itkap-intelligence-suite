# ⚡ GUÍA DE INICIO RÁPIDO

## 🚀 Empezar en 5 Minutos

### Paso 1: Instalar (2 minutos)

```bash
# 1. Abrir terminal en la carpeta del proyecto
cd itkap_hr_suite

# 2. Instalar todo (una línea)
pip install -r requirements.txt --break-system-packages

# 3. Ejecutar
streamlit run app.py
```

### Paso 2: Probar (1 minuto)

1. **Abrir navegador**: Se abre automáticamente en `http://localhost:8501`
2. **Cargar archivo**: Click en "Browse files" y selecciona `ejemplo_datos.xlsx`
3. **Ver resultados**: ¡Listo! Todos los gráficos aparecen automáticamente

### Paso 3: Exportar (30 segundos)

1. **Excel**: Click en "📊 Descargar Excel"
2. **PowerPoint**: Click en "📽️ Descargar PowerPoint"
3. **Imágenes**: Click en "🖼️ Descargar Imágenes"

---

## 🎨 Personalizar (2 minutos)

### En el Panel Lateral:

**1. Cambiar orden del heatmap:**
```
☐ Promedio (mayor a menor) ← Por defecto
☐ Promedio (menor a mayor)
☐ Alfabético
```

**2. Cambiar colores:**
```
☐ RdYlGn (Rojo-Verde) ← Por defecto
☐ Viridis (Azul-Amarillo)
☐ Blues (Azules)
☐ RdBu (Rojo-Azul)
☐ Spectral (Multicolor)
```

**3. Ajustar umbrales:**
```
Bajo (<): 3.0
Alto (>): 4.0
```

**4. Poner nombre de empresa:**
```
Nombre de la empresa: ____________
```

**5. Guardar:**
```
[💾 Guardar Configuración]
```

---

## 📊 Usando con Datos Reales

### Tu archivo Excel debe tener:

```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│ Nombre      │ Liderazgo    │ Comunicación │ Creatividad  │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Juan Pérez  │ 4.5          │ 4.2          │ 3.8          │
│ Ana López   │ 3.9          │ 4.5          │ 4.1          │
│ ...         │ ...          │ ...          │ ...          │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

**Requisitos:**
- ✅ Columna "Nombre" (exactamente así)
- ✅ Columnas numéricas para competencias
- ✅ Valores 1-5
- ✅ Sin celdas vacías

---

## 🎯 Flujo de Trabajo con Cliente

### Para Porfirio:

**1. Cliente te envía evaluaciones (Excel)**
   - Formato: Nombre + Competencias numéricas

**2. Tú subes el archivo (10 segundos)**
   - Click en "Browse files"
   - Selecciona el Excel del cliente

**3. Personalizas (2 minutos)**
   - Panel lateral → Nombre de la empresa
   - Ajustas colores si quieres
   - Defines umbrales según su cultura

**4. Revisas gráficos (30 segundos)**
   - Mapa de calor automático (ordenado)
   - Top 10 colaboradores
   - Barras de competencias
   - Distribución por nivel

**5. Exportas TODO (1 minuto)**
   - PowerPoint → Para presentar
   - Excel → Para análisis detallado
   - Imágenes → Para emails/docs

**6. Presentas al cliente (1 hora)**
   - Abres el PowerPoint generado
   - Explicas cada slide
   - ¡Cliente feliz!

**Total tiempo: 4-5 horas**
**Antes: 20-25 horas**

---

## 💡 Tips Pro

### Tip 1: Plantillas por Industria
Crea configuraciones guardadas mentalmente:

**Salud:**
- Colores: Blues (profesional)
- Umbral bajo: 3.5 (más estricto)
- Umbral alto: 4.5

**Retail:**
- Colores: RdYlGn (semáforo)
- Umbral bajo: 3.0 (estándar)
- Umbral alto: 4.0

**Tech:**
- Colores: Viridis (moderno)
- Umbral bajo: 3.5
- Umbral alto: 4.5

### Tip 2: Branding por Cliente
- Siempre pon el nombre del cliente
- Aparece en portada del PowerPoint
- Se ve súper profesional

### Tip 3: Múltiples Exportaciones
- Descarga TODOS los formatos
- Envía PowerPoint por email
- Deja Excel para análisis profundo
- Usa imágenes en reportes Word

### Tip 4: Backup
- Guarda configuración al terminar
- Exporta CSV raw por si acaso
- Siempre conserva el Excel original

---

## 🐛 Problemas Comunes

### "ModuleNotFoundError"
```bash
# Solución:
pip install -r requirements.txt --break-system-packages
```

### "Port already in use"
```bash
# Solución: Usa otro puerto
streamlit run app.py --server.port 8502
```

### Gráficos no se ven
```bash
# Solución: Actualiza plotly
pip install -U plotly kaleido
```

### Error en PowerPoint
```bash
# Solución: Reinstala python-pptx
pip install --upgrade python-pptx
```

---

## 📱 Demo para Cliente

### Qué mostrarle a Porfirio:

**1. Carga de datos (En vivo)**
   - "Mira, subo tu Excel aquí..."
   - [Browse files → ejemplo_datos.xlsx]
   - "Y automáticamente genera..."

**2. Visualizaciones (En vivo)**
   - "Mapa de calor ordenado por promedio"
   - "Top 10 colaboradores destacados"
   - "Análisis de competencias organizacionales"
   - "Distribución por nivel"

**3. Personalización (En vivo)**
   - Panel lateral → "Puedes cambiar..."
   - Orden: Cambia a alfabético → se actualiza
   - Colores: Cambia a Viridis → se actualiza
   - "Todo sin programar"

**4. Exportación (En vivo)**
   - Click en PowerPoint → "Mira, se descarga..."
   - Abre el PPTX → "7 slides profesionales listos"
   - Click en Excel → "4 hojas con análisis"
   - Click en Imágenes → "ZIP con todos los gráficos"

**Total demo: 10-15 minutos**

---

## 🎬 Script de Presentación

### Para Kenneth presentando a Porfirio:

**Inicio (1 min):**
> "Porfirio, te voy a mostrar el sistema que hablamos. Es flexible, lo controlas tú, y exporta a Excel, PowerPoint e imágenes."

**Carga de datos (2 min):**
> "Subes el Excel del cliente aquí... [cargar archivo]... Y automáticamente genera todo el análisis."

**Visualizaciones (3 min):**
> "Mira, este es el mapa de calor ORDENADO por promedio como me pediste. Los mejores colaboradores arriba.
>
> Aquí está el Top 10 de tu empresa.
>
> Y este gráfico de barras muestra las competencias organizacionales, igual que el que me mostraste."

**Personalización (3 min):**
> "Lo mejor: TODO lo puedes cambiar sin programar.
>
> [Panel lateral]
>
> Quieres ordenar alfabético? Click. Quieres cambiar colores? Click. Quieres ajustar umbrales? Click.
>
> Pones el nombre del cliente aquí y aparece en la portada."

**Exportación (3 min):**
> "Y ahora lo bueno:
>
> [Click PowerPoint] → Presentación ejecutiva completa, 7 slides listos para presentar.
>
> [Click Excel] → 4 hojas con todo el análisis detallado.
>
> [Click Imágenes] → Todos los gráficos en PNG para usar donde quieras.
>
> Todo en menos de 1 minuto."

**Cierre (1 min):**
> "¿Y el precio? 50 mil pesos. Pagas 20K al inicio, 15K al mes, 15K al mes 2.
>
> Con 3 proyectos recuperas. Después todo es ganancia.
>
> ¿Qué dices?"

**Total: 12-15 minutos**

---

## 📋 Checklist de Entrega

### Cuando cierres con Porfirio:

**Día 1:**
- [ ] Contrato firmado
- [ ] Primer pago recibido
- [ ] Enviar código completo por email
- [ ] Enviar video tutorial

**Día 2:**
- [ ] Sesión de capacitación parte 1 (1 hr)
- [ ] Instalar en su computadora
- [ ] Probar con datos de ejemplo
- [ ] Resolver dudas

**Día 7:**
- [ ] Sesión de capacitación parte 2 (1 hr)
- [ ] Probar con datos reales
- [ ] Tips avanzados
- [ ] Dudas finales

**Día 30:**
- [ ] Segundo pago
- [ ] Check-in: ¿Cómo va?
- [ ] Resolver problemas si hay

**Día 60:**
- [ ] Tercer pago
- [ ] Cierre formal
- [ ] Testimonio (si está feliz)
- [ ] Referidos (si está MUY feliz)

---

## 🎁 Bonus: Qué Incluir en la Entrega

1. **Código Completo**
   - Carpeta `itkap_hr_suite/` con todo

2. **Documentación**
   - README.md (manual completo)
   - GUIA_COMERCIAL.md (para él vender)
   - Esta guía rápida

3. **Ejemplos**
   - ejemplo_datos.xlsx
   - Capturas de pantalla
   - Video tutorial (grábalo con Loom)

4. **Extras**
   - Contrato de licencia
   - Factura
   - Recibo de pagos

---

## 🚀 ¡Listo!

Ya tienes TODO para:
1. ✅ Usar el sistema tú mismo
2. ✅ Mostrárselo a Porfirio
3. ✅ Cerrar la venta
4. ✅ Entregarlo profesionalmente

**¿Dudas?**
- Revisa el README.md completo
- Prueba con ejemplo_datos.xlsx
- Experimenta con las configuraciones

**¡A vender!** 💰
