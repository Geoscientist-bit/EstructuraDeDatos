# Sistema de Administración de Estudiantes - Laboratorio 3

Este repositorio contiene la implementación y el estudio experimental de tres estrategias de almacenamiento y búsqueda de datos para un sistema de administración de estudiantes. El objetivo principal es analizar estadísticamente cómo escala el rendimiento de las estructuras a medida que aumenta el tamaño de la entrada (N) y bajo diferentes condiciones de ordenamiento.

## 📋 Integrante
* **Jhon Edison Muñoz Banguero** - *jedison.munoz@udea.edu.co*
* *Universidad de Antioquia*
* *Curso de Estructuras de Datos*

---

## 🚀 Características del Sistema

El sistema modela un registro de `Estudiante` (ID, Nombre, Edad, Promedio) y evalúa tres operaciones fundamentales:
1. **Insertar** un nuevo estudiante.
2. **Buscar** un estudiante por su ID único.
3. **Listar** todos los estudiantes en orden ascendente de ID.

### Estructuras de Datos Implementadas
* **Lista Dinámica (Array/List):** Búsqueda secuencial O(N) e inserción O(1).
* **Árbol Binario de Búsqueda (ABB):** Implementación desde cero. Complejidad promedio de \(O(\log N)\), susceptible a degradación.
* **Árbol B+ (Balanceado):** Estructura multi-camino auto-balanceada con punteros secuenciales en las hojas. Mantiene un rendimiento estricto de \(O(\log N)\) e inmunidad al peor caso.

---

## 📊 Metodología Experimental y Rigor Estadístico

El módulo de pruebas implementa el siguiente diseño experimental:
* **Réplicas (K=5):** Cada escenario de tamaño N se ejecuta 5 veces de forma independiente.
* **Muestreo Temporal de Precisión:** Medición con `time.perf_counter()`.
* **Cálculo Metrológico:** Desviaciones estándar (σ) y promedios (μ) calculados automáticamente mediante `NumPy`.
* **Escenarios Evaluados:**
  1. **IDs Aleatorios:** Simula un flujo de inserción desordenado.
  2. **IDs Ordenados:** Activa el peor escenario teórico para estructuras no balanceadas.

---

## 🛠️ Estructura del Proyecto

El código está modularizado para mantener buenas prácticas de diseño:

```text
├── estructuras.py      # Definición del modelo Estudiante y las 3 estructuras de datos.
├── graficas.py         # Generador .
├── README.md           # Documentación del proyecto.
└── grafica_*.png       # Gráficas de rendimiento exportadas en alta resolución.
```

---

## 💻 Requisitos e Instalación

El proyecto está desarrollado en **Python 3.8+** y requiere las siguientes dependencias de análisis de datos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Geoscientist-bit/EstructuraDeDatos/edit/main/Laboratorio%203/   
   ```

2. Instala las librerías necesarias con `pip`:
   ```bash
   pip install numpy matplotlib
   ```

3. Ejecuta el experimento estadístico:
   ```bash
   python estructuras.py
   python graficas.py
   ```

---

## 📈 Resumen de Resultados y Tendencias

### 1. Caso: IDs de Entrada Aleatorios
* **Lista:** Muestra un crecimiento lineal exacto debido a su naturaleza de búsqueda secuencial.
* **ABB y Árbol B+:** Se mantienen estables y eficientes en la base de la gráfica gracias a su división logarítmica.

### 2. Caso: Peor Escenario (IDs Ordenados)
* **La Catástrofe del ABB:** Al no tener auto-balanceo, el ABB se degrada a una lista enlazada gigante. Su tiempo de búsqueda se dispara de forma lineal superando incluso a la lista nativa debido a la sobrecarga de recursión en memoria y fallos de caché.
* **La Inmunidad del Árbol B+:** Demuestra visualmente el poder del auto-balanceo. Sus nodos se dividen internamente manteniendo una altura mínima y constante, preservando su velocidad $O(\log N)$ intacta.

*Las gráficas comparativas con barras de error se generan automáticamente en el directorio raíz al finalizar la ejecución del script.*

---

## 📄 Licencia

Este proyecto es de uso exclusivamente académico para la asignatura de Estructuras de Datos.

---

## Nota
Se utilizó la IA para generar las graficas y entender la el comportamiento de los árboles frente a las listas 

