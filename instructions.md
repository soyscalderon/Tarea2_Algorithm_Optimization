# Ejercicios

## Instrucciones

A continuación se presentan los ejercicios que debes realizar. Implementa los algoritmos, genera las gráficas necesarias para respaldar tus experimentos y responde las preguntas analíticas en tu reporte final.

## Requisitos de entrega

### 1. Repositorio (GitHub / GitLab)

- Incluye en tu reporte la URL pública de tu repositorio.
- Organiza el código y los recursos con la estructura exacta solicitada por el curso o la rúbrica.

### 2. Video de demostración (máximo 8 minutos)

- Adjunta un enlace a tu video (YouTube, Loom, Google Drive u otro servicio accesible).
- Muestra la ejecución en vivo del código y explica brevemente las visualizaciones generadas.

## Ejercicio 1: Aceleración paralela (*Parallel Speedup*)

### Indicaciones

- Ejecuta `estimate_pi` con **1, 2, 4 y 8 procesos**.

### Visualización

- Grafica la aceleración (*speedup*) frente al número de procesos.
- Incluye en la gráfica la línea de aceleración ideal.

### Análisis

Explica por qué la aceleración no es perfectamente lineal. Considera los sobrecostos de comunicación y sincronización, así como la ley de Amdahl.

## Ejercicio 2: Análisis algorítmico (*Greedy Knapsack*)

### Indicaciones

- Modifica el algoritmo voraz de la mochila para priorizar los objetos de **menor peso primero**.

### Visualización

- Presenta una tabla o gráfica de barras que compare ambos métodos en cuanto a:
  - Objetos seleccionados.
  - Capacidad utilizada.
  - Valor total obtenido.

### Entregable

Diseña una instancia pequeña en la que el criterio de menor peso produzca un resultado peor que el método basado en la relación **valor/peso**.

## Ejercicio 3: Búsqueda local (2-opt para TSP)

### Indicaciones

- Implementa la heurística **2-opt** para el problema del agente viajero (*Traveling Salesperson Problem*, TSP).

### Experimento

Evalúa el número de mejoras necesarias para alcanzar el óptimo local desde estos dos escenarios:

1. Una solución inicial **aleatoria**.
2. Una solución inicial generada mediante **Vecino Más Cercano**, comenzando desde un nodo aleatorio.

### Visualización

Utiliza un diagrama de caja o una gráfica de barras para comparar:

- El número de mejoras realizadas.
- La calidad del óptimo local alcanzado.

### Análisis

¿La solución inicial de Vecino Más Cercano requiere menos mejoras para converger que una solución inicial aleatoria? Justifica tu respuesta con los resultados y las gráficas.

## Ejercicio 4: Ajuste de parámetros (*Simulated Annealing*)

### Indicaciones

- Implementa **Recocido Simulado** (*Simulated Annealing*) usando **2-opt** como operador de movimiento sobre una solución inicial aleatoria para el TSP.
- Evalúa distintos esquemas de enfriamiento (*cooling schedules*), por ejemplo, lineal y exponencial.

### Visualizaciones

1. Curvas de convergencia: costo frente a iteraciones o temperatura.
2. Gráfica comparativa de tiempo de ejecución frente a calidad de la solución final.

### Análisis

Explica cómo afecta cada esquema de enfriamiento a la calidad del resultado y al tiempo de cómputo.

## Ejercicio 5: Razón de aproximación (MST Approximation)

### Indicaciones

- Ejecuta el algoritmo de aproximación basado en un árbol de expansión mínima (*Minimum Spanning Tree*, MST) sobre **100 instancias aleatorias de 9 ciudades** para el TSP.

### Visualizaciones

1. Crea un histograma o gráfico de dispersión de la razón de aproximación:

   `C_obtenido / C_óptimo`

   Incluye una línea de referencia en el límite teórico de **2**.
2. Crea una gráfica comparativa (diagramas de caja o barras) del costo obtenido con:
   - MST puro.
   - MST + 2-opt.
   - Búsqueda Local.
   - Recocido Simulado.

### Análisis

- ¿Qué tan cerca se mantiene la razón de aproximación observada del límite teórico de 2?
- ¿Qué impacto tiene aplicar **2-opt** como postprocesamiento al resultado de MST, en comparación con los resultados de los experimentos anteriores?