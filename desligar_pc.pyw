"""
Desligar PC - Agendador de Desligamento e Reinicio
====================================================

Interface grafica (Tkinter) para agendar o desligamento ou reinicio do
Windows, de duas formas:

- Manual: horario especifico ou contagem regressiva, com cancelamento.
- Automatico: agendamento recorrente nos dias da semana escolhidos,
  criado como um script na pasta de Inicializacao do Windows.

Requisitos: Windows, Python 3.10+. Apenas biblioteca padrao.
"""

import os
import subprocess
import datetime
from tkinter import *
from tkinter import ttk, messagebox


def _shutdown(*args):
    """Executa o comando shutdown.exe do Windows com os argumentos dados."""
    subprocess.run(['shutdown', *args], shell=False)


# ============================================================
# ABA 1 - MANUAL
# ============================================================

def get_current_time():
    """Retorna o datetime atual."""
    return datetime.datetime.now()


def desligar_as_22h():
    """Atalho: agenda o desligamento para as 22:00 (hoje, ou amanha se ja passou)."""
    _shutdown('/a')
    agora = get_current_time()
    hora_desligar = datetime.time(22, 0)
    momento_desligar = datetime.datetime.combine(agora.date(), hora_desligar)

    if momento_desligar < agora:
        momento_desligar += datetime.timedelta(days=1)

    diferenca_tempo = int((momento_desligar - agora).total_seconds())
    _shutdown('/s', '/t', str(diferenca_tempo))


def schedule_shutdown_or_restart(hora_marcada, opcao, escolha):
    """Agenda desligamento/reinicio por horario definido ou contagem regressiva."""
    agora = get_current_time()

    try:
        if opcao == 'Definir horário':
            tempo = datetime.datetime.strptime(hora_marcada, '%H:%M')
            tempo = tempo.replace(year=agora.year, month=agora.month, day=agora.day)

            if tempo < agora:
                tempo += datetime.timedelta(days=1)

            segundos = int((tempo - agora).total_seconds())

        elif opcao == 'Contagem regressiva':
            horas, minutos = map(int, hora_marcada.split(':'))
            if not (0 <= horas <= 23 and 0 <= minutos <= 59):
                raise ValueError
            segundos = horas * 3600 + minutos * 60
        else:
            return

    except ValueError:
        messagebox.showerror("Erro", "Formato inválido. Use HH:MM (horas 0-23, minutos 0-59).")
        return

    if escolha == 'Desligar':
        flag = '/s'
    elif escolha == 'Reiniciar':
        flag = '/r'
    else:
        return

    _shutdown(flag, '/t', str(segundos))


def cancelar():
    """Cancela qualquer desligamento/reinicio agendado e avisa o usuario."""
    _shutdown('/a')
    messagebox.showinfo("Cancelado", "Desligamento/reinício agendado foi cancelado.")


# ============================================================
# ABA 2 - AUTOMATICO (recorrente, via pasta de Inicializacao)
# ============================================================

DIAS_SEMANA = [
    ("Domingo", 6),
    ("Segunda", 0),
    ("Terça", 1),
    ("Quarta", 2),
    ("Quinta", 3),
    ("Sexta", 4),
    ("Sábado", 5),
]  # numeros seguem datetime.weekday(): Segunda=0 ... Domingo=6


def caminho_startup():
    """Retorna o caminho da pasta de Inicializacao do usuario atual no Windows."""
    return os.path.join(
        os.getenv('APPDATA'),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )


def caminho_script_automatico():
    """Caminho do script gerado para o desligamento automatico."""
    return os.path.join(caminho_startup(), "desligar_auto.pyw")


def criar_automatico(hora, minuto, dias_selecionados):
    """Gera um script .pyw na pasta de Inicializacao para desligar
    automaticamente no horario definido, nos dias da semana selecionados.

    Nota: isso depende da associacao de arquivo .pyw no Windows estar
    configurada para executar com o Python no login. Teste apos reiniciar
    a maquina para confirmar que funciona no seu ambiente.
    """
    if not dias_selecionados:
        messagebox.showerror("Erro", "Selecione ao menos um dia da semana.")
        return

    script_path = caminho_script_automatico()

    conteudo = f'''"""Script gerado automaticamente por Desligar PC. Não editar manualmente."""
import subprocess
from datetime import datetime, time, timedelta

agora = datetime.now()
dia = agora.weekday()
dias_ativos = {dias_selecionados}

if dia in dias_ativos:
    horario = datetime.combine(agora.date(), time({hora}, {minuto}))

    if horario <= agora:
        horario += timedelta(days=1)

    segundos = int((horario - agora).total_seconds())

    subprocess.run(["shutdown", "/a"])
    subprocess.run(["shutdown", "/s", "/t", str(segundos)])
'''

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(conteudo)

    nomes_dias = [nome for nome, numero in DIAS_SEMANA if numero in dias_selecionados]
    messagebox.showinfo(
        "Ativado",
        f"Desligamento automático definido para {hora:02d}:{minuto:02d}\n"
        f"Dias: {', '.join(nomes_dias)}"
    )


def remover_automatico():
    """Remove o script de desligamento automatico, se existir."""
    script_path = caminho_script_automatico()

    if os.path.exists(script_path):
        os.remove(script_path)
        messagebox.showinfo("Removido", "Desligamento automático desativado.")
    else:
        messagebox.showinfo("Info", "Nenhum desligamento automático ativo.")


# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

root = Tk()
root.title("Desligar PC")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- Aba 1: Manual ---
aba1 = Frame(notebook)
notebook.add(aba1, text="Manual")

escolha = StringVar(value="Desligar")
opcao = StringVar(value="Definir horário")
hora_marcada = StringVar()

frame_acao = Frame(aba1)
frame_acao.pack(pady=5)
Label(frame_acao, text="Ação:").pack(side=LEFT, padx=5)
OptionMenu(frame_acao, escolha, "Desligar", "Reiniciar").pack(side=LEFT)

frame_tipo = Frame(aba1)
frame_tipo.pack(pady=5)
Label(frame_tipo, text="Modo:").pack(side=LEFT, padx=5)
OptionMenu(frame_tipo, opcao, "Definir horário", "Contagem regressiva").pack(side=LEFT)

frame_entrada = Frame(aba1)
frame_entrada.pack(pady=5)
Label(frame_entrada, text="Hora (HH:MM):").pack(side=LEFT, padx=5)
Entry(frame_entrada, textvariable=hora_marcada, width=10).pack(side=LEFT)

frame_botoes = Frame(aba1)
frame_botoes.pack(pady=10)
Button(frame_botoes, text="Confirmar",
       command=lambda: schedule_shutdown_or_restart(
           hora_marcada.get(), opcao.get(), escolha.get())
       ).pack(side=LEFT, padx=5)
Button(frame_botoes, text="Cancelar desligamento",
       command=cancelar).pack(side=LEFT, padx=5)

Button(aba1, text="Desligar às 22:00", command=desligar_as_22h).pack(pady=5)

# --- Aba 2: Automático ---
aba2 = Frame(notebook)
notebook.add(aba2, text="Automático")

Label(aba2, text="Horário fixo (HH:MM):").pack(pady=(10, 0))
entrada_auto = Entry(aba2, width=10)
entrada_auto.pack(pady=(0, 10))

Label(aba2, text="Dias da semana:").pack()
frame_dias = Frame(aba2)
frame_dias.pack(pady=5)

dia_vars = {}
for nome, numero in DIAS_SEMANA:
    var = BooleanVar(value=False)
    dia_vars[numero] = var
    Checkbutton(frame_dias, text=nome, variable=var).pack(side=LEFT, padx=3)


def ativar_auto():
    try:
        h, m = map(int, entrada_auto.get().split(":"))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Formato inválido. Use HH:MM (horas 0-23, minutos 0-59).")
        return

    dias_selecionados = [numero for numero, var in dia_vars.items() if var.get()]
    criar_automatico(h, m, dias_selecionados)


frame_auto_botoes = Frame(aba2)
frame_auto_botoes.pack(pady=10)
Button(frame_auto_botoes, text="Ativar automático", command=ativar_auto).pack(side=LEFT, padx=5)
Button(frame_auto_botoes, text="Desativar automático", command=remover_automatico).pack(side=LEFT, padx=5)

root.mainloop()
