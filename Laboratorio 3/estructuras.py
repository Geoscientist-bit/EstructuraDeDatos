import time
import random
import sys

# Aumentar el límite de recursión por si el ABB se desbalancea críticamente con datos ordenados
sys.setrecursionlimit(50000)

# ==========================================
# 0. MODELO DE DATOS
# ==========================================
class Estudiante:
    def __init__(self, id_estudiante, nombre, edad, promedio):
        self.id = id_estudiante
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

    def __repr__(self):
        return f"[{self.id}] {self.nombre}"

# ==========================================
# 1. ESTRATEGIA 1: LISTAS (ARRAY/DYNAMIC LIST)
# ==========================================
class ImplementacionLista:
    def __init__(self):
        self.estudiantes = []

    def insertar(self, estudiante):
        # Inserción O(1) al final
        self.estudiantes.append(estudiante)

    def buscar(self, id_buscado):
        # Búsqueda lineal O(N)
        for est in self.estudiantes:
            if est.id == id_buscado:
                return est
        return None

    def listar_ascendente(self):
        # Ordenamiento O(N log N) para cumplir con el listado ascendente
        return sorted(self.estudiantes, key=lambda x: x.id)


# ==========================================
# 2. ESTRATEGIA 2: ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ==========================================
class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izq = None
        self.der = None

class ImplementacionABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        if not self.raiz:
            self.raiz = NodoABB(estudiante)
        else:
            self._insertar_recursivo(self.raiz, estudiante)

    def _insertar_recursivo(self, nodo, estudiante):
        if estudiante.id < nodo.estudiante.id:
            if nodo.izq is None:
                nodo.izq = NodoABB(estudiante)
            else:
                self._insertar_recursivo(nodo.izq, estudiante)
        else:
            if nodo.der is None:
                nodo.der = NodoABB(estudiante)
            else:
                self._insertar_recursivo(nodo.der, estudiante)

    def buscar(self, id_buscado):
        return self._buscar_recursivo(self.raiz, id_buscado)

    def _buscar_recursivo(self, nodo, id_buscado):
        if nodo is None or nodo.estudiante.id == id_buscado:
            return nodo.estudiante if nodo else None
        if id_buscado < nodo.estudiante.id:
            return self._buscar_recursivo(nodo.izq, id_buscado)
        return self._buscar_recursivo(nodo.der, id_buscado)

    def listar_ascendente(self):
        # Inorden: O(N) siempre
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.estudiante)
            self._inorden(nodo.der, resultado)


# ==========================================
# 3. ESTRATEGIA 3: ÁRBOL B+ (SIMPLIFICADO)
# ==========================================
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []      # IDs de los estudiantes
        self.hijos = []       # Referencias a nodos hijos (si no es hoja) o a objetos Estudiante (si es hoja)
        self.siguiente = None # Puntero al siguiente nodo hoja (característico de B+)

class ImplementacionBPlus:
    def __init__(self, grado=4):
        self.raiz = NodoBPlus(es_hoja=True)
        self.grado = grado

    def buscar(self, id_buscado):
        nodo = self.raiz
        while not nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and id_buscado >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        
        for i, clave in enumerate(nodo.claves):
            if clave == id_buscado:
                return nodo.hijos[i]
        return None

    def insertar(self, estudiante):
        raiz = self.raiz
        if len(raiz.claves) == self.grado - 1:
            nuevo_nodo = NodoBPlus()
            self.raiz = nuevo_nodo
            nuevo_nodo.hijos.append(raiz)
            self._dividir_hijo(nuevo_nodo, 0, raiz)
            self._insertar_no_lleno(nuevo_nodo, estudiante)
        else:
            self._insertar_no_lleno(raiz, estudiante)

    def _insertar_no_lleno(self, nodo, estudiante):
        if nodo.es_hoja:
            i = 0
            while i < len(nodo.claves) and estudiante.id > nodo.claves[i]:
                i += 1
            nodo.claves.insert(i, estudiante.id)
            nodo.hijos.insert(i, estudiante)
        else:
            i = 0
            while i < len(nodo.claves) and estudiante.id > nodo.claves[i]:
                i += 1
            if len(nodo.hijos[i].claves) == self.grado - 1:
                self._dividir_hijo(nodo, i, nodo.hijos[i])
                if estudiante.id > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], estudiante)

    def _dividir_hijo(self, padre, i, hijo):
        t = self.grado // 2
        nuevo_hijo = NodoBPlus(es_hoja=hijo.es_hoja)
        padre.claves.insert(i, hijo.claves[t-1])
        padre.hijos.insert(i + 1, nuevo_hijo)
        
        nuevo_hijo.claves = hijo.claves[t:]
        nuevo_hijo.hijos = hijo.hijos[t:]
        hijo.claves = hijo.claves[:t-1]
        hijo.hijos = hijo.hijos[:t]

        if hijo.es_hoja:
            nuevo_hijo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo_hijo

    def listar_ascendente(self):
        # Ventaja del B+: Seguir los punteros de las hojas en O(N) secuencial directo
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        
        resultado = []
        while nodo:
            resultado.extend(nodo.hijos)
            nodo = nodo.siguiente
        return resultado


# ==========================================
# 4. MÓDULO EXPERIMENTAL Y ESTADÍSTICO
# ==========================================
def ejecutar_experimento(N, M, ordenado=False):
    # Crear set de datos base
    if ordenado:
        ids = list(range(1, N + 1))
    else:
        ids = list(range(1, N + 1))
        random.shuffle(ids)

    estudiantes_test = [Estudiante(id_id, f"Estudiante_{id_id}", random.randint(17, 30), round(random.uniform(1.0, 5.0), 2)) for id_id in ids]
    
    # IDs a buscar (aleatorios, algunos existentes, otros no)
    ids_busqueda = [random.randint(1, int(N * 1.2)) for _ in range(M)]

    estructuras = {
        "Lista": ImplementacionLista(),
        "ABB": ImplementacionABB(),
        "Árbol B+": ImplementacionBPlus(grado=16)
    }

    resultados = {}

    for nombre, struct in estructuras.items():
        # --- Medir Inserción ---
        start = time.perf_counter()
        for est in estudiantes_test:
            struct.insertar(est)
        tiempo_ins = time.perf_counter() - start

        # --- Medir Búsqueda ---
        start = time.perf_counter()
        for b_id in ids_busqueda:
            struct.buscar(b_id)
        tiempo_bus = time.perf_counter() - start

        # --- Medir Listado ---
        start = time.perf_counter()
        _ = struct.listar_ascendente()
        tiempo_list = time.perf_counter() - start

        resultados[nombre] = {
            "Inserción (s)": tiempo_ins,
            "Búsqueda (s)": tiempo_bus,
            "Listado (s)": tiempo_list
        }

    return resultados

# ==========================================
# EJECUCIÓN DEL BENCHMARK
# ==========================================
if __name__ == "__main__":
    # Tamaños de muestra para evaluar escalabilidad (puedes añadir más)
    tamanios_N = [1000, 5000, 10000] 
    M_busquedas = 1000

    print(f"--- INICIANDO PRUEBAS EMPÍRICAS (M = {M_busquedas} búsquedas) ---\n")

    for tipo_orden in [False, True]:
        estado_orden = "ORDENADOS (Peor caso ABB)" if tipo_orden else "ALEATORIOS"
        print(f"=========================================================")
        print(f" CASO: IDs DE ENTRADA {estado_orden}")
        print(f"=========================================================")
        
        for N in tamanios_N:
            print(f"\n---> Evaluando para N = {N} estudiantes")
            res = ejecutar_experimento(N, M_busquedas, ordenado=tipo_orden)
            
            # Imprimir formato tabla corta
            print(f"{'Estructura':<15} | {'Inserción':<12} | {'Búsqueda':<12} | {'ListadoAsc':<12}")
            print("-" * 60)
            for est_nom, metricas in res.items():
                print(f"{est_nom:<15} | {metricas['Inserción (s)']:12.6f} | {metricas['Búsqueda (s)']:12.6f} | {metricas['Listado (s)']:12.6f}")
