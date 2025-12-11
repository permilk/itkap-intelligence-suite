# 🎨 AGRUPACIÓN DE COMPETENCIAS - Guía Completa

## ✅ NUEVA FUNCIONALIDAD IMPLEMENTADA

### Lo que se agregó:

1. **Agrupación Visual de Competencias en el Heatmap**
   - Las competencias se agrupan en 3 categorías
   - Cada categoría tiene su color distintivo
   - Headers visuales muestran la agrupación

2. **Mapa de Calor de Promedios Organizacionales**
   - Nueva visualización adicional
   - Muestra solo el promedio por competencia
   - Agrupación visual por categoría

3. **Configuración Personalizable**
   - Archivo `config_grupos.py` para personalizar grupos
   - Detección automática basada en palabras clave
   - Fácil de modificar sin programar

---

## 📊 GRUPOS POR DEFECTO

### Grupo 1: Operaciones Administrativas e Intelectuales
**Color:** 🔵 Azul (#6495ED)

**Competencias detectadas automáticamente:**
- Análisis de Problemas
- Aprendizaje
- Control Administrativo
- Enfoque en Resultados
- Organización
- Perseverancia
- Pensamiento Estratégico

**Palabras clave:** Análisis, Aprendizaje, Control, Enfoque, Organización, Perseverancia, Pensamiento, Planificación, Orientación, Estratégico, Resultados, Administrativo, Problemas

---

### Grupo 2: Orientadas a las Relaciones
**Color:** 🔴 Rojo (#DC143C)

**Competencias detectadas automáticamente:**
- Comunicación Efectiva
- Relaciones Interpersonales
- Trabajo en Equipo
- Persuasión
- Negociación

**Palabras clave:** Comunicación, Relación, Interacción, Trabajo en Equipo, Persuasión, Negociación, Colaboración, Influencia, Efectiva, Interpersonal

---

### Grupo 3: Orientadas a Sí Mismo
**Color:** 🟢 Verde (#32CD32)

**Competencias detectadas automáticamente:**
- Delegación Efectiva
- Liderazgo
- Autocontrol
- Iniciativa
- Responsabilidad
- Desarrollo Personal

**Palabras clave:** Delegación, Liderazgo, Autocontrol, Iniciativa, Responsabilidad, Autonomía, Desarrollo, Personal

---

## 🎨 CÓMO SE VE

### En el Heatmap Principal:

```
┌─────────────────────────────────────────────────────────────┐
│  [AZUL: Ops Admin]  [ROJO: Relaciones]  [VERDE: Sí Mismo]  │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────┤
│Anál. │Apren.│Contr.│Comun.│Relac.│Deleg.│Lider.│...   │Prom│
├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼────┤
│ 4.5  │ 4.2  │ 3.8  │ 4.7  │ 4.1  │ 3.9  │ 4.3  │ ...  │4.2 │ Juan (4.21)
│ 3.9  │ 4.1  │ 4.0  │ 3.8  │ 4.2  │ 4.5  │ 3.7  │ ...  │4.0 │ María (4.03)
│ ...  │ ...  │ ...  │ ...  │ ...  │ ...  │ ...  │ ...  │... │ ...
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴────┘
```

### En el Mapa de Promedios:

```
┌─────────────────────────────────────────────────────────────┐
│  [AZUL: Ops Admin]  [ROJO: Relaciones]  [VERDE: Sí Mismo]  │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────┤
│Anál. │Apren.│Contr.│Comun.│Relac.│Deleg.│Lider.│...   │Prom│
├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼────┤
│ 3.8  │ 4.1  │ 3.5  │ 4.2  │ 4.0  │ 3.7  │ 4.1  │ ...  │3.9 │ Promedio Org
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴────┘
```

---

## 🔧 PERSONALIZAR GRUPOS

### Método 1: Editar config_grupos.py

1. **Abrir el archivo:**
   ```
   itkap_hr_suite/config_grupos.py
   ```

2. **Modificar grupos:**
   ```python
   GRUPOS_COMPETENCIAS = {
       'Tu Grupo Personalizado 1': {
           'color': '#FF0000',  # Color en hex
           'keywords': ['Palabra1', 'Palabra2', 'Palabra3']
       },
       'Tu Grupo Personalizado 2': {
           'color': '#00FF00',
           'keywords': ['PalabraA', 'PalabraB']
       }
   }
   ```

3. **Guardar y ejecutar** - Los cambios se aplican automáticamente

### Método 2: Agregar Nuevas Palabras Clave

Si tienes una competencia que no se asigna correctamente:

```python
'Operaciones Administrativas e Intelectuales': {
    'color': '#6495ED',
    'keywords': [
        'Análisis', 
        'Aprendizaje', 
        # ... keywords existentes ...
        'TU_NUEVA_PALABRA',  # <- Agregar aquí
        'OTRA_PALABRA'
    ]
}
```

### Método 3: Cambiar Colores

Colores sugeridos:

```python
# Azules
'#6495ED'  # Azul claro (default)
'#4169E1'  # Azul royal
'#0000FF'  # Azul puro

# Rojos
'#DC143C'  # Carmesí (default)
'#FF0000'  # Rojo puro
'#8B0000'  # Rojo oscuro

# Verdes
'#32CD32'  # Verde lima (default)
'#00FF00'  # Verde puro
'#228B22'  # Verde bosque

# Amarillos
'#FFD700'  # Oro
'#FFFF00'  # Amarillo puro
'#FFA500'  # Naranja

# Morados
'#9370DB'  # Morado medio
'#8A2BE2'  # Violeta azulado
'#4B0082'  # Índigo
```

---

## 📈 EN EL POWERPOINT

El PowerPoint automático ahora incluye:

1. **Slide 1:** Portada
2. **Slide 2:** Resumen Ejecutivo
3. **Slide 3:** Mapa de Calor por Colaborador (con grupos coloreados)
4. **Slide 4:** Mapa de Calor de Promedios (NUEVO)
5. **Slide 5:** Top 10 Colaboradores
6. **Slide 6:** Distribución por Nivel
7. **Slide 7:** Competencias Organizacionales
8. **Slide 8:** Recomendaciones
9. **Slide 9:** Cierre

---

## 📊 EN EL EXCEL

El Excel incluye ahora en la hoja "Estadísticas":
- Columna adicional: "Grupo"
- Cada competencia tiene su grupo asignado
- Fácil filtrar y analizar por grupo

---

## 🎯 CASOS DE USO

### Caso 1: Cliente con Modelo de Competencias Específico

Cliente tiene su propio modelo con 4 categorías:

```python
GRUPOS_COMPETENCIAS = {
    'Técnicas': {
        'color': '#4169E1',
        'keywords': ['Técnico', 'Especializado', 'Conocimiento']
    },
    'Estratégicas': {
        'color': '#DC143C',
        'keywords': ['Estrategia', 'Visión', 'Planificación']
    },
    'Interpersonales': {
        'color': '#32CD32',
        'keywords': ['Relación', 'Comunicación', 'Equipo']
    },
    'Personales': {
        'color': '#FFD700',
        'keywords': ['Auto', 'Iniciativa', 'Desarrollo']
    }
}
```

### Caso 2: Industria Específica (Salud)

```python
GRUPOS_COMPETENCIAS = {
    'Competencias Clínicas': {
        'color': '#0000FF',
        'keywords': ['Diagnóstico', 'Tratamiento', 'Clínico']
    },
    'Competencias Administrativas': {
        'color': '#FF0000',
        'keywords': ['Administrativo', 'Gestión', 'Planificación']
    },
    'Competencias Humanas': {
        'color': '#00FF00',
        'keywords': ['Empatía', 'Comunicación', 'Relación']
    }
}
```

---

## ⚠️ IMPORTANTE

### Detección Automática

El sistema busca las palabras clave en el **NOMBRE** de la competencia.

**Ejemplo:**
- Competencia: "Comunicación Efectiva"
- Sistema busca: "Comunicación" en las keywords
- Encuentra match en: "Orientadas a las Relaciones"
- Asigna: Grupo Rojo

### Prioridad de Asignación

Si una competencia coincide con múltiples grupos:
- Se asigna al **PRIMER** grupo que coincida
- Orden: 1) Operaciones Admin, 2) Relaciones, 3) Sí Mismo

Para cambiar esto, reordena los grupos en `config_grupos.py`

### Competencias Sin Grupo

Si una competencia no coincide con ninguna keyword:
- Se asigna automáticamente al **primer grupo** de la lista
- Recomendación: agregar la palabra clave relevante

---

## 🚀 TESTING

### Probar tus cambios:

1. **Edita config_grupos.py**
2. **Guarda el archivo**
3. **Recarga la aplicación:**
   ```bash
   # Ctrl+C para detener
   streamlit run app.py
   ```
4. **Sube tu archivo Excel**
5. **Verifica** que las competencias estén en los grupos correctos

---

## 📞 SOPORTE

Si una competencia no se agrupa correctamente:

1. Revisa el nombre exacto de la competencia en tu Excel
2. Agrega una palabra clave relevante en `config_grupos.py`
3. Guarda y recarga la aplicación

**Ejemplo:**

```
Competencia en Excel: "Trabajo Colaborativo"
No se asigna correctamente porque falta "Trabajo" en las keywords

Solución:
'Orientadas a las Relaciones': {
    'keywords': ['Comunicación', 'Relación', 'Trabajo', ...]  # <- Agregar
}
```

---

## ✅ CHECKLIST DE CONFIGURACIÓN

Para cada nuevo cliente:

- [ ] Revisar nombres de competencias en su Excel
- [ ] Identificar qué competencias van en cada grupo
- [ ] Editar `config_grupos.py` si es necesario
- [ ] Probar con su archivo real
- [ ] Verificar que los colores sean apropiados
- [ ] Generar reporte de prueba
- [ ] Confirmar con cliente antes de entrega final

---

**¡Listo para usar con cualquier modelo de competencias!** 🎉
