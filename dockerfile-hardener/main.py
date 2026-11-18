import math
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class DockerfileAuditorUi:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root['bg'] = '#999694'
        self.root.title('Dockerfile Hardener')
        self.root.geometry('800x600')
        self.root.wm_attributes('-alpha', 0.9)

        self.selected_file_path = None

        button_frame = tk.Frame(root, bg='#999694')
        button_frame.place(x=30, y=30)  

        for column in range(3):
            button_frame.grid_columnconfigure(column, weight=1, uniform='buttons')

        #select file button
        self.file_button = tk.Button(button_frame, text='Select file', command=self.select_file, width=18, height=2)
        self.file_button.grid(row=0, column=0, padx=35, pady=10)

        #analyze file button
        self.analyze_button = tk.Button(button_frame, text='Analyze file', command=lambda: self.analyze_file(self.selected_file_path), width=18, height=2)
        self.analyze_button.grid(row=0, column=1, padx=35, pady=10)

        #harden file button
        self.harden_button = tk.Button(button_frame, text='Harden file', command=lambda: self.harden_file(self.selected_file_path), width=18, height=2)
        self.harden_button.grid(row=0, column=2, padx=35, pady=10)

        self.file_text = tk.Label(button_frame, text='Select file:', bg='#999694', fg='#1C1F1D', font=('Arial', 20))
        self.file_text.grid(row=1, column=1, padx=35, pady=(10, 2))

        self.file_label = tk.Label(button_frame, text='No file selected', bg='#999694', fg='#1C1F1D', font=('Arial', 20), anchor='center', justify='center', relief='sunken', width=30)
        self.file_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(2, 10))

        self.log_box = tk.Text(button_frame, width=72, height=18, state='disabled', bg='#2D2D2D')
        self.log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.log_box.tag_configure('system', foreground='green')
        self.log_box.tag_configure('high', foreground='red')
        self.log_box.tag_configure('medium', foreground='orange')
        self.log_box.tag_configure('low', foreground='yellow')

    def calculate_entropy(self, text: str) -> float:
        '''calculates entropy of text'''
        if not text:
            return 0.0
        entropy = 0.0
        frequencies = {char: text.count(char) / len(text) for char in set(text)}
        for frequency in frequencies.values():
            entropy -= frequency * math.log2(frequency)
        return entropy

    def select_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        
        file = Path(path)

        self.log_box.config(state='normal')
        self.log_box.delete('1.0', tk.END)
        self.log_box.config(state='disabled')

        if file.name.startswith('Dockerfile') or file.suffix.lower() == '.dockerfile':
            self.file_label.config(text=Path(path).name)
            self.selected_file_path = str(file)
        else:
            self.file_label.config(text='Please select a Dockerfile')
            self.selected_file_path = None

    def analyze_file(self, path):
        if path is None:
            return

        self.log_box.config(state='normal')

        with open(path, 'r', encoding='utf-8') as file:
            self.log_box.delete('1.0', tk.END)
            self.log_box.insert(tk.END, 'Analysis started:\n', 'system')
            user_switched = False
            severity = 0

            for number, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                line_entropy = self.calculate_entropy(line)
                if 'USER ' in line and 'USER root' not in line:
                    user_switched = True

                if line_entropy > 4.5 and not '@sha256:' in line:
                    self.log_box.insert(tk.END, f'[HIGH] Hardcoded secrets possible in line {number}\n', 'high')
                    severity += 1
                if ':latest' in line:
                    self.log_box.insert(tk.END, f'[MEDIUM] ":latest" version usage in line {number}\n', 'medium')
                    severity += 1
                if 'ADD ' in line:
                   self.log_box.insert(tk.END, f'[MEDIUM] "ADD" usage instead of "COPY" in line {number}\n', 'medium')
                   severity += 1
                if 'RUN'  in line and 'pip install' in line and '--no-cache-dir' not in line:
                    self.log_box.insert(tk.END, f'[LOW] No pip cache disabled with "--no-cache-dir" in line {number}\n', 'low')
                    severity += 1
                if 'RUN ' in line and 'apt-get install' in line and '--no-install-recommends' not in line:
                    self.log_box.insert(tk.END, f'[LOW] Package installation without "--no-install-recommends" in line {number}\n', 'low')
                    severity += 1
                if 'EXPOSE ' in line and any(port in line.split() for port in ('22', '23')):
                    self.log_box.insert(tk.END, f'[HIGH] Exposing administrative ports in line {number}\n', 'high') 
                    severity += 1 

            if user_switched == False:
                self.log_box.insert(tk.END, f'[HIGH] USER instruction missed. Container runs as root by default.\n', 'high') 
                severity += 1

            self.log_box.insert(tk.END, f'[SEVERITY] {severity} points\n', 'system')

        self.log_box.config(state='disabled')  

    def harden_file(self, path):
        if path is None:
            return

        source_path = Path(path)
        output_path = source_path.with_name(f'{source_path.name}.hardened')

        self.log_box.config(state='normal')

        with open(source_path, 'r', encoding='utf-8') as infile, \
            open(output_path, 'w', encoding='utf-8') as outfile:

            self.log_box.delete('1.0', tk.END)
            self.log_box.insert(tk.END, 'Hardening started:\n', 'system')

            user_switched = False
            user_block = (
                'RUN useradd -u 1001 appuser\n'
                'USER appuser\n\n'
            )

            for line in infile:
                fixed_line = line

                if fixed_line.lstrip().startswith('USER ') and 'USER root' not in fixed_line:
                    user_switched = True

                if fixed_line.lstrip().startswith('ADD '):
                    fixed_line = fixed_line.replace('ADD', 'COPY', 1)

                if 'pip install' in fixed_line and '--no-cache-dir' not in fixed_line:
                    fixed_line = fixed_line.replace('pip install', 'pip install --no-cache-dir')

                if 'apt-get install' in fixed_line and '--no-install-recommends' not in fixed_line:
                    fixed_line = fixed_line.replace('apt-get install', 'apt-get install --no-install-recommends')

                if fixed_line.lstrip().startswith('EXPOSE '):
                    parts = [part for part in fixed_line.split() if part not in ('22', '23')]

                    if len(parts) > 1:
                        fixed_line = ' '.join(parts) + '\n'
                    else:
                        continue
                
                if not user_switched and fixed_line.lstrip().startswith(('CMD', 'ENTRYPOINT')):
                    outfile.write(user_block)
                    user_switched = True

                stripped = fixed_line.lstrip()

                if stripped and not stripped.startswith('#'):
                    entropy = self.calculate_entropy(stripped)

                    if entropy > 4.5 and '@sha256' not in stripped:
                        outfile.write('# [SECURITY WARNING] Possible hardcoded secret detected below. Injact at runtime instead:\n')

                outfile.write(fixed_line)
            
            if not user_switched:
                outfile.write(user_block)

            self.log_box.insert(tk.END, 'Hardening finished\n', 'system')

        self.log_box.config(state='disabled')  
                    

if __name__ == '__main__':
    root = tk.Tk()
    root.wait_visibility()
    app = DockerfileAuditorUi(root)
    root.mainloop()