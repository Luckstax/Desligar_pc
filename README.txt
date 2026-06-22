# Desligar PC

Ferramenta com interface gráfica (Tkinter) para agendar o desligamento ou reinício do Windows — manualmente ou de forma automática e recorrente.

## Funcionalidades

**Aba Manual**
- Desligar ou reiniciar em um horário definido (HH:MM)
- Desligar ou reiniciar por contagem regressiva (HH:MM a partir de agora)
- Atalho rápido para desligar às 22:00
- Cancelar um desligamento/reinício agendado

**Aba Automático**
- Agendar um desligamento recorrente, em horário fixo, nos dias da semana selecionados
- Funciona criando um pequeno script na pasta de Inicialização do Windows, executado a cada login
- Pode ser desativado a qualquer momento

> ℹ️ **Nota:** o recurso automático depende da associação de arquivos `.pyw` no Windows estar configurada para executar com `pythonw.exe`, o que é o padrão em instalações comuns do Python. Testado com sucesso após login/reinicialização. Se no seu sistema essa associação tiver sido alterada (por exemplo, por outro editor/IDE configurado como app padrão para `.pyw`), o script não será executado — nesse caso, uma alternativa é registrar a tarefa diretamente no Agendador de Tarefas do Windows (`schtasks`).

## Requisitos

- Windows
- Python 3.10 ou superior
- Nenhuma dependência externa — usa apenas a biblioteca padrão (`tkinter`, `subprocess`, `datetime`, `os`)

## Como usar

```bash
git clone https://github.com/Luckstax/desligar-pc.git
cd desligar-pc
python desligar_pc.pyw
```

Ou dê duplo clique em `desligar_pc.pyw` no Explorador de Arquivos (não abre uma janela de console).

## Estrutura do projeto

```
desligar-pc/
├── desligar_pc.pyw
├── README.md
├── LICENSE
└── .gitignore
```

## Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
