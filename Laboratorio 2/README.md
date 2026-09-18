# Árbol de Merkle

Implementación de un Árbol de Merkle con SHA-256, prueba de inclusión y verificación.

## Especificaciones implementadas

- **Hoja:** SHA-256 de un bloque de datos (transacción).
- **Nodo interno:** SHA-256 de la concatenación (en hexadecimal) de los hashes de sus dos hijos.
- **Cantidad impar:** si un nivel tiene un número impar de nodos, el último se duplica.
- **Merkle Root:** hash del nivel superior; representa todo el conjunto de datos.

## Requisitos y ejecución

Solo usa la librería estándar (`hashlib`). 

```bash
python merkle_tree.py
```

## Estructura

```
.
├── merkle_tree.py     # Código fuente + experimento
├── README.md
└── capturas/          # Capturas de verificación válida e inválida
```

## Diseño

La clase `MerkleTree` guarda **todos los niveles** del árbol (`levels[0]` = hojas,
`levels[-1]` = raíz), lo que permite dibujar el árbol y generar pruebas.

| Método | Descripción |
|---|---|
| `MerkleTree(transactions)` | Construye el árbol. |
| `.root` | Atributo con la Merkle Root (se calcula al construir el árbol). |
| `.get_proof(index)` | Prueba de inclusión: lista de `(hash_hermano, "left"/"right")`. |
| `.render()` | Diagrama ASCII del árbol. |
| `verify_proof(data, proof, root)` | Función independiente: recalcula la raíz desde el dato y la prueba. No necesita el árbol. |

### ¿Cómo funciona la prueba de inclusión?

Para demostrar que una transacción pertenece al árbol **no se necesita el árbol
completo**, solo un hash hermano por nivel (O(log n)). El verificador:

1. Calcula el hash de la transacción.
2. Lo combina con cada hermano de la prueba (respetando si va a la izquierda o derecha).
3. Compara el resultado con la Merkle Root conocida.

Si cualquier bit del dato cambia, el resultado difiere de la raíz y la verificación falla.

## Diagrama del árbol construido (5 transacciones)

```
RAÍZ  4baeb803…
├── Nodo  cc3d2a66…
│   ├── Nodo  08773624…
│   │   ├── H(T1)  23f76c36…
│   │   └── H(T2)  8885a3b9…
│   └── Nodo  78cca931…
│       ├── H(T3)  59be14a3…
│       └── H(T4)  0c0421f8…
└── Nodo  146589b3…
    ├── Nodo  d2a4447f…
    │   ├── H(T5)  fe0fc8b8…
    │   └── H(T5) (copia)  fe0fc8b8…
    └── Nodo (copia)  d2a4447f…
```

Las 5 hojas son impares, por lo que **H(T5) se duplica**. En el siguiente nivel
quedan 3 nodos (también impar), por lo que el nodo `d2a4447f…` **se duplica de nuevo**.

## Resultados del experimento

**Merkle Root original:**
`4baeb80336372a2f27c4ef8e36de836bbd1721805f0edcdddaebee59817fbbd2`

### 1. Modificar una transacción → la raíz cambia

| | Transacción 2 | Merkle Root |
|---|---|---|
| Original | `Bob envía 5 BTC a Charlie` | `4baeb803…fbbd2` |
| Alterada | `Bob envía 500 BTC a Charlie` | `13e138ca…bc343` |

### 2. Prueba de inclusión de la transacción 3

```
Paso 1: right 0c0421f8…   (hash de T4)
Paso 2: left  08773624…   (nodo T1+T2)
Paso 3: right 146589b3…   (nodo T5+T5+copia)
```

Resultado: ✅ **VERIFICACIÓN VÁLIDA**

### 3. Verificación con un dato incorrecto

Dato falso: `Transacción 3: Charlie envía 2000 BTC a Dave`

Resultado: ✅ **La verificación falla** (comportamiento esperado).

## Capturas de pantalla

<img width="807" height="532" alt="resultado1" src="https://github.com/user-attachments/assets/e59ba29f-8bc2-479f-9936-c0f7685bca77" />

<img width="815" height="512" alt="resultado2" src="https://github.com/user-attachments/assets/a815b1e9-9898-411a-b808-6dc018128dc3" />
 
<img width="785" height="302" alt="resultado3" src="https://github.com/user-attachments/assets/d7be466d-5110-4470-9e7f-e998bc726009" />

 <img width="792" height="157" alt="resultado4" src="https://github.com/user-attachments/assets/9f8a5158-420b-4b4a-b44d-3e48cc0c907d" />


## Notas

- Se concatenan los hashes en **hexadecimal** (texto). Bitcoin real concatena los
  bytes crudos y aplica doble SHA-256; 
- Duplicar el último nodo permite que dos listas de transacciones distintas
  (p. ej. `[a, b, c]` y `[a, b, c, c]`) generen la misma raíz (CVE-2012-2459 en Bitcoin).
  Es una limitación conocida de esta regla, requerida por el enunciado.
- Se usó la IA para generar la estructura del readme y para complementar el código que se tenía de la construcción del árbol de Merkle. De igual manera se utilizo para profundizar en el tema y de esa forma encontrar opciones para optimizar el código. 
