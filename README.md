# Taller: Estructuras de Árboles y Análisis Sintáctico

Este repositorio contiene la solución teórica y práctica del taller sobre estructuras de datos en árbol, recorridos (DFS / BFS), complejidad computacional y análisis sintáctico mediante gramáticas LL(1).

---

- Julian Beltran
- Santiago Ortegon
- Juan Orjuela

---

## Contenido

- **`Taller_Sintactico_Codigo.py`**: Implementación en Python que incluye:
  - Estructura de árbol general (`Nodo`).
  - Recorridos en profundidad (**DFS** recursivo e iterativo, cálculo de altura, conteo de hojas y búsqueda).
  - Recorridos en anchura (**BFS** con cola y exploración por niveles).
  - Construcción del árbol de análisis sintáctico para la expresión `id + id * id` con gramática LL(1).
- **`Taller_Sintactico_Solucion.pdf`**: Documento con el desarrollo completo y justificación teórica de cada punto del taller.

---

## Requisitos y Ejecución

Solo requiere **Python 3.x** (no utiliza librerías externas).

Para ejecutar las pruebas y demostraciones en consola:

```bash
python Taller_Sintactico_Codigo.py
