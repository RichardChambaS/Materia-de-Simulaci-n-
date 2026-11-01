# Práctica 05: Generador Congruencial Lineal

Implementación básica del generador LCG en **Java y Python**, organizada en Modelo, Vista y Controlador (MVC), con salida por consola.

Cada programa genera 10 000 valores. Python compara sus resultados con el CSV de Java y crea gráficas para mostrar la coincidencia entre lenguajes y el efecto de cambiar la semilla.

## Requisitos

- JDK 11 o superior, con `java` y `javac` disponibles en la terminal.
- Python 3 con el módulo `venv` disponible.
- Matplotlib, instalado con las instrucciones siguientes.

Ejecutar todos los comandos **desde la carpeta `practica05-simulacion`**, que contiene este README. Así ambos programas guardan y buscan los archivos en la misma carpeta `resultados`.

## Linux

### 1. Preparar Python (solo la primera vez)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r python/requirements.txt
```

Si el sistema indica que falta `venv`, instala el paquete correspondiente a tu distribución (por ejemplo, `python3-venv` en Ubuntu/Debian) y repite el comando.

### 2. Compilar Java

```bash
javac -encoding UTF-8 -d java/bin java/Main.java java/modelo/GeneradorLCG.java java/vista/VistaConsola.java java/controlador/ControladorLCG.java
```

Repite la compilación si modificas los archivos Java.

### 3. Ejecutar y generar las comparaciones

```bash
java -cp java/bin Main 12345
.venv/bin/python python/main.py 12345 --comparar-semilla 54321
```

Para comprobar también la coincidencia entre Java y Python con la segunda semilla:

```bash
java -cp java/bin Main 54321
.venv/bin/python python/main.py 54321
```

## Windows (PowerShell o CMD)

### 1. Preparar Python (solo la primera vez)

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r python\requirements.txt
```

Si el comando `py` no está disponible, utiliza `python` en su lugar. Los comandos llaman directamente al Python del entorno virtual; no es necesario activarlo.

### 2. Compilar Java

```powershell
javac -encoding UTF-8 -d java\bin java\Main.java java\modelo\GeneradorLCG.java java\vista\VistaConsola.java java\controlador\ControladorLCG.java
```

Repite la compilación si modificas los archivos Java.

### 3. Ejecutar y generar las comparaciones

```powershell
java -cp java\bin Main 12345
.venv\Scripts\python.exe python\main.py 12345 --comparar-semilla 54321
```

Para comprobar también la coincidencia entre Java y Python con la segunda semilla:

```powershell
java -cp java\bin Main 54321
.venv\Scripts\python.exe python\main.py 54321
```

## Semillas y resultados

La semilla debe ser un entero entre `0` y `4294967295`. Si se omite, el programa la solicita por consola; al pulsar Enter utiliza `12345`.

**Ejecuta Java antes que Python con la misma semilla** para obtener la tabla y la gráfica comparativa. Si falta el CSV de Java, Python muestra un aviso y genera sus propios datos y la gráfica de su secuencia.

Con la semilla `12345` y `--comparar-semilla 54321` se generan:

| Archivo en `resultados/` | Contenido |
| --- | --- |
| `java_12345.csv` | Los 10 000 valores generados por Java. |
| `python_12345.csv` | Los 10 000 valores generados por Python. |
| `comparacion_12345.csv` | Comparación de los valores enteros y normalizados de ambos lenguajes. |
| `secuencia_12345.png` | Gráfica de la secuencia normalizada. |
| `java_python_12345.png` | Primeras 20 observaciones y diferencia entre los 10 000 valores. |
| `semillas_12345_54321.png` | Comparación de dos semillas en Python: primeras 20 observaciones e histogramas. |

Las imágenes se guardan como PNG; no se abre una ventana gráfica. Puedes abrirlas desde el explorador de archivos e incorporarlas a una presentación.

## Estructura

```text
java/
  modelo/          Datos y fórmula del generador.
  vista/           Presentación por consola.
  controlador/     Coordinación y exportación a CSV.
  Main.java        Inicio del programa Java.
python/
  modelo/          Datos y fórmula del generador.
  vista/           Consola y gráficas.
  controlador/     Coordinación, exportación y comparación.
  main.py          Inicio del programa Python.
  requirements.txt
```

Ambas versiones implementan `X siguiente = (a * X actual + c) mod m` y `U = X / m`, con `a = 1664525`, `c = 1013904223` y `m = 2^32`. Con los mismos parámetros y semilla deben producir exactamente la misma secuencia.

El `.gitignore` excluye documentos académicos, resultados generados, archivos compilados, entornos virtuales y temporales. Estos archivos se conservan localmente y no se incluyen al subir el proyecto.
