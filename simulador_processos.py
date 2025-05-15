import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque

# Classe que representa um processo
class Processo:
    def __init__(self, pid, chegada, duracao, tipo):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.restante = duracao
        self.tipo = tipo
        self.estado = 'PRONTO'
        self.tempo_espera = 0
        self.inicio = None
        self.fim = None

# Simulação do algoritmo FIFO
def simular_fifo(processos):
    tempo = 0
    fila = sorted(processos, key=lambda p: p.chegada)
    gantt = []

    while fila:
        proc = fila.pop(0)
        tempo = max(tempo, proc.chegada)
        proc.inicio = tempo
        gantt.append((proc.pid, tempo, tempo + proc.duracao))
        tempo += proc.duracao
        proc.restante = 0
        proc.fim = tempo
        proc.tempo_espera = proc.inicio - proc.chegada

    return processos, gantt

# Simulação do algoritmo Round Robin
def simular_round_robin(processos, quantum):
    tempo = 0
    fila_espera = deque(sorted(processos, key=lambda p: p.chegada))
    fila_execucao = deque()
    gantt = []

    while fila_espera or fila_execucao:
        while fila_espera and fila_espera[0].chegada <= tempo:
            fila_execucao.append(fila_espera.popleft())

        if fila_execucao:
            proc = fila_execucao.popleft()

            if proc.inicio is None:
                proc.inicio = tempo

            tempo_execucao = min(quantum, proc.restante)
            gantt.append((proc.pid, tempo, tempo + tempo_execucao))
            tempo += tempo_execucao
            proc.restante -= tempo_execucao

            while fila_espera and fila_espera[0].chegada <= tempo:
                fila_execucao.append(fila_espera.popleft())

            if proc.restante > 0:
                fila_execucao.append(proc)
            else:
                proc.fim = tempo

            for p in fila_execucao:
                p.tempo_espera += tempo_execucao
        else:
            tempo += 1

    return processos, gantt

# Exibição do gráfico de Gantt
def exibir_grafico_gantt(gantt, titulo):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 4))
    cores_modernas = ['#007ACC', '#00BFA5', '#F9A825', '#D32F2F', '#7B1FA2', '#0288D1', '#C2185B', '#388E3C', '#FFA000', '#303F9F']
    legendas = []

    for pid, inicio, fim in gantt:
        cor = cores_modernas[(pid - 1) % len(cores_modernas)]
        ax.broken_barh([(inicio, fim - inicio)], (10, 9), facecolors=cor)
        legendas.append(mpatches.Patch(color=cor, label=f'P{pid}'))

    ax.set_ylim(5, 25)
    ax.set_xlim(0, max(fim for _, _, fim in gantt) + 2)
    ax.set_xlabel('Tempo', fontsize=12)
    ax.set_yticks([])
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend(handles=list(dict.fromkeys(legendas)), bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Exibição dos resultados
def mostrar_resultados(processos):
    texto = ""
    for p in processos:
        tempo_vida = p.fim - p.chegada
        texto += f"P{p.pid} | Espera: {p.tempo_espera} | Tempo de vida: {tempo_vida}\n"
    messagebox.showinfo("Resultados", texto)

# Aplicação principal
class Aplicacao:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Escalonamento de Processos")
        self.raiz.attributes("-fullscreen", True)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(".", font=("Segoe UI", 12))
        estilo.configure("TButton", padding=6, background="#1976D2", foreground="white", relief="flat")
        estilo.map("TButton", background=[("active", "#1565C0")])
        estilo.configure("TLabelFrame", background="#F5F5F5", foreground="#212121", padding=10)
        estilo.configure("TFrame", background="#F5F5F5")
        estilo.configure("TLabel", background="#F5F5F5", foreground="#212121")
        estilo.configure("TEntry", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#212121")
        estilo.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#212121")

        self.processos = []
        self.proximo_pid = 1

        # Formulário de entrada
        quadro_dados = ttk.LabelFrame(raiz, text="Novo Processo")
        quadro_dados.pack(padx=20, pady=20, fill="x")

        ttk.Label(quadro_dados, text="Chegada:").grid(row=0, column=0, padx=5, pady=5)
        self.entrada_chegada = ttk.Entry(quadro_dados, width=5)
        self.entrada_chegada.grid(row=0, column=1)

        ttk.Label(quadro_dados, text="Duração:").grid(row=0, column=2, padx=5, pady=5)
        self.entrada_duracao = ttk.Entry(quadro_dados, width=5)
        self.entrada_duracao.grid(row=0, column=3)

        ttk.Label(quadro_dados, text="Tipo:").grid(row=0, column=4, padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(quadro_dados, values=["CPU-bound", "IO-bound"], width=10)
        self.combo_tipo.grid(row=0, column=5)
        self.combo_tipo.set("CPU-bound")

        ttk.Button(quadro_dados, text="Adicionar", command=self.adicionar_processo).grid(row=0, column=6, padx=10)

        # Lista de processos
        self.lista_processos = tk.Listbox(raiz, width=80, height=10, bg="#FAFAFA", fg="#212121", selectbackground="#BBDEFB")
        self.lista_processos.pack(padx=20, pady=10)

        # Quantum para Round Robin
        quadro_quantum = ttk.LabelFrame(raiz, text="Round-Robin")
        quadro_quantum.pack(padx=20, pady=10, fill="x")

        ttk.Label(quadro_quantum, text="Quantum:").grid(row=0, column=0, padx=5)
        self.entrada_quantum = ttk.Entry(quadro_quantum, width=5)
        self.entrada_quantum.grid(row=0, column=1)
        self.entrada_quantum.insert(0, "2")

        # Botões
        quadro_botoes = ttk.Frame(raiz)
        quadro_botoes.pack(padx=20, pady=20)

        ttk.Button(quadro_botoes, text="Simular FIFO", command=self.executar_fifo).grid(row=0, column=0, padx=15)
        ttk.Button(quadro_botoes, text="Simular Round-Robin", command=self.executar_round_robin).grid(row=0, column=1, padx=15)
        ttk.Button(quadro_botoes, text="Sair", command=self.raiz.destroy).grid(row=0, column=2, padx=15)

    def adicionar_processo(self):
        try:
            chegada = int(self.entrada_chegada.get())
            duracao = int(self.entrada_duracao.get())
            tipo = self.combo_tipo.get()

            novo_proc = Processo(self.proximo_pid, chegada, duracao, tipo)
            self.processos.append(novo_proc)
            self.lista_processos.insert(tk.END, f"P{self.proximo_pid} | Chegada: {chegada} | Duração: {duracao} | Tipo: {tipo}")
            self.proximo_pid += 1

            self.entrada_chegada.delete(0, tk.END)
            self.entrada_duracao.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Chegada e duração devem ser números inteiros.")

    def executar_fifo(self):
        if not self.processos:
            messagebox.showerror("Erro", "Cadastre pelo menos um processo.")
            return

        copia = [Processo(p.pid, p.chegada, p.duracao, p.tipo) for p in self.processos]
        resultado, gantt = simular_fifo(copia)
        mostrar_resultados(resultado)
        exibir_grafico_gantt(gantt, "Escalonamento FIFO")

    def executar_round_robin(self):
        if not self.processos:
            messagebox.showerror("Erro", "Cadastre pelo menos um processo.")
            return

        try:
            quantum = int(self.entrada_quantum.get())
            copia = [Processo(p.pid, p.chegada, p.duracao, p.tipo) for p in self.processos]
            resultado, gantt = simular_round_robin(copia, quantum)
            mostrar_resultados(resultado)
            exibir_grafico_gantt(gantt, "Escalonamento Round-Robin")

        except ValueError:
            messagebox.showerror("Erro", "Quantum deve ser um número inteiro.")

# Execução do programa
if __name__ == "__main__":
    raiz = tk.Tk()
    app = Aplicacao(raiz)
    raiz.mainloop()