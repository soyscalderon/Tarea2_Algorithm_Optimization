import argparse

def inverse_greedy_knapsack(values: list[int], weights: list[int], capacity: int):
    order = sorted(range(len(values)), key=lambda i: weights[i])   # lightest item first
    chosen, used, total = [], 0, 0
    for i in order:                                 # heavier items never fit again once skipped
        if used + weights[i] <= capacity:
            chosen.append(i)
            used += weights[i]
            total += values[i]
    return chosen, used, total

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inverse greedy knapsack.")
    parser.add_argument("--graph", action="store_true",
                        help="Also generate the matplotlib figures.")
    args = parser.parse_args()

    items, values, weights, capacity = ["A", "B", "C"], [60, 100, 120], [10, 20, 30], 50
    chosen, used, total = inverse_greedy_knapsack(values, weights, capacity)
    print("Inverse Greedy Knapsack (Choose less weight first)\n")
    print(f"Items = {[i for i in items]}  Values = {[i for i in values]}  Weight = {[i for i in weights]}  Capacity = {capacity}")
    print(f"Selected = {[items[i] for i in chosen]}  Capacity used = {used}/{capacity}  Total value = {total}")

# Graficas
if __name__ == "__main__" and args.graph:
    import matplotlib.pyplot as plt
    from pathlib import Path

    def ratio_greedy_knapsack(values: list[int], weights: list[int], capacity: int):
        """Greedy by value-to-weight ratio: best ratio first."""
        order = sorted(range(len(values)), key=lambda i: values[i] / weights[i], reverse=True)
        chosen, used, total = [], 0, 0
        for i in order:
            if used + weights[i] <= capacity:
                chosen.append(i)
                used += weights[i]
                total += values[i]
        return chosen, used, total

    # Small instance where "least weight first" gives a worse result than "value/weight"
    comparison_items = ["A", "B", "C"]     # A: treasure, B and C: light but worthless
    comparison_values = [100, 9, 8]
    comparison_weights = [10, 1, 2]
    comparison_capacity = 10

    least_weight_result = inverse_greedy_knapsack(comparison_values, comparison_weights,
                                                  comparison_capacity)
    ratio_result = ratio_greedy_knapsack(comparison_values, comparison_weights,
                                         comparison_capacity)
    method_names = ["Least weight first", "Value/weight ratio"]
    method_results = [least_weight_result, ratio_result]

    print("\nGreedy comparison on the designed instance")
    print(f"Values = {comparison_values}  Weights = {comparison_weights}  "
          f"Capacity = {comparison_capacity}")
    for method_name, (chosen_items, used_capacity, total_value) in zip(method_names,
                                                                      method_results):
        print(f"{method_name:20s}: selected = {[comparison_items[i] for i in chosen_items]}"
              f"  capacity used = {used_capacity}/{comparison_capacity}"
              f"  total value = {total_value}")

    figure_directory = Path(__file__).resolve().parents[1] / "graphs"
    figure_directory.mkdir(parents=True, exist_ok=True)

    knapsack_figure, (selected_axis, totals_axis) = plt.subplots(1, 2, figsize=(12, 5))
    bar_width = 0.35
    item_positions = list(range(len(comparison_items)))

    # Left graph: which objects each method selects
    least_weight_selection = [int(i in least_weight_result[0]) for i in item_positions]
    ratio_selection = [int(i in ratio_result[0]) for i in item_positions]
    selected_axis.bar([p - bar_width / 2 for p in item_positions], least_weight_selection,
                      bar_width, label=method_names[0])
    selected_axis.bar([p + bar_width / 2 for p in item_positions], ratio_selection,
                      bar_width, label=method_names[1])
    selected_axis.set_xticks(item_positions, comparison_items)
    selected_axis.set_ylim(0, 1.4)
    selected_axis.set_ylabel("Selected (1 = yes, 0 = no)")
    selected_axis.set_title("Objects selected")
    selected_axis.grid(alpha=0.3, axis="y")
    selected_axis.legend()

    # Right graph: capacity used and total value of each method
    method_positions = list(range(len(method_names)))
    capacity_bars = totals_axis.bar([p - bar_width / 2 for p in method_positions],
                                    [result[1] for result in method_results],
                                    bar_width, label="Capacity used")
    value_bars = totals_axis.bar([p + bar_width / 2 for p in method_positions],
                                 [result[2] for result in method_results],
                                 bar_width, label="Total value")
    totals_axis.bar_label(capacity_bars, fmt="%g")
    totals_axis.bar_label(value_bars, fmt="%g")
    totals_axis.set_xticks(method_positions, method_names)
    totals_axis.set_ylim(0, 115)
    totals_axis.set_ylabel("Capacity units / value units")
    totals_axis.set_title("Capacity used vs total value")
    totals_axis.grid(alpha=0.3, axis="y")
    totals_axis.legend()

    knapsack_figure.suptitle("Greedy knapsack: least weight first vs value/weight ratio"
                             f" (capacity = {comparison_capacity})")
    knapsack_figure.tight_layout()

    knapsack_path = figure_directory / "2.knapsack_greedy.png"
    knapsack_figure.savefig(knapsack_path, dpi=150)
    print(f"\nFigure saved to {knapsack_path}")
    
