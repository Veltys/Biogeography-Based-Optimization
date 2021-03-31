#!/usr/bin/env pwsh

# Preprocesamiento: variables
$alg = 'BBO'

if(
	$args.Length -lt 2 -or
	(!($args[0] -match '^\d+$') -or $args[0] -lt 1) -or
	(!($args[1] -match '^\d+$') -or $args[1] -lt 1)
) {
	$funciones		= @( 1, 10, 1)
	$dimensiones	= @(10, 20, 5)
}
else {
	$funciones		= @($args[0], $args[1], 1)

	if(
		$args.Length -lt 4 -or
		(!($args[1] -match '^\d+$') -or $args[2] -lt 5) -or
		(!($args[3] -match '^\d+$') -or $args[3] -lt 5)
	) {
		$dimensiones	= @(10, 20, 5)
	}
	else {
		$dimensiones	= @($args[2], $args[3], 5)
	}
}

for($i = $funciones[0]; $i -le $funciones[1]; $i += $funciones[2]) {
	for($j = $dimensiones[0]; $j -le $dimensiones[1]; $j += $dimensiones[2]) {
		# Procesamiento condicional a la no existencia del parámetro -r
		if(
			!(
				$args[0] -eq '-r' -or
				($args.Length -eq 5 -and $args[4] -eq '-r')
			)
		) {
			# Procesamiento: ejecución del programa
			Write-Output "Función $i, dimensión $j"

			.\optimizer.py -b $i -d $j
		}

		# Posprocesamiento: recopilación de resultados
		# Recogida de todos los archivos de salida
		$archivo = Get-ChildItem -Path . -Filter experiment*.csv

		# Preparación de la matriz de resultados
		[System.Collections.ArrayList]$res = @()

		for($k = 0; $k -lt 16; $k++) {
			$null = $res.Add(@(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
		}

		for($k = 0; $k -lt 30; $k++) {
	        $linea = Get-Content $archivo.FullName | Select -Index (($k + 1) * 2)

			$linea = $linea.Split(',')

			for($l = 0; $l -lt 16; $l++) {
				# Número de columna a leer
				$numColumna = [Math]::Round([Math]::Pow($j, $l / 5 - 3) * 150000)

				$elemento = $linea[$numColumna + 4]

				# Algunas líneas podrían no existir, debido a los criterios de parada
		        if($linea -match '^[-]?[0-9]+\.?[0-9]*$') {
					$res[$l][$k] = $elemento
				}
				else {
					# En tal caso, se copia el resultado de la línea anterior
					$res[$l][$k] = $res[$l - 1][$k]
				}
			}
		}

		$out = '';

		if(Test-Path -Path "${alg}_${i}_${j}.txt" -PathType Leaf) {
			Clear-Content "${alg}_${i}_${j}.txt"
		}

		for($k = 0; $k -lt 16; $k++) {
			for($l = 0; $l -lt 30; $l++) {
				$out += $res[$k][$l]

				 if($l -ne 29) {
				 	$out += ','
			 	}
			}

			$out += [Environment]::NewLine
		}

		$out | Out-File "${alg}_${i}_${j}.txt"

		# Borrado de resultados ya no necesarios
		Remove-Item .\$archivo -Recurse -Confirm:$false
	}
}
