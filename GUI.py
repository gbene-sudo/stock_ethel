import tkinter as tk
from tkinter import messagebox
from models import Barril
from CRUD import actualizar_barril,filtro_por_estado,obtener_barriles,filtro_por_litros,filtro_por_tipo,borrar_barril,crear_barril

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Control de Stock")
    ventana.geometry("400x400")

    # Etiqueta de bienvenida
    label = tk.Label(ventana, text="Bienvenido al Control de Stock")
    label.pack(pady=20)

    # Entradas para agregar o editar barriles
    etiqueta_tipo = tk.Label(ventana, text="Tipo de Barril:")
    etiqueta_tipo.pack()
    entry_tipo = tk.Entry(ventana)
    entry_tipo.pack(pady=5)

    etiqueta_capacidad = tk.Label(ventana, text="Capacidad (en L):")
    etiqueta_capacidad.pack()
    entry_capacidad = tk.Entry(ventana)
    entry_capacidad.pack(pady=5)

    etiqueta_estado = tk.Label(ventana, text="Estado del Barril:")
    etiqueta_estado.pack()
    entry_estado = tk.Entry(ventana)
    entry_estado.pack(pady=5)

    etiqueta_id = tk.Label(ventana, text="ID del Barril (para eliminar o actualizar):")
    etiqueta_id.pack()
    entry_id = tk.Entry(ventana)
    entry_id.pack(pady=5)

    # Función para agregar barril
    def agregar():
        tipo = entry_tipo.get()
        capacidad = entry_capacidad.get()
        estado = entry_estado.get()
        if tipo and capacidad and estado:
            # Aquí agregas el barril con la función agregar_barril (debes adaptarlo si es necesario)
            crear_barril(tipo, capacidad, estado)
            messagebox.showinfo("Éxito", f"Barril de tipo '{tipo}' agregado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese todos los campos.")

    # Función para eliminar barril
    def eliminar():
        barril_id = entry_id.get()
        if barril_id:
            # Eliminar barril por ID
            borrar_barril(barril_id)
            messagebox.showinfo("Éxito", f"Barril con ID '{barril_id}' eliminado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ID válido.")

    # Función para actualizar barril
    def actualizar():
        barril_id = entry_id.get()
        tipo = entry_tipo.get()
        capacidad = entry_capacidad.get()
        estado = entry_estado.get()

        if barril_id and tipo and capacidad and estado:
            # Actualizar barril con la función actualizar_barril (debes adaptarlo si es necesario)
            actualizar_barril(barril_id, tipo, capacidad, estado)
            messagebox.showinfo("Éxito", f"Barril con ID '{barril_id}' actualizado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese todos los campos.")

    # Función para mostrar barriles
    def mostrar_barriles():
        tipo = entry_tipo.get()  # Podemos filtrar por tipo si se ingresa
        barriles = filtro_por_tipo(tipo)
        if barriles:
            resultados = "\n".join([f"ID: {barril.id}, Tipo: {barril.tipo}, Capacidad: {barril.capacidad}L, Estado: {barril.estado}" for barril in barriles])
            messagebox.showinfo("Resultado", resultados)
        else:
            messagebox.showinfo("Resultado", "No se encontraron barriles.")

    # Botón para agregar barril
    btn_agregar = tk.Button(ventana, text="Agregar Barril", command=agregar)
    btn_agregar.pack(pady=10)

    # Botón para eliminar barril
    btn_eliminar = tk.Button(ventana, text="Eliminar Barril", command=eliminar)
    btn_eliminar.pack(pady=10)

    # Botón para actualizar barril
    btn_actualizar = tk.Button(ventana, text="Actualizar Barril", command=actualizar)
    btn_actualizar.pack(pady=10)

    # Botón para mostrar barriles
    btn_mostrar = tk.Button(ventana, text="Mostrar Barriles", command=mostrar_barriles)
    btn_mostrar.pack(pady=10)

    ventana.lift()
    # Iniciar la interfaz gráfica
    ventana.mainloop()

