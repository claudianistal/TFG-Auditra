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
    
    # Obtener ruta del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_path = os.path.join(project_root, "backend")
    
    # Ruta del ícono
    icon_path = os.path.join(project_root, "frontend", "public", "LogoSinFondo.png")
    main_file = os.path.join(backend_path, "app", "main.py")
    
    # Rutas para incluir datos
    frontend_dist = os.path.join(project_root, "frontend", "dist")
    
    # Comando de PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Auditra",
        f"--icon={icon_path}",
        f"--paths={backend_path}",
        f"--add-data={frontend_dist}{os.pathsep}frontend/dist",  # Usar os.pathsep para Windows/Linux compatibility
        "--collect-all=fastapi",
        "--collect-all=uvicorn",
        "--collect-all=pywebview",
        main_file
    ]
    
    print("Compilando la aplicación con PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n¡Compilación exitosa!")
        print("El ejecutable está en: dist/Auditra.exe")
    else:
        print("\nError durante la compilación")
        sys.exit(1)

if __name__ == "__main__":
    build()
