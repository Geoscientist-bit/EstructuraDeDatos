# Laboratorio 1

## Manipulación eficiente de matrices gigantes en disco (100000 x 100000)
**Estudiante:** Jhon Edison Muñoz Banguero

### Descripción del proyecto
Este proyecto resuelve el desafío técnico de crear, almacenar, manipular y mostrar una matriz de de **100000 x 100000 elementos**

Si guardáramos esta matriz de forma tradicional (por ejemplo, en texto plano o cargándola completa en memoria), requeriría más de **40 GB de RAM**, provocando un fallo de desbordamiento (*Out of Memory*).

### Estrategia de Optimización

* **Consumo excesivo de RAM:** En lugar de intentar cargar la matriz en memoria (lo que requeriría >40 GB de RAM), el script procesa y empaqueta la información por bloques controlados (Chunks). La matriz completa nunca reside en la memoria RAM, manteniendo el consumo estable por debajo de los 15 MB.
* **Escritura lenta a disco:** El cuello de botella tradicional de escribir gigabytes de datos se elimina aplicando **compresión GZIP binaria al vuelo**. Al reducir el volumen de datos en más de un 99%, la carga de estrés de escritura en el disco se reduce drásticamente y el almacenamiento final es minúsculo.
* **Optimización en Manipulación, Creación, Almacenamiento y Lectura:** Se implementa un mecanismo de salto secuencial estructurado en bytes. Esto permite inspeccionar fragmentos de la matriz o celdas de forma ágil sin necesidad de descomprimir el archivo completo en el disco o en la RAM.

### Requisitos
* Python 3.x instalado

### Instrucciones de Uso
1. **Creación:** Ejecute `python generar_matriz.py` para construir el archivo optimizado en disco (`matriz_gigante.bin.gz`).
2. **Verificación ("Mostrar"):** Ejecute `python verificar_matriz.py` para visualizar y demostrar que el contenido ha sido almacenado de manera correcta.
