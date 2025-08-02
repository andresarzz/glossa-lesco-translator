"""
Script de configuración para GLOSSA
Instala automáticamente las dependencias necesarias
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala las dependencias del archivo requirements.txt"""
    try:
        print("🔧 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def main():
    print("🚀 Configurando GLOSSA - Traductor de LESCO")
    print("=" * 50)
    
    # Verificar versión de Python
    if not check_python_version():
        return
    
    # Instalar dependencias
    if not install_requirements():
        return
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Para ejecutar la aplicación:")
    print("   python main.py")
    print("\n📚 Palabras disponibles:")
    palabras = ["hola", "gracias", "por favor", "si", "no", "agua", "comer", "casa", "familia", "trabajo"]
    print("   " + ", ".join(palabras))

if __name__ == "__main__":
    main()
