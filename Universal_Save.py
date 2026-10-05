# -*- coding: utf-8 -*-
import base64
import gzip
import io
import json
import os
import pickle
import platform
import re
import shutil
import struct
import sys
import types
import zipfile
import zlib
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# ==============================================================================
# 0. DICIONARIO DE IDIOMAS (PT-BR & EN-US) COM PROTECAO UNICODE
# ==============================================================================

TRANSLATIONS = {
    "pt-BR": {
        "app_title": "Universal Save Editor - Edi\u00e7\u00e3o & Atalhos Inteligentes",
        "lang_label": "Idioma / Language:",
        "sub_logo": "Ren'Py | RPG Maker | .DAT | .SAVE",
        "btn_smart_browser": "Explorar Jogos & Atalhos (Ctrl+O)",
        "btn_open_classic": "Procurar Arquivo no PC...",
        "lbl_recent": "Saves Recentes (1 Clique):",
        "recent_empty": "Nenhum save recente",
        "recent_select": "Abrir recente...",
        "btn_save": "Salvar Tudo (Ctrl+S)",
        "btn_save_as": "Salvar Como...",
        "btn_restore": "Restaurar Backup (.bak)",
        "info_no_file": (
            "Nenhum save aberto.\n\n"
            "Clique em 'Explorar Jogos & Atalhos' para localizar seus saves automaticamente."
        ),
        "btn_view_folder": "Abrir Pasta no Explorer",
        "btn_pin_folder": "+ Fixar Pasta nos Atalhos",
        "search_placeholder": "Pesquisar vari\u00e1vel (ex: gold, money, hp) ou valor atual (Ctrl+F)...",
        "btn_clear": "Limpar",
        "filter_all": "Todos",
        "filter_fav": "Favoritos",
        "filter_mod": "Modificados",
        "filter_num": "N\u00fameros",
        "filter_bool": "Booleanos",
        "filter_str": "Texto",
        "col_var": "Vari\u00e1vel / Caminho (Ordenar)",
        "col_type": "Tipo",
        "col_orig": "Valor Original",
        "col_val": "Valor Atual",
        "col_status": "Status",
        "status_mod_fav": "* Editado",
        "status_mod": "Editado",
        "status_fav": "* Favorito",
        "status_orig": "Original",
        "insp_header": "Painel de Edi\u00e7\u00e3o",
        "insp_sub": "Selecione uma vari\u00e1vel na tabela",
        "var_none": "Nenhuma selecionada",
        "var_meta_empty": "Tipo: -   |   Original: -",
        "var_meta_fmt": "Tipo: {type}   |   Original: {orig}",
        "btn_fav_add": "Fixar Vari\u00e1vel nos Favoritos",
        "btn_fav_rem": "Remover dos Favoritos",
        "lbl_new_val": "Novo Valor:",
        "entry_placeholder": "Selecione uma linha...",
        "btn_apply": "Aplicar Valor (Enter)",
        "lbl_quick_num": "Ajuste R\u00e1pido de N\u00fameros:",
        "btn_zero": "Zerar (0)",
        "btn_max": "M\u00c1X 999k",
        "lbl_quick_bool": "Alternar Interruptor (Booleano):",
        "btn_bool_true": "Ativar (True)",
        "btn_bool_false": "Desativar (False)",
        "btn_revert_var": "Restaurar Valor Original da Vari\u00e1vel",
        "status_ready": "Pronto. Pressione Ctrl+O ou clique em 'Explorar Jogos & Atalhos' para localizar saves.",
        "status_showing": "Exibindo {count} de {total} vari\u00e1veis  |  Altera\u00e7\u00f5es pendentes: {mods}",
        "status_loaded": "Save carregado ({fmt}): {path} ({total} campos edit\u00e1veis).",
        "status_updated": "Atualizado: '{key}' -> {val}  (Pressione Ctrl+S para salvar no arquivo)",
        "status_reverted": "Vari\u00e1vel '{key}' restaurada para o valor original ({val}).",
        "status_saved": "Save gravado com sucesso em: {path}",
        "status_exported": "Save exportado com sucesso para: {path}",
        "status_backup_restored": "Backup original (.bak) restaurado com sucesso.",
        "summary_fmt": (
            "Jogo/Pasta: {folder}\n"
            "Arquivo: {name}\n"
            "Formato: {engine}\n"
            "Vari\u00e1veis: {total} (Editadas: {mods})\n"
            "Backup .bak: Ativo"
        ),
        "msg_pin_title": "Pasta Fixada",
        "msg_pin_added": "A pasta '{name}' foi adicionada aos seus Atalhos Fixados!",
        "msg_pin_exists_title": "Atalho Existente",
        "msg_pin_exists": "Esta pasta j\u00e1 est\u00e1 nos seus Atalhos Fixados.",
        "msg_err_open": "Erro ao Abrir Save",
        "msg_invalid_val": "Valor Inv\u00e1lido",
        "msg_invalid_val_body": "N\u00e3o foi poss\u00edvel alterar o valor:\n{err}",
        "msg_err_save": "Erro ao Salvar",
        "msg_err_save_body": "Ocorreu um erro ao salvar o arquivo:\n{err}",
        "msg_success": "Sucesso",
        "msg_saved_body": "As altera\u00e7\u00f5es foram salvas no arquivo com sucesso!",
        "msg_exported_body": "Arquivo salvo com sucesso em:\n{path}",
        "msg_restore_title": "Restaurar Backup (.bak)",
        "msg_restore_confirm": (
            "Deseja substituir o save atual pelo backup original (.bak)?\n"
            "Todas as altera\u00e7\u00f5es feitas ser\u00e3o desfeitas."
        ),
        "msg_restore_done_title": "Backup Restaurado",
        "msg_restore_done_body": "O arquivo original foi restaurado com sucesso!",
        "msg_restore_missing_title": "Backup N\u00e3o Encontrado",
        "msg_restore_missing_body": "N\u00e3o foi encontrado nenhum arquivo .bak para este save.",
        "dlg_open_title": "Selecionar Arquivo de Save",
        "dlg_save_as_title": "Salvar Arquivo Como",
        "ft_all_saves": "Todos os Saves Suportados",
        "ft_all_files": "Todos os Arquivos",
        "ft_save_file": "Arquivo de Save",
        "modal_title": "Explorar Jogos, Pastas e Atalhos R\u00e1pidos",
        "modal_loc": "Localiza\u00e7\u00e3o:",
        "modal_smart_scan_title": "Scan Inteligente (Saves Mais Recentes no PC)",
        "modal_btn_go": "Ir",
        "modal_btn_pick_folder": "Escolher Pasta...",
        "modal_btn_pin": "+ Fixar Pasta nos Atalhos",
        "modal_left_header": "Atalhos & Pastas de Jogos",
        "modal_filter_ph": "Filtrar por nome do jogo, pasta ou arquivo (ex: saves.dat, 1-1, file1)...",
        "modal_chk_hide_meta": "Ocultar arquivos de configura\u00e7\u00e3o (package/system)",
        "modal_col_game": "Jogo / Pasta",
        "modal_col_file": "Arquivo de Save",
        "modal_col_type": "Tipo",
        "modal_col_mod": "\u00daltima Grava\u00e7\u00e3o (Mais Recentes)",
        "modal_col_size": "Tamanho",
        "modal_count_fmt": "{count} saves listados (ordenados do mais recente para o mais antigo)",
        "modal_btn_win_file": "Procurar Arquivo no Windows...",
        "modal_btn_explorer": "Abrir Pasta no Explorer",
        "modal_btn_load": "Carregar Save Selecionado (Duplo Clique)",
        "modal_btn_quick_scan": "Scan R\u00e1pido (\u00daltimos Jogados)",
        "modal_sec_pinned": "MEUS ATALHOS FIXADOS:",
        "modal_no_pinned": "Nenhuma pasta fixada ainda.\nUse '+ Fixar Pasta' no topo.",
        "modal_sec_system": "PASTAS DO SISTEMA:",
        "modal_sec_renpy": "JOGOS REN'PY DETECTADOS:",
        "modal_recent_tag": "[Recente] ",
        "modal_msg_sel_folder_title": "Selecionar Pasta",
        "modal_msg_sel_folder_body": (
            "Primeiro escolha uma pasta na esquerda ou clique em 'Escolher Pasta...' "
            "para fix\u00e1-la nos seus atalhos."
        ),
        "modal_msg_invalid_path_title": "Caminho Inv\u00e1lido",
        "modal_msg_invalid_path_body": "A pasta informada n\u00e3o existe:\n{path}",
        "modal_msg_sel_save_title": "Selecionar Save",
        "modal_msg_sel_save_body": "Clique em um arquivo de save na tabela para abri-lo.",
        "modal_msg_open_dir_title": "Abrir Pasta",
        "modal_msg_open_dir_body": "Selecione um arquivo na tabela ou uma pasta na esquerda primeiro.",
        "sys_saved_games": "Jogos Salvos (Saved Games)",
        "sys_documents": "Documentos",
        "sys_my_games": "My Games (Documentos)",
        "sys_desktop": "\u00c1rea de Trabalho (Desktop)",
        "sys_downloads": "Downloads",
    },
    "en-US": {
        "app_title": "Universal Save Editor - Smart Editing & Shortcuts",
        "lang_label": "Language / Idioma:",
        "sub_logo": "Ren'Py | RPG Maker | .DAT | .SAVE",
        "btn_smart_browser": "Browse Games & Shortcuts (Ctrl+O)",
        "btn_open_classic": "Browse File on PC...",
        "lbl_recent": "Recent Saves (1-Click):",
        "recent_empty": "No recent saves",
        "recent_select": "Open recent...",
        "btn_save": "Save All (Ctrl+S)",
        "btn_save_as": "Save As...",
        "btn_restore": "Restore Backup (.bak)",
        "info_no_file": (
            "No save file loaded.\n\n"
            "Click 'Browse Games & Shortcuts' to automatically find your saves."
        ),
        "btn_view_folder": "Open Folder in Explorer",
        "btn_pin_folder": "+ Pin Folder to Shortcuts",
        "search_placeholder": "Search variable name (e.g., gold, money, hp) or current value (Ctrl+F)...",
        "btn_clear": "Clear",
        "filter_all": "All",
        "filter_fav": "Favorites",
        "filter_mod": "Modified",
        "filter_num": "Numbers",
        "filter_bool": "Booleans",
        "filter_str": "Text",
        "col_var": "Variable / Path (Sort)",
        "col_type": "Type",
        "col_orig": "Original Value",
        "col_val": "Current Value",
        "col_status": "Status",
        "status_mod_fav": "* Edited",
        "status_mod": "Edited",
        "status_fav": "* Favorite",
        "status_orig": "Original",
        "insp_header": "Inspector Panel",
        "insp_sub": "Select a variable from the table",
        "var_none": "None selected",
        "var_meta_empty": "Type: -   |   Original: -",
        "var_meta_fmt": "Type: {type}   |   Original: {orig}",
        "btn_fav_add": "Pin Variable to Favorites",
        "btn_fav_rem": "Remove from Favorites",
        "lbl_new_val": "New Value:",
        "entry_placeholder": "Select a row...",
        "btn_apply": "Apply Value (Enter)",
        "lbl_quick_num": "Quick Number Adjust:",
        "btn_zero": "Zero (0)",
        "btn_max": "MAX 999k",
        "lbl_quick_bool": "Toggle Switch (Boolean):",
        "btn_bool_true": "Enable (True)",
        "btn_bool_false": "Disable (False)",
        "btn_revert_var": "Restore Variable Original Value",
        "status_ready": "Ready. Press Ctrl+O or click 'Browse Games & Shortcuts' to locate saves.",
        "status_showing": "Showing {count} of {total} variables  |  Pending changes: {mods}",
        "status_loaded": "Save loaded ({fmt}): {path} ({total} editable fields).",
        "status_updated": "Updated: '{key}' -> {val}  (Press Ctrl+S to write changes to file)",
        "status_reverted": "Variable '{key}' restored to original value ({val}).",
        "status_saved": "Save successfully written to: {path}",
        "status_exported": "Save successfully exported to: {path}",
        "status_backup_restored": "Original backup (.bak) successfully restored.",
        "summary_fmt": (
            "Game/Folder: {folder}\n"
            "File: {name}\n"
            "Format: {engine}\n"
            "Variables: {total} (Edited: {mods})\n"
            "Backup .bak: Active"
        ),
        "msg_pin_title": "Folder Pinned",
        "msg_pin_added": "Folder '{name}' was added to your Pinned Shortcuts!",
        "msg_pin_exists_title": "Shortcut Exists",
        "msg_pin_exists": "This folder is already in your Pinned Shortcuts.",
        "msg_err_open": "Error Opening Save",
        "msg_invalid_val": "Invalid Value",
        "msg_invalid_val_body": "Could not update value:\n{err}",
        "msg_err_save": "Error Saving File",
        "msg_err_save_body": "An error occurred while saving the file:\n{err}",
        "msg_success": "Success",
        "msg_saved_body": "Changes were successfully saved to the file!",
        "msg_exported_body": "File successfully saved to:\n{path}",
        "msg_restore_title": "Restore Backup (.bak)",
        "msg_restore_confirm": (
            "Do you want to overwrite the current save with the original backup (.bak)?\n"
            "All changes will be reverted."
        ),
        "msg_restore_done_title": "Backup Restored",
        "msg_restore_done_body": "The original save file has been restored!",
        "msg_restore_missing_title": "Backup Not Found",
        "msg_restore_missing_body": "No .bak backup file was found for this save.",
        "dlg_open_title": "Select Save File",
        "dlg_save_as_title": "Save File As",
        "ft_all_saves": "All Supported Saves",
        "ft_all_files": "All Files",
        "ft_save_file": "Save File",
        "modal_title": "Browse Games, Folders & Quick Shortcuts",
        "modal_loc": "Location:",
        "modal_smart_scan_title": "Smart Scan (Most Recent Saves on PC)",
        "modal_btn_go": "Go",
        "modal_btn_pick_folder": "Choose Folder...",
        "modal_btn_pin": "+ Pin Folder to Shortcuts",
        "modal_left_header": "Shortcuts & Game Folders",
        "modal_filter_ph": "Filter by game name, folder, or file (e.g., saves.dat, 1-1, file1)...",
        "modal_chk_hide_meta": "Hide config files (package/system)",
        "modal_col_game": "Game / Folder",
        "modal_col_file": "Save File",
        "modal_col_type": "Type",
        "modal_col_mod": "Last Modified (Newest First)",
        "modal_col_size": "Size",
        "modal_count_fmt": "{count} saves listed (sorted from newest to oldest)",
        "modal_btn_win_file": "Browse File in Windows...",
        "modal_btn_explorer": "Open Folder in Explorer",
        "modal_btn_load": "Load Selected Save (Double-Click)",
        "modal_btn_quick_scan": "Quick Scan (Recently Played)",
        "modal_sec_pinned": "MY PINNED SHORTCUTS:",
        "modal_no_pinned": "No pinned folders yet.\nUse '+ Pin Folder' at the top.",
        "modal_sec_system": "SYSTEM FOLDERS:",
        "modal_sec_renpy": "DETECTED REN'PY GAMES:",
        "modal_recent_tag": "[Recent] ",
        "modal_msg_sel_folder_title": "Select Folder",
        "modal_msg_sel_folder_body": (
            "First select a folder on the left or click 'Choose Folder...' "
            "to pin it to your shortcuts."
        ),
        "modal_msg_invalid_path_title": "Invalid Path",
        "modal_msg_invalid_path_body": "The specified folder does not exist:\n{path}",
        "modal_msg_sel_save_title": "Select Save",
        "modal_msg_sel_save_body": "Click a save file in the table to open it.",
        "modal_msg_open_dir_title": "Open Folder",
        "modal_msg_open_dir_body": "Select a file in the table or a folder on the left first.",
        "sys_saved_games": "Saved Games",
        "sys_documents": "Documents",
        "sys_my_games": "My Games (Documents)",
        "sys_desktop": "Desktop",
        "sys_downloads": "Downloads",
    },
}


try:
    import customtkinter as ctk
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Missing Library / Biblioteca Faltando",
        "O modulo 'customtkinter' nao esta instalado.\n"
        "Execute no terminal: pip install customtkinter lzstring"
    )
    sys.exit(1)

try:
    import lzstring
    HAS_LZSTRING = True
except ImportError:
    HAS_LZSTRING = False


# ==============================================================================
# 1. GERENCIADOR DE CONFIGURACOES, IDIOMA, ATALHOS E HISTORICO
# ==============================================================================

class ShortcutConfigManager:
    def __init__(self):
        self.config_path = Path.home() / ".universal_save_editor_cfg.json"
        self.language = "pt-BR"
        self.pinned_folders = []
        self.recent_files = []
        self.favorites_vars = {}
        self.load()

    def load(self):
        if not self.config_path.exists():
            return
        try:
            raw = json.loads(self.config_path.read_text(encoding="utf-8"))
            lang = raw.get("language", "pt-BR")
            if lang in TRANSLATIONS:
                self.language = lang
            self.pinned_folders = [p for p in raw.get("pinned_folders", []) if Path(p).exists()]
            self.recent_files = [f for f in raw.get("recent_files", []) if Path(f).exists()]
            self.favorites_vars = raw.get("favorites_vars", {})
        except Exception:
            pass

    def save(self):
        data = {
            "language": self.language,
            "pinned_folders": self.pinned_folders,
            "recent_files": self.recent_files[:15],
            "favorites_vars": self.favorites_vars,
        }
        try:
            self.config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

    def set_language(self, lang_code):
        if lang_code in TRANSLATIONS:
            self.language = lang_code
            self.save()

    def add_recent_file(self, file_path_str):
        norm = str(Path(file_path_str).resolve())
        if norm in self.recent_files:
            self.recent_files.remove(norm)
        self.recent_files.insert(0, norm)
        self.recent_files = self.recent_files[:15]
        self.save()

    def add_pinned_folder(self, folder_path_str):
        norm = str(Path(folder_path_str).resolve())
        if norm not in self.pinned_folders:
            self.pinned_folders.append(norm)
            self.save()
            return True
        return False

    def remove_pinned_folder(self, folder_path_str):
        norm = str(Path(folder_path_str).resolve())
        if norm in self.pinned_folders:
            self.pinned_folders.remove(norm)
            self.save()
            return True
        return False

    def get_system_shortcuts(self, tr):
        shortcuts = []
        home = Path.home()
        system = platform.system()

        if system == "Windows":
            appdata = os.environ.get("APPDATA", "")
            localappdata = os.environ.get("LOCALAPPDATA", "")
            if appdata:
                renpy_p = Path(appdata) / "RenPy"
                if renpy_p.exists():
                    shortcuts.append(("Ren'Py (AppData Roaming)", renpy_p))
                shortcuts.append(("AppData (Roaming)", Path(appdata)))
            if localappdata:
                locallow = Path(localappdata).parent / "LocalLow"
                if locallow.exists():
                    shortcuts.append(("Unity / LocalLow", locallow))
                shortcuts.append(("AppData (Local)", Path(localappdata)))
        elif system == "Darwin":
            renpy_p = home / "Library" / "RenPy"
            if renpy_p.exists():
                shortcuts.append(("Ren'Py (Library)", renpy_p))
        else:
            renpy_p = home / ".renpy"
            if renpy_p.exists():
                shortcuts.append(("Ren'Py (~/.renpy)", renpy_p))

        common_dirs = [
            (tr["sys_saved_games"], home / "Saved Games"),
            (tr["sys_my_games"], home / "Documents" / "My Games"),
            (tr["sys_documents"], home / "Documents"),
            (tr["sys_desktop"], home / "Desktop"),
            (tr["sys_downloads"], home / "Downloads"),
        ]
        for label, path_obj in common_dirs:
            if path_obj.exists():
                shortcuts.append((label, path_obj))

        return shortcuts


# ==============================================================================
# 2. MOTOR PICKLE & REN'PY: CLASSES SUBSTITUTAS TOLERANTES A QUALQUER ESTRUTURA
# ==============================================================================

_NO_RAW_STATE = object()


class RenpyDummyObject:
    """
    Substituto universal para objetos pickled (Ren'Py, RevertableObject,
    RevertableSet, classes customizadas do jogo com __slots__, listas ou dicts).
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._raw_pickle_state = _NO_RAW_STATE
        instance._pickle_list_items = None
        instance._pickle_dict_items = None
        return instance

    def __init__(self, *args, **kwargs):
        pass

    def __setstate__(self, state):
        if isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self._raw_pickle_state = state

    def __getstate__(self):
        raw = self.__dict__.get("_raw_pickle_state", _NO_RAW_STATE)
        if raw is not _NO_RAW_STATE:
            return raw
        state = dict(self.__dict__)
        state.pop("_raw_pickle_state", None)
        state.pop("_pickle_list_items", None)
        state.pop("_pickle_dict_items", None)
        return state

    def append(self, item):
        if self._pickle_list_items is None:
            self._pickle_list_items = []
        self._pickle_list_items.append(item)

    def extend(self, items):
        if self._pickle_list_items is None:
            self._pickle_list_items = []
        self._pickle_list_items.extend(items)

    def __setitem__(self, key, val):
        if self._pickle_dict_items is None:
            self._pickle_dict_items = {}
        self._pickle_dict_items[key] = val

    def __getitem__(self, key):
        if self._pickle_dict_items and key in self._pickle_dict_items:
            return self._pickle_dict_items[key]
        raise KeyError(key)


class RevertableDict(dict):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._raw_pickle_state = _NO_RAW_STATE
        return instance

    def __setstate__(self, state):
        if isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self._raw_pickle_state = state

    def __getstate__(self):
        raw = self.__dict__.get("_raw_pickle_state", _NO_RAW_STATE)
        if raw is not _NO_RAW_STATE:
            return raw
        state = dict(self.__dict__)
        state.pop("_raw_pickle_state", None)
        return state


class RevertableList(list):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._raw_pickle_state = _NO_RAW_STATE
        return instance

    def __setstate__(self, state):
        if isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self._raw_pickle_state = state

    def __getstate__(self):
        raw = self.__dict__.get("_raw_pickle_state", _NO_RAW_STATE)
        if raw is not _NO_RAW_STATE:
            return raw
        state = dict(self.__dict__)
        state.pop("_raw_pickle_state", None)
        return state


class RevertableSet(set):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._raw_pickle_state = _NO_RAW_STATE
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __setstate__(self, state):
        if isinstance(state, tuple) and len(state) == 1 and isinstance(state[0], (set, list, tuple)):
            self.update(state[0])
            self._raw_pickle_state = state
        elif isinstance(state, (set, list, tuple)):
            self.update(state)
            self._raw_pickle_state = state
        elif isinstance(state, dict):
            self.__dict__.update(state)
        else:
            self._raw_pickle_state = state

    def __getstate__(self):
        raw = self.__dict__.get("_raw_pickle_state", _NO_RAW_STATE)
        if raw is not _NO_RAW_STATE:
            return raw
        state = dict(self.__dict__)
        state.pop("_raw_pickle_state", None)
        return state


class RenpyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        try:
            return super().find_class(module, name)
        except Exception:
            return self._get_or_create_surrogate(module, name)

    @staticmethod
    def _get_or_create_surrogate(module_name, class_name):
        parts = module_name.split(".")
        for i in range(1, len(parts) + 1):
            pkg_name = ".".join(parts[:i])
            if pkg_name not in sys.modules:
                mod = types.ModuleType(pkg_name)
                sys.modules[pkg_name] = mod
                if i > 1:
                    parent_name = ".".join(parts[: i - 1])
                    setattr(sys.modules[parent_name], parts[i - 1], mod)

        target_module = sys.modules[module_name]
        if hasattr(target_module, class_name):
            return getattr(target_module, class_name)

        if class_name in ("RevertableDict", "OrderedDict"):
            base_cls = RevertableDict
        elif class_name in ("RevertableList", "CompressedList"):
            base_cls = RevertableList
        elif class_name == "RevertableSet":
            base_cls = RevertableSet
        else:
            base_cls = RenpyDummyObject

        surrogate_cls = type(class_name, (base_cls,), {"__module__": module_name})
        setattr(target_module, class_name, surrogate_cls)
        return surrogate_cls


# ==============================================================================
# 3. MOTOR DE DETECCAO AUTOMATICA EM 7 CAMADAS (.SAVE, .DAT, .SAV, .RPGSAVE...)
# ==============================================================================

class UniversalSaveBackend:
    """
    Detecta automaticamente a estrutura real de qualquer arquivo .save, .dat, .sav,
    .rpgsave, .rmmzsave, persistent ou .json analisando a assinatura de bytes.
    """
    def __init__(self):
        self.filepath = None
        self.file_format = None
        self.compression_mode = "none"  # 'none', 'zlib', 'gzip', 'raw_deflate'
        self.text_encoding = "utf-8"
        self.json_prefix = b""
        self.json_suffix = b""
        self.root_container = None
        self.renpy_rollback = None
        self.raw_binary = None
        self.ini_lines = []
        self.zip_inner_files = {}
        self.entries = {}
        self.favorites = set()
        self.lz = lzstring.LZString() if HAS_LZSTRING else None

    def load_file(self, path_str):
        filepath = Path(path_str)
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo n\u00e3o encontrado: {filepath}")

        backup_path = filepath.with_suffix(filepath.suffix + ".bak")
        if not backup_path.exists():
            try:
                shutil.copy2(filepath, backup_path)
            except Exception:
                pass

        raw_bytes = filepath.read_bytes()
        if not raw_bytes:
            raise ValueError("O arquivo selecionado est\u00e1 vazio (0 bytes).")

        self._reset_state()
        self.filepath = filepath

        # Deteccao automatica em 7 camadas
        self._auto_detect_and_parse(filepath, raw_bytes)
        self._build_flat_index()

        # Se mesmo apos abrir um formato estruturado houver 0 variaveis simples,
        # ativar o inspetor binario/texto como fallback para nunca ficar vazio
        if not self.entries and raw_bytes:
            self._parse_as_smart_binary(raw_bytes)
            self._build_flat_index()

        return len(self.entries)

    def _reset_state(self):
        self.file_format = None
        self.compression_mode = "none"
        self.text_encoding = "utf-8"
        self.json_prefix = b""
        self.json_suffix = b""
        self.root_container = None
        self.renpy_rollback = None
        self.raw_binary = None
        self.ini_lines = []
        self.zip_inner_files = {}
        self.entries.clear()

    def _auto_detect_and_parse(self, filepath, raw_bytes):
        # ------------------------------------------------------------------
        # CAMADA 1: ARQUIVO ZIP (Ren'Py .save ou ZIP contendo JSON/Pickle/INI)
        # ------------------------------------------------------------------
        if raw_bytes[:4] == b"PK\x03\x04" or zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, "r") as zf:
                names = zf.namelist()
                if "log" in names:
                    raw_log = zf.read("log")
                    log_bytes, _ = self._try_decompress_bytes(raw_log)
                    unpickler = RenpyUnpickler(io.BytesIO(log_bytes), encoding="latin1")
                    data = unpickler.load()
                    if isinstance(data, tuple) and len(data) == 2:
                        self.root_container, self.renpy_rollback = data
                    else:
                        self.root_container = data
                        self.renpy_rollback = None
                    self.file_format = "renpy_zip"
                    return
                else:
                    # ZIP generico contendo saves em JSON ou texto (.save / .dat compactado)
                    parsed_zip = {}
                    for name in names:
                        if name.endswith("/"):
                            continue
                        inner_bytes = zf.read(name)
                        dec_bytes, _ = self._try_decompress_bytes(inner_bytes)
                        obj = self._try_parse_json_bytes(dec_bytes)
                        if obj is not None:
                            parsed_zip[name] = obj
                    if parsed_zip:
                        self.root_container = parsed_zip
                        self.file_format = "zip_json"
                        return

        # ------------------------------------------------------------------
        # CAMADA 2: DESCOMPRESSAO AUTOMATICA (Zlib, Gzip, Raw Deflate)
        # ------------------------------------------------------------------
        payload_bytes, comp_mode = self._try_decompress_bytes(raw_bytes)
        self.compression_mode = comp_mode

        # ------------------------------------------------------------------
        # CAMADA 3: PYTHON PICKLE DIRETO (Ren'Py persistent, .dat / .save em Pickle)
        # ------------------------------------------------------------------
        if self._looks_like_pickle(payload_bytes):
            try:
                unpickler = RenpyUnpickler(io.BytesIO(payload_bytes), encoding="latin1")
                data = unpickler.load()
                if isinstance(data, tuple) and len(data) == 2 and isinstance(data[0], dict):
                    self.root_container, self.renpy_rollback = data
                    self.file_format = "pickle_renpy_tuple"
                else:
                    self.root_container = data
                    self.file_format = "pickle_raw"
                return
            except Exception:
                pass

        # ------------------------------------------------------------------
        # CAMADA 4: JSON PURO, MULTI-LINE JSON (NDJSON) OU JSON COM CABECALHO (.dat/.save)
        # ------------------------------------------------------------------
        json_res = self._try_parse_json_flexible(payload_bytes)
        if json_res is not None:
            obj, fmt_kind, enc, prefix_b, suffix_b = json_res
            self.root_container = obj
            self.file_format = fmt_kind  # 'json', 'ndjson', 'header_json'
            self.text_encoding = enc
            self.json_prefix = prefix_b
            self.json_suffix = suffix_b
            return

        # ------------------------------------------------------------------
        # CAMADA 5: BASE64 / LZSTRING (.rpgsave, .dat, .save codificados)
        # ------------------------------------------------------------------
        b64_res = self._try_parse_base64_or_lzstring(payload_bytes)
        if b64_res is not None:
            obj, b64_fmt = b64_res
            self.root_container = obj
            self.file_format = b64_fmt  # 'rpgmv', 'base64_json', 'base64_zlib_json'
            return

        # ------------------------------------------------------------------
        # CAMADA 6: FORMATO INI / CHAVE=VALOR (.dat, .save, .sav, .ini)
        # ------------------------------------------------------------------
        ini_res = self._try_parse_ini_kv(payload_bytes)
        if ini_res is not None:
            self.root_container, self.ini_lines, self.text_encoding = ini_res
            self.file_format = "ini_kv"
            return

        # ------------------------------------------------------------------
        # CAMADA 7: INSPETOR BINARIO INTELIGENTE (.dat / .save Binario Puro)
        # ------------------------------------------------------------------
        self._parse_as_smart_binary(payload_bytes)

    @staticmethod
    def _try_decompress_bytes(raw_bytes):
        # 1. Gzip (\x1f\x8b)
        if raw_bytes[:2] == b"\x1f\x8b":
            try:
                return gzip.decompress(raw_bytes), "gzip"
            except Exception:
                pass

        # 2. Zlib padrao (\x78\x01, \x78\x5e, \x78\x9c, \x78\xda)
        if len(raw_bytes) > 2 and raw_bytes[0] == 0x78 and raw_bytes[1] in (0x01, 0x5E, 0x9C, 0xDA):
            try:
                return zlib.decompress(raw_bytes), "zlib"
            except Exception:
                pass

        # 3. Tentativa geral Zlib / Raw Deflate (para .rmmzsave, persistent, .dat)
        try:
            return zlib.decompress(raw_bytes), "zlib"
        except Exception:
            pass

        try:
            dec = zlib.decompress(raw_bytes, -zlib.MAX_WBITS)
            if len(dec) > 4:
                return dec, "raw_deflate"
        except Exception:
            pass

        return raw_bytes, "none"

    @staticmethod
    def _looks_like_pickle(data_bytes):
        if len(data_bytes) < 2:
            return False
        # Protocolos 2, 3, 4, 5 comecam com 0x80 seguido de 2..5
        if data_bytes[0] == 0x80 and data_bytes[1] in (2, 3, 4, 5):
            return True
        # Protocolo 0/1 em texto
        if data_bytes.startswith((b"(dp", b"ccopy_reg", b"c__builtin__", b"crenpy", b"}q", b"]q")):
            return True
        return False

    @staticmethod
    def _try_parse_json_bytes(data_bytes):
        for enc in ("utf-8-sig", "utf-8", "utf-16", "latin-1"):
            try:
                txt = data_bytes.decode(enc).strip("\x00 \t\r\n")
                if txt.startswith(("{", "[")):
                    return json.loads(txt)
            except Exception:
                continue
        return None

    def _try_parse_json_flexible(self, data_bytes):
        for enc in ("utf-8-sig", "utf-8", "utf-16"):
            try:
                text = data_bytes.decode(enc)
            except UnicodeDecodeError:
                continue

            clean = text.strip("\x00 \t\r\n")
            if not clean:
                continue

            # Caso 4A: JSON padrao direto
            if clean.startswith(("{", "[")):
                try:
                    obj = json.loads(clean)
                    return obj, "json", enc, b"", b""
                except json.JSONDecodeError:
                    # Caso 4B: Multi-Line JSON (NDJSON - muito comum em saves .dat e .save da Unity/GameMaker)
                    lines = [ln.strip("\x00 \t\r") for ln in clean.splitlines() if ln.strip("\x00 \t\r")]
                    if len(lines) > 1 and all(ln.startswith(("{", "[")) for ln in lines):
                        try:
                            parsed_lines = {f"line_{i}": json.loads(ln) for i, ln in enumerate(lines)}
                            return parsed_lines, "ndjson", enc, b"", b""
                        except Exception:
                            pass

        # Caso 4C: Arquivo .dat / .save com pequeno cabecalho binario (ex: 4 a 64 bytes) antes do JSON
        first_brace = data_bytes.find(b"{")
        last_brace = data_bytes.rfind(b"}")
        if 0 < first_brace <= 128 and last_brace > first_brace:
            prefix = data_bytes[:first_brace]
            suffix = data_bytes[last_brace + 1:]
            core_bytes = data_bytes[first_brace:last_brace + 1]
            try:
                obj = json.loads(core_bytes.decode("utf-8"))
                return obj, "header_json", "utf-8", prefix, suffix
            except Exception:
                pass

        return None

    def _try_parse_base64_or_lzstring(self, data_bytes):
        try:
            text = data_bytes.decode("utf-8").strip().strip("\x00")
        except UnicodeDecodeError:
            return None

        if not text or len(text) < 8:
            return None

        # 1. Tentar LZString Base64 (RPG Maker MV .rpgsave e jogos web .save / .dat)
        if HAS_LZSTRING and self.lz:
            try:
                lz_dec = self.lz.decompressFromBase64(text)
                if lz_dec and lz_dec.strip().startswith(("{", "[")):
                    return json.loads(lz_dec), "rpgmv"
            except Exception:
                pass

        # 2. Tentar Base64 padrao (muito usado em saves .dat e .save de jogos Indie/Unity)
        compact_text = "".join(text.split())
        if len(compact_text) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/=_-]+", compact_text):
            try:
                b64_bytes = base64.b64decode(compact_text)
                dec_b64, comp_kind = self._try_decompress_bytes(b64_bytes)
                obj = self._try_parse_json_bytes(dec_b64)
                if obj is not None:
                    fmt = "base64_zlib_json" if comp_kind != "none" else "base64_json"
                    return obj, fmt
            except Exception:
                pass

        return None

    @staticmethod
    def _try_parse_ini_kv(data_bytes):
        # Verificar se parece texto legivel sem excesso de bytes nulos
        if b"\x00\x00" in data_bytes[:256]:
            return None

        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                text = data_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            return None

        lines = text.splitlines()
        if not lines:
            return None

        kv_data = {}
        parsed_lines = []
        current_section = "root"
        kv_count = 0

        section_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
        kv_re = re.compile(r"^(\s*([A-Za-z0-9_.\-]+)\s*([=:])\s*)(.*)$")

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";", "//")):
                parsed_lines.append(("raw", line))
                continue

            sec_match = section_re.match(line)
            if sec_match:
                current_section = sec_match.group(1).strip()
                if current_section not in kv_data:
                    kv_data[current_section] = {}
                parsed_lines.append(("raw", line))
                continue

            kv_match = kv_re.match(line)
            if kv_match:
                prefix_part, key_name, _sep, raw_val = kv_match.groups()
                val_clean = raw_val.strip()
                quote_char = ""
                if len(val_clean) >= 2 and val_clean[0] == val_clean[-1] and val_clean[0] in ('"', "'"):
                    quote_char = val_clean[0]
                    inner_v = val_clean[1:-1]
                    typed_v = inner_v
                elif val_clean.lower() in ("true", "false"):
                    typed_v = (val_clean.lower() == "true")
                else:
                    try:
                        if "." in val_clean:
                            typed_v = float(val_clean)
                        else:
                            typed_v = int(val_clean)
                    except ValueError:
                        typed_v = val_clean

                if current_section not in kv_data:
                    kv_data[current_section] = {}
                kv_data[current_section][key_name] = typed_v
                parsed_lines.append(("kv", current_section, key_name, prefix_part, quote_char))
                kv_count += 1
            else:
                parsed_lines.append(("raw", line))

        if kv_count >= 1:
            return kv_data, parsed_lines, enc
        return None

    def _parse_as_smart_binary(self, data_bytes):
        """
        Analisador para arquivos .dat / .save em binario puro (Unreal GVAS, Unity, C++, etc.).
        Extrai chaves identificadoras + valores proximos, textos legiveis e inteiros de 32 bits.
        """
        self.file_format = "binary_dat"
        self.raw_binary = bytearray(data_bytes)
        self.root_container = {}

        # 1. Procurar strings legiveis (ASCII >= 4 chars) e valores numericos adjacentes
        ascii_pattern = re.compile(rb"[A-Za-z_][A-Za-z0-9_.\-]{2,40}")
        found_strings = 0
        for match in ascii_pattern.finditer(data_bytes):
            start, end = match.span()
            raw_s = match.group(0)
            try:
                s_val = raw_s.decode("ascii")
            except Exception:
                continue

            # Verificar se logo apos a string (alinhado ou apos null byte) existe um int32 plausivel
            probe_pos = end
            while probe_pos < len(data_bytes) and probe_pos < end + 8 and data_bytes[probe_pos] == 0:
                probe_pos += 1

            if probe_pos + 4 <= len(data_bytes):
                val_i32 = struct.unpack_from("<i", data_bytes, probe_pos)[0]
                if -1000000 <= val_i32 <= 999999999:
                    key_label = f"bin.{s_val}_[0x{probe_pos:04X}]"
                    self.entries[key_label] = {
                        "steps": [("binary_int32", probe_pos)],
                        "value": val_i32,
                        "orig_value": val_i32,
                        "orig_type": int,
                        "modified": False,
                    }

            if found_strings < 400 and len(s_val) >= 4:
                str_key = f"str.[0x{start:04X}]_{s_val[:18]}"
                self.entries[str_key] = {
                    "steps": [("binary_str", (start, len(raw_s)))],
                    "value": s_val,
                    "orig_value": s_val,
                    "orig_type": str,
                    "modified": False,
                }
                found_strings += 1

        # 2. Mapear inteiros de 32 bits (int32) alinhados de 4 em 4 bytes (ate 1500 entradas)
        max_scan = min(len(data_bytes) - 3, 6000)
        for offset in range(0, max_scan, 4):
            val_i32 = struct.unpack_from("<i", data_bytes, offset)[0]
            if 0 < val_i32 <= 99999999:
                k_name = f"int32.[0x{offset:04X}]"
                if k_name not in self.entries:
                    self.entries[k_name] = {
                        "steps": [("binary_int32", offset)],
                        "value": val_i32,
                        "orig_value": val_i32,
                        "orig_type": int,
                        "modified": False,
                    }

    # ---------------- INDEXACAO EM ARVORE PROFUNDA ----------------

    def _build_flat_index(self):
        if self.file_format == "binary_dat":
            return

        self.entries.clear()
        visited = set()

        def walk(node, steps, display_prefix, depth):
            if depth > 14:
                return

            if isinstance(node, (int, float, bool, str)):
                key_name = display_prefix if display_prefix else "value"
                self.entries[key_name] = {
                    "steps": steps,
                    "value": node,
                    "orig_value": node,
                    "orig_type": type(node),
                    "modified": False,
                }
                return

            node_id = id(node)
            if node_id in visited:
                return
            visited.add(node_id)

            if isinstance(node, dict):
                for k, v in node.items():
                    if not isinstance(k, (str, int)):
                        continue
                    k_str = str(k)
                    if display_prefix:
                        next_disp = f"{display_prefix}.{k_str}" if k_str.isidentifier() else f"{display_prefix}[{k_str!r}]"
                    else:
                        next_disp = k_str
                    walk(v, steps + [("dict", k)], next_disp, depth + 1)

            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    next_disp = f"{display_prefix}[{idx}]" if display_prefix else f"[{idx}]"
                    walk(item, steps + [("list", idx)], next_disp, depth + 1)

            elif isinstance(node, tuple):
                for idx, item in enumerate(node):
                    # Dentro de tuplas, objetos mutaveis (dicts/lists/objetos) podem ser editados
                    if isinstance(item, (dict, list, RenpyDummyObject)):
                        next_disp = f"{display_prefix}({idx})" if display_prefix else f"({idx})"
                        walk(item, steps + [("tuple", idx)], next_disp, depth + 1)

            if isinstance(node, RenpyDummyObject) or hasattr(node, "__dict__"):
                obj_dict = getattr(node, "__dict__", {})
                for attr, val in obj_dict.items():
                    if attr in ("_raw_pickle_state", "_pickle_list_items", "_pickle_dict_items") or attr.startswith("__"):
                        continue
                    next_disp = f"{display_prefix}.{attr}" if display_prefix else attr
                    walk(val, steps + [("attr", attr)], next_disp, depth + 1)

                # Inspecionar tambem estados guardados em _raw_pickle_state (ex: objetos com __slots__ ou tuplas)
                raw_st = obj_dict.get("_raw_pickle_state", _NO_RAW_STATE)
                if raw_st is not _NO_RAW_STATE and isinstance(raw_st, (dict, list, tuple)):
                    walk(raw_st, steps + [("raw_state", None)], display_prefix, depth + 1)

                # Inspecionar itens adicionados via SETITEMS ou APPENDS em classes customizadas
                dict_items = obj_dict.get("_pickle_dict_items")
                if isinstance(dict_items, dict):
                    walk(dict_items, steps + [("pickle_dict", None)], display_prefix, depth + 1)

                list_items = obj_dict.get("_pickle_list_items")
                if isinstance(list_items, list):
                    walk(list_items, steps + [("pickle_list", None)], display_prefix, depth + 1)

        if self.file_format in ("renpy_zip", "pickle_renpy_tuple") and isinstance(self.root_container, dict):
            # 1. Mapear variaveis store.* limpando o prefixo
            for key, val in self.root_container.items():
                if not isinstance(key, str):
                    continue
                short_name = key[6:] if key.startswith("store.") else key
                if short_name.startswith("__"):
                    continue
                walk(val, [("dict", key)], short_name, 0)
        else:
            walk(self.root_container, [], "", 0)

    def _write_to_container(self, steps, typed_value):
        if not steps:
            self.root_container = typed_value
            return

        first_kind, first_arg = steps[0]
        if first_kind == "binary_int32":
            struct.pack_into("<i", self.raw_binary, first_arg, int(typed_value))
            return
        elif first_kind == "binary_str":
            offset, max_len = first_arg
            encoded = str(typed_value).encode("ascii", errors="replace")[:max_len]
            padded = encoded.ljust(max_len, b"\x00")
            self.raw_binary[offset:offset + max_len] = padded
            return

        target = self.root_container
        for step_kind, step_key in steps[:-1]:
            if step_kind in ("dict", "list", "tuple"):
                target = target[step_key]
            elif step_kind == "attr":
                target = target.__dict__[step_key]
            elif step_kind == "raw_state":
                target = target._raw_pickle_state
            elif step_kind == "pickle_dict":
                target = target._pickle_dict_items
            elif step_kind == "pickle_list":
                target = target._pickle_list_items

        last_kind, last_key = steps[-1]
        if last_kind in ("dict", "list"):
            target[last_key] = typed_value
        elif last_kind == "attr":
            target.__dict__[last_key] = typed_value

    def update_entry(self, display_path, raw_new_value):
        if display_path not in self.entries:
            raise KeyError(f"Variable '{display_path}' not found.")

        entry = self.entries[display_path]
        orig_type = entry["orig_type"]

        if orig_type is bool:
            if isinstance(raw_new_value, bool):
                typed_value = raw_new_value
            else:
                lowered = str(raw_new_value).strip().lower()
                if lowered in ("true", "1", "sim", "yes", "verdadeiro", "on"):
                    typed_value = True
                elif lowered in ("false", "0", "nao", "n\u00e3o", "no", "falso", "off"):
                    typed_value = False
                else:
                    raise ValueError("Use True / False.")
        elif orig_type is int:
            typed_value = int(float(str(raw_new_value).strip()))
        elif orig_type is float:
            typed_value = float(str(raw_new_value).strip().replace(",", "."))
        else:
            typed_value = str(raw_new_value)

        self._write_to_container(entry["steps"], typed_value)
        entry["value"] = typed_value
        entry["modified"] = (typed_value != entry["orig_value"])
        return typed_value

    def revert_single_entry(self, display_path):
        if display_path not in self.entries:
            return None
        entry = self.entries[display_path]
        orig_val = entry["orig_value"]
        self._write_to_container(entry["steps"], orig_val)
        entry["value"] = orig_val
        entry["modified"] = False
        return orig_val

    def toggle_favorite(self, display_path):
        if display_path in self.favorites:
            self.favorites.remove(display_path)
            return False
        else:
            self.favorites.add(display_path)
            return True

    def count_modified(self):
        return sum(1 for info in self.entries.values() if info["modified"])

    def _apply_compression(self, raw_bytes):
        if self.compression_mode == "gzip":
            return gzip.compress(raw_bytes)
        elif self.compression_mode == "zlib":
            return zlib.compress(raw_bytes)
        elif self.compression_mode == "raw_deflate":
            comp_obj = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
            return comp_obj.compress(raw_bytes) + comp_obj.flush()
        return raw_bytes

    def save_file(self, output_path=None):
        if not self.filepath:
            raise RuntimeError("No save file loaded.")

        target_path = Path(output_path) if output_path else self.filepath
        temp_path = target_path.with_suffix(target_path.suffix + ".tmp")

        if self.file_format == "renpy_zip":
            payload = (self.root_container, self.renpy_rollback) if self.renpy_rollback is not None else self.root_container
            new_log_bytes = pickle.dumps(payload, protocol=2)
            with zipfile.ZipFile(self.filepath, "r") as orig_zip:
                with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as new_zip:
                    for item in orig_zip.infolist():
                        if item.filename in ("log", "signatures"):
                            continue
                        new_zip.writestr(item, orig_zip.read(item.filename))
                    new_zip.writestr("log", new_log_bytes)

        elif self.file_format == "zip_json":
            with zipfile.ZipFile(self.filepath, "r") as orig_zip:
                with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as new_zip:
                    for item in orig_zip.infolist():
                        if item.filename in self.root_container:
                            j_bytes = json.dumps(self.root_container[item.filename], ensure_ascii=False, indent=2).encode("utf-8")
                            new_zip.writestr(item, j_bytes)
                        else:
                            new_zip.writestr(item, orig_zip.read(item.filename))

        elif self.file_format == "pickle_renpy_tuple":
            raw_p = pickle.dumps((self.root_container, self.renpy_rollback), protocol=2)
            temp_path.write_bytes(self._apply_compression(raw_p))

        elif self.file_format == "pickle_raw":
            raw_p = pickle.dumps(self.root_container, protocol=2)
            temp_path.write_bytes(self._apply_compression(raw_p))

        elif self.file_format == "rpgmv":
            json_str = json.dumps(self.root_container, ensure_ascii=False, separators=(",", ":"))
            compressed = self.lz.compressToBase64(json_str)
            temp_path.write_text(compressed, encoding="utf-8")

        elif self.file_format in ("base64_json", "base64_zlib_json"):
            json_bytes = json.dumps(self.root_container, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            if self.file_format == "base64_zlib_json":
                json_bytes = zlib.compress(json_bytes)
            b64_str = base64.b64encode(json_bytes).decode("ascii")
            temp_path.write_text(b64_str, encoding="utf-8")

        elif self.file_format == "ndjson":
            lines = [json.dumps(v, ensure_ascii=False, separators=(",", ":")) for v in self.root_container.values()]
            raw_out = ("\n".join(lines) + "\n").encode(self.text_encoding)
            temp_path.write_bytes(self._apply_compression(raw_out))

        elif self.file_format == "header_json":
            core_b = json.dumps(self.root_container, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            raw_out = self.json_prefix + core_b + self.json_suffix
            temp_path.write_bytes(self._apply_compression(raw_out))

        elif self.file_format == "ini_kv":
            out_lines = []
            for item in self.ini_lines:
                if item[0] == "raw":
                    out_lines.append(item[1])
                else:
                    _, sec, k_name, prefix_part, q_char = item
                    val = self.root_container[sec][k_name]
                    if isinstance(val, bool):
                        val_s = "true" if val else "false"
                    else:
                        val_s = str(val)
                    out_lines.append(f"{prefix_part}{q_char}{val_s}{q_char}")
            raw_out = "\n".join(out_lines).encode(self.text_encoding)
            temp_path.write_bytes(self._apply_compression(raw_out))

        elif self.file_format == "binary_dat":
            temp_path.write_bytes(self._apply_compression(bytes(self.raw_binary)))

        else:
            # JSON padrao (comprimido ou texto puro)
            if self.compression_mode != "none":
                json_str = json.dumps(self.root_container, ensure_ascii=False, separators=(",", ":"))
            else:
                json_str = json.dumps(self.root_container, ensure_ascii=False, indent=2)
            raw_out = json_str.encode(self.text_encoding)
            temp_path.write_bytes(self._apply_compression(raw_out))

        os.replace(temp_path, target_path)
        self.filepath = target_path

        for entry in self.entries.values():
            entry["orig_value"] = entry["value"]
            entry["modified"] = False

    def restore_backup(self):
        if not self.filepath:
            return False
        backup_path = self.filepath.with_suffix(self.filepath.suffix + ".bak")
        if not backup_path.exists():
            return False
        shutil.copy2(backup_path, self.filepath)
        self.load_file(str(self.filepath))
        return True

    def get_human_format_name(self):
        names = {
            "renpy_zip": "Ren'Py (.save ZIP)",
            "zip_json": "ZIP Save Archive",
            "pickle_renpy_tuple": "Ren'Py Pickle",
            "pickle_raw": "Python Pickle (.dat/.save)",
            "rpgmv": "LZString Base64 (RPG Maker)",
            "base64_json": "Base64 JSON (.dat/.save)",
            "base64_zlib_json": "Base64 + Zlib JSON",
            "ndjson": "Multi-Line JSON (.dat/.save)",
            "header_json": "Header + JSON (.dat/.save)",
            "ini_kv": "INI / Key-Value (.dat/.save)",
            "binary_dat": "Binary Save (.dat/.save)",
            "json": "JSON",
        }
        base = names.get(self.file_format, str(self.file_format))
        if self.compression_mode != "none":
            return f"{base} [{self.compression_mode.upper()}]"
        return base


# ==============================================================================
# 4. NAVEGADOR INTELIGENTE DE PASTAS E ATALHOS (COM SUPORTE A .DAT E .SAVE)
# ==============================================================================

class SmartSaveBrowserModal(ctk.CTkToplevel):
    SUPPORTED_EXTS = {
        ".save", ".dat", ".sav", ".rpgsave", ".rmmzsave",
        ".json", ".rvdata2", ".rxdata", ".lsd", ".ini"
    }
    IGNORED_NAMES = {"package.json", "system.json", "tsconfig.json"}

    def __init__(self, parent_app, config_mgr, on_select_callback):
        super().__init__(parent_app)
        self.parent_app = parent_app
        self.config_mgr = config_mgr
        self.on_select_callback = on_select_callback
        self.tr = TRANSLATIONS[self.config_mgr.language]

        self.title(self.tr["modal_title"])
        self.geometry("1080x640")
        self.minsize(920, 520)
        self.transient(parent_app)
        self.grab_set()

        self.current_folder = None
        self.discovered_files = []

        self._build_ui()
        self._populate_left_shortcuts()
        self.run_smart_scan()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=52, corner_radius=8)
        self.top_bar.grid(row=0, column=0, columnspan=2, padx=12, pady=(12, 6), sticky="ew")
        self.top_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.top_bar,
            text=self.tr["modal_loc"],
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=(12, 6), pady=10)

        self.path_var = tk.StringVar(value=self.tr["modal_smart_scan_title"])
        self.entry_path = ctk.CTkEntry(
            self.top_bar,
            textvariable=self.path_var,
            height=34,
            font=ctk.CTkFont(size=12)
        )
        self.entry_path.grid(row=0, column=1, padx=6, pady=10, sticky="ew")
        self.entry_path.bind("<Return>", lambda _: self._open_typed_path())

        self.btn_go_path = ctk.CTkButton(
            self.top_bar,
            text=self.tr["modal_btn_go"],
            width=50,
            height=34,
            command=self._open_typed_path
        )
        self.btn_go_path.grid(row=0, column=2, padx=4, pady=10)

        self.btn_browse_os = ctk.CTkButton(
            self.top_bar,
            text=self.tr["modal_btn_pick_folder"],
            width=135,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=self.action_pick_custom_folder
        )
        self.btn_browse_os.grid(row=0, column=3, padx=4, pady=10)

        self.btn_pin_current = ctk.CTkButton(
            self.top_bar,
            text=self.tr["modal_btn_pin"],
            width=185,
            height=34,
            fg_color="#ca8a04",
            hover_color="#a16207",
            font=ctk.CTkFont(weight="bold"),
            command=self.action_pin_current_folder
        )
        self.btn_pin_current.grid(row=0, column=4, padx=(4, 12), pady=10)

        self.left_panel = ctk.CTkScrollableFrame(
            self,
            width=285,
            corner_radius=8,
            label_text=self.tr["modal_left_header"],
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.left_panel.grid(row=1, column=0, padx=(12, 6), pady=6, sticky="nsew")
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.right_panel = ctk.CTkFrame(self, corner_radius=8)
        self.right_panel.grid(row=1, column=1, padx=(6, 12), pady=6, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        self.search_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=10, pady=(10, 6), sticky="ew")
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._refresh_file_tree())

        self.entry_filter = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.filter_var,
            placeholder_text=self.tr["modal_filter_ph"],
            height=34
        )
        self.entry_filter.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.chk_hide_meta_var = tk.BooleanVar(value=True)
        self.chk_hide_meta = ctk.CTkCheckBox(
            self.search_frame,
            text=self.tr["modal_chk_hide_meta"],
            variable=self.chk_hide_meta_var,
            font=ctk.CTkFont(size=12),
            command=self._refresh_file_tree
        )
        self.chk_hide_meta.grid(row=0, column=1, padx=6)

        self.tree_container = ctk.CTkFrame(self.right_panel, corner_radius=6)
        self.tree_container.grid(row=1, column=0, padx=10, pady=4, sticky="nsew")
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

        cols = ("jogo", "ficheiro", "formato", "modificado", "tamanho")
        self.file_tree = ttk.Treeview(
            self.tree_container,
            columns=cols,
            show="headings",
            selectmode="browse"
        )
        self.file_tree.heading("jogo", text=self.tr["modal_col_game"])
        self.file_tree.heading("ficheiro", text=self.tr["modal_col_file"])
        self.file_tree.heading("formato", text=self.tr["modal_col_type"])
        self.file_tree.heading("modificado", text=self.tr["modal_col_mod"])
        self.file_tree.heading("tamanho", text=self.tr["modal_col_size"])

        self.file_tree.column("jogo", width=230, anchor="w")
        self.file_tree.column("ficheiro", width=180, anchor="w")
        self.file_tree.column("formato", width=90, anchor="center")
        self.file_tree.column("modificado", width=175, anchor="center")
        self.file_tree.column("tamanho", width=85, anchor="e")

        sb_y = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=sb_y.set)

        self.file_tree.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)
        sb_y.grid(row=0, column=1, sticky="ns", pady=2, padx=(0, 2))

        self.file_tree.bind("<Double-1>", lambda _: self.action_confirm_selection())
        self.file_tree.tag_configure("recent_top", foreground="#4ade80")
        self.file_tree.tag_configure("even", background="#1e293b")
        self.file_tree.tag_configure("odd", background="#243247")

        self.bottom_bar = ctk.CTkFrame(self, height=50, corner_radius=8)
        self.bottom_bar.grid(row=2, column=0, columnspan=2, padx=12, pady=(6, 12), sticky="ew")
        self.bottom_bar.grid_columnconfigure(1, weight=1)

        self.lbl_count = ctk.CTkLabel(
            self.bottom_bar,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lbl_count.grid(row=0, column=0, padx=14, pady=10, sticky="w")

        self.btn_manual_file = ctk.CTkButton(
            self.bottom_bar,
            text=self.tr["modal_btn_win_file"],
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            command=self.action_fallback_filedialog
        )
        self.btn_manual_file.grid(row=0, column=2, padx=6, pady=8)

        self.btn_open_explorer = ctk.CTkButton(
            self.bottom_bar,
            text=self.tr["modal_btn_explorer"],
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            command=self.action_open_selected_in_explorer
        )
        self.btn_open_explorer.grid(row=0, column=3, padx=6, pady=8)

        self.btn_open_save = ctk.CTkButton(
            self.bottom_bar,
            text=self.tr["modal_btn_load"],
            height=36,
            fg_color="#16a34a",
            hover_color="#15803d",
            font=ctk.CTkFont(weight="bold"),
            command=self.action_confirm_selection
        )
        self.btn_open_save.grid(row=0, column=4, padx=(6, 12), pady=8)

    def _populate_left_shortcuts(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        row_idx = 0

        btn_scan = ctk.CTkButton(
            self.left_panel,
            text=self.tr["modal_btn_quick_scan"],
            height=36,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(weight="bold"),
            anchor="w",
            command=self.run_smart_scan
        )
        btn_scan.grid(row=row_idx, column=0, padx=4, pady=(2, 10), sticky="ew")
        row_idx += 1

        ctk.CTkLabel(
            self.left_panel,
            text=self.tr["modal_sec_pinned"],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#facc15"
        ).grid(row=row_idx, column=0, padx=6, pady=(6, 2), sticky="w")
        row_idx += 1

        if not self.config_mgr.pinned_folders:
            ctk.CTkLabel(
                self.left_panel,
                text=self.tr["modal_no_pinned"],
                font=ctk.CTkFont(size=11),
                text_color="#64748b",
                justify="left"
            ).grid(row=row_idx, column=0, padx=8, pady=(0, 8), sticky="w")
            row_idx += 1
        else:
            for pinned in self.config_mgr.pinned_folders:
                p_obj = Path(pinned)
                item_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
                item_frame.grid(row=row_idx, column=0, padx=2, pady=2, sticky="ew")
                item_frame.grid_columnconfigure(0, weight=1)

                b_open = ctk.CTkButton(
                    item_frame,
                    text=f"* {p_obj.name}",
                    height=30,
                    fg_color="#1e293b",
                    hover_color="#334155",
                    anchor="w",
                    command=lambda p=p_obj: self.scan_single_directory(p)
                )
                b_open.grid(row=0, column=0, sticky="ew", padx=(0, 2))

                b_del = ctk.CTkButton(
                    item_frame,
                    text="X",
                    width=28,
                    height=30,
                    fg_color="#7f1d1d",
                    hover_color="#991b1b",
                    command=lambda p=pinned: self._unpin_folder(p)
                )
                b_del.grid(row=0, column=1)
                row_idx += 1

        ctk.CTkLabel(
            self.left_panel,
            text=self.tr["modal_sec_system"],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#38bdf8"
        ).grid(row=row_idx, column=0, padx=6, pady=(12, 2), sticky="w")
        row_idx += 1

        for label, sys_path in self.config_mgr.get_system_shortcuts(self.tr):
            btn = ctk.CTkButton(
                self.left_panel,
                text=label,
                height=30,
                fg_color="#334155",
                hover_color="#475569",
                anchor="w",
                command=lambda p=sys_path: self.scan_single_directory(p)
            )
            btn.grid(row=row_idx, column=0, padx=4, pady=2, sticky="ew")
            row_idx += 1

        renpy_base = self._get_renpy_root()
        if renpy_base and renpy_base.exists():
            subfolders = []
            try:
                subfolders = sorted(
                    [d for d in renpy_base.iterdir() if d.is_dir() and not d.name.startswith(".")],
                    key=lambda d: d.stat().st_mtime,
                    reverse=True
                )
            except Exception:
                pass

            if subfolders:
                ctk.CTkLabel(
                    self.left_panel,
                    text=self.tr["modal_sec_renpy"],
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#a855f7"
                ).grid(row=row_idx, column=0, padx=6, pady=(12, 2), sticky="w")
                row_idx += 1

                for game_dir in subfolders[:25]:
                    btn_game = ctk.CTkButton(
                        self.left_panel,
                        text=game_dir.name[:30],
                        height=28,
                        fg_color="#1e293b",
                        hover_color="#334155",
                        anchor="w",
                        font=ctk.CTkFont(size=12),
                        command=lambda p=game_dir: self.scan_single_directory(p)
                    )
                    btn_game.grid(row=row_idx, column=0, padx=4, pady=2, sticky="ew")
                    row_idx += 1

    @staticmethod
    def _get_renpy_root():
        system = platform.system()
        if system == "Windows":
            appdata = os.environ.get("APPDATA", "")
            if appdata:
                return Path(appdata) / "RenPy"
        elif system == "Darwin":
            return Path.home() / "Library" / "RenPy"
        else:
            return Path.home() / ".renpy"
        return None

    def _unpin_folder(self, folder_str):
        self.config_mgr.remove_pinned_folder(folder_str)
        self._populate_left_shortcuts()

    def action_pin_current_folder(self):
        if not self.current_folder or not self.current_folder.exists():
            messagebox.showinfo(
                self.tr["modal_msg_sel_folder_title"],
                self.tr["modal_msg_sel_folder_body"],
                parent=self
            )
            return
        if self.config_mgr.add_pinned_folder(str(self.current_folder)):
            self._populate_left_shortcuts()
            messagebox.showinfo(
                self.tr["msg_pin_title"],
                self.tr["msg_pin_added"].format(name=self.current_folder.name),
                parent=self
            )
        else:
            messagebox.showinfo(
                self.tr["msg_pin_exists_title"],
                self.tr["msg_pin_exists"],
                parent=self
            )

    def action_pick_custom_folder(self):
        initial = str(self.current_folder) if self.current_folder else str(Path.home())
        folder = filedialog.askdirectory(parent=self, initialdir=initial, title=self.tr["modal_btn_pick_folder"])
        if folder:
            self.scan_single_directory(Path(folder), max_depth=4)

    def _open_typed_path(self):
        raw = self.path_var.get().strip()
        p = Path(raw)
        if p.exists() and p.is_dir():
            self.scan_single_directory(p, max_depth=4)
        elif p.exists() and p.is_file():
            self.destroy()
            self.on_select_callback(str(p))
        else:
            messagebox.showwarning(
                self.tr["modal_msg_invalid_path_title"],
                self.tr["modal_msg_invalid_path_body"].format(path=raw),
                parent=self
            )

    def run_smart_scan(self):
        self.current_folder = None
        self.path_var.set(self.tr["modal_smart_scan_title"])
        self.discovered_files.clear()
        seen_paths = set()

        for rec in self.config_mgr.recent_files:
            rp = Path(rec)
            if rp.exists() and rp.is_file():
                self._add_file_entry(rp, seen_paths, prefix_tag=self.tr["modal_recent_tag"])

        for pinned in self.config_mgr.pinned_folders:
            pp = Path(pinned)
            if pp.exists():
                self._walk_directory_fast(pp, seen_paths, max_depth=3)

        renpy_root = self._get_renpy_root()
        if renpy_root and renpy_root.exists():
            self._walk_directory_fast(renpy_root, seen_paths, max_depth=2)

        saved_games = Path.home() / "Saved Games"
        if saved_games.exists():
            self._walk_directory_fast(saved_games, seen_paths, max_depth=3)

        my_games = Path.home() / "Documents" / "My Games"
        if my_games.exists():
            self._walk_directory_fast(my_games, seen_paths, max_depth=3)

        if platform.system() == "Windows":
            localappdata = os.environ.get("LOCALAPPDATA", "")
            if localappdata:
                locallow = Path(localappdata).parent / "LocalLow"
                if locallow.exists():
                    self._walk_directory_fast(locallow, seen_paths, max_depth=3)

        self.discovered_files.sort(key=lambda item: item["mtime"], reverse=True)
        self._refresh_file_tree()

    def scan_single_directory(self, folder_path, max_depth=3):
        self.current_folder = folder_path
        self.path_var.set(str(folder_path))
        self.discovered_files.clear()
        seen_paths = set()

        self._walk_directory_fast(folder_path, seen_paths, max_depth=max_depth)
        self.discovered_files.sort(key=lambda item: item["mtime"], reverse=True)
        self._refresh_file_tree()

    def _walk_directory_fast(self, root_dir, seen_paths, max_depth=3):
        def _recurse(curr_dir, depth):
            if depth > max_depth or len(self.discovered_files) > 1000:
                return
            try:
                for entry in os.scandir(curr_dir):
                    if entry.name.startswith("."):
                        continue
                    if entry.is_file(follow_symlinks=False):
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in self.SUPPORTED_EXTS or entry.name.lower() == "persistent":
                            self._add_file_entry(Path(entry.path), seen_paths)
                    elif entry.is_dir(follow_symlinks=False):
                        low_name = entry.name.lower()
                        if low_name in (
                            "node_modules", "locales", "swiftshader", "cache",
                            "audio", "img", "movies", "js", "fonts", "crashes", "logs"
                        ):
                            continue
                        _recurse(Path(entry.path), depth + 1)
            except (PermissionError, OSError):
                pass

        _recurse(root_dir, 0)

    def _add_file_entry(self, file_path, seen_paths, prefix_tag=""):
        try:
            resolved = str(file_path.resolve())
            if resolved in seen_paths:
                return
            seen_paths.add(resolved)

            stat = file_path.stat()
            ext = file_path.suffix.lower()
            parent_name = file_path.parent.name
            if parent_name.lower() in ("saves", "save", "data") and file_path.parent.parent:
                game_label = f"{file_path.parent.parent.name} / {parent_name}"
            else:
                game_label = parent_name

            fmt_map = {
                ".save": "Save (.save)",
                ".dat": "Data (.dat)",
                ".sav": "Save (.sav)",
                ".rpgsave": "RPG Maker MV",
                ".rmmzsave": "RPG Maker MZ",
                ".json": "JSON",
                ".ini": "INI Config",
            }
            fmt_label = "Ren'Py Persistent" if file_path.name.lower() == "persistent" else fmt_map.get(ext, ext)

            self.discovered_files.append({
                "path": resolved,
                "game": f"{prefix_tag}{game_label}",
                "name": file_path.name,
                "fmt": fmt_label,
                "mtime": stat.st_mtime,
                "size_kb": max(1, int(stat.st_size / 1024)),
            })
        except OSError:
            pass

    def _refresh_file_tree(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        query = self.filter_var.get().strip().lower()
        hide_meta = self.chk_hide_meta_var.get()

        count = 0
        for item in self.discovered_files:
            fname_low = item["name"].lower()
            if hide_meta and fname_low in self.IGNORED_NAMES:
                continue

            if query and (query not in fname_low and query not in item["game"].lower()):
                continue

            dt_str = datetime.fromtimestamp(item["mtime"]).strftime("%Y-%m-%d  %H:%M:%S")
            size_str = f"{item['size_kb']} KB"

            if count < 3:
                tags = ("recent_top", "even" if count % 2 == 0 else "odd")
            else:
                tags = ("even" if count % 2 == 0 else "odd",)

            self.file_tree.insert(
                "",
                "end",
                iid=item["path"],
                values=(item["game"], item["name"], item["fmt"], dt_str, size_str),
                tags=tags
            )
            count += 1

        self.lbl_count.configure(text=self.tr["modal_count_fmt"].format(count=count))

    def action_confirm_selection(self):
        sel = self.file_tree.selection()
        if not sel:
            messagebox.showinfo(
                self.tr["modal_msg_sel_save_title"],
                self.tr["modal_msg_sel_save_body"],
                parent=self
            )
            return
        chosen_path = sel[0]
        self.destroy()
        self.on_select_callback(chosen_path)

    def action_open_selected_in_explorer(self):
        sel = self.file_tree.selection()
        target_dir = None
        if sel:
            target_dir = Path(sel[0]).parent
        elif self.current_folder and self.current_folder.exists():
            target_dir = self.current_folder

        if not target_dir or not target_dir.exists():
            messagebox.showinfo(
                self.tr["modal_msg_open_dir_title"],
                self.tr["modal_msg_open_dir_body"],
                parent=self
            )
            return

        self._open_os_folder(target_dir)

    @staticmethod
    def _open_os_folder(folder_path):
        try:
            if platform.system() == "Windows":
                os.startfile(str(folder_path))
            elif platform.system() == "Darwin":
                os.system(f'open "{folder_path}"')
            else:
                os.system(f'xdg-open "{folder_path}"')
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def action_fallback_filedialog(self):
        start_dir = str(self.current_folder) if self.current_folder else None
        file_path = filedialog.askopenfilename(
            parent=self,
            initialdir=start_dir,
            title=self.tr["dlg_open_title"],
            filetypes=[
                (self.tr["ft_all_saves"], "*.save *.dat *.sav *.rpgsave *.rmmzsave *.json *.ini *persistent*"),
                ("Save / Dat Files", "*.save *.dat *.sav"),
                ("Ren'Py Save", "*.save *persistent*"),
                ("RPG Maker MV/MZ", "*.rpgsave *.rmmzsave"),
                ("JSON / INI", "*.json *.ini"),
                (self.tr["ft_all_files"], "*.*"),
            ]
        )
        if file_path:
            self.destroy()
            self.on_select_callback(file_path)


# ==============================================================================
# 5. JANELA PRINCIPAL DO SAVE EDITOR (COM BOTAO DE TROCA DE IDIOMA PT-BR / EN-US)
# ==============================================================================

class SaveEditorApp(ctk.CTk):
    FILTER_KEYS = ["all", "fav", "mod", "num", "bool", "str"]

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.config_mgr = ShortcutConfigManager()
        self.lang = self.config_mgr.language
        self.tr = TRANSLATIONS[self.lang]

        self.title(self.tr["app_title"])
        self.geometry("1300x760")
        self.minsize(1080, 640)

        self.backend = UniversalSaveBackend()
        self.selected_key = None
        self.sort_col = "variavel"
        self.sort_reverse = False
        self.active_filter_key = "all"
        self._filter_label_to_key = {}
        self._filter_key_to_label = {}

        self._setup_layout()
        self._style_treeview()
        self._bind_shortcuts()
        self.apply_language(self.lang)

    def _bind_shortcuts(self):
        self.bind("<Control-s>", lambda _: self.action_save_file())
        self.bind("<Control-f>", lambda _: self.entry_search.focus_set())
        self.bind("<Control-o>", lambda _: self.action_open_smart_browser())

    def _setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- 1. BARRA LATERAL ESQUERDA ----------------
        self.sidebar = ctk.CTkFrame(self, width=245, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Save Editor",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=18, pady=(16, 2), sticky="w")

        self.sub_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.sub_label.grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        # SELETOR DE IDIOMA (PT-BR | EN-US)
        self.lang_frame = ctk.CTkFrame(self.sidebar, fg_color="#1e293b", corner_radius=8)
        self.lang_frame.grid(row=2, column=0, padx=14, pady=(0, 12), sticky="ew")
        self.lang_frame.grid_columnconfigure(0, weight=1)

        self.lbl_lang = ctk.CTkLabel(
            self.lang_frame,
            text="Idioma / Language:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#cbd5e1"
        )
        self.lbl_lang.grid(row=0, column=0, padx=10, pady=(6, 2), sticky="w")

        self.seg_lang = ctk.CTkSegmentedButton(
            self.lang_frame,
            values=["PT-BR", "EN-US"],
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            selected_color="#2563eb",
            command=self._on_language_button_clicked
        )
        self.seg_lang.set("PT-BR" if self.lang == "pt-BR" else "EN-US")
        self.seg_lang.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="ew")

        self.btn_smart_browser = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.action_open_smart_browser
        )
        self.btn_smart_browser.grid(row=3, column=0, padx=14, pady=4, sticky="ew")

        self.btn_open_classic = ctk.CTkButton(
            self.sidebar,
            text="",
            height=32,
            fg_color="#334155",
            hover_color="#475569",
            command=self.action_open_classic_dialog
        )
        self.btn_open_classic.grid(row=4, column=0, padx=14, pady=4, sticky="ew")

        self.lbl_recent = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#cbd5e1"
        )
        self.lbl_recent.grid(row=5, column=0, padx=16, pady=(8, 2), sticky="w")

        self.recent_var = tk.StringVar(value="")
        self.combo_recent = ctk.CTkOptionMenu(
            self.sidebar,
            variable=self.recent_var,
            values=[""],
            height=32,
            fg_color="#1e293b",
            button_color="#334155",
            command=self.action_open_from_recent_menu
        )
        self.combo_recent.grid(row=6, column=0, padx=14, pady=(0, 8), sticky="ew")

        self.btn_save = ctk.CTkButton(
            self.sidebar,
            text="",
            height=40,
            fg_color="#16a34a",
            hover_color="#15803d",
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled",
            command=self.action_save_file
        )
        self.btn_save.grid(row=7, column=0, padx=14, pady=(6, 4), sticky="ew")

        self.btn_save_as = ctk.CTkButton(
            self.sidebar,
            text="",
            height=32,
            fg_color="#334155",
            hover_color="#475569",
            state="disabled",
            command=self.action_save_as
        )
        self.btn_save_as.grid(row=8, column=0, padx=14, pady=4, sticky="ew")

        self.btn_restore = ctk.CTkButton(
            self.sidebar,
            text="",
            height=32,
            fg_color="#b45309",
            hover_color="#92400e",
            state="disabled",
            command=self.action_restore_backup
        )
        self.btn_restore.grid(row=9, column=0, padx=14, pady=4, sticky="ew")

        self.info_box = ctk.CTkFrame(self.sidebar, fg_color="#1e293b", corner_radius=8)
        self.info_box.grid(row=11, column=0, padx=12, pady=12, sticky="ew")
        self.info_box.grid_columnconfigure(0, weight=1)

        self.lbl_file_info = ctk.CTkLabel(
            self.info_box,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1",
            justify="left",
            wraplength=200
        )
        self.lbl_file_info.grid(row=0, column=0, padx=10, pady=(10, 6), sticky="w")

        self.btn_open_curr_dir = ctk.CTkButton(
            self.info_box,
            text="",
            height=28,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=11),
            state="disabled",
            command=self.action_open_current_folder_os
        )
        self.btn_open_curr_dir.grid(row=1, column=0, padx=10, pady=(2, 4), sticky="ew")

        self.btn_pin_curr_dir = ctk.CTkButton(
            self.info_box,
            text="",
            height=28,
            fg_color="#ca8a04",
            hover_color="#a16207",
            font=ctk.CTkFont(size=11, weight="bold"),
            state="disabled",
            command=self.action_pin_loaded_save_folder
        )
        self.btn_pin_curr_dir.grid(row=2, column=0, padx=10, pady=(2, 10), sticky="ew")

        # ---------------- 2. AREA CENTRAL (PESQUISA + TABELA) ----------------
        self.center_area = ctk.CTkFrame(self, fg_color="transparent")
        self.center_area.grid(row=0, column=1, padx=(14, 8), pady=14, sticky="nsew")
        self.center_area.grid_columnconfigure(0, weight=1)
        self.center_area.grid_rowconfigure(1, weight=1)

        self.filter_bar = ctk.CTkFrame(self.center_area, corner_radius=8)
        self.filter_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.filter_bar.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_table())

        self.entry_search = ctk.CTkEntry(
            self.filter_bar,
            textvariable=self.search_var,
            placeholder_text="",
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.entry_search.grid(row=0, column=0, padx=(10, 6), pady=10, sticky="ew")

        self.btn_clear_search = ctk.CTkButton(
            self.filter_bar,
            text="",
            width=75,
            height=38,
            fg_color="#475569",
            hover_color="#64748b",
            command=self._clear_filters
        )
        self.btn_clear_search.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.seg_filter = ctk.CTkSegmentedButton(
            self.filter_bar,
            values=["Todos"],
            command=self._on_filter_tab_changed,
            height=32
        )
        self.seg_filter.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.table_frame = ctk.CTkFrame(self.center_area, corner_radius=8)
        self.table_frame.grid(row=1, column=0, sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        columns = ("variavel", "tipo", "original", "valor", "estado")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("variavel", command=lambda: self.sort_by_column("variavel"))
        self.tree.heading("tipo", command=lambda: self.sort_by_column("tipo"))
        self.tree.heading("original", command=lambda: self.sort_by_column("original"))
        self.tree.heading("valor", command=lambda: self.sort_by_column("valor"))
        self.tree.heading("estado", command=lambda: self.sort_by_column("estado"))

        self.tree.column("variavel", width=330, anchor="w")
        self.tree.column("tipo", width=75, anchor="center")
        self.tree.column("original", width=130, anchor="w")
        self.tree.column("valor", width=150, anchor="w")
        self.tree.column("estado", width=105, anchor="center")

        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=(2, 0))
        self.scrollbar_y.grid(row=0, column=1, sticky="ns", pady=(2, 0), padx=(0, 2))
        self.scrollbar_x.grid(row=1, column=0, sticky="ew", padx=(2, 0), pady=(0, 2))

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # ---------------- 3. PAINEL INSPETOR DIREITO ----------------
        self.inspector = ctk.CTkFrame(self, width=340, corner_radius=10)
        self.inspector.grid(row=0, column=2, padx=(8, 14), pady=14, sticky="nsew")
        self.inspector.grid_propagate(False)
        self.inspector.grid_columnconfigure(0, weight=1)

        self.lbl_insp_header = ctk.CTkLabel(
            self.inspector,
            text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_insp_header.grid(row=0, column=0, padx=16, pady=(16, 4), sticky="w")

        self.lbl_insp_sub = ctk.CTkLabel(
            self.inspector,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lbl_insp_sub.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="w")

        self.card_var = ctk.CTkFrame(self.inspector, fg_color="#0f172a", corner_radius=8)
        self.card_var.grid(row=2, column=0, padx=14, pady=6, sticky="ew")
        self.card_var.grid_columnconfigure(0, weight=1)

        self.lbl_var_name = ctk.CTkLabel(
            self.card_var,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#38bdf8",
            wraplength=285,
            justify="left"
        )
        self.lbl_var_name.grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")

        self.lbl_var_meta = ctk.CTkLabel(
            self.card_var,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1",
            justify="left",
            wraplength=285
        )
        self.lbl_var_meta.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")

        self.btn_fav = ctk.CTkButton(
            self.inspector,
            text="",
            height=32,
            fg_color="#334155",
            hover_color="#475569",
            state="disabled",
            command=self.action_toggle_favorite
        )
        self.btn_fav.grid(row=3, column=0, padx=14, pady=(4, 12), sticky="ew")

        self.lbl_input_title = ctk.CTkLabel(
            self.inspector,
            text="",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_input_title.grid(row=4, column=0, padx=16, pady=(4, 4), sticky="w")

        self.entry_new_value = ctk.CTkEntry(
            self.inspector,
            placeholder_text="",
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            state="disabled"
        )
        self.entry_new_value.grid(row=5, column=0, padx=14, pady=4, sticky="ew")
        self.entry_new_value.bind("<Return>", lambda _: self.action_apply_value())

        self.btn_apply = ctk.CTkButton(
            self.inspector,
            text="",
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled",
            command=self.action_apply_value
        )
        self.btn_apply.grid(row=6, column=0, padx=14, pady=(6, 12), sticky="ew")

        # Painel Dinamico: Numeros
        self.num_tools_frame = ctk.CTkFrame(self.inspector, fg_color="#1e293b", corner_radius=8)
        self.num_tools_frame.grid(row=7, column=0, padx=14, pady=6, sticky="ew")
        for c in range(3):
            self.num_tools_frame.grid_columnconfigure(c, weight=1)

        self.lbl_quick_num = ctk.CTkLabel(
            self.num_tools_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        )
        self.lbl_quick_num.grid(row=0, column=0, columnspan=3, padx=10, pady=(8, 6), sticky="w")

        quick_deltas = [
            ("-100", -100), ("-10", -10), ("-1", -1),
            ("+1", 1), ("+10", 10), ("+100", 100),
            ("+1000", 1000), ("+10k", 10000), ("x2", "mul2"),
            ("zero", "zero"), ("999", "set999"), ("max", "max")
        ]

        self.btn_zero_ref = None
        self.btn_max_ref = None

        for idx, (label, action) in enumerate(quick_deltas):
            r = (idx // 3) + 1
            c = idx % 3
            btn = ctk.CTkButton(
                self.num_tools_frame,
                text=label,
                height=32,
                fg_color="#334155",
                hover_color="#475569",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda act=action: self.action_quick_number(act)
            )
            btn.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
            if action == "zero":
                self.btn_zero_ref = btn
            elif action == "max":
                self.btn_max_ref = btn

        # Painel Dinamico: Booleanos
        self.bool_tools_frame = ctk.CTkFrame(self.inspector, fg_color="#1e293b", corner_radius=8)
        self.bool_tools_frame.grid(row=8, column=0, padx=14, pady=6, sticky="ew")
        self.bool_tools_frame.grid_columnconfigure(0, weight=1)
        self.bool_tools_frame.grid_columnconfigure(1, weight=1)

        self.lbl_quick_bool = ctk.CTkLabel(
            self.bool_tools_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        )
        self.lbl_quick_bool.grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 6), sticky="w")

        self.btn_bool_true = ctk.CTkButton(
            self.bool_tools_frame,
            text="",
            height=36,
            fg_color="#15803d",
            hover_color="#166534",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.action_set_boolean(True)
        )
        self.btn_bool_true.grid(row=1, column=0, padx=(8, 4), pady=(0, 10), sticky="ew")

        self.btn_bool_false = ctk.CTkButton(
            self.bool_tools_frame,
            text="",
            height=36,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.action_set_boolean(False)
        )
        self.btn_bool_false.grid(row=1, column=1, padx=(4, 8), pady=(0, 10), sticky="ew")

        self.btn_revert_var = ctk.CTkButton(
            self.inspector,
            text="",
            height=34,
            fg_color="#475569",
            hover_color="#64748b",
            state="disabled",
            command=self.action_revert_single
        )
        self.btn_revert_var.grid(row=9, column=0, padx=14, pady=(12, 10), sticky="ew")

        self.num_tools_frame.grid_remove()
        self.bool_tools_frame.grid_remove()

        self.status_bar = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.status_bar.grid(row=1, column=1, columnspan=2, padx=16, pady=(0, 8), sticky="ew")

    # ---------------- SISTEMA DE TROCA DE IDIOMA ----------------

    def _on_language_button_clicked(self, value):
        target_lang = "pt-BR" if value == "PT-BR" else "en-US"
        self.apply_language(target_lang)

    def apply_language(self, lang_code):
        self.lang = lang_code
        self.config_mgr.set_language(lang_code)
        self.tr = TRANSLATIONS[lang_code]

        self.title(self.tr["app_title"])
        self.lbl_lang.configure(text=self.tr["lang_label"])
        self.sub_label.configure(text=self.tr["sub_logo"])

        self.btn_smart_browser.configure(text=self.tr["btn_smart_browser"])
        self.btn_open_classic.configure(text=self.tr["btn_open_classic"])
        self.lbl_recent.configure(text=self.tr["lbl_recent"])
        self.btn_save.configure(text=self.tr["btn_save"])
        self.btn_save_as.configure(text=self.tr["btn_save_as"])
        self.btn_restore.configure(text=self.tr["btn_restore"])
        self.btn_open_curr_dir.configure(text=self.tr["btn_view_folder"])
        self.btn_pin_curr_dir.configure(text=self.tr["btn_pin_folder"])

        self.entry_search.configure(placeholder_text=self.tr["search_placeholder"])
        self.btn_clear_search.configure(text=self.tr["btn_clear"])

        self._filter_key_to_label = {
            "all": self.tr["filter_all"],
            "fav": self.tr["filter_fav"],
            "mod": self.tr["filter_mod"],
            "num": self.tr["filter_num"],
            "bool": self.tr["filter_bool"],
            "str": self.tr["filter_str"],
        }
        self._filter_label_to_key = {v: k for k, v in self._filter_key_to_label.items()}
        filter_labels = [self._filter_key_to_label[k] for k in self.FILTER_KEYS]
        self.seg_filter.configure(values=filter_labels)
        self.seg_filter.set(self._filter_key_to_label.get(self.active_filter_key, filter_labels[0]))

        self.tree.heading("variavel", text=self.tr["col_var"])
        self.tree.heading("tipo", text=self.tr["col_type"])
        self.tree.heading("original", text=self.tr["col_orig"])
        self.tree.heading("valor", text=self.tr["col_val"])
        self.tree.heading("estado", text=self.tr["col_status"])

        self.lbl_insp_header.configure(text=self.tr["insp_header"])
        self.lbl_insp_sub.configure(text=self.tr["insp_sub"])
        self.lbl_input_title.configure(text=self.tr["lbl_new_val"])
        self.entry_new_value.configure(placeholder_text=self.tr["entry_placeholder"])
        self.btn_apply.configure(text=self.tr["btn_apply"])

        self.lbl_quick_num.configure(text=self.tr["lbl_quick_num"])
        if self.btn_zero_ref:
            self.btn_zero_ref.configure(text=self.tr["btn_zero"])
        if self.btn_max_ref:
            self.btn_max_ref.configure(text=self.tr["btn_max"])

        self.lbl_quick_bool.configure(text=self.tr["lbl_quick_bool"])
        self.btn_bool_true.configure(text=self.tr["btn_bool_true"])
        self.btn_bool_false.configure(text=self.tr["btn_bool_false"])
        self.btn_revert_var.configure(text=self.tr["btn_revert_var"])

        self._refresh_recent_dropdown()

        if not self.backend.filepath:
            self.lbl_file_info.configure(text=self.tr["info_no_file"])
            self.lbl_var_name.configure(text=self.tr["var_none"])
            self.lbl_var_meta.configure(text=self.tr["var_meta_empty"])
            self.btn_fav.configure(text=self.tr["btn_fav_add"])
            self.status_bar.configure(text=self.tr["status_ready"])
        else:
            self._update_sidebar_summary()
            self.refresh_table()
            if self.selected_key and self.selected_key in self.backend.entries:
                self._populate_inspector(self.selected_key)
            else:
                self.lbl_var_name.configure(text=self.tr["var_none"])
                self.lbl_var_meta.configure(text=self.tr["var_meta_empty"])
                self.btn_fav.configure(text=self.tr["btn_fav_add"])

    def _on_filter_tab_changed(self, selected_label):
        self.active_filter_key = self._filter_label_to_key.get(selected_label, "all")
        self.refresh_table()

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            rowheight=34,
            fieldbackground="#1e293b",
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#0f172a",
            foreground="#e2e8f0",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(6, 6)
        )
        style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#334155")]
        )

        self.tree.tag_configure("even", background="#1e293b")
        self.tree.tag_configure("odd", background="#243247")
        self.tree.tag_configure("modified", foreground="#4ade80", background="#143326")
        self.tree.tag_configure("favorite", foreground="#facc15")

    def _clear_filters(self):
        self.search_var.set("")
        self.active_filter_key = "all"
        self.seg_filter.set(self._filter_key_to_label["all"])
        self.refresh_table()

    def _refresh_recent_dropdown(self):
        self._recent_map = {}
        labels = []
        for idx, fpath in enumerate(self.config_mgr.recent_files[:10], start=1):
            p = Path(fpath)
            label = f"{idx}. {p.parent.name} / {p.name}"
            if len(label) > 34:
                label = label[:31] + "..."
            self._recent_map[label] = fpath
            labels.append(label)

        if not labels:
            self.combo_recent.configure(values=[self.tr["recent_empty"]])
            self.recent_var.set(self.tr["recent_empty"])
        else:
            self.combo_recent.configure(values=labels)
            self.recent_var.set(self.tr["recent_select"])

    def action_open_from_recent_menu(self, selected_label):
        if hasattr(self, "_recent_map") and selected_label in self._recent_map:
            target = self._recent_map[selected_label]
            self._load_save_into_ui(target)

    def action_open_smart_browser(self):
        SmartSaveBrowserModal(self, self.config_mgr, self._load_save_into_ui)

    def action_open_classic_dialog(self):
        initial = str(self.backend.filepath.parent) if self.backend.filepath else None
        file_path = filedialog.askopenfilename(
            initialdir=initial,
            title=self.tr["dlg_open_title"],
            filetypes=[
                (self.tr["ft_all_saves"], "*.save *.dat *.sav *.rpgsave *.rmmzsave *.json *.ini *persistent*"),
                ("Save / Dat Files", "*.save *.dat *.sav"),
                ("Ren'Py Save", "*.save *persistent*"),
                ("RPG Maker MV/MZ", "*.rpgsave *.rmmzsave"),
                ("JSON / INI", "*.json *.ini"),
                (self.tr["ft_all_files"], "*.*"),
            ]
        )
        if file_path:
            self._load_save_into_ui(file_path)

    def action_open_current_folder_os(self):
        if self.backend.filepath and self.backend.filepath.parent.exists():
            SmartSaveBrowserModal._open_os_folder(self.backend.filepath.parent)

    def action_pin_loaded_save_folder(self):
        if not self.backend.filepath:
            return
        folder = str(self.backend.filepath.parent)
        if self.config_mgr.add_pinned_folder(folder):
            messagebox.showinfo(
                self.tr["msg_pin_title"],
                self.tr["msg_pin_added"].format(name=self.backend.filepath.parent.name)
            )
        else:
            messagebox.showinfo(
                self.tr["msg_pin_exists_title"],
                self.tr["msg_pin_exists"]
            )

    def sort_by_column(self, col):
        if self.sort_col == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_col = col
            self.sort_reverse = False
        self.refresh_table()

    def _get_status_label(self, is_mod, is_fav):
        if is_mod and is_fav:
            return self.tr["status_mod_fav"]
        elif is_mod:
            return self.tr["status_mod"]
        elif is_fav:
            return self.tr["status_fav"]
        return self.tr["status_orig"]

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.backend.entries:
            return

        query = self.search_var.get().strip().lower()
        mode = self.active_filter_key

        filtered = []
        for key, info in self.backend.entries.items():
            val = info["value"]
            orig_val = info["orig_value"]
            orig_type = info["orig_type"]
            is_mod = info["modified"]
            is_fav = key in self.backend.favorites

            if mode == "fav" and not is_fav:
                continue
            elif mode == "mod" and not is_mod:
                continue
            elif mode == "num" and orig_type not in (int, float):
                continue
            elif mode == "bool" and orig_type is not bool:
                continue
            elif mode == "str" and orig_type is not str:
                continue

            val_str = str(val)
            if query and (query not in key.lower() and query not in val_str.lower()):
                continue

            estado_txt = self._get_status_label(is_mod, is_fav)
            filtered.append((key, orig_type.__name__, str(orig_val), val_str, estado_txt, is_mod, is_fav))

        col_idx = {"variavel": 0, "tipo": 1, "original": 2, "valor": 3, "estado": 4}.get(self.sort_col, 0)
        filtered.sort(key=lambda r: r[col_idx].lower(), reverse=self.sort_reverse)

        max_rows = 2500
        count = 0
        for idx, row in enumerate(filtered[:max_rows]):
            key, t_name, orig_s, val_s, est_s, is_mod, is_fav = row
            if is_mod:
                tags = ("modified",)
            elif is_fav:
                tags = ("favorite", "even" if idx % 2 == 0 else "odd")
            else:
                tags = ("even" if idx % 2 == 0 else "odd",)

            self.tree.insert(
                "",
                "end",
                iid=key,
                values=(key, t_name, orig_s, val_s, est_s),
                tags=tags
            )
            count += 1

        if self.selected_key and self.tree.exists(self.selected_key):
            self.tree.selection_set(self.selected_key)

        total_all = len(self.backend.entries)
        mod_count = self.backend.count_modified()
        self.status_bar.configure(
            text=self.tr["status_showing"].format(count=count, total=total_all, mods=mod_count)
        )

    def on_row_selected(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return

        key = selection[0]
        if key not in self.backend.entries:
            return

        self.selected_key = key
        self._populate_inspector(key)

    def _populate_inspector(self, key):
        info = self.backend.entries[key]
        orig_type = info["orig_type"]
        type_name = orig_type.__name__
        is_fav = key in self.backend.favorites

        self.lbl_var_name.configure(text=key)
        self.lbl_var_meta.configure(
            text=self.tr["var_meta_fmt"].format(type=type_name, orig=info["orig_value"])
        )

        self.btn_fav.configure(
            state="normal",
            text=self.tr["btn_fav_rem"] if is_fav else self.tr["btn_fav_add"],
            fg_color="#ca8a04" if is_fav else "#334155"
        )

        self.entry_new_value.configure(state="normal")
        self.entry_new_value.delete(0, tk.END)
        self.entry_new_value.insert(0, str(info["value"]))
        self.btn_apply.configure(state="normal")

        if info["modified"]:
            self.btn_revert_var.configure(state="normal", fg_color="#b45309")
        else:
            self.btn_revert_var.configure(state="disabled", fg_color="#475569")

        if orig_type in (int, float):
            self.bool_tools_frame.grid_remove()
            self.num_tools_frame.grid()
        elif orig_type is bool:
            self.num_tools_frame.grid_remove()
            self.bool_tools_frame.grid()
        else:
            self.num_tools_frame.grid_remove()
            self.bool_tools_frame.grid_remove()

    def on_row_double_click(self, _event=None):
        if not self.selected_key or self.selected_key not in self.backend.entries:
            return

        info = self.backend.entries[self.selected_key]
        if info["orig_type"] is bool:
            new_bool = not bool(info["value"])
            self.action_set_boolean(new_bool)
        else:
            self.entry_new_value.focus_set()
            self.entry_new_value.select_range(0, tk.END)

    def action_quick_number(self, action):
        if not self.selected_key or self.selected_key not in self.backend.entries:
            return

        info = self.backend.entries[self.selected_key]
        curr = info["value"]
        orig_type = info["orig_type"]

        if action == "zero":
            new_val = 0
        elif action == "set999":
            new_val = 999
        elif action == "max":
            new_val = 999999
        elif action == "mul2":
            new_val = curr * 2
        elif isinstance(action, (int, float)):
            new_val = curr + action
        else:
            return

        if orig_type is int:
            new_val = int(new_val)
        else:
            new_val = round(float(new_val), 4)

        self.entry_new_value.configure(state="normal")
        self.entry_new_value.delete(0, tk.END)
        self.entry_new_value.insert(0, str(new_val))
        self.action_apply_value()

    def action_set_boolean(self, bool_val):
        if not self.selected_key:
            return
        self.entry_new_value.configure(state="normal")
        self.entry_new_value.delete(0, tk.END)
        self.entry_new_value.insert(0, "True" if bool_val else "False")
        self.action_apply_value()

    def action_apply_value(self):
        if not self.selected_key:
            return

        raw_val = self.entry_new_value.get()
        try:
            new_typed_val = self.backend.update_entry(self.selected_key, raw_val)
        except Exception as exc:
            messagebox.showwarning(
                self.tr["msg_invalid_val"],
                self.tr["msg_invalid_val_body"].format(err=exc)
            )
            return

        self._update_single_tree_row(self.selected_key)
        self._populate_inspector(self.selected_key)
        self._update_sidebar_summary()

        self.status_bar.configure(
            text=self.tr["status_updated"].format(key=self.selected_key, val=repr(new_typed_val))
        )

    def action_revert_single(self):
        if not self.selected_key:
            return
        orig_val = self.backend.revert_single_entry(self.selected_key)
        self._update_single_tree_row(self.selected_key)
        self._populate_inspector(self.selected_key)
        self._update_sidebar_summary()
        self.status_bar.configure(
            text=self.tr["status_reverted"].format(key=self.selected_key, val=repr(orig_val))
        )

    def action_toggle_favorite(self):
        if not self.selected_key:
            return
        is_now_fav = self.backend.toggle_favorite(self.selected_key)
        if self.backend.filepath:
            self.config_mgr.favorites_vars[str(self.backend.filepath)] = list(self.backend.favorites)
            self.config_mgr.save()
        self._update_single_tree_row(self.selected_key)
        self._populate_inspector(self.selected_key)
        if self.active_filter_key == "fav" and not is_now_fav:
            self.refresh_table()

    def _update_single_tree_row(self, key):
        if not self.tree.exists(key):
            return
        info = self.backend.entries[key]
        is_mod = info["modified"]
        is_fav = key in self.backend.favorites
        estado_txt = self._get_status_label(is_mod, is_fav)

        tags = ("modified",) if is_mod else (("favorite",) if is_fav else ("even",))
        self.tree.item(
            key,
            values=(
                key,
                info["orig_type"].__name__,
                str(info["orig_value"]),
                str(info["value"]),
                estado_txt
            ),
            tags=tags
        )

    def _load_save_into_ui(self, file_path):
        try:
            total = self.backend.load_file(file_path)
        except Exception as exc:
            messagebox.showerror(self.tr["msg_err_open"], str(exc))
            return

        self.config_mgr.add_recent_file(file_path)
        self._refresh_recent_dropdown()
        saved_favs = self.config_mgr.favorites_vars.get(str(self.backend.filepath), [])
        self.backend.favorites = set(saved_favs)

        self.btn_save.configure(state="normal")
        self.btn_save_as.configure(state="normal")
        self.btn_restore.configure(state="normal")
        self.btn_open_curr_dir.configure(state="normal")
        self.btn_pin_curr_dir.configure(state="normal")

        self.selected_key = None
        self.lbl_var_name.configure(text=self.tr["var_none"])
        self.lbl_var_meta.configure(text=self.tr["var_meta_empty"])
        self.entry_new_value.configure(state="normal")
        self.entry_new_value.delete(0, tk.END)
        self.entry_new_value.configure(state="disabled")
        self.btn_apply.configure(state="disabled")
        self.btn_fav.configure(state="disabled", text=self.tr["btn_fav_add"])
        self.btn_revert_var.configure(state="disabled")
        self.num_tools_frame.grid_remove()
        self.bool_tools_frame.grid_remove()

        self._update_sidebar_summary()
        self.refresh_table()
        self.status_bar.configure(
            text=self.tr["status_loaded"].format(
                fmt=self.backend.get_human_format_name(),
                path=self.backend.filepath,
                total=total
            )
        )

    def _update_sidebar_summary(self):
        if not self.backend.filepath:
            return
        fmt_label = self.backend.get_human_format_name()
        total = len(self.backend.entries)
        mods = self.backend.count_modified()
        parent_folder = self.backend.filepath.parent.name

        info_text = self.tr["summary_fmt"].format(
            folder=parent_folder,
            name=self.backend.filepath.name,
            engine=fmt_label,
            total=total,
            mods=mods
        )
        self.lbl_file_info.configure(text=info_text)

    def action_save_file(self):
        if not self.backend.filepath:
            return
        try:
            self.backend.save_file()
        except Exception as exc:
            messagebox.showerror(
                self.tr["msg_err_save"],
                self.tr["msg_err_save_body"].format(err=exc)
            )
            return

        self.refresh_table()
        if self.selected_key:
            self._populate_inspector(self.selected_key)
        self._update_sidebar_summary()
        self.status_bar.configure(text=self.tr["status_saved"].format(path=self.backend.filepath))
        messagebox.showinfo(self.tr["msg_success"], self.tr["msg_saved_body"])

    def action_save_as(self):
        if not self.backend.filepath:
            return
        ext = self.backend.filepath.suffix
        out_path = filedialog.asksaveasfilename(
            initialdir=str(self.backend.filepath.parent),
            initialfile=self.backend.filepath.name,
            defaultextension=ext,
            title=self.tr["dlg_save_as_title"],
            filetypes=[(self.tr["ft_save_file"], f"*{ext}"), (self.tr["ft_all_files"], "*.*")]
        )
        if not out_path:
            return
        try:
            self.backend.save_file(output_path=out_path)
        except Exception as exc:
            messagebox.showerror(
                self.tr["msg_err_save"],
                self.tr["msg_err_save_body"].format(err=exc)
            )
            return

        self.config_mgr.add_recent_file(out_path)
        self._refresh_recent_dropdown()
        self.refresh_table()
        if self.selected_key:
            self._populate_inspector(self.selected_key)
        self._update_sidebar_summary()
        self.status_bar.configure(text=self.tr["status_exported"].format(path=out_path))
        messagebox.showinfo(self.tr["msg_success"], self.tr["msg_exported_body"].format(path=out_path))

    def action_restore_backup(self):
        if not self.backend.filepath:
            return
        confirm = messagebox.askyesno(
            self.tr["msg_restore_title"],
            self.tr["msg_restore_confirm"]
        )
        if not confirm:
            return

        if self.backend.restore_backup():
            self.refresh_table()
            self._update_sidebar_summary()
            self.status_bar.configure(text=self.tr["status_backup_restored"])
            messagebox.showinfo(self.tr["msg_restore_done_title"], self.tr["msg_restore_done_body"])
        else:
            messagebox.showwarning(self.tr["msg_restore_missing_title"], self.tr["msg_restore_missing_body"])


if __name__ == "__main__":
    app = SaveEditorApp()
    app.mainloop()