# Práctica 06: Validación de números pseudoaleatorios

Implementación sencilla en **Java y Python**, organizada en **Modelo, Vista y Controlador (MVC)**. Genera números con el método congruencial lineal (LCG), aplica las pruebas **Chi-cuadrado** y **Kolmogorov-Smirnov (KS)** y guarda gráficas y tablas CSV.

Al iniciar puedes elegir el **caso base de la práctica** o **ingresar tus propios datos** por consola. **No necesitas modificar el código para realizar otro análisis.** Al terminar puedes escribir `s` para volver al menú o pulsar Enter para salir.

## 1. Requisitos

- **JDK 11 o superior**, con `java` y `javac` disponibles en la terminal. Java usa únicamente su biblioteca estándar; no necesita Maven ni Python para generar sus gráficas.
- **Python 3.10 o superior**, con `pip` y `venv`.
- Matplotlib para las gráficas de Python y SciPy para calcular valores p. Se instalan con los comandos siguientes.

Ejecuta todos los comandos **desde la carpeta `practica06-simulacion`**, donde se encuentra este README. Java guarda sus resultados respecto de la carpeta actual; Python los guarda respecto de la carpeta del proyecto.

## 2. Ejecución en Linux

### Preparar Python (solo la primera vez)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r python/requirements.txt
```

Si falta `venv`, en Ubuntu/Debian puedes instalarlo con `sudo apt install python3-venv`. Si falta el JDK, instala `default-jdk`. Necesitas conexión a Internet para descargar las dependencias de Python.

### Compilar y ejecutar Java

```bash
javac -encoding UTF-8 --release 11 -d java/bin java/Main.java java/modelo/Simulacion.java java/vista/Vista.java java/controlador/Controlador.java
java -cp java/bin Main
```

Solo es necesario volver a compilar si cambias el código Java. Cambiar valores desde la consola no requiere recompilar.

### Ejecutar Python

```bash
.venv/bin/python python/main.py
```

### Comparar ambos lenguajes

Después de ejecutar Java y Python con los mismos parámetros:

```bash
.venv/bin/python python/comparar.py
```

## 3. Ejecución en Windows (PowerShell o CMD)

Instala Python y un JDK, y comprueba que `java -version` y `javac -version` funcionan. Abre la terminal dentro de la carpeta del proyecto.

### Preparar Python (solo la primera vez)

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r python\requirements.txt
```

Si no tienes el comando `py`, utiliza `python` en su lugar. Se llama directamente al Python del entorno virtual, así que no necesitas activarlo ni cambiar la política de PowerShell.

### Compilar y ejecutar Java

```powershell
javac -encoding UTF-8 --release 11 -d java\bin java\Main.java java\modelo\Simulacion.java java\vista\Vista.java java\controlador\Controlador.java
java -cp java\bin Main
```

### Ejecutar Python

```powershell
.venv\Scripts\python.exe python\main.py
```

### Comparar ambos lenguajes

```powershell
.venv\Scripts\python.exe python\comparar.py
```

Si la consola presenta problemas con tildes, usa una terminal con UTF-8; en CMD puedes ejecutar `chcp 65001` antes del programa.

## 4. Ingreso de valores

Ambas versiones muestran este menú al iniciar y al repetir un análisis:

```text
1. Caso base de la práctica
2. Ingresar mis propios datos
Selecciona una opción [1]:
```

- **Opción 1 o Enter:** ejecuta directamente con los valores de la tabla siguiente, sin pedir cada parámetro. Antes de calcular, muestra la configuración utilizada. N=10000, k=10 y alfa=0.05 corresponden a la guía; los parámetros LCG conservan la configuración base de la práctica anterior.
- **Opción 2:** solicita todos los parámetros por consola. En cada pregunta puedes escribir un valor o pulsar **Enter** para aceptar el sugerido.

El orden de los parámetros es el mismo en ambas versiones:

| Parámetro | Valor inicial | Valores permitidos |
|---|---:|---|
| Cantidad N | 10000 | Entero de 50 a 1000000 |
| Módulo m | 4294967296 | Entero de 2 a 4503599627370496 (2^52) |
| Multiplicador a | 1664525 | Entero de 0 a m−1 |
| Incremento c | 1013904223 | Entero de 0 a m−1 |
| Semilla | 12345 | Entero de 0 a m−1 |
| Intervalos k | 10 | Entero de 2 a min(100, N/5) |
| Significancia alfa | 0.05 | Número mayor que 0 y menor que 1 |

Si eliges un módulo pequeño, los valores sugeridos de `a`, `c` y semilla se reducen a `m−1` cuando sea necesario. Escribe los enteros sin separadores de miles; para alfa puedes usar punto o coma decimal. Si ingresas un valor inválido, el programa vuelve a solicitarlo.

El límite de intervalos mantiene una frecuencia esperada `N/k ≥ 5`. El máximo del módulo permite normalizar con precisión razonable en ambos lenguajes; Java usa `BigInteger` para evitar desbordamiento en `a*X+c`. Los límites de N y k mantienen manejables la memoria y las gráficas.

### Ejemplo rápido

1. Ejecuta Java y selecciona `1` (o pulsa Enter) para ejecutar el caso base.
2. Al preguntar si deseas otro análisis, pulsa Enter para salir.
3. Ejecuta Python y selecciona también el caso base.
4. Ejecuta `comparar.py` con el comando de tu sistema operativo.
5. Abre las imágenes dentro de `resultados/`.

Para estudiar otra configuración, selecciona la opción `2` y cambia, por ejemplo, la semilla a `54321`. Un caso deliberadamente malo es `N=10000, m=16, a=0, c=0, semilla=1, k=10, alfa=0.05`: genera únicamente ceros y ambas pruebas rechazan H0.

## 5. Resultados y gráficas

La carpeta `resultados/` se crea automáticamente.

| Archivo | Contenido |
|---|---|
| `java_secuencia.csv`, `python_secuencia.csv` | Toda la secuencia: índice i, entero X y normalizado U. |
| `java_frecuencias.csv`, `python_frecuencias.csv` | Límites de cada intervalo, frecuencia observada y esperada. |
| `java_resumen.csv`, `python_resumen.csv` | Parámetros, estadísticos, valores p, decisiones y tiempo de cálculo. |
| `java_graficas.png`, `python_graficas.png` | Tres paneles: frecuencias, distribución acumulada y primeros 200 valores. |
| `java_calculos.png`, `python_calculos.png` | Desglose de Chi-cuadrado y diferencias que determinan KS, con valores p y decisiones. |
| `java_hipotesis.png`, `python_hipotesis.png` | Distribución Chi-cuadrado, región de rechazo, valor crítico y estadístico observado. |
| `comparacion.csv` | Tabla fila por fila de las últimas secuencias de ambos lenguajes. |

En las gráficas de cálculo:

- **Chi-cuadrado:** cada barra representa `(Oj − Ej)² / Ej`; la suma de las barras es el estadístico Chi². Una barra alta identifica un intervalo que se aleja más de la frecuencia esperada.
- **KS:** se representan `i/N − U(i)` y `U(i) − (i−1)/N` para toda la secuencia ordenada. Los puntos destacados son sus máximos D+ y D−; el mayor de ambos es D. Las diferencias individuales pueden ser negativas; se usan los máximos de cada curva, no la suma.
- Se muestran los valores p y la decisión con el alfa elegido. El valor p de KS sigue siendo asintótico.

**¿Java y Python generan lo mismo?** Con los mismos parámetros generan exactamente los mismos enteros X y usan la misma normalización U=X/m. Los estadísticos y valores p coinciden dentro de la precisión numérica; los últimos decimales pueden variar por las operaciones y bibliotecas utilizadas. Los tiempos y el aspecto de las gráficas pueden diferir. Cambiar los parámetros sí puede cambiar la secuencia. Usa `comparar.py` para comprobar tus corridas.

Las imágenes se guardan sin abrir ventanas y pueden verse desde el explorador de archivos. Cada implementación produce sus propias gráficas de forma independiente.

**Cada ejecución reemplaza los archivos anteriores de su lenguaje.** Copia la carpeta de resultados a otra ubicación si deseas conservar un escenario antes de ejecutar uno nuevo. Vuelve a ejecutar `comparar.py` después de cambiar los datos: la tabla comparativa no se actualiza sola.

La consola muestra los primeros 20 valores y todas las frecuencias. Los CSV contienen la secuencia completa, incluso para un millón de datos. La comparación verifica los parámetros, los índices, los enteros exactos y los normalizados con tolerancia `1e-15`; si los parámetros difieren, pide ejecutar de nuevo con la misma configuración. Los CSV usan coma como separador y punto decimal.

Los tiempos incluyen **generación y cálculo de las dos pruebas**, incluido el ordenamiento para KS. Excluyen entrada, impresión, archivos y gráficas. Una sola corrida no permite concluir cuál lenguaje siempre es más rápido; para comparar rendimiento deben hacerse varias repeticiones en el mismo equipo.

## 6. Fórmulas e interpretación

### Generador LCG

```text
X siguiente = (a * X actual + c) mod m
U = X siguiente / m
```

La semilla es X₀ y no se incluye como primer dato. El primer valor guardado es X₁/m. Los valores generados pertenecen a `[0,1)`.

### Hipótesis

- **H0:** los datos son compatibles con una distribución uniforme U(0,1).
- **H1:** los datos no siguen esa distribución uniforme.
- Si `p < alfa`, se rechaza H0.
- Si `p ≥ alfa`, no se rechaza H0.

### Chi-cuadrado

```text
Ei = N / k
Chi² = suma de (Oi - Ei)² / Ei
gl = k - 1
p = P(Chi²_gl ≥ estadístico observado)
```

Los intervalos son `[i/k, (i+1)/k)`. Se cuentan usando aritmética entera para evitar clasificar incorrectamente valores que caigan en un límite. Python usa la cola `scipy.stats.chi2.sf`; Java calcula la misma cola mediante la función gamma regularizada. Ese cálculo numérico está separado de la lógica de consola.

### Kolmogorov-Smirnov

Con los datos ordenados y posiciones i de 1 a N:

```text
D+ = máximo de (i/N - U ordenado_i)
D- = máximo de (U ordenado_i - (i-1)/N)
D = máximo de D+ y D-
```

El estadístico D se calcula con todos los datos. **El valor p de KS es una aproximación asintótica bilateral**, no el cálculo exacto para muestras finitas. Python usa `scipy.stats.kstwobign.sf(sqrt(N)*D)` y Java las series equivalentes. La aproximación resulta más apropiada para N grande, como los 10000 datos de la guía; cerca del umbral de significancia o con N pequeño puede diferir del método exacto.

Las pruebas se interpretan bajo un modelo de observaciones independientes y una referencia uniforme continua. Un LCG es determinista y discreto; módulos pequeños, repeticiones o dependencia pueden afectar esa interpretación. Estas pruebas son diagnósticos de uniformidad y **no demuestran independencia, impredecibilidad ni aleatoriedad verdadera**. Un valor p puede mostrarse como cero por precisión numérica cuando la discrepancia es extrema.

Referencias técnicas: [Chi-cuadrado en SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html) y [métodos exactos y asintóticos de KS](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html).

### Nota sobre la guía

El procedimiento de la práctica 06 describe LCG, Chi-cuadrado y KS. La tabla final incluye “π estimado” y “Error”, que no corresponden a esos procedimientos. Esta implementación sigue el objetivo de validación de uniformidad y compara secuencias, Chi², KS, valores p y tiempos; no añade una simulación de π. Se pueden evaluar los tamaños 1000, 10000, 100000 y 1000000 ingresándolos en consola.

## 7. Estructura MVC

```text
practica06-simulacion/
├── README.md
├── .gitignore
├── java/
│   ├── Main.java
│   ├── modelo/Simulacion.java
│   ├── vista/Vista.java
│   └── controlador/Controlador.java
├── python/
│   ├── main.py
│   ├── requirements.txt
│   ├── comparar.py
│   ├── modelo/simulacion.py
│   ├── vista/vista.py
│   └── controlador/controlador.py
└── tests/
    ├── verificar.py
    └── VerificarModelo.java
```

- **Modelo:** genera la secuencia y calcula las pruebas.
- **Vista:** solicita valores, muestra resultados y dibuja gráficas.
- **Controlador:** coordina el modelo y la vista, guarda CSV y permite repetir.
- **Main:** inicia el programa.
- **Comparar:** utilidad separada para cotejar las dos ejecuciones.

No se utilizan frameworks, bases de datos ni interfaces gráficas de entrada. El `.gitignore` excluye entornos virtuales, compilados, resultados y PDF del repositorio.

## 8. Verificación opcional

Con las dependencias instaladas y el JDK disponible:

Linux:

```bash
.venv/bin/python tests/verificar.py
```

Windows:

```powershell
.venv\Scripts\python.exe tests\verificar.py
```

La verificación contrasta los valores p de Java con SciPy, comprueba una secuencia conocida y compara ambos modelos en escenarios normales, constantes, de módulo pequeño y de parámetros grandes. También contrasta el estadístico KS con `kstest`. Compila el auxiliar Java en una carpeta temporal; no requiere JUnit.

## 9. Preguntas de control

1. **¿Qué es H0?** La hipótesis de referencia; aquí, que los valores son compatibles con U(0,1).
2. **¿Qué representa el valor p?** Bajo H0 y los supuestos de la prueba, la probabilidad de observar un estadístico al menos tan extremo como el obtenido. No es la probabilidad de que H0 sea verdadera.
3. **¿Qué significa rechazar H0?** Que los datos aportan evidencia contra la uniformidad al nivel alfa elegido; no es una certeza absoluta.
4. **¿Qué diferencia existe entre Chi-cuadrado y KS?** Chi-cuadrado compara frecuencias por intervalos; KS mide la mayor separación entre la distribución acumulada empírica y la teórica, sin agrupar en intervalos.
5. **¿Por qué no demuestran aleatoriedad verdadera?** Porque examinan propiedades específicas de una muestra finita; un algoritmo determinista puede superar ambas y aun presentar dependencia o patrones.

La gráfica de hipótesis usa los grados de libertad `k−1` y el alfa ingresado. La línea roja marca el valor crítico y la azul, el Chi² observado. La cola derecha roja/rosa representa la región de rechazo (área total alfa); la zona verde indica no rechazo, no una demostración de H0. La decisión se calcula con `p < alfa`. El sombreado de rechazo representa alfa, no el valor p. Si el estadístico observado queda muy lejos, se indica que está fuera del eje para conservar visible la distribución. Para gl=1, la densidad crece sin límite al acercarse a cero; la curva se dibuja desde un pequeño valor positivo. La cola se recorta visualmente, pero el cálculo utiliza la distribución completa.
