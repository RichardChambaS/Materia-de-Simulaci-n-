import csv
from pathlib import Path

from modelo.generador_lcg import GeneradorLCG
from vista import vista_consola as vista


class ControladorLCG:
    def ejecutar(self, semilla, otra_semilla=None):
        modelo = GeneradorLCG(semilla)
        # Valida la segunda semilla antes de generar archivos.
        segundo_modelo = GeneradorLCG(otra_semilla) if otra_semilla is not None else None
        valores = modelo.generar(10000)
        vista.mostrar_resultados(semilla, valores)

        carpeta = Path("resultados")
        carpeta.mkdir(exist_ok=True)
        archivo = carpeta / f"python_{semilla}.csv"
        with archivo.open("w", newline="", encoding="utf-8") as salida:
            escritor = csv.writer(salida)
            escritor.writerow(["iteracion", "X", "U"])
            for i, valor in enumerate(valores, start=1):
                escritor.writerow([i, valor, modelo.normalizar(valor)])
        vista.mostrar_seccion("ARCHIVO DE DATOS")
        vista.mostrar_mensaje(f"Datos CSV: {archivo}")

        self.comparar(valores, semilla, carpeta)
        repetidos = len(valores) - len(set(valores))
        vista.mostrar_seccion("ANÁLISIS DEL PERÍODO")
        vista.mostrar_mensaje(f"Valores repetidos en la muestra: {repetidos}")
        vista.mostrar_mensaje(
            "Período teórico: 4294967296\n"
            "c es impar, m es una potencia de 2\n"
            "y a - 1 es divisible por 4.\n\n"
            "La muestra de 10000 valores no demuestra por sí sola ese período."
        )

        grafica = carpeta / f"secuencia_{semilla}.png"
        vista.guardar_grafica(valores, semilla, grafica)
        vista.mostrar_seccion("GRÁFICA GENERADA")
        vista.mostrar_mensaje(f"Imagen PNG: {grafica}")
        if segundo_modelo is not None:
            otros_valores = segundo_modelo.generar(len(valores))
            comparacion_semillas = carpeta / f"semillas_{semilla}_{otra_semilla}.png"
            vista.guardar_comparacion_semillas(
                valores, otros_valores, semilla, otra_semilla, comparacion_semillas)
            vista.mostrar_seccion("COMPARACIÓN DE SEMILLAS EN PYTHON")
            iguales = sum(x == y for x, y in zip(valores, otros_valores))
            vista.mostrar_mensaje(f"Semillas: {semilla} y {otra_semilla}")
            vista.mostrar_mensaje(f"Valores iguales en la misma posición: {iguales} de {len(valores)}")
            vista.mostrar_mensaje(f"Imagen PNG: {comparacion_semillas}")
        vista.mostrar_mensaje("\n====================== PROCESO FINALIZADO ======================\n")

    def comparar(self, valores, semilla, carpeta):
        vista.mostrar_seccion("COMPARACIÓN JAVA / PYTHON")
        archivo_java = carpeta / f"java_{semilla}.csv"
        if not archivo_java.exists():
            vista.mostrar_mensaje(
                "Comparación pendiente: ejecute Java con la misma semilla\n"
                "y vuelva a ejecutar Python."
            )
            return

        with archivo_java.open(newline="", encoding="utf-8") as entrada:
            datos_java = list(csv.DictReader(entrada))
        if len(datos_java) != len(valores):
            raise ValueError("El archivo Java no contiene los 10000 valores esperados.")

        filas = []
        for i, (dato, valor) in enumerate(zip(datos_java, valores), start=1):
            x_java = int(dato["X"])
            u_java = float(dato["U"])
            u_python = GeneradorLCG.normalizar(valor)
            # Ambos lenguajes representan exactamente X / 2**32 en doble precisión.
            coincide = int(dato["iteracion"]) == i and x_java == valor and u_java == u_python
            filas.append([i, x_java, valor, u_java, u_python, "Sí" if coincide else "No"])

        archivo = carpeta / f"comparacion_{semilla}.csv"
        with archivo.open("w", newline="", encoding="utf-8") as salida:
            escritor = csv.writer(salida)
            escritor.writerow(["iteracion", "X_java", "X_python", "U_java", "U_python", "coincide"])
            escritor.writerows(filas)
        vista.mostrar_comparacion(filas)
        coincidencias = sum(fila[5] == "Sí" for fila in filas)
        vista.mostrar_mensaje(f"Coincidencias: {coincidencias} de {len(valores)}")
        vista.mostrar_mensaje(f"Tabla completa guardada en {archivo}")
        grafica = carpeta / f"java_python_{semilla}.png"
        vista.guardar_comparacion_lenguajes(filas, semilla, grafica)
        diferencia_maxima = max(abs(fila[3] - fila[4]) for fila in filas)
        vista.mostrar_mensaje(f"Diferencia máxima entre U de Java y Python: {diferencia_maxima:.10g}")
        vista.mostrar_mensaje(f"Gráfica comparativa: {grafica}")
