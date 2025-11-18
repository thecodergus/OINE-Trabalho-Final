# Simulador Educacional de Escalas de Temperatura e Mudanças de Fase

Este projeto é um simulador educacional interativo desenvolvido em Python usando a biblioteca Arcade. O simulador permite aos usuários explorar diferentes escalas de temperatura (Celsius, Fahrenheit, Kelvin) e observar as mudanças de fase de várias substâncias.

---

## Pré-requisitos

- **Python 3.10+** (recomendado 3.13)
- **uv** (https://github.com/astral-sh/uv)
- Sistema operacional: Windows 10/11 (binário gerado para Windows)

---

## 1. Sincronização do Ambiente com uv

Para instalar todas as dependências do projeto e preparar o ambiente virtual:

```bash
uv sync
```

- Cria automaticamente o ambiente virtual `.venv/` se não existir.
- Instala todas as dependências de produção e desenvolvimento conforme `pyproject.toml`.
- Garante reprodutibilidade e isolamento do ambiente.

---

## 2. Execução Direta do Projeto

Após a sincronização, execute o simulador diretamente no ambiente virtual:

```bash
uv run python main.py
```

- O comando `uv run` garante que o script será executado no contexto do ambiente virtual criado pelo uv.
- O ponto de entrada do projeto é o arquivo `main.py` na raiz do repositório.

---

## 3. Geração do Binário Standalone

Para criar um executável Windows independente (não requer Python instalado no destino):

```bash
uv run build-bin
```

- O comando `build-bin` está registrado em `[project.scripts]` do `pyproject.toml` e executa o script `src/build_bin.py`.
- O binário gerado estará disponível na pasta `dist/` com o nome `trabalho-final.exe`.
- O executável inclui:
  - Interpretador Python embutido
  - Todas as dependências do projeto (incluindo Pygame)
  - Assets e módulos necessários para execução

---

## Observações Importantes

- O binário gerado **não requer Python, pip ou compiladores instalados** na máquina de destino.
- Em sistemas Windows antigos, pode ser necessário o Visual C++ Redistributable (já incluso no Windows 10/11).
- Para garantir portabilidade, teste o binário em uma máquina limpa antes de distribuir.

---

## Resumo dos Comandos

| Ação                        | Comando                        |
|-----------------------------|--------------------------------|
| Sincronizar dependências     | `uv sync`                      |
| Executar o projeto           | `uv run python main.py`        |
| Gerar binário standalone     | `uv run build-bin`             |

---

## Troubleshooting

- **Erro de dependências:** Execute `uv sync --reinstall` para forçar reinstalação.
- **Binário não executa:** Verifique se todos os assets estão incluídos e teste em ambiente limpo.
- **Dúvidas sobre uv:** Consulte [documentação oficial do uv](https://github.com/astral-sh/uv).