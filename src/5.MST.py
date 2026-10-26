import argparse
import itertools
import math
import random

def mst_prim(city_coordinates):
    """Prim's algorithm from city 0; returns the tree as {node: children}."""
    cheapest_edge = {v: (math.dist(city_coordinates[0], city_coordinates[v]), 0)
                     for v in range(1, len(city_coordinates))}
    children = {v: [] for v in range(len(city_coordinates))}
    while cheapest_edge:
        node = min(cheapest_edge, key=lambda u: cheapest_edge[u][0])
        parent = cheapest_edge.pop(node)[1]              # add the cheapest edge to the tree
        children[parent].append(node)
        for other in cheapest_edge:
            distance = math.dist(city_coordinates[node], city_coordinates[other])
            if distance < cheapest_edge[other][0]:
                cheapest_edge[other] = (distance, node)
    return children

def preorder_tour(children, root=0):
    """Walk around the tree; visiting each city once = shortcutting repeated cities."""
    return [root] + [c for child in children[root] for c in preorder_tour(children, child)]

def tour_length(city_coordinates, tour):
    return sum(math.dist(city_coordinates[tour[i]], city_coordinates[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def optimal_tour_length(city_coordinates):
    """Brute force over all tours starting at city 0: 8! = 40,320 tours."""
    return min(tour_length(city_coordinates, (0,) + permutation)
               for permutation in itertools.permutations(range(1, len(city_coordinates))))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TSP approximation with an MST tour.")
    parser.add_argument("--graph", action="store_true",
                        help="Also generate the matplotlib figures.")
    args = parser.parse_args()

    random.seed(7)
    instance_count, city_count = 100, 9

    print("Travelling Salesman Problem with MST (100 instances of 9 cities in a 10x10 grid)\n")
    
    ratios = []
    for instance in range(1, instance_count + 1):
        # Uses random coordinates in a 10x10 grid
        city_coordinates = [(random.uniform(0, 10), random.uniform(0, 10))
                            for _ in range(city_count)]
        approx_cost = tour_length(city_coordinates, preorder_tour(mst_prim(city_coordinates)))
        optimal_cost = optimal_tour_length(city_coordinates)
        ratio = approx_cost / optimal_cost
        ratios.append(ratio)
        print(f"Instance {instance:3d}: MST = {approx_cost:6.2f}  "
              f"optimal = {optimal_cost:6.2f}  ratio = {ratio:.3f}")

    print(f"\nMean ratio   = {sum(ratios) / len(ratios):.3f}")
    print(f"Min ratio    = {min(ratios):.3f}")
    print(f"Max ratio    = {max(ratios):.3f}   (theoretical bound = 2)")

# Graficas
if __name__ == "__main__" and args.graph:
    import importlib.util
    import matplotlib.pyplot as plt
    from pathlib import Path

    def load_sibling_module(file_name, module_name):
        """Load a sibling script (their names start with a digit, so importlib is needed)."""
        spec = importlib.util.spec_from_file_location(module_name,
                                                      Path(__file__).with_name(file_name))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    tsp_module = load_sibling_module("3.TSP.py", "tsp_two_opt")
    sa_module = load_sibling_module("4.simulated_annealing.py", "simulated_annealing_module")

    figure_directory = Path(__file__).resolve().parents[1] / "graphs"
    figure_directory.mkdir(parents=True, exist_ok=True)

    # 1) Histogram of the approximation ratio (ratios computed above), reference line at 2
    mean_ratio = sum(ratios) / len(ratios)
    ratio_figure, ratio_axis = plt.subplots(figsize=(8, 5))
    ratio_axis.hist(ratios, bins=15, edgecolor="black", alpha=0.75, label="Observed ratios")
    ratio_axis.axvline(2, color="red", linestyle="--", linewidth=2,
                       label="Theoretical bound (2)")
    ratio_axis.axvline(mean_ratio, color="green", linestyle="-.", linewidth=2,
                       label=f"Observed mean ({mean_ratio:.3f})")
    ratio_axis.set_xlabel("Approximation ratio (C_MST / C_optimal)")
    ratio_axis.set_ylabel("Number of instances")
    ratio_axis.set_title(f"MST approximation ratio over {len(ratios)} instances of {city_count}"
                         " cities")
    ratio_axis.grid(alpha=0.3)
    ratio_axis.legend()
    ratio_figure.tight_layout()

    ratio_path = figure_directory / "5.mst_approximation_ratio.png"
    ratio_figure.savefig(ratio_path, dpi=150)
    print(f"\nFigure saved to {ratio_path}")

    # 2) Cost of each method on the same 100 instances generated above (same seed)
    random.seed(7)
    method_costs = {"MST": [], "MST + 2-opt": [], "Local search": [],
                    "Simulated annealing": []}
    for _ in range(instance_count):
        instance_coordinates = [(random.uniform(0, 10), random.uniform(0, 10))
                                for _ in range(city_count)]

        mst_tour = preorder_tour(mst_prim(instance_coordinates))
        method_costs["MST"].append(tour_length(instance_coordinates, mst_tour))

        improved_mst_tour, _ = tsp_module.two_opt_local_search(mst_tour, instance_coordinates)
        method_costs["MST + 2-opt"].append(tour_length(instance_coordinates, improved_mst_tour))

        random_tour = list(range(city_count))
        random.shuffle(random_tour)
        local_search_tour, _ = tsp_module.two_opt_local_search(random_tour, instance_coordinates)
        method_costs["Local search"].append(tour_length(instance_coordinates, local_search_tour))

        sa_initial_tour = list(range(city_count))
        random.shuffle(sa_initial_tour)
        sa_tour = sa_module.simulated_annealing(
            sa_initial_tour, instance_coordinates, sa_module.exponential_cooling_schedule())
        method_costs["Simulated annealing"].append(tour_length(instance_coordinates, sa_tour))

    comparison_figure, comparison_axis = plt.subplots(figsize=(9, 6))
    comparison_axis.boxplot([method_costs[method_name] for method_name in method_costs],
                            tick_labels=list(method_costs))
    comparison_axis.set_ylabel("Tour cost")
    comparison_axis.set_title(f"TSP methods compared on the same {instance_count} instances"
                              f" ({city_count} cities)")
    comparison_axis.grid(alpha=0.3, axis="y")
    comparison_figure.tight_layout()

    comparison_path = figure_directory / "5.mst_method_comparison.png"
    comparison_figure.savefig(comparison_path, dpi=150)
    print(f"Figure saved to {comparison_path}")
    
