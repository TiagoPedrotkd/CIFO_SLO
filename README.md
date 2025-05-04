# CIFO_SLO
## ⚽ Sports League Optimization using Genetic Algorithms

### 📌 Project Overview

This project aims to optimize team formation in a fantasy football league using **Genetic Algorithms (GAs)**.  
The objective is to assign players to 5 teams in a way that ensures:

- A balanced distribution of skill levels between teams.
- Compliance with constraints:
  - Each team must have exactly **1 Goalkeeper (GK), 2 Defenders (DEF), 2 Midfielders (MID), and 2 Forwards (FWD)**.
  - No team exceeds a **total salary of €750 million**.
  - Each player is assigned to only one team.

The final goal is to **minimize the standard deviation** of average team skill ratings, creating a fair and competitive league.

---

### ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/TiagoPedrotkd/CIFO_SLO.git
   cd sports-league-ga

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Linux/macOS
    venv\Scripts\activate     # on Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the main script:
    ```bash
    python src/main.py


### 📂 Project Structure
CIFO_SLO/
│
├── src/
│   ├── main.py
│   ├── fitness.py
│   ├── selection.py
│   ├── crossover.py
│   ├── mutation.py
│   ├── utils.py
│
├── data/
│   └── players.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── results/
│   ├── stats.csv
│   └── plots/
│
├── report/
│   └── CIFO_Report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore

### 📊 Reproducing Results
To reproduce the results shown in the report:

1. Run the script src/main.py several times to collect statistics.

2. Use the Jupyter notebook in notebooks/analysis.ipynb to analyze and visualize performance (e.g., convergence graphs, final team balance).

3. Results will be saved automatically in the results/ folder.

### 👨‍💻 Authors
    - Tiago Pedro Soares , 20240655