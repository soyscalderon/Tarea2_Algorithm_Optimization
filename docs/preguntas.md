## Ejercicio 1: Aceleración paralela (*Parallel Speedup*)

### Análisis

Explica por qué la aceleración no es perfectamente lineal. Considera los sobrecostos de comunicación y sincronización, así como la ley de Amdahl.

`La aceleración no es lineal porque solo una parte del trabajo es paralelizable: la ley de Amdahl dice que la fracción secuencial (crear el pool, repartir las 8 semillas, serializar/entregar los resultados por IPC) limita la ganancia máxima, y a eso se suman los sobrecostos de comunicación y sincronización entre procesos, que crecen con el número de procesos. Además solo hay 8 tareas, así que más procesos que tareas no aportan. En los resultados: con 1 proceso se obtiene 0.92x (incluso más lento que la versión secuencial, por el sobrecosto del pool), con 2 procesos 1.95x, con 4 procesos 3.54x y con 8 procesos solo 4.68x en lugar de 8x; con 12 procesos la aceleración baja a 4.54x porque los procesos adicionales solo compiten por las 8 tareas. Por eso en la gráfica la curva observada se separa progresivamente de la línea ideal y se estanca alrededor de 4.5-4.7x.`

## Ejercicio 2: Análisis algorítmico (*Greedy Knapsack*)

### Análisis

Diseña una instancia pequeña en la que el criterio de menor peso produzca un resultado peor que el método basado en la relación **valor/peso**.

`Con capacidad 10: objeto A con valor 100 y peso 10 (relación valor/peso = 10), objeto B con valor 9 y peso 1 (relación 9), objeto C con valor 8 y peso 2 (relación 4). El criterio de menor peso toma primero B y luego C, usando solo 3/10 de la capacidad y obteniendo un valor total de 17; como ya no queda espacio para A (3+10 > 10), se queda con objetos ligeros pero casi inútiles. El criterio valor/peso toma primero A (la mejor relación), usa 10/10 de la capacidad y obtiene un valor total de 100. Así, el método de menor peso termina con un valor 17 frente a 100 del valor/peso (y además subutiliza la capacidad), demostrando que elegir por ligereza puede ser muy malo cuando los objetos ligeros no aportan valor.`

## Ejercicio 3: Búsqueda local (2-opt para TSP)

### Análisis

¿La solución inicial de Vecino Más Cercano requiere menos mejoras para converger que una solución inicial aleatoria? Justifica tu respuesta con los resultados y las gráficas.

`Sí. En las 50 pruebas con 10 ciudades, el tour aleatorio necesita en promedio 9.3 mejoras 2-opt para alcanzar el óptimo local (mediana ~9, con valores entre 2 y 16), mientras que el tour de Vecino Más Cercano solo 2.6 mejoras (mediana ~2, entre 0 y 8): las dos cajas de la gráfica de mejoras quedan claramente separadas. La razón es que el Vecino Más Cercano ya entrega un tour razonable, así que 2-opt solo debe pulir unos pocos cruces de aristas, mientras que un tour aleatorio tiene muchas aristas cruzadas que corregir. En cuanto a la calidad, las gráficas muestran óptimos locales prácticamente iguales (costo medio 28.31 con inicio aleatorio frente a 28.29 con Vecino Más Cercano, con cajas casi idénticas), es decir, el Vecino Más Cercano converge mucho más rápido sin sacrificar calidad.`

## Ejercicio 4: Ajuste de parámetros (*Simulated Annealing*)

### Análisis

Explica cómo afecta cada esquema de enfriamiento a la calidad del resultado y al tiempo de cómputo.

`El exponencial (T = 100 * 0.995^t) se enfría rápido: termina en 2297 pasos, tarda en promedio 0.0069 s y, en esta instancia, alcanza el mismo costo final que el lineal (26.71); es el más rápido porque acepta movimientos aleatorios solo durante las primeras iteraciones, pero explora poco y corre el riesgo de quedar atrapado en un óptimo local malo si la temperatura baja demasiado pronto. El lineal (T baja de 100 a 0 en 20000 pasos) mantiene la temperatura alta mucho más tiempo: en la curva de convergencia el costo oscila fuertemente casi hasta el final (acepta mucha solución peor durante todo el recorrido) y recién se estabiliza en los últimos pasos; explora más, así que tiene más probabilidad de escapar de óptimos locales, pero cuesta bastante más tiempo de cómputo: 0.0589 s, unas 8.5 veces más que el exponencial, por hacer 20000 pasos en lugar de 2297. En resumen: el exponencial gana velocidad a costa de exploración, el lineal gana exploración a costa de tiempo; en esta instancia ambos llegaron a la misma calidad (26.71), pero en instancias más difíciles la exploración extra del lineal podría traducirse en un mejor resultado final.`

## Ejercicio 5: Razón de aproximación (MST Approximation)

### Análisis

- ¿Qué tan cerca se mantiene la razón de aproximación observada del límite teórico de 2?
- ¿Qué impacto tiene aplicar **2-opt** como postprocesamiento al resultado de MST, en comparación con los resultados de los experimentos anteriores?

`La razón observada se mantiene muy por debajo del límite: en las 100 instancias de 9 ciudades los ratios van de 1.000 a 1.324 con una media de 1.119, o sea, el tour MST queda a solo ~12% del óptimo; en el histograma todo el dato está pegado a 1.0-1.35 y la línea del límite 2 queda muy a la derecha, lejos de cualquier instancia obtenida. Esto es esperado: la cota 2 es un peor caso garantizado para toda instancia métrica, pero con pocas ciudades y puntos uniformes en el plano casi nunca se alcanza. Respecto a 2-opt como postprocesamiento, la gráfica comparativa muestra que baja el costo mediano del MST puro (de ~31 a ~28), llevándolo al mismo nivel que la búsqueda local y el recocido simulado; es decir, un tour MST seguido de 2-opt prácticamente iguala a los métodos que arrancan de una solución aleatoria, y supera claramente al MST puro, mientras que los tres métodos "pulidores" quedan empatados entre sí.`