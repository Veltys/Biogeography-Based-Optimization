#!/bin/bash

# Preprocesamiento: variables
alg='BBO'

if [ $# -lt 2 ] || \
   [[ ! $1 == ?(-)+([0-9]) ]] || [ "$1" -lt 1 ] || \
   [[ ! $2 == ?(-)+([0-9]) ]] || [ "$2" -lt 1 ]
then
	funciones=(1 10 1)
	dimensiones=(10 20 5)
else
	funciones=($1 $2 1)

	if [ $# -lt 4 ] || \
	   [[ ! $3 == ?(-)+([0-9]) ]] || [ "$3" -lt 5 ] || \
	   [[ ! $4 == ?(-)+([0-9]) ]] || [ "$4" -lt 5 ]
	then
		dimensiones=(10 20 5)
	else
		dimensiones=($3 $4 5)
	fi
fi

for (( i=funciones[0]; i<=funciones[1]; i++ )); do
	for (( j=dimensiones[0]; j<=dimensiones[1]; j=j+5 )); do
		# Procesamiento condicional a la no existencia del parámetro -r
		if \
			! ( \
				[ "$1" = '-r' ] || \
				( [ $# -eq 5 ] && [ "$5" = '-r' ] )
			)
		then
			# Procesamiento: ejecución del programa
			echo "Función $i, dimensión $j"

			./optimizer.py -b "$i" -d "$j"
		fi

		# Posprocesamiento: recopilación de resultados
		# Recogida de todos los archivos de salida
		archivo=($(ls . | grep csv))

		# Preparación de la matriz de resultados
		declare -A res

		for (( k=0; k<30; k++ )); do
			linea=$(sed -n "$(((k + 2) * 2)) p" "./$archivo")

			linea=(${linea//,/ })

			for (( l=0; l<16; l++ )); do
				# Número de columna a leer
				numColumna=$(awk "BEGIN {print int($j ^ ($l / 5 - 3) * 150000)}")

				elemento=${linea[$((numColumna + 4))]}

				# Algunas líneas podrían no existir, debido a los criterios de parada
				if ! [[ -z "$linea" ]]; then
					res[$l,$k]=$elemento
				else
					# En tal caso, se copia el resultado de la línea anterior
					res[$l,$k]=${res[$((l - 1)),$k]}
				fi

				# Limpieza de caracteres no imprimibles no deseados que aparecen "because yes"
				res[$l,$k]=$(tr -dc '[[:print:]]' <<< "${res[$l,$k]}")
			done
		done

		if [ -f "${alg}_${i}_${j}.txt" ]; then
			truncate -s0 "${alg}_${i}_${j}.txt"
		fi

		for (( k=0; k<16; k++ )); do
			for (( l=0; l<30; l++ )); do
				echo -n "${res[$k,$l]}" >> "${alg}_${i}_${j}.txt"

				if [ "$l" -ne 29 ]; then
					echo -n ',' >> "${alg}_${i}_${j}.txt"
				fi
			done

			echo >> "${alg}_${i}_${j}.txt"

			# Borrado de resultados ya no necesarios
			rm -r "./$archivo"
		done
	done
done
