from controlador.controlador import ejecutar

if __name__ == '__main__':
    try:
        ejecutar()
    except (EOFError, KeyboardInterrupt):
        print('\nPrograma finalizado.')
    except OSError as error:
        print(f'No se pudieron guardar los resultados: {error}')
        raise SystemExit(1)
