import tkinter as tk

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Control de Stock")
    ventana.geometry("400x300")

    label = tk.Label(ventana, text="Bienvenido al Control de Stock")
    label.pack(pady=20)
    ventana.mainloop()

