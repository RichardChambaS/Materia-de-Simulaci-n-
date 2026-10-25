# Informe APE 004 en LaTeX

El archivo principal es `ape04_sir.tex`. El PDF compilado es `ape04_sir.pdf`.
El documento conserva el formato institucional compartido y adapta sus contenidos
al modelo SIR de la Guía APE 004 y al trabajo realizado con Java y NetLogo.

## Abrir en Overleaf

1. Descarga `ape04_sir_overleaf.zip`.
2. En Overleaf selecciona **New Project → Upload Project** y carga el ZIP.
3. Selecciona `ape04_sir.tex` como documento principal y compila con pdfLaTeX.
4. Conserva las carpetas `assets/` y `figures/` junto al archivo principal.

El paquete incluye el logo de la plantilla, las seis gráficas vectoriales, los CSV
que sustentan las figuras y los scripts utilizados para exportarlas o trazarlas.
Las citas están incluidas en el propio `.tex`; no hace falta un archivo `.bib`.

## Contenido y alcance

- Metodología: reglas SIR, actualización simultánea, organización MVC, ejecución
  Java, exportación y sincronización de parámetros y resultados con NetLogo.
- Cinco figuras de la corrida base y una figura con el cambio de gamma a 0.40.
- Resumen de resultados, comparación de experiencia, análisis y diez preguntas.
- Conclusiones, declaración de uso de IA y bibliografía verificable.
- Autor tomado del informe existente: Richard Ariel Chamba Santin.
- Fechas académicas de la guía: 22 y 23 de octubre de 2026.
- Preparación de los datos del informe: 24 de octubre de 2026.

La comparación experimental corresponde a Java y NetLogo. Python/SimPy se trata
conceptualmente en las preguntas y figura como no implementado en la tabla.
Python/Matplotlib se utilizó para trazar los CSV del informe.

## Datos de referencia

`data/resultados_java.csv` y `data/resultados_netlogo.csv` contienen la corrida base:
N=100, I inicial=5, beta=0.30, gamma=0.10, 100 pasos y semilla 42.
`data/gamma040_java.csv` y `data/gamma040_netlogo.csv` contienen la prueba de gamma=0.40.
Cada archivo tiene encabezado y 101 filas numéricas. Los archivos de parámetros,
las salidas de consola y `data/resumen_resultados.json` permiten comprobar los valores.

Las figuras son reproducciones gráficas de esos datos exportados, no capturas de
pantalla ni resultados de un motor SIR escrito en Python.

## Regenerar las gráficas

Desde la raíz del repositorio, con Python y Matplotlib disponibles:

```bash
python reports/scripts/generar_figuras.py
```

El script escribe PDF vectorial y PNG de cada figura en `reports/figures/`.
La configuración de gamma=0.40 se ejecutó en una copia temporal del proyecto;
el proyecto principal conserva gamma=0.10.

## Exportar una corrida de NetLogo

El script Java utiliza el mismo archivo `.nlogox` del proyecto. El ejemplo supone
NetLogo instalado en `/opt/netlogo` y un JDK 17 o posterior para el exportador:

```bash
javac --release 17 -cp '/opt/netlogo/lib/app/*' -d /tmp \
  reports/scripts/ExportarInformeNetLogo.java
/opt/netlogo/lib/runtime/bin/java \
  -Dnetlogo.extensions.dir=/opt/netlogo/extensions \
  -cp '/opt/netlogo/lib/app/*:/tmp' ExportarInformeNetLogo \
  netlogo/modelo_sir_netlogo.nlogox reports/data/resultados_netlogo.csv
```

Se ejecutan `setup`, `set PAUSA 0` y los pasos definidos por `tiempo-maximo`.
El modelo carga los parámetros Java situados en su carpeta.

Si cambias los parámetros para preparar otro informe, actualiza las instantáneas
Java y NetLogo, regenera las figuras y revisa las cifras escritas en el `.tex`.
Los datos guardados del informe corresponden a las corridas documentadas.
