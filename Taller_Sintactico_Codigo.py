"""
Taller de arboles, recorridos y complejidad computacional

Este archivo resuelve la parte practica del taller:
  - Punto 3: arbol general + DFS (recursivo, iterativo, busqueda, hojas, altura)
  - Punto 4: BFS con cola (orden de visita, niveles, busqueda con nivel)
  - Punto 5: arbol sintactico de "id + id * id" con la gramatica LL(1) del taller

Para ejecutarlo:  python Taller_Sintactico_Codigo.py
"""

from collections import deque


# ---------------------------------------------------------------------------
# ESTRUCTURA DE DATOS: arbol general (cada nodo puede tener 0 o mas hijos)
# ---------------------------------------------------------------------------

class Nodo:
    """Un nodo del arbol. Guarda un valor y la lista de referencias a sus hijos.

    Uso una lista y no dos punteros (izq/der) porque el taller pide un arbol
    GENERAL: el nodo A del punto 1 tiene tres hijos, asi que un arbol binario
    no me serviria.
    """

    def __init__(self, valor):
        self.valor = valor
        self.hijos = []          # lista de objetos Nodo

    def agregar(self, hijo):
        """Cuelga un hijo de este nodo y lo devuelve (asi puedo encadenar)."""
        self.hijos.append(hijo)
        return hijo

    def es_hoja(self):
        """Un nodo es hoja cuando no tiene hijos, es decir grado 0."""
        return len(self.hijos) == 0

    def __repr__(self):
        return f"Nodo({self.valor})"


def construir_arbol_punto1():
    """Arma el arbol de la tabla padre-hijo del punto 1.

        A -> B, C, D      B -> E, F      C -> G
        D -> H, I         F -> J         H -> K, L
    """
    # Creo todos los nodos primero y los guardo en un diccionario para
    # poder enlazarlos por nombre sin perderme.
    n = {letra: Nodo(letra) for letra in "ABCDEFGHIJKL"}

    relaciones = {
        "A": ["B", "C", "D"],
        "B": ["E", "F"],
        "C": ["G"],
        "D": ["H", "I"],
        "F": ["J"],
        "H": ["K", "L"],
    }

    for padre, hijos in relaciones.items():
        for h in hijos:
            n[padre].agregar(n[h])

    return n["A"]            # devuelvo la raiz


# ---------------------------------------------------------------------------
# PUNTO 3: RECORRIDOS EN PROFUNDIDAD (DFS)
# ---------------------------------------------------------------------------

def dfs_preorden_recursivo(nodo, visitados=None):
    """DFS recursivo en preorden: primero el padre y despues cada hijo.

    La recursion hace el trabajo de la pila por mi: cada llamada pendiente es
    un nodo al que todavia tengo que volver.
    Tiempo:  O(n)  -> toca todos los nodos una sola vez.
    Espacio: O(h)  -> profundidad maxima de la pila de llamadas.
    """
    if visitados is None:
        visitados = []

    if nodo is None:
        return visitados

    visitados.append(nodo.valor)             # visito el padre (PRE-orden)
    for hijo in nodo.hijos:                  # y luego bajo por cada hijo
        dfs_preorden_recursivo(hijo, visitados)

    return visitados


def dfs_preorden_iterativo(raiz):
    """El mismo recorrido pero con una pila explicita, sin recursion.

    Detalle importante: apilo los hijos AL REVES (reversed) porque la pila es
    LIFO; si los apilara en orden normal saldria primero el ultimo hijo y el
    resultado no coincidiria con el recursivo.
    """
    if raiz is None:
        return []

    visitados = []
    pila = [raiz]

    while pila:
        actual = pila.pop()                  # saco el ultimo que entro
        visitados.append(actual.valor)
        for hijo in reversed(actual.hijos):  # para que el primer hijo quede arriba
            pila.append(hijo)

    return visitados


def dfs_buscar(nodo, objetivo, contador=None):
    """Busca un valor con DFS y ademas cuenta cuantos nodos tuvo que mirar.

    Devuelve (encontrado, nodos_visitados).
    Mejor caso O(1) si el valor esta en la raiz; peor caso O(n) si el valor
    esta en la ultima hoja o si no existe (toca recorrer todo el arbol).
    """
    if contador is None:
        contador = [0]                       # lista de un elemento para que la
                                             # cuenta sobreviva a la recursion

    if nodo is None:
        return False, contador[0]

    contador[0] += 1
    if nodo.valor == objetivo:
        return True, contador[0]             # corto apenas lo encuentro

    for hijo in nodo.hijos:
        encontrado, _ = dfs_buscar(hijo, objetivo, contador)
        if encontrado:
            return True, contador[0]

    return False, contador[0]


def dfs_contar_hojas(nodo):
    """Cuenta los nodos sin hijos. Siempre O(n): no hay forma de saber cuantas
    hojas hay sin mirar todos los nodos."""
    if nodo is None:
        return 0
    if nodo.es_hoja():
        return 1
    return sum(dfs_contar_hojas(h) for h in nodo.hijos)


def dfs_altura(nodo):
    """Altura medida en aristas: una hoja sola tiene altura 0.

    Es un recorrido en POSTorden: necesito la altura de todos los hijos antes
    de poder decidir la del padre.
    """
    if nodo is None:
        return -1
    if nodo.es_hoja():
        return 0
    return 1 + max(dfs_altura(h) for h in nodo.hijos)


def dfs_contar_nodos(nodo):
    """Cantidad total de nodos, para reportarla en las pruebas."""
    if nodo is None:
        return 0
    return 1 + sum(dfs_contar_nodos(h) for h in nodo.hijos)


# ---------------------------------------------------------------------------
# PUNTO 4: RECORRIDO EN ANCHURA (BFS)
# ---------------------------------------------------------------------------

def bfs_orden_visita(raiz):
    """BFS clasico con cola FIFO: devuelve el orden de visita nivel por nivel.

    Uso deque porque popleft() es O(1); con una lista normal, pop(0) seria O(n)
    y el recorrido completo se volveria O(n^2).
    """
    if raiz is None:
        return []

    visitados = []
    cola = deque([raiz])

    while cola:
        actual = cola.popleft()              # sale el que lleva mas tiempo esperando
        visitados.append(actual.valor)
        for hijo in actual.hijos:
            cola.append(hijo)

    return visitados


def bfs_por_niveles(raiz):
    """Agrupa los nodos por nivel.

    El truco es procesar la cola por tandas: al empezar cada vuelta, todo lo
    que hay en la cola pertenece al mismo nivel, asi que mido su tamano y saco
    exactamente esa cantidad.
    """
    if raiz is None:
        return []

    niveles = []
    cola = deque([raiz])

    while cola:
        tam = len(cola)                      # cuantos nodos hay en este nivel
        nivel_actual = []
        for _ in range(tam):
            actual = cola.popleft()
            nivel_actual.append(actual.valor)
            for hijo in actual.hijos:
                cola.append(hijo)            # estos ya son del nivel siguiente
        niveles.append(nivel_actual)

    return niveles


def bfs_buscar(raiz, objetivo):
    """Busca un valor con BFS y reporta el nivel donde aparecio.

    Devuelve (encontrado, nivel, nodos_visitados). Como BFS avanza por niveles
    crecientes, el primer nodo que coincide es siempre el MENOS profundo que
    cumple la condicion.
    """
    if raiz is None:
        return False, -1, 0

    visitados = 0
    cola = deque([(raiz, 0)])                # guardo el nivel junto con el nodo

    while cola:
        actual, nivel = cola.popleft()
        visitados += 1
        if actual.valor == objetivo:
            return True, nivel, visitados
        for hijo in actual.hijos:
            cola.append((hijo, nivel + 1))

    return False, -1, visitados


# ---------------------------------------------------------------------------
# PUNTO 5: ARBOL SINTACTICO DE "id + id * id"
# ---------------------------------------------------------------------------
#
# Gramatica (ya sin recursion por la izquierda, lista para descendente):
#     E  -> T E'
#     E' -> + T E' | eps
#     T  -> F T'
#     T' -> * F T' | eps
#     F  -> ( E ) | id
#
# Escribo un analizador descendente recursivo: una funcion por no terminal.
# Cada funcion crea su propio nodo y le cuelga lo que vayan devolviendo las
# funciones que llama. El contador global me sirve para numerar los nodos en
# el orden exacto en que el analizador los va creando (punto 5.2).
# ---------------------------------------------------------------------------

class NodoSintactico(Nodo):
    """Nodo del arbol sintactico. Ademas del valor guarda el numero de creacion
    y si es terminal o no terminal, para poder contarlos despues."""

    def __init__(self, simbolo, numero, terminal=False):
        super().__init__(simbolo)
        self.numero = numero
        self.terminal = terminal

    def etiqueta(self):
        return f"{self.valor}({self.numero})"


class AnalizadorDescendente:
    """Analizador LL(1) hecho a mano para la gramatica del punto 5."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.contador = 0                    # numero del ultimo nodo creado
        self.traza = []                      # producciones aplicadas, en orden

    # --- utilidades del analizador ---------------------------------------

    def actual(self):
        """Token que estoy mirando (el lookahead). None si ya se acabo."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def nuevo(self, simbolo, terminal=False):
        """Crea un nodo y le asigna el siguiente numero consecutivo."""
        self.contador += 1
        return NodoSintactico(simbolo, self.contador, terminal)

    def consumir(self, esperado, padre):
        """Verifica el token actual, lo convierte en hoja y avanza."""
        if self.actual() != esperado:
            raise SyntaxError(f"Se esperaba '{esperado}' y llego '{self.actual()}'")
        hoja = self.nuevo(esperado, terminal=True)
        padre.agregar(hoja)
        self.pos += 1
        return hoja

    # --- una funcion por no terminal -------------------------------------

    def E(self):
        """E -> T E'"""
        nodo = self.nuevo("E")
        self.traza.append("E -> T E'")
        nodo.agregar(self.T())               # primero se crea y expande TODO T
        nodo.agregar(self.E_prima())         # y solo despues aparece E'
        return nodo

    def E_prima(self):
        """E' -> + T E'  |  eps"""
        nodo = self.nuevo("E'")
        if self.actual() == "+":
            self.traza.append("E' -> + T E'")
            self.consumir("+", nodo)
            nodo.agregar(self.T())
            nodo.agregar(self.E_prima())
        else:
            # No viene un '+', entonces aplico la produccion vacia.
            self.traza.append("E' -> eps")
            nodo.agregar(self.nuevo("eps", terminal=True))
        return nodo

    def T(self):
        """T -> F T'"""
        nodo = self.nuevo("T")
        self.traza.append("T -> F T'")
        nodo.agregar(self.F())
        nodo.agregar(self.T_prima())
        return nodo

    def T_prima(self):
        """T' -> * F T'  |  eps

        Aqui esta la clave de la precedencia: el '*' se queda DENTRO de T,
        o sea colgado mas abajo que el '+', que vive en E'.
        """
        nodo = self.nuevo("T'")
        if self.actual() == "*":
            self.traza.append("T' -> * F T'")
            self.consumir("*", nodo)
            nodo.agregar(self.F())
            nodo.agregar(self.T_prima())
        else:
            self.traza.append("T' -> eps")
            nodo.agregar(self.nuevo("eps", terminal=True))
        return nodo

    def F(self):
        """F -> ( E ) | id"""
        nodo = self.nuevo("F")
        if self.actual() == "(":
            self.traza.append("F -> ( E )")
            self.consumir("(", nodo)
            nodo.agregar(self.E())
            self.consumir(")", nodo)
        else:
            self.traza.append("F -> id")
            self.consumir("id", nodo)
        return nodo

    def analizar(self):
        """Arranca por el simbolo inicial y verifica que no sobren tokens."""
        raiz = self.E()
        if self.actual() is not None:
            raise SyntaxError(f"Sobraron tokens desde '{self.actual()}'")
        return raiz


def recorrido_postorden(nodo, salida=None):
    """Postorden: primero todos los hijos y de ultimo el padre."""
    if salida is None:
        salida = []
    for hijo in nodo.hijos:
        recorrido_postorden(hijo, salida)
    salida.append(nodo.etiqueta())
    return salida


def recorrido_preorden_sintactico(nodo, salida=None):
    """Preorden sobre el arbol sintactico, mostrando el numero de creacion."""
    if salida is None:
        salida = []
    salida.append(nodo.etiqueta())
    for hijo in nodo.hijos:
        recorrido_preorden_sintactico(hijo, salida)
    return salida


def bfs_sintactico_por_niveles(raiz):
    """Mismo BFS del punto 4 pero mostrando las etiquetas numeradas."""
    niveles = []
    cola = deque([raiz])
    while cola:
        tam = len(cola)
        nivel = []
        for _ in range(tam):
            actual = cola.popleft()
            nivel.append(actual.etiqueta())
            for hijo in actual.hijos:
                cola.append(hijo)
        niveles.append(nivel)
    return niveles


def estadisticas_arbol_sintactico(nodo):
    """Punto 5.7: en UN solo recorrido cuenta terminales, no terminales,
    producciones vacias y calcula la altura.

    Lo hago en postorden porque la altura del padre depende de la de los hijos.
    Tiempo O(n), espacio O(h). Devuelve un diccionario con los cuatro datos.
    """
    resultado = {"terminales": 0, "no_terminales": 0, "epsilon": 0, "altura": 0}

    def recorrer(n):
        if n.terminal:
            if n.valor == "eps":
                resultado["epsilon"] += 1    # las eps las cuento aparte
            else:
                resultado["terminales"] += 1
        else:
            resultado["no_terminales"] += 1

        if not n.hijos:
            return 0                         # hoja -> altura 0
        return 1 + max(recorrer(h) for h in n.hijos)

    resultado["altura"] = recorrer(nodo)
    return resultado


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL: imprime las evidencias de ejecucion
# ---------------------------------------------------------------------------

def linea(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def main():
    raiz = construir_arbol_punto1()

    # ---------------- PUNTO 3 ----------------
    linea("PUNTO 3 - RECORRIDOS DFS SOBRE EL ARBOL DEL PUNTO 1")

    print("DFS preorden recursivo :", " ".join(dfs_preorden_recursivo(raiz)))
    print("DFS preorden iterativo :", " ".join(dfs_preorden_iterativo(raiz)))
    print("Coinciden los dos      :",
          dfs_preorden_recursivo(raiz) == dfs_preorden_iterativo(raiz))
    print()
    print("Total de nodos         :", dfs_contar_nodos(raiz))
    print("Cantidad de hojas      :", dfs_contar_hojas(raiz))
    print("Altura del arbol       :", dfs_altura(raiz), "(medida en aristas)")

    print("\nPruebas de busqueda con DFS:")
    for objetivo, comentario in [("B", "valor cercano a la raiz"),
                                 ("L", "valor del ultimo nivel"),
                                 ("Z", "valor que no existe")]:
        encontrado, visitados = dfs_buscar(raiz, objetivo)
        estado = "encontrado" if encontrado else "no encontrado"
        print(f"  Buscar '{objetivo}' ({comentario}): {estado} "
              f"| nodos visitados: {visitados}")

    # ---------------- PUNTO 4 ----------------
    linea("PUNTO 4 - RECORRIDO BFS SOBRE EL ARBOL DEL PUNTO 1")

    print("Orden de visita BFS    :", " ".join(bfs_orden_visita(raiz)))
    print()
    for i, nivel in enumerate(bfs_por_niveles(raiz)):
        print(f"Nivel {i}: {', '.join(nivel)}")

    print("\nPruebas de busqueda con BFS (los mismos valores del punto 3):")
    for objetivo in ["B", "L", "Z"]:
        encontrado, nivel, visitados = bfs_buscar(raiz, objetivo)
        print(f"\n  Valor buscado: {objetivo}")
        print(f"  Resultado: {'encontrado' if encontrado else 'no encontrado'}")
        print(f"  Nivel del valor: {nivel if encontrado else 'no aplica'}")
        print(f"  Nodos visitados: {visitados}")

    # ---------------- PUNTO 5 ----------------
    linea("PUNTO 5 - ARBOL SINTACTICO DE  id + id * id")

    tokens = ["id", "+", "id", "*", "id"]
    print("Cadena de entrada:", " ".join(tokens))

    analizador = AnalizadorDescendente(tokens)
    arbol = analizador.analizar()

    print("\nProducciones aplicadas por el analizador descendente:")
    for i, produccion in enumerate(analizador.traza, start=1):
        print(f"  {i:2d}. {produccion}")

    print("\nNodos en el ORDEN EN QUE EL ANALIZADOR LOS CREO:")
    print("  " + "  ".join(recorrido_preorden_sintactico(arbol)))

    print("\nDFS preorden:")
    print("  " + "  ".join(recorrido_preorden_sintactico(arbol)))

    print("\nDFS postorden:")
    print("  " + "  ".join(recorrido_postorden(arbol)))

    print("\nBFS por niveles:")
    for i, nivel in enumerate(bfs_sintactico_por_niveles(arbol)):
        print(f"  Nivel {i}: {', '.join(nivel)}")

    print("\nEstadisticas del arbol sintactico (punto 5.7):")
    datos = estadisticas_arbol_sintactico(arbol)
    print(f"  Nodos no terminales      : {datos['no_terminales']}")
    print(f"  Nodos terminales         : {datos['terminales']}")
    print(f"  Producciones vacias (eps): {datos['epsilon']}")
    print(f"  Altura del arbol         : {datos['altura']}")
    total = datos['no_terminales'] + datos['terminales'] + datos['epsilon']
    print(f"  Total de nodos           : {total}")

    print("\nComprobacion: el orden de creacion y el preorden son identicos ->",
          recorrido_preorden_sintactico(arbol) ==
          sorted(recorrido_preorden_sintactico(arbol),
                 key=lambda e: int(e.split("(")[1][:-1])))


if __name__ == "__main__":
    main()
