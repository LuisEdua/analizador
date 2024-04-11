import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from AnalizadorLexico import analizador_lexico
from AnalizadorSintactico import analizador_sintactico
from AnalizadorSemantico import analizador_semantico

def procesar():
    entrada = texto_entrada.get("1.0", tk.END)

    # Analizador léxico
    tokens_lexicos = analizador_lexico(entrada)
    texto_lexico.delete("1.0", tk.END)
    for token in tokens_lexicos:
        texto_lexico.insert(tk.END, f"{token}\n")
        
    

    # Analizador sintáctico
    resultado_sintactico = analizador_sintactico(tokens_lexicos)
    texto_sintactico.delete("1.0", tk.END)
    texto_sintactico.insert(tk.END, resultado_sintactico)

    # Analizador semántico
    if "Error de sintaxis" not in resultado_sintactico:
        resultado_semantico = analizador_semantico(tokens_lexicos)
        texto_semantico.delete("1.0", tk.END)
        for res in resultado_semantico:
            texto_semantico.insert(tk.END, f"{res}\n")
    else:
        texto_semantico.delete("1.0", tk.END)
        texto_semantico.insert(tk.END, "El análisis semántico no se pudo realizar debido a errores sintácticos.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Compilador Básico")

# Frame para la entrada de texto
frame_entrada = ttk.Frame(ventana)
frame_entrada = ttk.LabelFrame(ventana, text="Entrada")
frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Campo de entrada de texto
texto_entrada = scrolledtext.ScrolledText(frame_entrada, width=60, height=13)
texto_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Botón para procesar
boton_procesar = ttk.Button(frame_entrada, text="Procesar", command=procesar)
boton_procesar.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

# Frame para el analizador léxico
frame_lexico = ttk.LabelFrame(ventana, text="Analizador Léxico")
frame_lexico.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Resultados del Analizador Léxico
texto_lexico = scrolledtext.ScrolledText(frame_lexico, width=60, height=8)
texto_lexico.pack(padx=10, pady=10, fill="both", expand=True)

# Frame para el analizador semántico
frame_semantico = ttk.LabelFrame(ventana, text="Analizador Semántico")
frame_semantico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Resultados del Analizador Semántico
texto_semantico = scrolledtext.ScrolledText(frame_semantico, width=60, height=10)
texto_semantico.pack(padx=10, pady=10, fill="both", expand=True)

# Frame para el analizador sintáctico
frame_sintactico = ttk.LabelFrame(ventana, text="Analizador Sintáctico")
frame_sintactico.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Resultados del Analizador Sintáctico
texto_sintactico = scrolledtext.ScrolledText(frame_sintactico, width=60, height=10)
texto_sintactico.pack(padx=10, pady=10, fill="both", expand=True)

ventana.mainloop()
