# Práctica 04 - Modelo SIR en Java y NetLogo

## 1. Descripción del proyecto

Simula la propagación de una infección en una población de 100 personas. Cada
persona puede ser susceptible (S), infectada (I) o recuperada (R). Los cambios
siguen el orden `S → I → R`, sin nacimientos, muertes ni reinfecciones.

El propósito es implementar el mismo modelo en Java y NetLogo y comparar su
programación, visualización y resultados. Java genera un CSV; NetLogo lo importa,
ejecuta también su propia simulación y muestra cinco gráficas.

La ficha incluye Python/SimPy, Java y NetLogo. Por el alcance indicado para este
trabajo, se implementan Java y NetLogo. La parte de Python y la comparación de las
tres herramientas quedan fuera de esta entrega. El informe técnico está en
`reports/ape04_sir.pdf`, con el fuente editable en `reports/ape04_sir.tex`.
La mención a M/M/1 en la rúbrica de la ficha es una errata: esta práctica usa SIR.

## 2. Tecnologías utilizadas

- Java, con JDK 11 o posterior. Se utiliza únicamente la biblioteca estándar.
- NetLogo 7.0.4 y su extensión `csv`, incluida en la distribución de escritorio.
- Organización Modelo, Vista y Controlador (MVC) para el código Java.

El modelo se entrega en `.nlogox`, el formato de NetLogo 7. No se debe cambiar
manualmente su extensión a `.nlogo`. Consulta los
[cambios oficiales del formato de NetLogo](https://docs.netlogo.org/versions).

## 3. Instalación y ejecución de Java

Instala un JDK y NetLogo de escritorio. No se necesita Maven, Gradle ni descargar
librerías de Java.

Abre una terminal **en la carpeta `practica04-simulacion`** y ejecuta:

```bash
javac -encoding UTF-8 --release 11 -d build src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
java -cp build Main
```

El programa imprime una tabla cada diez pasos, el máximo de infectados, su tiempo
y la duración del cálculo. Guarda las 101 filas, de t = 0 a t = 100, en:

- `resultados/resultados_java.csv`: resultados generados por Java.
- `netlogo/resultados_java.csv`: copia idéntica para que NetLogo pueda leerla.

Al ejecutar nuevamente Java se reemplazan ambos archivos. Si modificas el código,
vuelve a compilar antes de ejecutar.

## 4. Uso en NetLogo

1. Abre `netlogo/modelo_sir_netlogo.nlogox` con NetLogo 7.
2. Pulsa **setup**. Se crean las personas y se carga automáticamente el CSV si
   está junto al modelo. La gráfica de Java aparece completa.
3. Pulsa **go**. Es un botón continuo: avanza la simulación propia de NetLogo
   hasta el tiempo 100. Puedes volver a pulsarlo para interrumpirla.
4. Observa las figuras y las curvas de NetLogo, que se construyen por pasos.
5. Al terminar, compara las curvas completas de ambas herramientas.

**CARGAR JAVA** permite releer el CSV después de ejecutar Java otra vez, sin
borrar la ejecución de NetLogo. Antes debe haberse pulsado setup. Una recarga
reemplaza las curvas importadas; no duplica sus puntos.

**setup** reinicia los agentes, las gráficas y el tiempo; vuelve a cargar el CSV
disponible. Si no existe, la simulación propia sigue disponible. Para recuperar
las curvas de Java, ejecuta Java y pulsa CARGAR JAVA.

El control **Pausa entre pasos (s)** empieza en `0.10`. Puedes aumentarlo hasta
`0.50` para observar más despacio. La velocidad visual no cambia los parámetros
ni la unidad de tiempo del modelo. También puedes usar la barra de velocidad
de NetLogo si necesitas reducir más el ritmo.

Los colores representan el estado actual: azul = susceptible, rojo = infectado,
verde = recuperado. La etiqueta **P0** identifica al paciente cero y permanece
visible cuando se recupera. Es una de las cinco personas infectadas iniciales;
la variable I cuenta a todos los infectados.

## 5. Configuración y reglas

| Parámetro | Valor de la ficha |
| --- | ---: |
| Población | 100 |
| Susceptibles iniciales | 95 |
| Infectados iniciales | 5 |
| Recuperados iniciales | 0 |
| Beta, probabilidad de transmisión por contacto | 0.30 |
| Gamma, probabilidad de recuperación por paso | 0.10 |
| Tiempo máximo | 100 pasos |

La semilla elegida para repetir cada ejecución es `42`. Los valores están al
inicio de `src/modelo/SimulacionSIR.java` y en el procedimiento `setup` de NetLogo.
Si cambias parámetros para otro experimento, debes cambiar ambas implementaciones
y adaptar la validación del CSV, que comprueba los valores de esta ficha.

En cada paso:

1. Se copia el estado actual de las personas.
2. Cada infectado elige **un contacto**, al azar, entre las otras 99 personas.
3. Si el contacto era susceptible al inicio del paso, se intenta infectarlo con
   probabilidad 0.30.
4. El infectado se recupera con probabilidad 0.10, independientemente del contagio.
5. Se aplican todos los cambios juntos y se registran S, I y R.

Un recién infectado podrá contagiar o recuperarse a partir del siguiente paso.
Los contactos pueden repetirse entre distintos infectados; una persona se cuenta
una sola vez. Un infectado puede transmitir y recuperarse en el mismo paso.
Aunque no queden infectados, se sigue registrando hasta t = 100.

La ficha permite contactos cercanos o seleccionados. Se eligen contactos al azar
en toda la población para mantener la misma regla sencilla en ambas herramientas.
El movimiento en NetLogo es ilustrativo: **la cercanía de las figuras no determina
el contagio**. El azar de sus posiciones y movimiento se separa con
`with-local-randomness` del utilizado por las reglas epidemiológicas.

El fundamento de la ficha es:

```text
N = S + I + R
dS/dt = -beta * S * I / N
dI/dt = beta * S * I / N - gamma * I
dR/dt = gamma * I
```

Aquí se utiliza la alternativa discreta por agentes indicada en la ficha, sin
resolver directamente las ecuaciones diferenciales. Beta y gamma se interpretan
como probabilidades por contacto y por paso, respectivamente. `beta / gamma = 3`
es la referencia teórica de reproducción del modelo de la guía, no un número
exacto de contagios que deba producir cada persona en una ejecución aleatoria.

## 6. Estructura del proyecto

```text
practica04-simulacion/
├── README.md
├── .gitignore
├── ape_guia simulacion semana 4-firmado-signed.pdf
├── reports/
│   ├── ape04_sir.pdf
│   └── ape04_sir.tex
├── src/
│   ├── Main.java
│   ├── modelo/
│   │   ├── Persona.java
│   │   └── SimulacionSIR.java
│   ├── vista/
│   │   └── VistaConsola.java
│   └── controlador/
│       └── SimulacionControlador.java
├── resultados/
│   └── resultados_java.csv
└── netlogo/
    ├── modelo_sir_netlogo.nlogox
    └── resultados_java.csv
```

- `Main.java`: inicia el controlador y comunica errores al guardar archivos.
- `modelo/Persona.java`: representa a una persona y sus tres estados posibles.
- `modelo/SimulacionSIR.java`: define parámetros, realiza los cambios y cuenta estados.
- `vista/VistaConsola.java`: presenta parámetros y resultados en la terminal.
- `controlador/SimulacionControlador.java`: ejecuta el modelo, escribe el CSV y lo copia.
- `netlogo/`: contiene el modelo visual, sus controles, código y gráficas.
- `resultados/`: conserva los datos calculados por Java.

El flujo es `Main → controlador → modelo → vista`, con la exportación coordinada
por el controlador. `build/` contiene archivos compilados locales y se excluye
del repositorio. Para entregar, incluye el proyecto completo con los fuentes,
el modelo NetLogo y ambos CSV; no necesitas incluir `build/`.

## 7. Resultados y gráficas

Solo hace falta **un CSV de cuatro columnas**, porque todas las gráficas usan la
misma evolución temporal. La copia de NetLogo no es un segundo experimento.

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
```

No contiene posiciones, movimientos ni historiales individuales. No se genera
manualmente: se escribe desde Java. NetLogo valida encabezado, tiempos, conteos
enteros no negativos, estado inicial y conservación de la población al importarlo.

| Gráfica en NetLogo | Datos que presenta |
| --- | --- |
| Evolucion Java | S, I y R importados del CSV. |
| Evolucion NetLogo | S, I y R calculados por la simulación de NetLogo. |
| Comparacion S | Susceptibles de Java y NetLogo. |
| Comparacion I | Infectados de Java y NetLogo. |
| Comparacion R | Recuperados de Java y NetLogo. |

Las comparaciones usan negro para Java y naranja para NetLogo. La curva completa
de Java se carga desde el principio; NetLogo incorpora un punto por paso.

Resultados comprobados con los parámetros indicados y semilla 42:

| Medida | Java | NetLogo 7.0.4 |
| --- | ---: | ---: |
| Máximo de infectados | 29 | 44 |
| Primer tiempo con ese máximo | 31 | 11 |
| Susceptibles en t = 100 | 13 | 8 |
| Infectados en t = 100 | 0 | 0 |
| Recuperados en t = 100 | 87 | 92 |

Las mismas reglas y parámetros no garantizan la misma trayectoria: Java y NetLogo
emplean generadores y secuencias aleatorias diferentes. La semilla permite repetir
una ejecución en cada implementación; no sincroniza sus números aleatorios.
Estos valores corresponden a una corrida, no a promedios ni intervalos estadísticos.

Para el análisis del informe, las gráficas permiten observar el descenso de S,
el crecimiento y descenso de I, el aumento de R, el máximo de infectados y las
diferencias entre herramientas. También debe explicarse el efecto del azar.

Java informa el tiempo de ejecutar el modelo y contar sus resultados, sin escribir
archivos ni imprimir. El monitor de NetLogo suma el tiempo de actualizar estados,
sin movimiento, conteos para gráficas, CSV ni pausas. Las mediciones son orientativas
y no equivalen a una comparación controlada de rendimiento entre lenguajes.

## 8. Verificación

Se verificaron la compilación de Java para versión 11, la generación de los dos
CSV idénticos y la ejecución en NetLogo 7.0.4. En ambas simulaciones hay 101
registros, conteos enteros no negativos y una población constante de 100.

Se comprobó que S no aumenta, R no disminuye, las cinco gráficas contienen los
puntos esperados, la recarga no los duplica y setup reproduce la ejecución con
la misma semilla. La simulación visual tiene movimiento y go está configurado
como continuo con parada al alcanzar t = 100.

El informe incluye metodología, análisis de las cinco gráficas, respuestas a las
preguntas de control, la tabla de comparación y una declaración de uso de IA con
un prompt general representativo. La comparación de Python/SimPy y el video de
demostración quedan pendientes porque no se implementó esa tercera herramienta.
