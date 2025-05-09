import matplotlib.pyplot as plt
import os


class GAVisualizer:
    def __init__(self, save_dir="results/plots"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def plot_fitness_curve(self, fitness_history, label=None, title="Evolução do Fitness", save_as="fitness_curve.png"):
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_history, marker='o', label=label or "Fitness")
        plt.title(title)
        plt.xlabel("Geração")
        plt.ylabel("Fitness")
        plt.grid(True)
        if label:
            plt.legend()
        filepath = os.path.join(self.save_dir, save_as)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath)
        plt.close()
        print(f"✅ Gráfico guardado em: {filepath}")

    def compare_fitness_curves(self, histories, labels, title="Comparação de Fitness", save_as="fitness_comparison.png"):
        plt.figure(figsize=(10, 6))
        for history, label in zip(histories, labels):
            plt.plot(history, marker='o', label=label)
        plt.title(title)
        plt.xlabel("Geração")
        plt.ylabel("Fitness")
        plt.grid(True)
        plt.legend()
        filepath = os.path.join(self.save_dir, save_as)
        plt.savefig(filepath)
        plt.close()
        print(f"✅ Comparação guardada em: {filepath}")

    def print_team_summary(self, individual):
        print("\nResumo do melhor indivíduo:")
        print(f"Fitness: {individual.fitness():.2f}\n")
        for i, team in enumerate(individual.teams):
            print(f"Equipa {i+1} - Média: {team.average_skill():.2f} | Custo total: €{team.total_cost():.2f}")
            for p in team.players:
                print(f"  {p.name} ({p.position}) - Skill: {p.skill}, Custo: {p.cost}")
            print("")

