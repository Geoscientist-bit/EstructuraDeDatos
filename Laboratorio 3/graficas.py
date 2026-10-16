from estructuras import Estudiante, ImplementacionLista, ImplementacionABB, ImplementacionBPlus

import time
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# Aumentar límite de recursión por el peor caso del ABB
sys.setrecursionlimit(100000)

# ==========================================
# [REUTILIZA AQUÍ LAS CLASES DE TU CÓDIGO ANTERIOR]
# Asegúrate de tener aquí las clases: Estudiante, 
# ImplementacionLista, ImplementacionABB, ImplementacionBPlus
# ==========================================

def correr_experimento_estadistico(tamanios_N, M, replicas=5, ordenado=False):
    """
    Ejecuta el experimento múltiples veces (réplicas) por cada N 
    para calcular promedios y desviaciones estándar robustas.
    """
    estructuras = ["Lista", "ABB", "Árbol B+"]
    
    # Estructura para almacenar tiempos de cada réplica
    # { estructura: { N: [tiempo_rep1, tiempo_rep2, ...] } }
    tiempos_busqueda = {est: {N: [] for N in tamanios_N} for est in estructuras}
    tiempos_insercion = {est: {N: [] for N in tamanios_N} for est in estructuras}

    for N in tamanios_N:
        print(f"Evaluando N = {N} ({replicas} réplicas)...")
        for rep in range(replicas):
            # 1. Generar Datos del tamaño N
            if ordenado:
                ids = list(range(1, N + 1))
            else:
                ids = list(range(1, N + 1))
                random.shuffle(ids)
            
            estudiantes = [
                Estudiante(id_id, f"Est.", random.randint(17,30), round(random.uniform(1.0,5.0),2)) 
                for id_id in ids
            ]
            
            # IDs de búsqueda (M búsquedas aleatorias fijas por réplica)
            ids_busqueda = [random.randint(1, int(N * 1.2)) for _ in range(M)]
            
            # Instanciar soluciones
            instancias = {
                "Lista": ImplementacionLista(),
                "ABB": ImplementacionABB(),
                "Árbol B+": ImplementacionBPlus(grado=16)
            }
            
            # 2. Medir cada estructura
            for nombre, struct in instancias.items():
                # Inserción
                t0 = time.perf_counter()
                for est in estudiantes:
                    struct.insertar(est)
                t1 = time.perf_counter()
                tiempos_insercion[nombre][N].append(t1 - t0)
                
                # Búsqueda
                t0 = time.perf_counter()
                for b_id in ids_busqueda:
                    struct.buscar(b_id)
                t1 = time.perf_counter()
                tiempos_busqueda[nombre][N].append(t1 - t0)
                
    return tiempos_insercion, tiempos_busqueda

def procesar_y_graficar(tamanios_N, datos_tiempo, titulo_grafica, eje_y_label, M_info, caso_texto):
    """
    Calcula promedio y desviación estándar, e imprime las tablas métricas requeridas
    junto con la generación de las gráficas comparativas.
    """
    plt.figure(figsize=(10, 6))
    
    print(f"\n========================================================")
    print(f" ESTADÍSTICAS METROLÓGICAS: {titulo_grafica} ({caso_texto})")
    print(f"========================================================")
    print(f"{'Estructura':<12} | {'N':<6} | {'M':<5} | {'Promedio (s)':<12} | {'Desv. Est (s)':<12}")
    print("-" * 60)

    # Estilos de línea para diferenciar curvas claramente
    estilos = {"Lista": "o-r", "ABB": "s-g", "Árbol B+": "^-b"}

    for est, n_dict in datos_tiempo.items():
        promedios = []
        desviaciones = []
        
        for N in tamanios_N:
            reps = n_dict[N]
            prom = np.mean(reps)
            desv = np.std(reps)
            promedios.append(prom)
            desviaciones.append(desv)
            
            print(f"{est:<12} | {N:<6} | {M_info:<5} | {prom:12.6f} | {desv:12.6f}")
        
        # Graficar curvas con barras de error que representan la Desviación Estándar
        plt.errorbar(
            tamanios_N, promedios, yerr=desviaciones, fmt=estilos[est], 
            capsize=5, label=f"{est} (±1σ)"
        )

    # Configuración estricta de la gráfica para el entregable
    plt.title(f"{titulo_grafica}\nCaso: Entradas con IDs {caso_texto}", fontsize=13, fontweight='bold')
    plt.xlabel("Tamaño de la muestra de estudiantes (N)", fontsize=11)
    plt.ylabel(f"{eje_y_label} (segundos)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left", fontsize=10)
    
    # Texto descriptivo embebido en la gráfica como pie de foto
    descripcion = (
        "Interpretación: Las curvas muestran cómo escala el tiempo real del sistema.\n"
        "Las barras verticales indican la variabilidad (desviación estándar) en las ejecuciones."
    )
    plt.figtext(0.15, 0.01, descripcion, fontsize=9, style='italic')

    
    plt.tight_layout()
    # Guardar en formato de alta calidad listo para el documento LaTeX/Word
    nombre_archivo = f"grafica_{titulo_grafica.replace(' ', '_')}_{caso_texto}.png"
    plt.savefig(nombre_archivo, dpi=300)
    print(f"\n[INFO] Gráfica guardada exitosamente como: {nombre_archivo}")
    plt.show()

# ==========================================
# CONFIGURACIÓN Y EJECUCIÓN GENERAL
# ==========================================
if __name__ == "__main__":
    # Parámetros del estudio
    TAMANIOS_N = [1000, 3000, 5000, 8000, 10000] # Suficientes puntos para notar tendencias
    M_BUSQUEDAS = 1500                          # Cantidad de consultas fijas
    NUM_REPLICAS = 5                            # Número de ejecuciones independientes
    
    # --- EXPERIMENTO 1: CASO ALEATORIO ---
    t_ins_aleat, t_bus_aleat = correr_experimento_estadistico(
        TAMANIOS_N, M_BUSQUEDAS, replicas=NUM_REPLICAS, ordenado=False
    )
    
    procesar_y_graficar(
        TAMANIOS_N, t_bus_aleat, "Tiempo Total de Búsqueda para M Consultas", 
        f"Tiempo de Búsqueda (M={M_BUSQUEDAS})", M_BUSQUEDAS, "ALEATORIOS"
    )

    # --- EXPERIMENTO 2: CASO PEOR ESCENARIO (ORDENADOS) ---
    t_ins_ord, t_bus_ord = correr_experimento_estadistico(
        TAMANIOS_N, M_BUSQUEDAS, replicas=NUM_REPLICAS, ordenado=True
    )
    
    procesar_y_graficar(
        TAMANIOS_N, t_bus_ord, "Tiempo Total de Búsqueda para M Consultas", 
        f"Tiempo de Búsqueda (M={M_BUSQUEDAS})", M_BUSQUEDAS, "ORDENADOS"
    )
