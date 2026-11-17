import tkinter as tk
from tkinter import filedialog
from tkinter import font
from pathlib import Path

class DockerfileAuditorUi:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root['bg'] = '#228253'
        self.root.title('Dockerfile Hardener')
        self.root.geometry('800x600')
        self.root.wm_attributes('-alpha', 0.7)

        button_frame = tk.Frame(root, bg='#228253')
        button_frame.place(x=30, y=30)  

        for column in range(3):
            button_frame.grid_columnconfigure(column, weight=1, uniform='buttons')

        self.file_button = tk.Button(button_frame, text='Select file', command=self.select_file, width=18, height=2)
        self.file_button.grid(row=0, column=0, padx=35, pady=10)

        self.analyze_button = tk.Button(button_frame, text='Analyze file', command=self.select_file, width=18, height=2)
        self.analyze_button.grid(row=0, column=1, padx=35, pady=10)

        self.harden_button = tk.Button(button_frame, text='Harden file', command=self.select_file, width=18, height=2)
        self.harden_button.grid(row=0, column=2, padx=35, pady=10)

        self.file_text = tk.Label(button_frame, text='Select file:', bg='#228253', fg='#1C1F1D', font=('Arial', 20))
        self.file_text.grid(row=1, column=1, padx=35, pady=(10, 2))

        self.file_label = tk.Label(button_frame, text='No file selected', bg='#228253', fg='#1C1F1D', font=('Arial', 20), anchor='center', justify='center', relief='sunken', width=30)
        self.file_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(2, 10))

        self.log_box = tk.Text(button_frame, width=64, height=16, state='disabled')
        self.log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def select_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        
        file = Path(path)

        if file.suffix.lower() == '.dockerfile' or file.name == 'Dockerfile':
            self.file_label.config(text=Path(path).name)
            self.selected_file_path = str(file)
        else:
            self.file_label.config(text='Please select a Dockefile')

if __name__ == '__main__':
    root = tk.Tk()
    root.wait_visibility()
    app = DockerfileAuditorUi(root)
    root.mainloop()