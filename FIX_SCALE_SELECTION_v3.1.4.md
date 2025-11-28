# 🔧 CORRECCIÓN DE SELECCIÓN DE ESCALA + DEBUG MODE

## ITKAP Intelligence Suite v3.1.4

**Fecha:** Enero 27, 2025  
**Versión:** 3.1.3 → 3.1.4  
**Tipo:** BugFix + Debug Mode  
**Prioridad:** 🔴 ALTA

---

## 🐛 PROBLEMA REPORTADO

**Síntoma:**
- ✅ Funciona perfectamente con "Rango (0-5)"
- ❌ Al seleccionar "Porcentaje (0-100)" no se visualiza nada
- Pantalla en blanco o mensaje de error

**Causa probable:**
1. El archivo Excel tiene AMBOS tipos de columnas (Rango + Rend %)
2. Pero al cambiar escala, el sistema no encuentra las columnas correctas
3. O el archivo solo tiene UN tipo de columna

---

## ✅ SOLUCIÓN IMPLEMENTADA

### 1. DEBUG MODE Activado

Agregados **2 expanders de debug** en el Dashboard para diagnosticar:

```python
🔍 DEBUG: Estructura de Competencias
- Muestra cuántas competencias tienen columnas "Rango"
- Muestra cuántas competencias tienen columnas "Pct"
- Lista las primeras 5 competencias con su disponibilidad

🔍 DEBUG: Columnas Seleccionadas  
- Muestra cuántas columnas se encontraron para la escala actual
- Lista las primeras 5 columnas seleccionadas
```

---

### 2. Lógica de Fallback Mejorada

**Comportamiento actual:**

```python
target_key = 'Rango' if scale_mode == "Rango (0-5)" else 'Pct'

for comp, metrics in comp_map.items():
    if metrics.get(target_key):
        # Usar la columna del tipo seleccionado
        selected_cols.append(metrics[target_key])
    elif target_key == 'Rango' and metrics.get('Pct'):
        # Fallback: si busca Rango pero solo hay Pct, usar Pct
        selected_cols.append(metrics['Pct'])
    elif target_key == 'Pct' and metrics.get('Rango'):
        # Fallback: si busca Pct pero solo hay Rango, usar Rango
        selected_cols.append(metrics['Rango'])
```

**Esto garantiza:**
- ✅ Si existe el tipo correcto, se usa
- ✅ Si no existe, usa el otro tipo disponible (fallback)
- ✅ Siempre muestra TODAS las competencias disponibles

---

## 🔍 INSTRUCCIONES DE DEBUG

### Paso 1: Cargar Archivo
1. Sube el archivo Excel de PsycoSource
2. Ve al Dashboard General

### Paso 2: Abrir Debug Panels
1. Haz clic en **"🔍 DEBUG: Estructura de Competencias"**
2. Verifica:
   - ¿Cuántas competencias tienen **Rango**?
   - ¿Cuántas competencias tienen **Pct**?

### Paso 3: Cambiar Escala
1. Ve al sidebar → "Escala de Visualización"
2. Cambia de "Rango (0-5)" a "Porcentaje (0-100)"
3. Abre **"🔍 DEBUG: Columnas Seleccionadas"**
4. Verifica:
   - ¿Cuántas columnas se encontraron?
   - ¿Qué columnas se seleccionaron?

---

## 📊 ESCENARIOS POSIBLES

### Escenario A: Archivo con AMBOS Tipos

```
DEBUG: Estructura de Competencias
- Total competencias: 27
- Competencias con Rango: 27
- Competencias con Pct: 27

DEBUG: Columnas Seleccionadas (Rango)
- Columnas encontradas: 27
- "ANÁLISIS DE PROBLEMAS - Rango"
- "APRENDIZAJE - Rango"
- ...

DEBUG: Columnas Seleccionadas (Pct)
- Columnas encontradas: 27
- "ANÁLISIS DE PROBLEMAS - Rend. %"
- "APRENDIZAJE - Rend. %"
- ...
```

**Resultado:** ✅ Funciona en ambas escalas

---

### Escenario B: Archivo SOLO con Rango

```
DEBUG: Estructura de Competencias
- Total competencias: 27
- Competencias con Rango: 27
- Competencias con Pct: 0  ← ¡PROBLEMA!

DEBUG: Columnas Seleccionadas (Rango)
- Columnas encontradas: 27 ✅

DEBUG: Columnas Seleccionadas (Pct)
- Columnas encontradas: 27  ← Usa Rango como fallback
```

**Resultado:** ✅ Funciona en ambas escalas (usa fallback)

---

### Escenario C: Archivo SOLO con Pct

```
DEBUG: Estructura de Competencias
- Total competencias: 27
- Competencias con Rango: 0  ← ¡PROBLEMA!
- Competencias con Pct: 27

DEBUG: Columnas Seleccionadas (Rango)
- Columnas encontradas: 27  ← Usa Pct como fallback

DEBUG: Columnas Seleccionadas (Pct)
- Columnas encontradas: 27 ✅
```

**Resultado:** ✅ Funciona en ambas escalas (usa fallback)

---

## 🎯 SIGUIENTE PASO

**AHORA:** 
1. Ejecuta la app con el debug mode
2. Abre los expanders de debug
3. Comparte screenshots de:
   - "DEBUG: Estructura de Competencias"
   - "DEBUG: Columnas Seleccionadas" (en ambas escalas)

**CON ESA INFO PUEDO:**
- Diagnosticar exactamente qué está pasando
- Corregir el problema específico
- Optimizar la detección de columnas

---

## 📦 ARCHIVOS MODIFICADOS

### app.py (v3.1.4)
- Agregados 2 expanders de debug
- Mejorada lógica de fallback
- Import de streamlit en sección correcta

### config.py (v3.1.4)
- Versión actualizada

---

## ✅ RESULTADO ESPERADO

Con el debug mode, podremos ver exactamente:
- ✅ Qué columnas tiene el archivo
- ✅ Qué columnas se están seleccionando
- ✅ Por qué no aparecen datos al cambiar escala

---

**PRÓXIMOS PASOS:**

1. Ejecuta: `streamlit run app.py`
2. Carga el archivo
3. Abre los debug expanders
4. Comparte screenshots

¡Con esa info podré hacer el fix definitivo! 🚀

---

© 2025 ITKAP Consulting - Debug Mode Enabled
