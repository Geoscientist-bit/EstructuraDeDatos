'''
Laboratorio 2

Implementar un Árbol de Merkle con las siguientes especificaciones:
* Cada hoja contiene el hash SHA-256 de un bloque de datos.
* Cada nodo interno contiene el hash SHA-256 de la concatenación de sus dos hijos.
* Si el número de hojas o ramas es impar, la última se duplica.
* La raíz (Merkle Root) es el hash que representa todo el conjunto.

Experimento:
* Crear 5 transacciones de datos (pueden ser transacciones simuladas).
* Construir el árbol y mostrar la raíz.
* Modificar una transacción y demostrar que la raíz cambia.
* Generar una prueba de inclusión para la transacción 3 y verificar que es válida.
* verificar con un dato incorrecto → debe fallar.

'''
import hashlib
from typing import List, Tuple

# Una prueba es una lista de pasos: (hash_del_hermano, "left" | "right")
Proof = List[Tuple[str, str]]


def sha256_hex(data: str) -> str:
    """Devuelve el SHA-256 (hex) de un texto."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def verify_proof(data: str, proof: Proof, root: str) -> bool:
    """
    Verifica una prueba de inclusión.
    No necesita el árbol: solo el dato, la prueba y la raíz conocida.
    """
    current = sha256_hex(data)
    for sibling, position in proof:
        if position == "left":
            current = sha256_hex(sibling + current)
        else:
            current = sha256_hex(current + sibling)
    return current == root


class MerkleTree:
    def __init__(self, transactions: List[str]):
        if not transactions:
            raise ValueError("Se necesita al menos una transacción.")
        self.transactions = list(transactions)
        # levels[0] = hojas, levels[-1] = [raíz]. Cada nivel impar se guarda
        # ya con su último nodo duplicado.
        self.levels: List[List[str]] = []
        # Cantidad de nodos reales (sin copias) de cada nivel.
        self._real_sizes: List[int] = []
        # Merkle Root (se calcula en _build).
        self.root: str = ""
        self._build()

    
    # CONSTRUCCIÓN DEL ÁRBOL
    
    def _build(self) -> None:
        level = [sha256_hex(tx) for tx in self.transactions]
        while True:
            self._real_sizes.append(len(level))
            if len(level) == 1:
                self.levels.append(level)
                break
            if len(level) % 2 == 1:
                level = level + [level[-1]]  # duplicar el último
            self.levels.append(level)
            level = [
                sha256_hex(level[i] + level[i + 1])
                for i in range(0, len(level), 2)
            ]
        self.root = self.levels[-1][0]

    
    # PRUEBA DE INCLUSIÓN

    def get_proof(self, index: int) -> Proof:
        """Prueba de inclusión de la transacción en la posición `index` (base 0)."""
        if not 0 <= index < len(self.transactions):
            raise IndexError("Índice de transacción fuera de rango.")
        proof: Proof = []
        idx = index
        for level in self.levels[:-1]:
            if idx % 2 == 0:
                proof.append((level[idx + 1], "right"))
            else:
                proof.append((level[idx - 1], "left"))
            idx //= 2
        return proof

    
    # DIAGRAMA ASCII DEL ÁRBOL
    
    def render(self, short: int = 8) -> str:
        top = len(self.levels) - 1
        lines: List[str] = []

        def is_copy(level: int, idx: int) -> bool:
            return idx >= self._real_sizes[level]

        def label(level: int, idx: int) -> str:
            h = self.levels[level][idx][:short] + "…"
            if level == top:
                return f"RAÍZ  {h}"
            if level == 0:
                n = min(idx, self._real_sizes[0] - 1) + 1
                extra = " (copia)" if is_copy(level, idx) else ""
                return f"H(T{n}){extra}  {h}"
            extra = " (copia)" if is_copy(level, idx) else ""
            return f"Nodo{extra}  {h}"

        def walk(level: int, idx: int, prefix: str, connector: str) -> None:
            lines.append(prefix + connector + label(level, idx))
            if level == 0 or is_copy(level, idx):
                return  # hoja, o copia (no tiene subárbol propio)
            if connector == "":
                child_prefix = ""
            else:
                child_prefix = prefix + ("    " if connector == "└── " else "│   ")
            walk(level - 1, 2 * idx, child_prefix, "├── ")
            walk(level - 1, 2 * idx + 1, child_prefix, "└── ")

        walk(top, 0, "", "")
        return "\n".join(lines)



# EXPERIMENTO

def titulo(texto: str) -> None:
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def main() -> None:
    transactions = [
        "Transacción 1: Alice envía 10 BTC a Bob",
        "Transacción 2: Bob envía 5 BTC a Charlie",
        "Transacción 3: Charlie envía 2 BTC a Dave",
        "Transacción 4: Dave envía 1 BTC a Eve",
        "Transacción 5: Eve envía 0.5 BTC a Frank",
    ]

    # 1. Construir el árbol y mostrar la raíz
    titulo("1. CONSTRUCCIÓN DEL ÁRBOL (5 transacciones)")
    tree = MerkleTree(transactions)
    for i, tx in enumerate(transactions, start=1):
        print(f"  T{i}: {tx}")
    print(f"\nMerkle Root: {tree.root}\n")
    print(tree.render())

    # 2. Modificar una transacción -> la raíz cambia
    titulo("2. MODIFICAR UNA TRANSACCIÓN")
    modified = transactions.copy()
    modified[1] = "Transacción 2: Bob envía 500 BTC a Charlie"  # ¡alterada!
    tree_mod = MerkleTree(modified)
    print(f"Original : {transactions[1]}")
    print(f"Alterada : {modified[1]}\n")
    print(f"Raíz original: {tree.root}")
    print(f"Raíz alterada: {tree_mod.root}")
    print(f"¿Raíces distintas? -> {tree.root != tree_mod.root}")

    # 3. Prueba de inclusión para la transacción 3 (índice 2)
    titulo("3. PRUEBA DE INCLUSIÓN DE LA TRANSACCIÓN 3")
    idx = 2
    proof = tree.get_proof(idx)
    print(f"Transacción: {transactions[idx]}")
    print(f"Raíz de referencia: {tree.root}\n")
    print("Prueba (hash hermano + lado en que se concatena):")
    for step, (sibling, side) in enumerate(proof, start=1):
        print(f"  Paso {step}: {side:<5} {sibling}")

    valid = verify_proof(transactions[idx], proof, tree.root)
    print("\n✅ VERIFICACIÓN VÁLIDA" if valid else "\n❌ VERIFICACIÓN FALLIDA")
    print(f"   Resultado: {valid}")

    # 4. Verificar con un dato incorrecto -> debe fallar
    titulo("4. VERIFICACIÓN CON DATO INCORRECTO")
    wrong = "Transacción 3: Charlie envía 2000 BTC a Dave"
    invalid = verify_proof(wrong, proof, tree.root)
    print(f"Dato falso: {wrong}")
    print("\n✅ LA VERIFICACIÓN FALLÓ (comportamiento esperado)" if not invalid
          else "\n❌ ERROR: aceptó un dato falso")
    print(f"   Resultado: {invalid}")


if __name__ == "__main__":
    main()
