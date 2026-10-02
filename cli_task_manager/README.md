### CLI Task Manager

A robust and lightweight Command Line Interface (CLI) application for task management built with Python. This project was designed using Object-Oriented Programming (OOP) principles and leverages native Python modules to deliver a completely standalone, zero-dependency tool with built-in terminal color-coding.

### 🚀 Key Features

* **Object-Oriented Architecture:** Clear separation of concerns with isolated Task and TaskManager models, making the core logic completely independent of the user interface.
* **Smart CLI Parser:** Utilizes Python's native `argparse` with structured subparsers to handle user commands smoothly.
* **Priority & Color Coding:** Features intuitive `[HIGH]`, `[MED]`, and `[LOW]` text tags mapped to ANSI color escape codes (Red, Yellow, Green) for immediate visual urgency. Completed tasks automatically fade out in Gray.
* **Persistent Storage:** Automatically preserves your task list between terminal sessions by serializing data into a local `tasks.json` file.
* **Advanced Filtering:** View all tasks, only completed tasks, or active tasks using optimized filtering flags.

### 🛠️ Tech Stack & Concepts Applied

* **Language:** Python 3.x
* **Core Modules:** `argparse`, `json`, `pathlib`
* **OOP Concepts:** Encapsulation, static methods, object lifecycle management.
* **Design Patterns:** Guard Clauses (clean conditional flows via early exits), interface/logic decoupling.

### 📦 Installation & Setup

1. **Clone the repository and navigate to the project folder:**
   ```bash
   git clone https://github.com/Trid147/python-portfolio.git
   cd python-portfolio/cli_task_manager
   ```

2. **Run the script:**
   No external dependencies, `colorama`, or virtual environments are required. You can start managing tasks right away using your native Python interpreter.

### 📖 Usage Examples

Here is how you can interact with the Task Manager from your terminal:

* **Add a new task (Default priority is MED):**
   ```bash
   python task_manager.py add "Finish my Python OOP project"
   ```

* **Add a task with a specific priority (1 = HIGH, 2 = MED, 3 = LOW):**
   ```bash
   python task_manager.py add "Fix README formatting bugs" -p 1
   ```

* **List active tasks (Default view):**
   ```bash
   python task_manager.py list
   ```

* **List all tasks (Including completed ones):**
   ```bash
   python task_manager.py list --all
   # Or using the shorthand:
   python task_manager.py list -a
   ```

* **List only completed tasks:**
   ```bash
   python task_manager.py list --completed
   # Or using the shorthand:
   python task_manager.py list -c
   ```

* **Mark a task as completed:**
   ```bash
   python task_manager.py done 1
   ```

* **Remove a task from the list:**
   ```bash
   python task_manager.py remove 1
   ```

### 🗄️ Data Structure

Tasks are stored locally in a beautifully formatted JSON file (`tasks.json`):

```json
[
    {
        "id": 1,
        "title": "Fix README formatting bugs",
        "status": false,
        "priority": 1
    }
]
```