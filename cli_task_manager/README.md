### CLI Task Manager

A robust and lightweight Command Line Interface (CLI) application for task management built with Python. This project was designed using Object-Oriented Programming (OOP) principles and leverages native Python modules to deliver a completely standalone, zero-dependency tool. 

### 🚀 Key Features

* **Object-Oriented Architecture:** Clear separation of concerns with isolated Task and TaskManager models, making the core logic completely independent of the user interface.
* **Smart CLI Parser:** Utilizes Python's native argparse with structured subparsers to handle user commands smoothly.
* **Persistent Storage:** Automatically preserves your task list between terminal sessions by serializing data into a local tasks.json file.
* **Advanced Filtering:** View all tasks, only completed tasks, or active tasks using optimized filtering flags.

### 🛠️ Tech Stack & Concepts Applied

* **Language:** Python 3.x
* **Core Modules:** argparse, json, pathlib
* **OOP Concepts:** Encapsulation, static methods, object lifecycle management.
* **Design Patterns:** Guard Clauses (clean conditional flows via early exits), interface/logic decoupling.

### 📦 Installation & Setup

1. **Clone the repository:** 

bash

git clone https://github.com/Trid147/python-portfolio.git
cd python-portfolio

Use code with caution.
2. **Run the script:**
No external dependencies or virtual environments are required. You can start managing tasks right away using your native Python interpreter.

### 📖 Usage Examples

Here is how you can interact with the Task Manager from your terminal: 

* **Add a new task:** 

bash

python main.py add "Finish my Python OOP project"

Use code with caution.
* **List active tasks (Default):** 

bash

python main.py list

Use code with caution.
* **List all tasks (Including completed ones):** 

bash

python main.py list --all
# Or using the shorthand: python main.py list -a

Use code with caution.
* **List only completed tasks:** 

bash

python main.py list --completed
# Or using the shorthand: python main.py list -c

Use code with caution.
* **Mark a task as completed:** 

bash

python main.py done <task_id>
# Example: python main.py done 1

Use code with caution.
* **Remove a task from the list:** 

bash

python main.py remove <task_id>
# Example: python main.py remove 1

Use code with caution.

### 🗄️ Data Structure

Tasks are stored locally in a beautifully formatted JSON file (tasks.json): 

json

[
    {
        "id": 1,
        "title": "Finish my Python OOP project",
        "status": true
    }
]

Use code with caution.