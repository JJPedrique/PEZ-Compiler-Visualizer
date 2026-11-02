# PEZ - C++ Compiler Visualizer

![Build](https://img.shields.io/badge/build-no_configurado-lightgrey)
![Pruebas](https://img.shields.io/badge/tests-no_configuradas-lightgrey)
![Cobertura](https://img.shields.io/badge/coverage-no_disponible-lightgrey)
![Versión](https://img.shields.io/badge/version-sin_release-lightgrey)
![Licencia](https://img.shields.io/badge/license-no_especificada-lightgrey)

PEZ es una aplicación de escritorio educativa para explorar las etapas léxica, sintáctica y semántica del análisis de código C++. Permite editar o importar archivos `.cpp` y visualizar los resultados de cada análisis en una interfaz gráfica.

## Tabla de contenidos

1. [PEZ - C++ Compiler Visualizer](#pez---c-compiler-visualizer)
2. [Tabla de contenidos](#tabla-de-contenidos)
3. [Características principales](#características-principales)
4. [Stack tecnológico](#stack-tecnológico)
5. [Requisitos previos e instalación](#requisitos-previos-e-instalación)
6. [Variables de entorno y configuración](#variables-de-entorno-y-configuración)
7. [Uso y guía rápida](#uso-y-guía-rápida)
8. [Pruebas](#pruebas)
9. [Estructura del proyecto](#estructura-del-proyecto)
10. [Contribución y licencia](#contribución-y-licencia)

## Características principales

- Crear, editar, renombrar y eliminar archivos `.cpp` desde el editor integrado.
- Importar archivos C++ y exportar el contenido del editor a `Downloads/PEZ_Compiler-<fecha>`.
- Ejecutar análisis léxico y consultar la tokenización, los tokens y sus categorías.
- Ejecutar análisis sintáctico y visualizar el árbol generado.
- Ejecutar análisis semántico y consultar símbolos, tipos, ámbitos, niveles, parámetros y memoria.
- Activar o desactivar los visores de análisis y cambiar el modo de apariencia y el tema de color.

> La aplicación analiza un subconjunto de C++; no reemplaza un compilador C++ de propósito general.

## Stack tecnológico

- **Backend y lógica de análisis:** Python; analizadores léxico, sintáctico y semántico propios.
- **Frontend de escritorio:** Tkinter y [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).
- **Imágenes:** Pillow.
- **Base de datos:** no utiliza.
- **DevOps y herramientas:** Git. El repositorio no incluye configuración de CI, contenedores ni empaquetado.

## Requisitos previos e instalación

- Python 3 con Tkinter disponible.
- Git.
- Un entorno de escritorio capaz de ejecutar aplicaciones Tkinter.

Clona el repositorio, crea un entorno virtual e instala las dependencias:

```bash
git clone https://github.com/JJPedrique/PEZ-Compiler-Visualizer.git
cd PEZ-Compiler-Visualizer
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install customtkinter pillow
```

En Windows PowerShell, activa el entorno virtual con:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si Tkinter no está disponible en tu instalación de Python, instala o habilita el componente Tk correspondiente a tu sistema operativo.

## Variables de entorno y configuración

La aplicación no requiere variables de entorno. El repositorio no contiene `.env.example`, por lo que no es necesario crear ni copiar un archivo `.env`.

| Configuración | Propósito |
| --- | --- |
| `src/BackEnd/_Cache.txt` | Guarda el tema de color seleccionado (`blue`, `dark-blue` o `green`). El cambio se aplica al reiniciar la aplicación. |
| `res/` | Contiene el icono y las imágenes que carga la interfaz. Debe conservarse esta carpeta y ejecutarse la aplicación desde la raíz del repositorio. |

## Uso y guía rápida

Desde la raíz del repositorio y con las dependencias instaladas, inicia la aplicación en desarrollo:

```bash
python src/main.py
```

1. En la pestaña **Editor**, crea un archivo `.cpp` o selecciónalo después de importarlo.
2. Escribe o modifica el código y pulsa el botón de compilar.
3. Consulta las pestañas **Léxico**, **Sintáctico** y **Semántico** para revisar los resultados.
4. En **Opciones**, configura los visores, el modo de apariencia y el tema.
5. Usa **Importar** y **Exportar** en **Opciones** para gestionar archivos.

Como ejemplo, puedes importar uno de los archivos de `res/C++ Examples/`, como `FizzBuzz.cpp` o `TablaMultiplicar.cpp`. La aplicación se ejecuta directamente con Python; no hay un comando o perfil de producción separado.

## Pruebas

El repositorio no incluye pruebas automatizadas ni configuración de cobertura; no hay comandos de pruebas unitarias, integración o cobertura disponibles.

Para comprobar manualmente que la aplicación inicia correctamente, ejecuta desde la raíz del proyecto:

```bash
python src/main.py
```

## Estructura del proyecto

```text
PEZ-Compiler-Visualizer/
├── README.md
├── res/                         # Icono, imágenes y ejemplos C++
│   └── C++ Examples/
├── src/
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── BackEnd/                 # Analizadores, árbol, errores y datos
│   └── FrontEnd/                # Editor, pestañas y ventanas de interfaz
└── .gitignore
```

## Contribución y licencia

Para contribuir:

1. Haz un fork del repositorio y clónalo localmente.
2. Crea una rama para tu cambio: `git switch -c feature/mi-cambio`.
3. Implementa el cambio y verifica manualmente la aplicación.
4. Crea un commit descriptivo y sube la rama a tu fork.
5. Abre un Pull Request hacia el repositorio original.

**Licencia:** no se encontró un archivo de licencia ni una declaración del tipo de licencia en el repositorio. Consulta con los mantenedores antes de redistribuir o reutilizar el software.
