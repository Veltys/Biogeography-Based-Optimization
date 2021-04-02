#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import linecache
import os
import re
import sys

import numpy

import optimizer


def main(argv):
    # Preprocesamiento: variables

    alg = 'BBO'

    if \
        len(argv) < 2 or \
        (not(re.match(r"[0-9]+", argv[0])) or int(argv[0]) < 1) or \
        (not(re.match(r"[0-9]+", argv[1])) or int(argv[1]) < 1):
        funciones = [ 1, 10, 1]
        dimensiones = [10, 20, 5]
    else:
        funciones = [int(argv[0]), int(argv[1]), 1]

        if \
            len(argv) < 4 or \
            (not(re.match(r"[0-9]+", argv[2])) or int(argv[2]) < 5) or \
            (not(re.match(r"[0-9]+", argv[3])) or int(argv[3]) < 5):
            dimensiones = [10, 20, 5]
        else:
            dimensiones = [int(argv[2]), int(argv[3]), 5]

    for i in range(funciones[0] - funciones[2], funciones[1], funciones[2]):
        for j in range(dimensiones[0] - dimensiones[2], dimensiones[1], dimensiones[2]):
            # Procesamiento condicional a la no existencia del parámetro -r

            if \
                not(\
                    (len(argv) == 1 and argv[0] == '-r') or \
                    (len(argv) == 5 and argv[4] == '-r') \
                ):
                # Procesamiento: ejecución del programa
                print('Función ' + str(i + funciones[2]) + ' dimensión ' + str(j + dimensiones[2]))

                optimizer.main(['-b', str(i + funciones[2]), '-d', str(j + dimensiones[2])])

            # Posprocesamiento: recopilación de resultados

            # Recogida de todos los archivos de salida
            archivos = [ name for name in os.listdir('.') if os.path.isfile(os.path.join('.', name)) and re.match(r"^experiment\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.csv$", name) ]

            archivo = archivos[0]

            # Preparación de la matriz de resultados
            res = numpy.zeros((16, 30))

            for k in range(30):
                linea = linecache.getline(archivo, k * 2 + 3)

                linea = linea.split(',')

                for l in range(16):
                    # Número de columna a leer
                    numColumna = int(round((j ** (l / 5 - 3)) * 150000, 0))

                    elemento = linea[numColumna + 4]

                    # Algunas líneas podrían no existir, debido a los criterios de parada
                    if re.match(r"^\d*[.,]?\d*$", elemento):
                        res[l][k] = elemento
                    else:
                        # En tal caso, se copia el resultado de la línea anterior
                        res[l][k] = res[l - 1][k]

            try:
                out = open(alg + '_' + str(i + funciones[2]) + '_' + str(j + dimensiones[2]) + '.txt', 'w')

            except IOError:
                print('Error de apertura del archivo <' + alg + '_' + i + '_' + j + '.txt>')
                print('ERROR: imposible abrir el archivo <' + alg + '_' + i + '_' + j + '.txt>', file = sys.stderr)

                exit(os.EX_OSFILE) # @UndefinedVariable

            else:
                for k in range(16):
                    for l in range(30):
                        out.write(str(res[k][l]))

                        if l != 29:
                            out.write(',')

                    # out.write(os.linesep)
                    out.write("\n")

                out.close()

                os.remove(archivo)


if __name__ == '__main__':
    main(sys.argv[1:])

