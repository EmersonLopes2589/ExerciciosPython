import tkinter as tk
from tkinter import filedialog, messagebox


# JANELA PRINCIPAL E ÁREA DE TEXTO
class EditorNotas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de Notas")
        self.geometry("600x400")

        self.area_texto = tk.Text(self)
        self.area_texto.pack(expand=True, fill=tk.BOTH)

        self.criar_menu()

    # MENU DE ARQUIVO (ABRIR, SALVAR, SAIR)
    def criar_menu(self):
        menubar = tk.Menu(self)
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menu_arquivo.add_command(label="Abrir", command=self.abrir_arquivo)
        menu_arquivo.add_command(label="Salvar", command=self.salvar_arquivo)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        self.config(menu=menubar)

    # ABRIR ARQUIVO DE TEXTO
    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos", "*.*")])
        if not caminho:
            return
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
            self.area_texto.delete("1.0", tk.END)
            self.area_texto.insert(tk.END, conteudo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir: {e}")

    # SALVAR ARQUIVO DE TEXTO
    def salvar_arquivo(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt")
        if not caminho:
            return
        try:
            conteudo = self.area_texto.get("1.0", tk.END)
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")


if __name__ == "__main__":
    app = EditorNotas()
    app.mainloop()