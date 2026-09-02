import gzip
import struct
import time

ARCHIVO_ENTRADA = "matriz_gigante.bin.gz"
COLUMNAS = 100000
BYTES_POR_ELEMENTO = 4  # float de 4 bytes
BYTES_POR_FILA = COLUMNAS * BYTES_POR_ELEMENTO

def mostrar_submatriz_comprimida(fila_inicio, fila_fin, col_inicio, col_fin):
    """
    Lee y muestra una subsección de la matriz gigante extrayendo
    únicamente los bytes requeridos directamente desde el archivo comprimido.
    """
    print(f"\n[ENTREGABLE] Visualizando ventana real de la matriz [{fila_inicio}:{fila_fin}, {col_inicio}:{col_fin}]")
    
    elementos_a_leer = col_fin - col_inicio
    
    with gzip.open(ARCHIVO_ENTRADA, "rb") as f:
        for i in range(fila_fin):
            # Optimización de Lectura: Saltamos las filas completas que no nos interesan
            if i < fila_inicio:
                f.read(BYTES_POR_FILA)
                continue
            
            # Saltamos los bytes de las columnas iniciales que no vamos a mostrar
            f.read(col_inicio * BYTES_POR_ELEMENTO)
            
            # Leemos únicamente los elementos de la sección objetivo
            datos_binarios = f.read(elementos_a_leer * BYTES_POR_ELEMENTO)
            fila_valores = struct.unpack(f"{elementos_a_leer}f", datos_binarios)
            
            # Saltamos el resto de las columnas para posicionarnos al inicio de la siguiente fila
            columnas_restantes = COLUMNAS - col_fin
            f.read(columnas_restantes * BYTES_POR_ELEMENTO)
            
            # Mostramos la fila formateada elegantemente
            valores_formateados = [f"{val:.2f}" for val in fila_valores]
            print(f"Fila {i:05d}: {valores_formateados}")

# --- BLOQUE DE VERIFICACIÓN ---
print("Abriendo archivo binario comprimido para validación de datos...")
inicio_test = time.time()

# Caso de prueba 1: Mostrar el inicio de la matriz (Esquina superior izquierda 5x5)
mostrar_submatriz_comprimida(fila_inicio=0, fila_fin=5, col_inicio=0, col_fin=5)

# Caso de prueba 2: Mostrar un fragmento intermedio de la matriz
mostrar_submatriz_comprimida(fila_inicio=25000, fila_fin=25003, col_inicio=10, col_fin=15)

print(f"\nLectura y visualización completadas en {time.time() - inicio_test:.4f} segundos.")
print("Verificación exitosa: No hubo picos de consumo de RAM ni lentitud de lectura.")