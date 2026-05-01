# ===============================
# IMPORTS
# ===============================
import sys        # Para leer argumentos desde la terminal
import re         # Para usar expresiones regulares (parseo)
import os         # Para manejar archivos
# ===============================


# ===============================
# VARIABLES GLOBALES DEL COMPILADOR
# ===============================

codigo_py = []   # Lista donde se va armando el código Python final
indent = 0       # Nivel de indentación actual (cantidad de tabs/espacios)
stack = []       # Pila para controlar estructuras (if, while, for)

# ===============================


# ===============================
# FUNCION PARA AGREGAR LINEAS AL CODIGO GENERADO
# ===============================
def emitir(linea):
    # Agrega la línea con la indentación correcta
    codigo_py.append("    " * indent + linea)
# ===============================


# ===============================
# TRADUCE CONDICIONES DE DANTE A PYTHON
# ===============================
def traducir_condicion(condicion):
    # Reemplaza operadores lógicos del lenguaje DANTE
    condicion = condicion.replace(" Y ", " and ")
    condicion = condicion.replace(" O ", " or ")
    return condicion
# ===============================


# ===============================
# GENERA INPUT INTELIGENTE (INT O STRING)
# ===============================
def generar_input_variable(var):
    # Guarda el input como texto temporal
    emitir(f"{var}_temp = input()")

    # Intenta convertir a número
    emitir("try:")
    emitir(f"    {var} = int({var}_temp)")

    # Si falla, lo deja como string
    emitir("except:")
    emitir(f"    {var} = {var}_temp")
# ===============================


# ===============================
# CIERRA IFs QUE ESPERABAN UN SINO
# ===============================
def cerrar_ifs_pendientes():
    # Mientras haya ifs esperando un SINO
    while stack and stack[-1]["tipo"] == "if" and stack[-1]["esperando_sino"]:
        stack.pop()
# ===============================


# ===============================
# BUSCA EL IF CORRECTO PARA UN SINO
# ===============================
def buscar_if_para_sino():
    # Recorre el stack desde el final (último abierto)
    for i in range(len(stack) - 1, -1, -1):
        elem = stack[i]

        # Encuentra un if que aún no tenga sino
        if elem["tipo"] == "if" and not elem["tiene_sino"]:
            return i

    return None
# ===============================


# ===============================
# FUNCION PRINCIPAL: PROCESA CADA LINEA
# ===============================
def procesar_linea(linea, numero_linea):
    global indent

    linea = linea.strip()

    # Ignorar líneas vacías
    if not linea:
        return

    # Si no viene un SINO, cerrar IFs pendientes
    if linea != "SINO":
        cerrar_ifs_pendientes()

    # ---------------- APLICACION ----------------
    if linea.startswith("APLICACION"):
        return  # No hace nada por ahora

    # ---------------- CREAR ----------------
    match = re.match(r"CREAR\s+([a-zA-Z]+)", linea)
    if match:
        emitir(f"{match.group(1)} = 0")
        return

    # ---------------- MOSTRAR ----------------
    match = re.match(r'MOSTRAR\s+"(.+)"', linea)
    if match:
        emitir(f'print("{match.group(1)}")')
        return

    match = re.match(r"MOSTRAR\s+([a-zA-Z]+)", linea)
    if match:
        emitir(f"print({match.group(1)})")
        return

    # ---------------- PEDIR ----------------
    match = re.match(r"PEDIR\s+([a-zA-Z]+)", linea)
    if match:
        generar_input_variable(match.group(1))
        return

    # ---------------- EDITAR ----------------
    match = re.match(r"EDITAR\s+([a-zA-Z]+)\s*=\s*(.+)", linea)
    if match:
        emitir(f"{match.group(1)} = {match.group(2)}")
        return

    # ---------------- PREGUNTA (IF) ----------------
    match = re.match(r"PREGUNTA\s+(.+)", linea)
    if match:
        emitir(f"if {traducir_condicion(match.group(1))}:")
        stack.append({
            "tipo": "if",
            "tiene_sino": False,
            "esperando_sino": False,
            "linea": numero_linea
        })
        return

    # ---------------- SINO ----------------
    if linea == "SINO":
        indice = buscar_if_para_sino()

        if indice is None:
            print(f"Error línea {numero_linea}: SINO sin PREGUNTA correspondiente")
            return

        stack[indice]["tiene_sino"] = True
        stack[indice]["esperando_sino"] = False

        indent = max(0, indent - 1)
        emitir("else:")
        indent += 1
        return

    # ---------------- REPETIR ----------------
    match = re.match(r"REPETIR\s+(\d+)", linea)
    if match:
        emitir(f"for _ in range({match.group(1)}):")
        stack.append({"tipo": "for", "linea": numero_linea})
        return

    match = re.match(r"REPETIR\s+MIENTRAS\s+(.+)", linea)
    if match:
        emitir(f"while ({traducir_condicion(match.group(1))}):")
        stack.append({"tipo": "while", "linea": numero_linea})
        return

    # ---------------- INICIO ----------------
    if linea == "INICIO":
        indent += 1
        return

    # ---------------- FIN ----------------
    if linea == "FIN":
        indent = max(0, indent - 1)

        if stack:
            top = stack[-1]

            if top["tipo"] == "if":
                if top["tiene_sino"]:
                    stack.pop()
                else:
                    top["esperando_sino"] = True

            elif top["tipo"] in ("for", "while"):
                stack.pop()

        return

    print(f"Instruccion no reconocida (línea {numero_linea}): {linea}")
# ===============================


# ===============================
# GENERA EL ARCHIVO PYTHON FINAL
# ===============================
def generar_archivo_py(nombre_py):
    global indent

    cerrar_ifs_pendientes()

    # Aviso si quedaron estructuras abiertas
    if stack:
        print("\n⚠️ Advertencia: estructuras sin cerrar:")
        for elem in stack:
            print(f" - {elem['tipo']} (línea {elem['linea']})")

    indent = 0

    # Pausa final del programa
    emitir('input("Presiona ENTER para finalizar...")')

    with open(nombre_py, "w", encoding="utf-8") as f:
        for linea in codigo_py:
            f.write(linea + "\n")
# ===============================


# ===============================
# GENERA EL .EXE CON PYINSTALLER
# ===============================
def generar_exe(nombre_py):
    os.system(f"pyinstaller --onefile {nombre_py}")
# ===============================


# ===============================
# MAIN (PUNTO DE ENTRADA)
# ===============================
def main():
    if len(sys.argv) < 2:
        print("Uso: python dante.py programa.dante")
        return

    archivo = sys.argv[1]
    salida = os.path.splitext(archivo)[0] + ".py"

    with open(archivo, encoding="utf-8") as f:
        for i, linea in enumerate(f, start=1):
            procesar_linea(linea, i)

    generar_archivo_py(salida)
    generar_exe(salida)


if __name__ == "__main__":
    main()