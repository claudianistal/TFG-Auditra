#!/usr/bin/env python
"""
Script para compilar la aplicación TFG-Auditra a .exe con PyInstaller
Ejecutar: python build.py
"""
import subprocess
import sys
import os

def build():
    """Compila la aplicación con PyInstaller con la configuración correcta"""
    
    # Ruta del ícono
    icon_path = os.path.join("frontend", "public", "LogoSinFondo.png")
    
    # Comando de PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Auditra",
        f"--icon={icon_path}",
        "--add-data=frontend/dist;frontend/dist",
        "backend/app/main.py"
    ]
    
    print("Compilando la aplicación con PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ ¡Compilación exitosa!")
        print("📦 El ejecutable está en: dist/Auditra.exe")
    else:
        print("\n❌ Error durante la compilación")
        sys.exit(1)

if __name__ == "__main__":
    build()
