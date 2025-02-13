import tkinter as tk
import subprocess

class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler")
        self.code = ""

        self.root.configure(bg="light gray")

        # Text Editor
        self.text_editor = tk.Text(root, wrap="word", bg="white")
        self.text_editor.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Output Console
        self.output_console = tk.Text(root, height=10, bg="light yellow")
        self.output_console.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Buttons Frame
        buttons_frame = tk.Frame(root, bg="light gray")
        buttons_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Compile Button
        self.compile_button = tk.Button(buttons_frame, text="Compile", bg="light blue", width=10, height=2)
        self.compile_button.grid(row=0, column=0, padx=(5, 10), pady=5)

        # Run Button
        self.run_button = tk.Button(buttons_frame, text="Run", bg="light green", width=10, height=2)
        self.run_button.grid(row=0, column=1, padx=(10, 5), pady=5)

        # Delete Button
        self.delete_button = tk.Button(buttons_frame, text="Delete", command=self.delete_code, bg="salmon", width=10, height=2)
        self.delete_button.grid(row=0, column=2, padx=(5, 10), pady=5)

        # Configure grid to expand with the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    


    def set_compile_command(self, command): 
        self.compile_button.config(command=command)
    def set_run_command(self, command): 
        self.run_button.config(command=command)
    
    def delete_code(self):
        self.output_console.delete("1.0","end")

    def compile_code(self):
        self.code = self.text_editor.get("1.0", "end-1c")

    def run_code(self):
        try:
            result = subprocess.run(['./output'], text=True, capture_output=True)
            self.output_console.insert("end", f"Program output:\n{result.stdout}\n")
        except Exception as e:
            self.output_console.insert("end", f"Error during execution: {e}\n")



