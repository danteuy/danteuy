# ===============================
# IMPORTS
# ===============================

import tkinter as tk  # Librería principal para la interfaz gráfica
from tkinter import filedialog, messagebox  # Ventanas de archivos y mensajes
import subprocess  # Para ejecutar el compilador (dante.py)
import os  # Manejo de archivos
import shutil  # Mover archivos (ej: .exe generado)
import re  # Expresiones regulares (syntax highlighting)
import threading  # Para ejecutar compilación sin congelar la UI

# ===============================
# CONSTANTES DEL LENGUAJE
# ===============================

# Palabras reservadas de DANTE (se usan para colorear)
PALABRAS_RESERVADAS = [
    "CREAR", "EDITAR", "PEDIR", "MOSTRAR",
    "PREGUNTA", "INICIO", "FIN", "SINO",
    "REPETIR", "HASTA", "MIENTRAS",
    "OPCIONES", "OPCION",
    "Y", "O",
    "APLICACION"
]

# Operadores a resaltar
OPERADORES = [
    "=", r"\+", "-", "<", ">", "<=", ">=", "=="
]

# ===============================
# AUTOINDENTACIÓN
# ===============================

def auto_indent(event):
    """
    Se ejecuta cuando el usuario presiona ENTER.
    Ajusta automáticamente la indentación según el contexto.
    """

    # Número de línea actual donde está el cursor
    linea_actual = editor.index(tk.INSERT).split(".")[0]

    # Obtener texto completo de esa línea
    linea_completa = editor.get(f"{linea_actual}.0", f"{linea_actual}.end")

    # Texto sin espacios
    texto_linea = linea_completa.strip()

    # Cantidad de espacios al inicio (indentación actual)
    espacios_actuales = len(linea_completa) - len(linea_completa.lstrip(" "))

    nueva_indentacion = espacios_actuales

    # Si la línea es FIN → reducir indentación
    if texto_linea == "FIN":
        nueva_indentacion = max(0, espacios_actuales - 1)

        # Reescribir la línea con la indentación correcta
        editor.delete(f"{linea_actual}.0", f"{linea_actual}.end")
        editor.insert(f"{linea_actual}.0", (" " * nueva_indentacion) + "FIN")

    # Si termina en INICIO → aumentar indentación
    elif texto_linea.endswith("INICIO"):
        nueva_indentacion += 1

    # Insertar nueva línea con indentación
    editor.insert(tk.INSERT, "\n" + (" " * nueva_indentacion))

    return "break"  # Evita comportamiento por defecto


# ===============================
# GUARDAR ARCHIVO
# ===============================

def guardar_archivo():
    """
    Abre diálogo para guardar el código como archivo .dante
    """

    archivo = filedialog.asksaveasfilename(
        defaultextension=".dante",
        filetypes=[("Archivos D.A.N.T.E.", "*.dante")]
    )

    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

        messagebox.showinfo("Guardado", "Archivo guardado correctamente 😈")


# ===============================
# ABRIR ARCHIVO
# ===============================

def abrir_archivo():
    """
    Permite abrir un archivo .dante y cargarlo en el editor
    """

    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos D.A.N.T.E.", "*.dante")]
    )

    if archivo:
        with open(archivo, encoding="utf-8") as f:
            contenido = f.read()

        editor.delete("1.0", tk.END)
        editor.insert("1.0", contenido)

        actualizar_todo()  # refresca colores y cajas


# ===============================
# MENSAJES TEMPORALES
# ===============================

def mostrar_estado_temporal(texto, tiempo=3000):
    """
    Muestra un mensaje en la barra de estado por unos segundos
    """

    estado_var.set(texto)

    # Después de X milisegundos vuelve a "Listo"
    ventana.after(tiempo, lambda: estado_var.set("Listo"))


# ===============================
# COMPILACIÓN (HILO SEPARADO)
# ===============================

def ejecutar_compilacion(temp_dante, exe_path):
    """
    Ejecuta el compilador en segundo plano (thread)
    """

    try:
        # Ejecuta el compilador
        subprocess.run(["python", "dante.py", temp_dante], check=True)

        # Nombre del exe generado
        nombre_base = os.path.splitext(temp_dante)[0]
        exe_generado = nombre_base + ".exe"

        # Mover exe a ubicación elegida
        if os.path.exists(exe_generado):
            shutil.move(exe_generado, exe_path)

        # Actualizar UI (desde el hilo principal)
        ventana.after(0, lambda: mostrar_estado_temporal("✔ Ejecutable generado"))
        ventana.after(0, lambda: messagebox.showinfo("Éxito", "Ejecutable generado"))

    except subprocess.CalledProcessError:
        ventana.after(0, lambda: mostrar_estado_temporal("❌ Error al compilar"))
        ventana.after(0, lambda: messagebox.showerror("Error", "Algo salió mal"))

    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_dante):
            os.remove(temp_dante)


# ===============================
# BOTÓN GENERAR EXE
# ===============================

def generar_exe():
    """
    Guarda el código actual y lanza la compilación
    """

    exe_path = filedialog.asksaveasfilename(
        defaultextension=".exe",
        filetypes=[("Ejecutable", "*.exe")]
    )

    if not exe_path:
        return

    temp_dante = "temp_program.dante"

    # Guardar código actual temporalmente
    with open(temp_dante, "w", encoding="utf-8") as f:
        f.write(editor.get("1.0", tk.END))

    estado_var.set("⏳ Compilando...")

    # Ejecutar compilación en hilo (para no congelar UI)
    threading.Thread(
        target=ejecutar_compilacion,
        args=(temp_dante, exe_path),
        daemon=True
    ).start()


# ===============================
# ANALIZADOR DE VARIABLES (CAJAS)
# ===============================

def analizar_cajas(event=None):
    """
    Analiza el código hasta la línea actual y muestra
    las variables como "cajas" tipo memoria
    """

    codigo = editor.get("1.0", tk.END).splitlines()
    cursor_line = int(editor.index(tk.INSERT).split(".")[0])

    cajas = {}

    for i, linea in enumerate(codigo, start=1):

        if i > cursor_line:
            break

        linea = linea.strip()
        if not linea:
            continue

        partes = linea.split()

        if len(partes) >= 2:
            comando = partes[0]
            nombre = partes[1]

            if comando == "CREAR":
                if nombre not in cajas:
                    cajas[nombre] = "0"

            elif comando == "PEDIR":
                cajas[nombre] = "?"

            elif comando == "EDITAR" and "=" in linea:
                cajas[nombre] = linea.split("=", 1)[1].strip()

    # Dibujar cajas
    sidebar.delete("1.0", tk.END)
    sidebar.insert(tk.END, "Cajas\n\n")

    for nombre, valor in cajas.items():
        caja = (
            "┌───────────────┐\n"
            f"│ {nombre:<13} │\n"
            "├───────────────┤\n"
            f"│ {valor:<13} │\n"
            "└───────────────┘\n\n"
        )
        sidebar.insert(tk.END, caja)


# ===============================
# SYNTAX HIGHLIGHTING
# ===============================

def colorear_sintaxis(event=None):
    """
    Aplica colores al código según su tipo
    """

    codigo = editor.get("1.0", tk.END)

    # Limpiar colores anteriores
    for tag in ["reservada", "string", "numero", "operador"]:
        editor.tag_remove(tag, "1.0", tk.END)

    # Strings
    for match in re.finditer(r'"[^"]*"', codigo):
        editor.tag_add("string", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    # Números
    for match in re.finditer(r"\b\d+\b", codigo):
        editor.tag_add("numero", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    # Palabras reservadas
    for palabra in PALABRAS_RESERVADAS:
        for match in re.finditer(rf"\b{palabra}\b", codigo):
            editor.tag_add("reservada", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    # Operadores
    for op in OPERADORES:
        for match in re.finditer(op, codigo):
            editor.tag_add("operador", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")


# ===============================
# ACTUALIZACIÓN GLOBAL
# ===============================

def actualizar_todo(event=None):
    """
    Se ejecuta cada vez que el usuario escribe o mueve el cursor
    """
    analizar_cajas()
    colorear_sintaxis()


# ===============================
# CREACIÓN DE LA VENTANA
# ===============================

ventana = tk.Tk()
ventana.title("D.A.N.T.E.")
ventana.geometry("1000x600")
ventana.configure(bg="#1e1e1e")

# ===============================
# LAYOUT PRINCIPAL
# ===============================

frame_principal = tk.Frame(ventana, bg="#1e1e1e")
frame_principal.pack(fill="both", expand=True)

# Sidebar (cajas)
sidebar = tk.Text(
    frame_principal,
    width=28,
    bg="#0e0e0e",
    fg="#00ff90",
    font=("Courier New", 11),
    bd=0
)
sidebar.pack(side="right", fill="y")

# Editor principal
editor = tk.Text(
    frame_principal,
    bg="#1e1e1e",
    fg="#d4d4d4",
    insertbackground="white",
    selectbackground="#264f78",
    font=("Consolas", 12),
    wrap="none",
    bd=0
)
editor.pack(side="left", fill="both", expand=True)

# Colores
editor.tag_config("reservada", foreground="#569cd6")
editor.tag_config("string", foreground="#ce9178")
editor.tag_config("numero", foreground="#b5cea8")
editor.tag_config("operador", foreground="#d4d4d4")

# Eventos
editor.bind("<KeyRelease>", actualizar_todo)
editor.bind("<ButtonRelease>", actualizar_todo)
editor.bind("<Return>", auto_indent)

# ===============================
# BARRA DE ESTADO
# ===============================

estado_var = tk.StringVar(value="Listo")

barra_estado = tk.Label(
    ventana,
    textvariable=estado_var,
    bg="#252526",
    fg="#d4d4d4",
    anchor="w"
)
barra_estado.pack(fill="x")

# ===============================
# BOTONES
# ===============================

frame_botones = tk.Frame(ventana, bg="#1e1e1e")
frame_botones.pack(fill="x")

tk.Button(frame_botones, text="Guardar", command=guardar_archivo).pack(side="left")
tk.Button(frame_botones, text="Abrir", command=abrir_archivo).pack(side="left")
tk.Button(frame_botones, text="Generar EXE", command=generar_exe).pack(side="right")

# ===============================
# LOOP PRINCIPAL
# ===============================

ventana.mainloop()