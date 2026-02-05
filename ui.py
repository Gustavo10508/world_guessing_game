import tkinter as tk
from tkinter import ttk, messagebox
from game import Game
from database import BancoDados

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("World Guessing Game")
        self.root.geometry("420x420")

        self.db = BancoDados()
        self.game = Game()
        self.jogador = ""

        self._login()

    def _login(self):
        self._clear()

        tk.Label(
            self.root,
            text="World Guessing Game",
            font=("Arial", 18, "bold")
        ).pack(pady=30)

        self.nome = tk.Entry(self.root, font=("Arial", 14))
        self.nome.pack(pady=10)

        tk.Button(
            self.root,
            text="Iniciar",
            command=self._start
        ).pack(pady=20)

    def _start(self):
        self.jogador = self.nome.get().strip()
        if not self.jogador:
            return

        self._game()

    def _game(self):
        self._clear()

        self.info = tk.Label(self.root, font=("Arial", 12))
        self.info.pack(pady=10)

        self.dica = tk.Label(self.root, font=("Arial", 16))
        self.dica.pack(pady=20)

        self.entrada = tk.Entry(self.root, font=("Arial", 14))
        self.entrada.pack()

        tk.Button(
            self.root,
            text="Chutar",
            command=self._check
        ).pack(pady=10)

        self._round()

    def _round(self):
        pais = self.game.nova_rodada()

        capital = pais.get("capital", ["Sem capital"])[0]

        # DICA EM PORTUGUÊS
        self.info.config(
            text=f"{self.jogador} | Pontos: {self.game.pontos}"
        )
        self.dica.config(
            text=f"Capital: {capital}"
        )

        self.entrada.delete(0, tk.END)

    def _check(self):
        certo, pontos = self.game.verificar(self.entrada.get())

        if certo:
            self.db.salvar(self.jogador, self.game.pontos)
            messagebox.showinfo(
                "Acertou",
                f"+{pontos} pontos"
            )
            self._ranking()
        else:
            messagebox.showerror(
                "Errou",
                "Resposta incorreta"
            )
            self._round()

    def _ranking(self):
        self._clear()

        tree = ttk.Treeview(
            self.root,
            columns=("j", "p", "d"),
            show="headings"
        )
        tree.heading("j", text="Jogador")
        tree.heading("p", text="Pontuação")
        tree.heading("d", text="Data")

        tree.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

        for j, p, d in self.db.top5():
            tree.insert("", "end", values=(j, p, d))

        tk.Button(
            self.root,
            text="Voltar",
            command=self._login
        ).pack(pady=10)

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()
