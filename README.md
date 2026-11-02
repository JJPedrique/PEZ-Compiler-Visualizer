# PEZ - C++ Compiler Visualizer

![Estado de compilación](https://img.shields.io/badge/build-no_configurado-lightgrey)
![Pruebas](https://img.shields.io/badge/tests-no_configuradas-lightgrey)
![Cobertura](https://img.shields.io/badge/coverage-no_disponible-lightgrey)
![Versión](https://img.shields.io/badge/version-sin_release-lightgrey)
![Licencia](https://img.shields.io/badge/license-no_especificada-lightgrey)

Aplicación de escritorio educativa para explorar las etapas léxica, sintáctica y semántica del análisis de código C++. Permite editar o importar archivos `.cpp` y visualizar los resultados de cada análisis en una interfaz gráfica.

## Tabla de contenidos

- [Características principales](#características-principales)
- [Stack tecnológico](#stack-tecnológico)
- [Requisitos previos e instalación](#requisitos-previos-e-instalación)
- [Variables de entorno y configuración](#variables-de-entorno-y-configuración)
- [Uso y guía rápida](#uso-y-guía-rápida)
- [Pruebas](#pruebas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Contribución y licencia](#contribución-y-licencia)

## Características principales

- Crear, editar, renombrar y eliminar archivos de código `.cpp` desde el editor integrado.
- Importar archivos C++ y exportar el contenido del editor a la carpeta `Downloads/PEZ_Compiler-<fecha>`.
- Ejecutar análisis léxico y consultar la tokenización, los tokens y sus categorías.
- Ejecutar análisis sintáctico y visualizar el árbol generado.
- Ejecutar análisis semántico y consultar símbolos, tipos, ámbitos, niveles y parámetros.
- Activar o desactivar los visores de análisis y cambiar el modo de apariencia y el tema de color.

> La aplicación visualiza análisis implementados para un subconjunto de C++; no reemplaza un compilador C++ de propósito general.

## Stack tecnológico

- **Interfaz de escritorio:** Python, Tkinter y [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).
- **Procesamiento:** analizadores léxico, sintáctico y semántico implementados en Python.
- **Imágenes:** Pillow.
- **Base de datos:** no utiliza.
- **DevOps y herramientas:** Git; no se encontró configuración de CI, empaquetado ni contenedores.

## Requisitos previos e instalación

- Python 3 instalado, con Tkinter disponible.
- Git para clonar el repositorio.
- Un entorno de escritorio capaz de ejecutar aplicaciones Tkinter.

Clona el repositorio y ejecuta los comandos desde la carpeta del proyecto (donde están `scr/` y `res/`). La aplicación usa rutas relativas para cargar recursos.

```bash
git clone https://github.com/JJPedrique/PEZ-Compiler-Visualizer.git
cd "PEZ-Compiler-Visualizer/PEZ Compiler Visualizer"
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install customtkinter pillow
```

En Windows PowerShell, activa el entorno virtual con:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Variables de entorno y configuración

El proyecto no requiere variables de entorno y no incluye un archivo `.env.example`. No es necesario crear un archivo `.env`.

La preferencia de tema se guarda en `scr/BackEnd/_Cache.txt`. El tema debe ser uno de los valores admitidos por CustomTkinter que la aplicación ofrece: `blue`, `dark-blue` o `green`. Los recursos de interfaz se cargan desde `res/`, por lo que inicia la aplicación desde la carpeta `PEZ Compiler Visualizer`.

## Uso y guía rápida

Desde la carpeta `PEZ Compiler Visualizer`, inicia la aplicación en desarrollo con:

```bash
python scr/main.py
```

1. En la pestaña **Editor**, crea un archivo `.cpp` o selecciona uno importado.
2. Escribe o modifica el código y pulsa el botón de compilar.
3. Consulta las pestañas **Léxico**, **Sintáctico** y **Semántico** para revisar los resultados.
4. En **Opciones**, configura los visores, la apariencia y el tema. Los cambios de tema se aplican al reiniciar.
5. Usa **Importar** y **Exportar** en **Opciones** para gestionar archivos.

No se encontró un comando o perfil de producción separado; la aplicación se ejecuta mediante el mismo punto de entrada de Python.

## Pruebas

El repositorio no incluye una suite de pruebas automatizadas ni configuración de cobertura. Por tanto, no hay comandos de pruebas o cobertura disponibles.

Para comprobar que la aplicación abre correctamente, instala las dependencias y ejecuta:

```bash
python scr/main.py
```

## Estructura del proyecto

```text
PEZ-Compiler-Visualizer/
├── README.md
└── PEZ Compiler Visualizer/
    ├── scr/
    │   ├── main.py                 # Punto de entrada de la aplicación
    │   ├── BackEnd/                # Analizadores, árbol, errores y datos
    │   └── FrontEnd/               # Editor, pestañas y ventanas de interfaz
    ├── res/                        # Icono e imágenes de la interfaz
    ├── Informes/                   # Documentación y material del proyecto
    ├── FizzBuzz.cpp                # Ejemplo de código C++
    └── TablaMultiplicar.cpp        # Ejemplo de código C++
```

## Contribución y licencia

Para contribuir:

1. Haz un fork del repositorio y clónalo localmente.
2. Crea una rama para tu cambio: `git switch -c feature/mi-cambio`.
3. Implementa el cambio y verifica manualmente la aplicación.
4. Crea un commit descriptivo y sube la rama a tu fork.
5. Abre un Pull Request hacia la rama principal del repositorio.

**Licencia:** el repositorio no contiene un archivo de licencia ni declara un tipo de licencia. Consulta con los mantenedores antes de redistribuir o reutilizar el software.
