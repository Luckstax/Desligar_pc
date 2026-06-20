Desligar PC – Agendador de Desligamento e Reinício

Ferramenta em Python com interface gráfica para agendar o desligamento ou reinício do computador, permitindo:

Definir um horário específico

Definir uma contagem regressiva

Escolher entre desligar ou reiniciar

Projeto voltado para automação simples em ambiente Windows.

Funcionalidades

Interface gráfica (Tkinter)

Agendamento por:

Horário definido (HH:MM)

Contagem regressiva (horas e minutos)

Ações disponíveis:

Desligar o computador

Reiniciar o computador

Cálculo automático do tempo restante

Validação básica de entradas

Requisitos

Python 3.10 ou superior

Sistema operacional: Windows

Bibliotecas utilizadas:

tkinter (padrão do Python)

time

os

datetime

Como executar

Clone o repositório:

git clone https://github.com/seu-usuario/desligar-pc.git


Acesse a pasta do projeto:

cd desligar-pc


Execute o programa:

python src/desligar_pc.py

Estrutura do projeto
desligar-pc/
│
├─ src/
│   └─ desligar_pc.py
│
├─ legacy/
│   └─ desligar_pc_v1.py
│
├─ README.md
├─ requirements.txt
└─ .gitignore

Observações

A pasta legacy/ contém a versão 1.0 do projeto, mantida apenas para fins de histórico.

A versão principal e recomendada é a 2.0, localizada em src/.