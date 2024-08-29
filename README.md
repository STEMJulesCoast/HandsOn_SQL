# SQL GUI und JSON-Datenbank

Dieses Repository enthält zwei Python-Projekte, die demonstrieren, wie man mit SQL-Datenbanken in Python arbeitet:

1. **example_json_sql.ipynb**: Ein Jupyter Notebook, das zeigt, wie man JSON-Daten in Python verarbeitet und in eine SQLite-Datenbank importiert.
12. **example_sql_gui.py**: Ein Skript, das eine grafische Benutzeroberfläche (GUI) zur Erstellung und Abfrage von SQL-Datenbanken bereitstellt.


## Inhalt

- `example_json_sql.ipynb`: Jupyter Notebook zum Arbeiten mit JSON-Daten und einer SQLite-Datenbank.
- `example_sql_gui.py`: Python-Skript zur Erstellung einer SQL GUI.
- `requirements.txt`: Liste der erforderlichen Python-Bibliotheken.

## Voraussetzungen

Dieses Projekt wurde mit Python 3.12.2 entwickelt. Zum Arbeiten mit Notebooks kann in VS Code die Jupyter-Extension installiert werden oder Anaconda genutzt werden, das Jupyter Notebook bereits vorinstalliert enthält. Beide Optionen ermöglichen eine einfache und bequeme Nutzung der Jupyter Notebooks.

## Installation

1. Klone das Repository:
    ```bash
    git clone https://github.com/STEMJulesCoast/HandsOn_SQL
    cd HandsOn_SQL
    ```

2. Erstelle eine virtuelle Umgebung und installiere die Abhängigkeiten:
    ```bash
    python -m venv env
    source env/bin/activate  # Auf Windows: env\Scripts\activate
    pip install -r requirements.txt
    ```

## Verwendung

### 1. **SQL GUI ausführen**

Starte die GUI durch Ausführen des folgenden Befehls im Terminal:

```bash
python example_sql_gui.py