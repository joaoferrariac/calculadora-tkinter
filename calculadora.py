import tkinter as tk
from tkinter import messagebox
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.historico = []
        
        self.criar_interface()
        self.vincular_teclado()
    
    def criar_interface(self):
        # Frame principal
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Entry para exibir a expressão
        self.entry = tk.Entry(
            frame, font=("Arial", 18), 
            borderwidth=2, relief="groove", 
            justify="right"
        )
        self.entry.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")
        
        # Widget para o histórico
        self.historico_text = tk.Text(
            frame, height=5, font=("Arial", 10),
            state="disabled", bg="#fafafa"
        )
        self.historico_text.grid(row=1, column=0, columnspan=5, pady=5, sticky="nsew")
        
        # Botões
        botoes = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3), ("C", 2, 4),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3), ("√", 3, 4),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3), ("x²", 4, 4),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2), ("+", 5, 3), ("^", 5, 4),
        ]
        
        for (texto, linha, coluna) in botoes:
            botao = tk.Button(
                frame, text=texto, font=("Arial", 14), 
                command=lambda t=texto: self.clique_botao(t),
                padx=15, pady=15, bg="#e0e0e0"
            )
            botao.grid(row=linha, column=coluna, sticky="nsew", padx=2, pady=2)
        
        # Ajustar tamanho das linhas/colunas
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)
    
    def vincular_teclado(self):
        self.root.bind("<Key>", self.tecla_pressionada)
    
    def tecla_pressionada(self, event):
        tecla = event.char
        if tecla in "0123456789+-*/.=":
            self.clique_botao(tecla)
        elif event.keysym == "Return":
            self.clique_botao("=")
        elif event.keysym == "Escape":
            self.clique_botao("C")
    
    def atualizar_historico(self, expressao, resultado):
        self.historico.append(f"{expressao} = {resultado}")
        self.historico_text.config(state="normal")
        self.historico_text.insert(tk.END, self.historico[-1] + "\n")
        self.historico_text.config(state="disabled")
        self.historico_text.see(tk.END)
    
    def clique_botao(self, valor):
        if valor == "C":
            self.entry.delete(0, tk.END)
        elif valor == "=":
            try:
                expressao = self.entry.get()
                resultado = eval(expressao.replace("^", "**"))
                self.atualizar_historico(expressao, resultado)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(resultado))
            except Exception as e:
                messagebox.showerror("Erro", f"Expressão inválida! {e}")
        elif valor == "√":
            try:
                num = float(self.entry.get())
                resultado = math.sqrt(num)
                self.atualizar_historico(f"√({num})", resultado)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(resultado))
            except ValueError:
                messagebox.showerror("Erro", "Número inválido para raiz!")
        elif valor == "x²":
            try:
                num = float(self.entry.get())
                resultado = num ** 2
                self.atualizar_historico(f"({num})²", resultado)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(resultado))
            except ValueError:
                messagebox.showerror("Erro", "Número inválido!")
        else:
            self.entry.insert(tk.END, valor)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()