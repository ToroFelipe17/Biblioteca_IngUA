# Sistema de Gestión de Biblioteca – Evaluación Ingeniería de Software

> Proyecto individual desarrollado por Felipe Toro  
> Universidad Autónoma, 2025


## 📚 Descripción

Sistema de gestión de biblioteca implementado en Python, orientado a la consola, aplicando principios SOLID y mejores prácticas de desarrollo de software.  
Permite gestionar usuarios, libros y préstamos, con registro de multas y validación mediante pruebas unitarias (PyTest).


## 🚀 Características principales

- Registrar y listar usuarios
- Agregar y buscar libros
- Prestar y devolver libros (con cálculo automático de multas)
- Visualización de préstamos activos y devueltos
- Diseño modular y responsable (SRP, OCP, LSP, DIP)
- Pruebas unitarias con PyTest
- Análisis de calidad con SonarQube/SonarCloud
- Control de versiones con Git y repositorio en GitHub


## 🛠️ Instalación y uso

### 1. Clona el repositorio


git clone https://github.com/ToroFelipe17/biblioteca_ingenieria_software.git

cd biblioteca_ingenieria_software

2. Crea entorno virtual e instala dependencias

python3 -m venv .venv
source .venv/bin/activate    
pip install -r requirements.txt

3. Ejecuta el sistema

python biblioteca.py

4. Ejecuta las pruebas unitarias

pytest

🧪 Estructura del proyecto


biblioteca.py         # Código principal (clases y funciones)
test_biblioteca.py    # Pruebas unitarias con PyTest
requirements.txt      # Dependencias del proyecto (al menos pytest)
README.md             # Este archivo

💡 Principios SOLID aplicados

SRP (Single Responsibility Principle): Cada clase tiene una única responsabilidad (Libro, Usuario, Biblioteca, Prestamo, etc.).

OCP (Open/Closed Principle): Las clases base pueden ser extendidas sin modificar el código existente.

LSP (Liskov Substitution Principle): Las subclases (Prestamo) pueden reemplazar a la clase base (PrestamoBase) sin afectar el sistema.

ISP (Interface Segregation Principle): Las clases implementan solo las interfaces necesarias.

DIP (Dependency Inversion Principle): La clase Biblioteca depende de abstracciones (RepositorioLibros), no de implementaciones concretas.

🔎 Análisis de calidad con SonarQube/SonarCloud

El código fue analizado usando SonarCloud, verificando calidad, cobertura de pruebas y ausencia de bugs críticos.

Evidencia:



📝 Autor

Felipe Toro Bustamante
[GitHub](https://github.com/ToroFelipe17)

📑 Licencia

Este proyecto es solo para fines académicos y formativos.
