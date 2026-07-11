import os
import re
import sys
import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import parser as parser_module
from logger import generar_log

USUARIO = "vicmmoraM" 

COLOR = {
    "ventana":        "#000000",
    "barra":          "#0A0A0A",
    "editor_bg":      "#000000",
    "editor_fg":      "#D4D4D4",
    "numeros_bg":     "#0A0A0A",
    "numeros_fg":     "#4B5563",
    "consola_bg":     "#000000",
    "consola_fg":     "#C9D4E3",
    "error":          "#D9534F",
    "contexto":       "#7FA8C9",
    "exito":          "#3FA372",
    "btn_primario":   "#2E6DA4",
    "btn_primario_a": "#3B82C4",   
    "btn_secundario": "#1A1A1A",
    "btn_secundario_a": "#2A2A2A",
    "seleccion":      "#264F78",
    "etiqueta":       "#8A9BB5",
}


SINTAXIS = {
    "kw":         "#569CD6",   # public, class, if, while, return :D
    "tipo":       "#4EC9B0",   # int, decimal, string, bool, List, Dictionary
    "literal":    "#C586C0",   # true, false, new, break
    "string":     "#CE9178",   # "cadenas"
    "numero":     "#B5CEA8",   # 10, 0.50
    "comentario": "#6A9955",   # // y /* */
}

PATRONES_SINTAXIS = [
    ("comentario", r"//[^\n]*|/\*[\s\S]*?\*/"),
    ("string",     r"\"([^\\\n]|(\\.))*?\""),
    ("kw",         r"\b(public|class|if|else|while|for|switch|case|return|void|var)\b"),
    ("tipo",       r"\b(int|decimal|string|bool|List|Dictionary|Console)\b"),
    ("literal",    r"\b(true|false|new|break)\b"),
    ("numero",     r"\b\d+(\.\d+)?\b"),
]

FUENTE_CODIGO = ("Consolas", 11)
FUENTE_UI = ("Segoe UI", 10)
FUENTE_UI_BOLD = ("Segoe UI", 10, "bold")


class LinterGUI:
    def __init__(self, root):
        self.root = root
        root.title("Safe C# Linter")
        root.geometry("920x680")
        root.configure(bg=COLOR["ventana"])

        barra = tk.Frame(root, bg=COLOR["barra"])
        barra.pack(fill="x")
        contenido_barra = tk.Frame(barra, bg=COLOR["barra"])
        contenido_barra.pack(fill="x", padx=12, pady=10)

        self._boton(contenido_barra, "Cargar archivo", self.cargar_archivo,
                    COLOR["btn_secundario"], COLOR["btn_secundario_a"],
                    fg=COLOR["consola_fg"]).pack(side="left")
        self._boton(contenido_barra, "Ejecutar", self.ejecutar_analisis,
                    COLOR["btn_primario"], COLOR["btn_primario_a"],
                    fg="#FFFFFF").pack(side="left", padx=(10, 0))
        self.lbl_archivo = tk.Label(contenido_barra, text="(sin archivo)",
                                    bg=COLOR["barra"], fg=COLOR["etiqueta"], font=FUENTE_UI)
        self.lbl_archivo.pack(side="left", padx=14)

        marco_editor = tk.Frame(root, bg=COLOR["ventana"])
        marco_editor.pack(fill="both", expand=True, padx=12, pady=(12, 0))

        self.numeros = tk.Text(marco_editor, width=4, font=FUENTE_CODIGO, state="disabled",
                               bg=COLOR["numeros_bg"], fg=COLOR["numeros_fg"],
                               takefocus=0, bd=0, padx=6, pady=8)
        self.numeros.pack(side="left", fill="y")

        self.editor = tk.Text(marco_editor, font=FUENTE_CODIGO, undo=True, wrap="none",
                              bg=COLOR["editor_bg"], fg=COLOR["editor_fg"],
                              insertbackground=COLOR["editor_fg"],
                              selectbackground=COLOR["seleccion"],
                              bd=0, padx=10, pady=8)
        scroll = tk.Scrollbar(marco_editor, command=self._scroll_ambos,
                              troughcolor=COLOR["ventana"], bg=COLOR["btn_secundario"],
                              activebackground=COLOR["btn_secundario_a"], bd=0)
        self.editor.configure(yscrollcommand=self._sync_scroll)
        scroll.pack(side="right", fill="y")
        self.editor.pack(side="left", fill="both", expand=True)
        self.scroll = scroll

        for tag, color in SINTAXIS.items():
            self.editor.tag_configure(tag, foreground=color)
        self.editor.tag_raise("string")
        self.editor.tag_raise("comentario")

        try:
            self.editor.tag_configure("linea_error", underline=True, underlinefg=COLOR["error"])
        except tk.TclError:  # Tk < 8.6.6 no soporta underlinefg
            self.editor.tag_configure("linea_error", underline=True, foreground=COLOR["error"])
        self.editor.tag_raise("linea_error")

        self.editor.bind("<KeyRelease>", lambda e: (self._actualizar_numeros(), self._resaltar_sintaxis()))
        self.editor.bind("<MouseWheel>", lambda e: self.root.after_idle(self._sincronizar_vista))

        tk.Label(root, text="CONSOLA DE SALIDA", anchor="w", bg=COLOR["ventana"],
                 fg=COLOR["etiqueta"], font=("Segoe UI", 8, "bold")).pack(fill="x", padx=14, pady=(10, 2))
        self.consola = tk.Text(root, height=10, font=FUENTE_CODIGO, state="disabled",
                               bg=COLOR["consola_bg"], fg=COLOR["consola_fg"],
                               bd=0, padx=10, pady=8)
        self.consola.pack(fill="x", padx=12, pady=(0, 12))
        self.consola.tag_configure("error", foreground=COLOR["error"])
        self.consola.tag_configure("ok", foreground=COLOR["exito"])
        self.consola.tag_configure("contexto", foreground=COLOR["contexto"])

        self._actualizar_numeros()

    @staticmethod
    def _boton(padre, texto, comando, bg, bg_activo, fg):
        return tk.Button(padre, text=texto, command=comando, font=FUENTE_UI_BOLD,
                         bg=bg, fg=fg, activebackground=bg_activo, activeforeground=fg,
                         relief="flat", bd=0, padx=16, pady=6, cursor="hand2")

    def _resaltar_sintaxis(self):
        texto = self.editor.get("1.0", "end-1c")
        for tag in SINTAXIS:
            self.editor.tag_remove(tag, "1.0", "end")
        for tag, patron in PATRONES_SINTAXIS:
            for m in re.finditer(patron, texto):
                self.editor.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    def _actualizar_numeros(self):
        total = int(self.editor.index("end-1c").split(".")[0])
        self.numeros.configure(state="normal")
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(i) for i in range(1, total + 1)))
        self.numeros.configure(state="disabled")
        self._sincronizar_vista()

    def _sync_scroll(self, *args):
        self.scroll.set(*args)
        self.numeros.yview_moveto(args[0])

    def _scroll_ambos(self, *args):
        self.editor.yview(*args)
        self.numeros.yview(*args)

    def _sincronizar_vista(self):
        self.numeros.yview_moveto(self.editor.yview()[0])

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Cargar archivo Safe C#",
            filetypes=[("Archivos C#", "*.cs"), ("Todos", "*.*")])
        if not ruta:
            return
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", contenido)
        self.lbl_archivo.config(text=os.path.basename(ruta))
        self._actualizar_numeros()
        self._resaltar_sintaxis()
        self._escribir_consola([])  

    def ejecutar_analisis(self):
        codigo = self.editor.get("1.0", "end-1c")
        if not codigo.strip():
            self._escribir_consola([("No hay código para analizar.", "error")])
            return

        self.editor.tag_remove("linea_error", "1.0", "end")
        resultado = parser_module.analizar(codigo)

        generar_log("lexico", USUARIO, resultado["tokens"],
                    resultado["errores_lexicos"], source=codigo)
        generar_log("sintactico", USUARIO, [],
                    resultado["errores_sintacticos"], source=codigo)
        generar_log("semantico", USUARIO, [],
                    resultado["errores_semanticos"], source=codigo)

        errores = (resultado["errores_lexicos"]
                   + resultado["errores_sintacticos"]
                   + resultado["errores_semanticos"])
        if errores:
            lineas_codigo = codigo.split("\n")
            salida = []
            for e in errores:
                salida.append((e, "error"))
                salida.extend(self._contexto_error(e, lineas_codigo))
                self._subrayar_linea(e)
            self._escribir_consola(salida)
        else:
            self._escribir_consola([("Análisis ejecutado con éxito", "ok")])

    def _subrayar_linea(self, mensaje):
        """Subraya en el editor la línea referida por el mensaje de error."""
        m = re.search(r"línea (\d+)", mensaje)
        if not m:
            return
        num = m.group(1)

        inicio = self.editor.search(r"\S", f"{num}.0", stopindex=f"{num}.end", regexp=True)
        if inicio:
            self.editor.tag_add("linea_error", inicio, f"{num}.end")

    @staticmethod
    def _contexto_error(mensaje, lineas_codigo):
        """Extrae 'línea N' del mensaje y devuelve la línea de código señalada."""
        m_linea = re.search(r"línea (\d+)", mensaje)
        if not m_linea:
            return []
        num = int(m_linea.group(1))
        if not (1 <= num <= len(lineas_codigo)):
            return []
        return [(f"  {num:>4} | {lineas_codigo[num - 1]}", "contexto")]

    def _escribir_consola(self, lineas):
        self.consola.configure(state="normal")
        self.consola.delete("1.0", "end")
        for texto, tag in lineas:
            self.consola.insert("end", texto + "\n", tag)
        self.consola.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    LinterGUI(root)
    root.mainloop()
