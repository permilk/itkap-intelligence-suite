"""
Script de Verificación - ITKAP Intelligence Suite
Verifica que no haya errores de sintaxis en el código principal
"""

import sys

def verificar_imports():
    """Verifica que todos los imports necesarios estén disponibles"""
    print("🔍 Verificando dependencias...")
    
    modulos_requeridos = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'streamlit_option_menu': 'streamlit-option-menu',
        'openpyxl': 'openpyxl'
    }
    
    faltantes = []
    
    for modulo, nombre_pip in modulos_requeridos.items():
        try:
            __import__(modulo)
            print(f"  ✅ {modulo}")
        except ImportError:
            print(f"  ❌ {modulo} - Instalar con: pip install {nombre_pip}")
            faltantes.append(nombre_pip)
    
    if faltantes:
        print(f"\n⚠️  Faltan dependencias. Ejecuta:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas correctamente")
        return True

def verificar_sintaxis():
    """Verifica que el archivo principal no tenga errores de sintaxis"""
    print("\n🔍 Verificando sintaxis del código...")
    
    try:
        with open('hr_competencias_app_professional.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        compile(codigo, 'hr_competencias_app_professional.py', 'exec')
        print("  ✅ Sin errores de sintaxis")
        return True
    except SyntaxError as e:
        print(f"  ❌ Error de sintaxis en línea {e.lineno}: {e.msg}")
        return False
    except FileNotFoundError:
        print("  ❌ Archivo 'hr_competencias_app_professional.py' no encontrado")
        return False

def verificar_estructura():
    """Verifica que la estructura del código sea correcta"""
    print("\n🔍 Verificando estructura del código...")
    
    try:
        with open('hr_competencias_app_professional.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar elementos clave
        elementos = {
            'st.set_page_config': 'Configuración de página',
            'def cargar_datos': 'Función de carga de datos',
            'def generar_reporte_html': 'Función de generación de reportes',
            'def plot_radar_chart': 'Función de gráfico radar',
            'def plot_gap_analysis': 'Función de análisis de brechas',
            'def plot_top_performers': 'Función de rankings',
            'def plot_heatmap': 'Función de matriz de calor',
            'option_menu': 'Menú de navegación'
        }
        
        todos_presentes = True
        for elemento, descripcion in elementos.items():
            if elemento in contenido:
                print(f"  ✅ {descripcion}")
            else:
                print(f"  ❌ Falta: {descripcion}")
                todos_presentes = False
        
        return todos_presentes
        
    except FileNotFoundError:
        print("  ❌ Archivo no encontrado")
        return False

def main():
    """Función principal de verificación"""
    print("=" * 60)
    print("ITKAP Intelligence Suite - Verificación del Sistema")
    print("=" * 60)
    
    resultado_imports = verificar_imports()
    resultado_sintaxis = verificar_sintaxis()
    resultado_estructura = verificar_estructura()
    
    print("\n" + "=" * 60)
    if resultado_imports and resultado_sintaxis and resultado_estructura:
        print("✅ VERIFICACIÓN EXITOSA")
        print("La aplicación está lista para ejecutarse.")
        print("\nPara iniciar la aplicación ejecuta:")
        print("  streamlit run hr_competencias_app_professional.py")
    else:
        print("❌ VERIFICACIÓN FALLIDA")
        print("Revisa los errores mostrados arriba.")
    print("=" * 60)

if __name__ == "__main__":
    main()
