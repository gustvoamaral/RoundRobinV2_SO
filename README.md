# 🖥️ Simulador de Escalonamento de Processos

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data_Vis-orange?style=for-the-badge)

Uma aplicação desktop desenvolvida em Python para simular e visualizar algoritmos de escalonamento de processos. O projeto foi desenvolvido para a disciplina de Sistemas Operacionais com foco educacional, facilitando o entendimento prático de como a CPU gerencia a fila de processos.
## 🎯 Objetivo do Projeto

Facilitar o entendimento prático e visual do funcionamento de algoritmos de escalonamento clássicos, permitindo o cadastro de processos e o acompanhamento de sua execução através de métricas e gráficos de Gantt.

## ✨ Funcionalidades

* **Cadastro de Processos:** Insira o tempo de chegada, duração e defina o tipo (CPU-bound ou IO-bound).
* **Simulação FIFO (First-In, First-Out):** Escalonamento não preemptivo baseado na ordem de chegada.
* **Simulação Round-Robin:** Escalonamento preemptivo com suporte à customização do *Quantum* de tempo.
* **Cálculo de Métricas:** Exibição automática do Tempo de Espera e Tempo de Vida (Turnaround) de cada processo.
* **Gráficos de Gantt:** Geração de gráficos visuais modernos e coloridos utilizando Matplotlib para ilustrar a linha do tempo de execução da CPU.
* **Interface Gráfica (GUI):** Interface totalmente customizada e intuitiva construída com Tkinter (tema *clam*).

## 🚀 Como Executar

Certifique-se de ter o **Python 3** instalado (o `tkinter` é nativo na maioria das instalações). 

No seu terminal, rode os seguintes comandos:

```bash
#1. Clone o repositório
git clone https://github.com/gustvoamaral/RoundRobinV2_SO

#2. Entre na pasta do projeto
cd RoundRobinV2_SO

#3. Instale a dependência dos gráficos
pip install matplotlib

# 4. Execute a aplicação
python simulador.py
```

## 🛠️ Tecnologias Utilizadas
* **Python:** Linguagem base do projeto.
* **Tkinter (ttk):** Construção da interface gráfica de usuário.
* **Matplotlib:** Renderização dos gráficos de Gantt.
* **Collections (deque):** Estrutura de dados otimizada para o gerenciamento das filas no algoritmo Round-Robin.

## 📖 Open Source 
O projeto é **Open Source** (código aberto), o que significa que você é livre para clonar, estudar, modificar e usar como base para os seus próprios projetos de aprendizado!

## 🤝 Como Contribuir

Sinta-se à vontade para enviar melhorias ou adicionar novos algoritmos (como SJF, SRTF ou Escalonamento por Prioridade):

1. Faça um *Fork* do projeto
2. Crie uma *Branch* para sua modificação (`git checkout -b feature/NovoAlgoritmo`)
3. Faça o *Commit* de suas mudanças (`git commit -m 'Adiciona algoritmo X'`)
4. Faça o *Push* para a branch (`git push origin feature/NovoAlgoritmo`)
5. Abra um *Pull Request*

