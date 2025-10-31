import customtkinter as ctk
import os
import math
import threading
import pygame

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x800")
        if os.path.exists("calculator.ico"):
            self.iconbitmap('calculator.ico')
        else:
            self.iconbitmap("Calculator/calculator.ico")
        self.resizable(False, False)
        self.title("Scientific Calculator")
        
        # Pygame mixer başlat ve ses yükle
        pygame.mixer.init()
        try:
            self.click_sound = pygame.mixer.Sound("click.wav")
        except:
            self.click_sound = None
        
        self.is_dark_mode = True
        ctk.set_appearance_mode("dark")
        
        self.bg_color = "#121212"
        self.button_color = "#1e1e1e"
        self.accent_color = "#4fd1c5"
        self.science_color = "#FF6B6B"
        
        self.configure(fg_color=self.bg_color)
        self.current_expression = "0"
        self.create_widgets()
        self.current_font_size = 64

    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

    def create_widgets(self):
        # Top frame with theme button
        top_frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        top_frame.pack(fill="x", padx=0, pady=0)
        
        theme_btn = ctk.CTkButton(top_frame, text="🌙", width=40, height=40,
                                  fg_color=self.accent_color, text_color="black",
                                  font=("Arial", 20), corner_radius=8,
                                  command=lambda: [self.play_click(), self.toggle_theme()])
        theme_btn.pack(side="right", padx=20, pady=15)
        
        # Display frame
        display_frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        display_frame.pack(fill="x", padx=0, pady=0)

        # Equal sign
        equal_sign = ctk.CTkLabel(display_frame, text="=", font=("Arial", 45), 
                                  text_color=self.accent_color, bg_color=self.bg_color)
        equal_sign.pack(side="left", padx=(20, 10), pady=15)

        # Result display
        self.result = ctk.CTkEntry(display_frame, font=("Arial", 64), 
                                   fg_color=self.bg_color, text_color="white", 
                                   border_width=0, justify="right")
        self.result.pack(fill="x", expand=True, padx=(0, 20), pady=15)
        self.result.insert(0, "0")
        self.result.configure(state="normal")  # Düzenlenebilir yap
        self.result.bind("<Return>", lambda e: self.calculate())  # Enter tuşu
        self.result.bind("<BackSpace>", lambda e: self.backspace())  # Backspace tuşu

        # Operation display
        self.operation = ctk.CTkLabel(self, text="", font=("Arial", 24), 
                                      fg_color=self.bg_color, text_color=self.accent_color, 
                                      anchor="e")
        self.operation.pack(pady=(0, 20), padx=20, fill="x")

        # Scientific button frame
        self.science_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.science_frame.pack(fill="x", padx=20, pady=(0, 10))

        science_buttons = ['√', 'x²', 'π', 'sin', 'cos', 'tan', 'log', 'ln']
        self.science_btns = []
        
        for button in science_buttons:
            btn = ctk.CTkButton(self.science_frame, text=button, width=45, height=45,
                                fg_color=self.science_color, text_color="white",
                                font=("Arial", 16), corner_radius=8,
                                hover_color=self.lighten_color(self.science_color, 0.1),
                                command=lambda x=button: self.science_click(x))
            btn.pack(side="left", padx=3, expand=True, fill="x")
            self.science_btns.append(btn)

        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.button_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        buttons = [
            'CE', '+/-', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=', 'DEL'  # DEL tuşu ekle
        ]

        self.button_dict = {}
        row, col = 0, 0
        for button in buttons:
            if button in ['CE', '+/-', '%', '/', '*', '-', '+', '=']:
                color = self.accent_color
                text_color = "black"
                hover_color = self.lighten_color(self.accent_color, 0.1)
            else:
                color = self.button_color
                text_color = "white"
                hover_color = self.lighten_color(self.button_color, 0.1)
            
            btn = ctk.CTkButton(self.button_frame, text=button, width=60, height=60, 
                                fg_color=color, text_color=text_color, 
                                font=("Arial", 24), corner_radius=10,
                                hover_color=hover_color,
                                command=lambda x=button: self.button_click(x))
            
            self.button_dict[button] = (btn, color, text_color, hover_color)
            
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=5, pady=5, sticky="nsew")
                col += 2
            else:
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                col += 1
            
            if col > 3:
                col = 0
                row += 1

        # Configure grid
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.bg_color = "#121212"
            self.button_color = "#1e1e1e"
            self.accent_color = "#4fd1c5"
            self.science_color = "#FF6B6B"
            text_color = "white"
            result_text = "white"
        else:
            ctk.set_appearance_mode("light")
            self.bg_color = "#ffffff"
            self.button_color = "#e8e8e8"
            self.accent_color = "#00a8a8"
            self.science_color = "#FF6B6B"
            text_color = "black"
            result_text = "black"
        
        self.configure(fg_color=self.bg_color)
        
        # Update top frames
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.bg_color)
        
        self.button_frame.configure(fg_color=self.bg_color)
        self.science_frame.configure(fg_color=self.bg_color)
        self.operation.configure(fg_color=self.bg_color, text_color=self.accent_color)
        
        self.result.configure(fg_color=self.bg_color, text_color=result_text)
        
        # Update all buttons
        for button, (btn, _, _, _) in self.button_dict.items():
            if button in ['CE', '+/-', '%', '/', '*', '-', '+', '=']:
                color = self.accent_color
                text_col = "black"
            else:
                color = self.button_color
                text_col = text_color
            
            hover_color = self.lighten_color(color, 0.1)
            btn.configure(fg_color=color, text_color=text_col, hover_color=hover_color)
        
        # Update science buttons
        for btn in self.science_btns:
            hover_color = self.lighten_color(self.science_color, 0.1)
            btn.configure(fg_color=self.science_color, hover_color=hover_color)

    def lighten_color(self, color, factor=0.05):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [min(int(c + (255 - c) * factor), 255) for c in rgb]
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def science_click(self, key):
        self.play_click()
        if key == "√":
            self.current_expression = f"sqrt({self.current_expression})"
        elif key == "x²":
            self.current_expression = f"({self.current_expression})**2"
        elif key == "π":
            self.current_expression += str(math.pi)
        elif key == "sin":
            self.current_expression = f"sin(radians({self.current_expression}))"
        elif key == "cos":
            self.current_expression = f"cos(radians({self.current_expression}))"
        elif key == "tan":
            self.current_expression = f"tan(radians({self.current_expression}))"
        elif key == "log":
            self.current_expression = f"log10({self.current_expression})"
        elif key == "ln":
            self.current_expression = f"log({self.current_expression})"
        
        self.update_result()
        self.update_operation()

    def backspace(self):
        self.play_click()
        self.current_expression = self.current_expression[:-1]
        if self.current_expression == "":
            self.current_expression = "0"
        self.update_result()
        self.update_operation()

    def button_click(self, key):
        self.play_click()
        if key == "=":
            self.calculate()
        elif key == "CE":
            self.clear()
        elif key == "+/-":
            self.negate()
        elif key == "%":
            self.percentage()
        elif key == "DEL":
            self.backspace()
        else:
            self.add_to_expression(key)

    def add_to_expression(self, value):
        operators = ['+', '-', '*', '/', '%']
        
        # Eğer son karakter operatör ve yeni giriş de operatör ise engelle
        if self.current_expression and self.current_expression[-1] in operators and value in operators:
            return
        
        if self.current_expression == "0" or self.current_expression == "":
            self.current_expression = str(value)
        else:
            self.current_expression += str(value)
        self.update_result()
        self.update_operation()

    def update_operation(self):
        self.operation.configure(text=self.current_expression)

    def calculate(self):
        try:
            result = eval(self.current_expression, {"__builtins__": {}}, 
                         {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, 
                          "tan": math.tan, "log10": math.log10, "log": math.log, 
                          "radians": math.radians, "pi": math.pi})
            self.current_expression = str(result)
        except:
            self.current_expression = "Error"
        self.update_result()
        self.update_operation()

    def clear(self):
        self.current_expression = "0"
        self.update_result()
        self.update_operation()

    def negate(self):
        try:
            value = float(self.result.get())
            self.current_expression = str(-value)
        except ValueError:
            pass
        self.update_result()
        self.update_operation()

    def percentage(self):
        if self.current_expression == "0" or self.current_expression == "":
            pass
        else:
            self.current_expression += "%"
        self.update_result()
        self.update_operation()

    def update_result(self):
        self.result.configure(state="normal")
        self.result.delete(0, ctk.END)
        self.result.insert(0, self.current_expression)
        
        text_length = len(self.current_expression)
        if text_length > 7:
            new_font_size = 40
        else:
            new_font_size = 64
        
        self.result.configure(font=("Arial", new_font_size))
        self.result.configure(state="normal")  # Düzenlenebilir kalsın

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
