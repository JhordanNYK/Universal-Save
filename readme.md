# 🎮 Universal Save Editor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Interface](https://img.shields.io/badge/UI-CustomTkinter-1f6feb)
![Platform](https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Languages](https://img.shields.io/badge/Idiomas-PT--BR%20%7C%20EN--US-success)
![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-green)

Um editor de saves universal, moderno e seguro desenvolvido em Python com interface **CustomTkinter** em modo escuro. Projetado para abrir, inspecionar, filtrar e editar variáveis de jogos criados em **Ren'Py**, **RPG Maker (MV / MZ)** e múltiplos formatos de arquivos de progresso (`.save`, `.dat`, `.sav`, `.json`, `.ini` e `persistent`).

> 🌐 **Bilingual Interface:** Includes instant real-time language switching between **Portuguese (PT-BR)** and **English (EN-US)**. *(See the [English section](#-english-documentation) below).*

---

## ✨ Funcionalidades Principais

* 🔍 **Motor de Detecção Automática em 7 Camadas:** Identifica a assinatura real dos bytes (*Magic Bytes*) de arquivos `.save`, `.dat` e `.sav`, independentemente da extensão utilizada pelo jogo.
* 🐍 **Desbloqueio Nativo de Ren'Py (Sem precisar do motor do jogo):** Lê e regrava arquivos `.save` e `persistent` usando classes substitutas dinâmicas (`RevertableDict`, `RevertableList`, `RevertableSet` e objetos customizados) compatíveis com **Ren'Py 7 (Python 2)** e **Ren'Py 8 (Python 3)**.
* 📂 **Central Inteligente de Jogos e Atalhos (`Ctrl + O`):**
  * **Scan Rápido:** Localiza automaticamente os saves jogados mais recentemente no PC (ordenados por data e hora de gravação).
  * **Atalhos do Sistema:** Acesso em 1 clique para `AppData\Roaming\RenPy`, `Unity / LocalLow`, `Saved Games` e `My Games`.
  * **Pastas Fixadas & Histórico:** Fixe as pastas dos seus jogos favoritos e acesse os últimos arquivos abertos diretamente na barra lateral.
* ⚡ **Painel Inspetor para Edição Confortável:**
  * **Ajuste Rápido de Números:** Botões dedicados (`-100`, `-10`, `-1`, `+1`, `+10`, `+100`, `+1000`, `+10k`, `x2`, `Zerar`, `999` e `MÁX 999k`).
  * **Interruptores Booleanos:** Alterne entre `True` e `False` com botões dedicados ou dando **duplo clique** diretamente na linha da tabela.
  * **Favoritos e Restauração Individual:** Fixe variáveis importantes (como *Gold*, *HP*, *XP*) na aba **Favoritos** e compare ou restaure o **Valor Original** de qualquer variável individualmente.
* 🛡️ **Segurança Contra Corrupção de Dados:**
  * Criação automática de backup (`.bak`) na primeira abertura do arquivo.
  * Preservação estrita dos tipos de dados originais (`int`, `float`, `bool`, `str`).
  * Gravação atômica via arquivo temporário (`.tmp`) antes de substituir o save final.
* 🌎 **Bilingue em Tempo Real:** Alternância instantânea entre **Português do Brasil (`PT-BR`)** e **Inglês (`EN-US`)**.

---

## 🗂️ Formatos e Motores Suportados

| Motor / Tipo de Save | Extensões Comuns | Tecnologia de Leitura e Gravação |
| :--- | :--- | :--- |
| **Ren'Py Visual Novels** | `.save`, `persistent` | Arquivo ZIP + Python `pickle` (Protocolo 2, remoção automática de `signatures`) |
| **RPG Maker MV** | `.rpgsave` | Compressão Base64 (`LZString`) + JSON compacto |
| **RPG Maker MZ** | `.rmmzsave` | Compressão `zlib` / Deflate + JSON |
| **Arquivos Comprimidos** | `.dat`, `.save`, `.sav` | Descompressão e recompressão automática `zlib`, `gzip` e `raw deflate` |
| **JSON & Variantes** | `.json`, `.dat`, `.save` | JSON Padrão, Multi-Line JSON (`NDJSON`), Base64 JSON e Header+JSON |
| **Configurações / Chave-Valor** | `.ini`, `.dat`, `.sav` | Mapeamento de seções `[Section]` e chaves `key=value` preservando formatação |
| **Saves Binários Puros** | `.dat`, `.save` | Inspetor Binário Inteligente (mapeamento de identificadores ASCII, textos e `int32`) |

---

## 🚀 Como Executar pelo Código-Fonte

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.9** (ou superior) instalado.

### 2. Instalar as dependências
No terminal ou Prompt de Comando (CMD), instale as bibliotecas necessárias:

```bash
pip install customtkinter lzstring Pillow
```

### 3. Iniciar o aplicativo
```bash
python Universal_Save.py
```

---

## 📦 Como Compilar o Executável (`.exe`)

Para gerar um arquivo **`Universal Save Editor.exe`** portátil (arquivo único, sem janela de console):

1. Instale o **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```
2. *(Opcional)* Coloque uma imagem **`icone.png`** ou **`icone.ico`** na mesma pasta do script (o aplicativo converte `icone.png` para `.ico` automaticamente).
3. Execute o comando de compilação:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "Universal Save Editor" --icon="icone.ico" --add-data "icone.ico;." --collect-all customtkinter --collect-all lzstring "Universal_Save.py"
   ```
4. O executável final estará disponível dentro da pasta **`dist/`**.

---

## ⌨️ Atalhos de Teclado

| Atalho | Ação |
| :--- | :--- |
| **`Ctrl + O`** | Abre a Central de Jogos, Pastas e Atalhos Inteligentes |
| **`Ctrl + F`** | Foca diretamente na barra de pesquisa de variáveis e valores |
| **`Ctrl + S`** | Salva todas as alterações pendentes no arquivo atual |
| **`Enter`** | Aplica o novo valor digitado no Painel Inspetor |
| **`Duplo Clique`** | Alterna imediatamente valores booleanos (`True` ↔ `False`) ou foca na edição |

---

## 🌐 English Documentation

**Universal Save Editor** is a modern, dark-themed desktop application built with Python and **CustomTkinter** to safely inspect, search, and modify game save files without corrupting data structures.

### Key Highlights
* **7-Layer Auto-Detection Engine:** Automatically detects and parses Ren'Py `.save` / `persistent` archives, RPG Maker MV (`.rpgsave`) and MZ (`.rmmzsave`), Zlib/Gzip compressed saves, standard/multi-line/Base64 JSON, INI files, and raw binary `.dat`/`.save` files.
* **Smart Game Browser (`Ctrl + O`):** Quickly scans your PC for recently modified saves across Ren'Py, Unity (`LocalLow`), `Saved Games`, and custom pinned folders.
* **Comfortable Value Inspector:** One-click quick math buttons for numbers (`+100`, `+10k`, `x2`, `MAX`), instant boolean switches, variable pinning (Favorites), and individual variable reset.
* **Safe & Atomic Saving:** Automatically creates a `.bak` backup file when opening any save and preserves original Python/JSON data types on export.

---

## 📄 Licença / License

Este projeto está sob a licença **MIT**. Sinta-se livre para usar, estudar e contribuir!
