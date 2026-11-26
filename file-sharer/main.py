#!/usr/bin/env python3
import os
import socket
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

HOST = '0.0.0.0'
PORT = 50001

class FileSharerUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('File Sharer')
        self.root.geometry('600x600')
        self.root.wm_attributes('-alpha', 0.95)
        self.root.resizable(False, False)

        self.bg = '#1E293B'
        self.fg = '#F8FAFC'
        self.button_style = {'bg': '#2563EB', 'fg': '#F8FAFC', 'activebackground': '#3B82F6', 'activeforeground': '#F8FAFC',
        'font': ('Arial', 14, 'bold'), 'bd': 0, 'highlightthickness': 0, 'cursor': 'hand2'}

        self.main_frame = tk.Frame(root, bg=self.bg)
        self.main_frame.pack(fill='both', expand=True)

        self.show_main_menu()

    def clear_screen(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self) -> None:
        self.clear_screen()
        self.receiving = False

        main_label = tk.Label(self.main_frame, text='Choose what to do:', bg=self.bg, fg=self.fg, font=('Arial', 25, 'bold'))
        main_label.pack(pady=(50, 150))

        button_frame = tk.Frame(self.main_frame, bg=self.bg)
        button_frame.pack(fill='x', padx=100)

        send_button = tk.Button(button_frame, text='Send', width=10, pady=50, command=self.show_send_screen, **self.button_style)
        send_button.pack(side='left')

        receive_button = tk.Button(button_frame, text='Receive', width=10, pady=50, command=self.show_receive_screen, **self.button_style)
        receive_button.pack(side='right')

    def show_send_screen(self) -> None:
        self.clear_screen()

        self.send_label = tk.Label(self.main_frame, text='Select a file and write receiver IP', bg=self.bg, fg='#F8FAFC', font=('Arial', 20, 'bold'))
        self.send_label.pack(pady=(50, 50))

        file_frame = tk.Frame(self.main_frame, bg=self.bg)
        file_frame.pack(fill='x', padx=50, pady=(0, 15))

        self.path_label = tk.Label(file_frame, text='File: ', bg=self.bg, fg=self.fg, font=('Arial', 16))
        self.path_label.pack(side='left')

        browse_button = tk.Button(file_frame, text='Browse', padx=12, pady=2, command=self.select_file, **self.button_style)
        browse_button.pack(side='right')

        ip_frame = tk.Frame(self.main_frame, bg=self.bg)
        ip_frame.pack(fill='x', padx=50, pady=(0, 40))

        ip_label = tk.Label(ip_frame, text='Recipient IP: ', bg=self.bg, fg=self.fg, font=('Arial', 16))
        ip_label.pack(side='left')

        self.ip_entry = tk.Entry(ip_frame, bg='#0F172A', fg=self.fg, insertbackground=self.fg, font=('Arial', 16), bd=0, highlightthickness=1, highlightbackground='#334155', highlightcolor='#2563EB')
        self.ip_entry.pack(side='left', fill='x', expand=True, ipady=4)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Blue.Horizontal.TProgressbar', troughcolor='#0F172A', background='#2563EB', bordercolor='#0F172A', lightcolor='#2563EB', darkcolor='#2563EB')

        self.send_progress = ttk.Progressbar(self.main_frame, style='Blue.Horizontal.TProgressbar', mode='determinate', maximum=100, value=0)
        self.send_progress.pack(fill='x', padx=50, pady=(0, 20))

        start_button = tk.Button(self.main_frame, text='Send file', width=15, pady=12, command=lambda: threading.Thread(target=self.start_sending, daemon=True).start(), **self.button_style)
        start_button.pack(pady=20)

        back_button = tk.Button(self.main_frame, text='← Back', font=('Arial', 10, 'bold'), padx=10, pady=4, command=self.show_main_menu, **{k: v for k, v in self.button_style.items() if k != 'font'})
        back_button.place(x=15, y=15)

    def select_file(self) -> None:
        path = filedialog.askopenfilename()
        if path:
            self.file_path = path
            self.file_name = os.path.basename(path)
            self.file_size = os.path.getsize(path)
            self.path_label.config(text=f'File: {self.file_name}')

    def start_sending(self) -> None:
        if not hasattr(self, 'file_path'):
            self.root.after(0, lambda: self.send_label.configure(text='Select a file first!'))
            return

        recepient_ip = self.ip_entry.get().strip()

        if recepient_ip and len(recepient_ip) <= 16:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                try:
                    client.connect((recepient_ip,PORT))
                    self.root.after(0, lambda: self.send_label.configure(text=f'Sending started...'))
                    client.sendall((f'{self.file_name}|{self.file_size}\n').encode('utf-8'))

                    sent_bytes = 0
                    with open(self.file_path, 'rb') as file:
                        while chunk := file.read(4096):
                            client.sendall(chunk)
                            sent_bytes += len(chunk)
                            percent = (sent_bytes / self.file_size) * 100
                            self.root.after(0, lambda p=percent: self.send_progress.configure(value=p))
                        
                    self.root.after(0, lambda: self.send_label.configure(text='File sent!'))
                except Exception:
                    self.root.after(0, lambda: self.send_label.configure(text=f'Could not connect to {recepient_ip}'))

    def show_receive_screen(self) -> None:
        self.clear_screen()

        self.receive_label = tk.Label(self.main_frame, text='Waiting for connection...', bg=self.bg, fg='#F8FAFC', font=('Arial', 20, 'bold'))
        self.receive_label.pack(pady=(50, 50))

        self.file_label = tk.Label(self.main_frame, text='File: ', bg=self.bg, fg=self.fg, font=('Arial', 16))
        self.file_label.pack(anchor='w', padx=50)

        self.connection_label = tk.Label(self.main_frame, text='Sender IP: ', bg=self.bg, fg=self.fg, font=('Arial', 16))
        self.connection_label.pack(anchor='w', padx=50)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Blue.Horizontal.TProgressbar', troughcolor='#0F172A', background='#2563EB', bordercolor='#0F172A', lightcolor='#2563EB', darkcolor='#2563EB')

        self.receive_progress = ttk.Progressbar(self.main_frame, style='Blue.Horizontal.TProgressbar', mode='determinate', maximum=100, value=0)
        self.receive_progress.pack(fill='x', padx=50, pady=(40, 20))

        self.finish_label = tk.Label(self.main_frame, text='', bg=self.bg, fg=self.fg, font=('Arial', 16))
        self.finish_label.pack()

        back_button = tk.Button(self.main_frame, text='← Back', font=('Arial', 10, 'bold'), padx=10, pady=4, command=self.show_main_menu, **{k: v for k, v in self.button_style.items() if k != 'font'})
        back_button.place(x=15, y=15)

        self.receiving = True
        receive_thread = threading.Thread(target=self.start_receiving, daemon=True)
        receive_thread.start()

    def start_receiving(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self.server = server
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST,PORT))
            server.listen(1)
            server.settimeout(0.5)

            while self.receiving:
                try:
                    connection, address = server.accept()
                    break
                except socket.timeout:
                    continue
            else:
                return

            self.root.after(0, lambda: self.connection_label.configure(text=f'Sender IP: {address[0]}'))
            with connection:
                header = b''

                while not header.endswith(b'\n'):
                    byte = connection.recv(1)
                    if not byte:
                        return
                    header += byte

                file_name, file_size_str = header.decode('utf-8').strip().split('|')
                file_size = int(file_size_str)

                self.root.after(0, lambda: self.file_label.configure(text=f'File: {file_name}'))

                received_bytes = 0

                with open(file_name, 'wb') as file:
                    while received_bytes < file_size:
                        chunk = connection.recv(min(4096, file_size - received_bytes))
                        if not chunk:
                            break
                        file.write(chunk)
                        received_bytes += len(chunk)

                        percent = (received_bytes / file_size) * 100
                        self.root.after(0, lambda p=percent: self.receive_progress.configure(value=p))

                self.root.after(0, lambda: self.receive_label.configure(text='Done!'))
                self.root.after(0, lambda: self.finish_label.configure(text=f'Saved as {file_name}'))

if __name__ == '__main__':
    root = tk.Tk()
    root.wait_visibility()
    app = FileSharerUI(root)
    root.mainloop()