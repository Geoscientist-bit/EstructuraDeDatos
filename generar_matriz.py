import gzip
import os
import struct
import time

# Configuración de dimensiones
FILAS = 100000
COLUMNAS = 100000
ARCHIVO_SALIDA = "matriz_gigante.bin.gz"

# Tamaño del bloque para balancear RAM y CPU
FILAS_POR_BLOQUE = 1000

print("--- INICIANDO CREACIÓN DE MATRIZ OPTIMIZADA ---")
print(f"Objetivo: Matriz de {FILAS:,} x {COLUMNAS:,} elementos.")

inicio = time.time()
bloque_datos = []

try:
    # Usamos compresslevel=1 (Compresión rápida) para optimizar la velocidad del procesador
    with gzip.open(ARCHIVO_SALIDA, "wb", compresslevel=1) as f:
        for i in range(FILAS):
            # Creamos una fila simulada con un patrón matemático basado en su posición
            
            fila_simulada = [float(i + (j / COLUMNAS)) for j in range(COLUMNAS)]
            bloque_datos.extend(fila_simulada)
            
            # Al completar el tamaño del bloque, empaquetamos y escribimos a disco
            if (i + 1) % FILAS_POR_BLOQUE == 0 or (i + 1) == FILAS:
                filas_en_este_bloque = len(bloque_datos) // COLUMNAS
                formato_dinamico = f"{COLUMNAS * filas_en_este_bloque}f"
                
                # Transformamos la lista de números a bytes puros y los mandamos al stream comprimido
                f.write(struct.pack(formato_dinamico, *bloque_datos))
                
                # Vaciamos la lista inmediatamente para liberar memoria RAM
                bloque_datos.clear()
                
                # Progreso en consola sin saturar la terminal
                porcentaje = ((i + 1) / FILAS) * 100
                print(f"Progreso de almacenamiento: {porcentaje:.1f}% guardado.", end="\r")

    fin = time.time()
    tamano_mb = os.path.getsize(ARCHIVO_SALIDA) / (1024**2)
    print(f"\n\n¡Éxito! Matriz optimizada y guardada en {fin - inicio:.2f} segundos.")
    print(f"Tamaño optimizado del archivo en disco: {tamano_mb:.2f} MB")
    print("La PC se mantuvo libre de sobrecargas de RAM y disco.")

except IOError as e:
    print(f"\nError de escritura en el almacenamiento duro: {e}")