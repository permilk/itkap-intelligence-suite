# Configuración de Grupos de Competencias
# Este archivo permite personalizar cómo se agrupan las competencias en el mapa de calor

# Formato:
# Grupo 1: Color (Hex), [lista de palabras clave]
# Grupo 2: Color (Hex), [lista de palabras clave]
# etc.

GRUPOS_COMPETENCIAS = {
    'Operaciones Administrativas e Intelectuales': {
        'color': '#6495ED',  # Azul
        'keywords': [
            'Análisis', 
            'Aprendizaje', 
            'Control', 
            'Enfoque', 
            'Organización', 
            'Perseverancia', 
            'Pensamiento', 
            'Planificación', 
            'Orientación',
            'Estratégico',
            'Resultados',
            'Administrativo',
            'Problemas',
            'Intelectual'
        ]
    },
    'Orientadas a las Relaciones': {
        'color': '#DC143C',  # Rojo
        'keywords': [
            'Comunicación', 
            'Relación', 
            'Interacción', 
            'Trabajo en Equipo',
            'Persuasión', 
            'Negociación', 
            'Colaboración', 
            'Influencia',
            'Efectiva',
            'Interpersonal',
            'Social'
        ]
    },
    'Orientadas a Sí Mismo': {
        'color': '#32CD32',  # Verde
        'keywords': [
            'Delegación', 
            'Liderazgo', 
            'Autocontrol', 
            'Iniciativa',
            'Responsabilidad', 
            'Autonomía', 
            'Desarrollo',
            'Efectiva',
            'Personal',
            'Auto'
        ]
    }
}

# CÓMO PERSONALIZAR:
# 
# 1. Puedes cambiar los nombres de los grupos
# 2. Puedes cambiar los colores (usa códigos hex como #FF0000 para rojo)
# 3. Puedes agregar más palabras clave a cada grupo
# 4. El sistema buscará estas palabras en los nombres de las competencias
# 
# EJEMPLO:
# Si tienes una competencia llamada "Comunicación Verbal", 
# el sistema la asignará a "Orientadas a las Relaciones" porque 
# contiene la palabra "Comunicación" en las keywords.
#
# COLORES SUGERIDOS:
# Azul: #6495ED, #4169E1, #0000FF
# Rojo: #DC143C, #FF0000, #8B0000
# Verde: #32CD32, #00FF00, #228B22
# Amarillo: #FFD700, #FFFF00, #FFA500
# Morado: #9370DB, #8A2BE2, #4B0082
