# Math Trainer: Multiplication Table

A simple, interactive terminal-based script to learn and practice the multiplication table from 1 to 10. The application features a colored Command Line Interface (CLI) to make the learning experience engaging.

## Features

- **Interactive Training Mode:** Generates random math tasks and provides instant feedback (correct/incorrect). Type `0` at any time to exit the training session.
- **Visual Multiplication Table:** Prints a beautifully formatted table with a highlighted diagonal (perfect squares) for better visualization.
- **Colorized Interface:** Uses terminal text coloring to differentiate menus, success statuses, and errors.
- **Input Validation:** Prevents crashes by checking if the user mistakenly inputs letters instead of numbers.

## Requirements

Before running the project, make sure you have **Python 3.x** installed. 

This project requires the `colorama` library for colored console output.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```bash
   pip install colorama
   ```

## How to Run

Execute the script using the following command in your terminal:

```bash
python multiplication_table.py
```

## Usage

When you run the script, a main menu will appear with three options:
1. **Test your knowledge:** Enters the random practice loop.
2. **View the multiplication table:** Displays the full 1-10 grid.
3. **Exit the program:** Safely closes the trainer.