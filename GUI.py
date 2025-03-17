import tkinter as tk
from tkinter import ttk, messagebox
from models import Barril
from CRUD import actualizar_barril, obtener_barriles, borrar_barril, crear_barril

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Cervecería Ethel")
    ventana.geometry("800x500")

    # Función para refrescar los datos en la tabla
    def cargar_barriles():
        for row in tree.get_children():
            tree.delete(row)

        barriles = obtener_barriles()

        for barril in barriles:
            tree.insert("", tk.END, values=(barril.id, barril.tipo, barril.capacidad, barril.estado))

    # Función para abrir la ventana emergente de "Cargar"
    def abrir_ventana_cargar():
        def guardar_barril():
            tipo = entry_tipo.get()
            capacidad = entry_capacidad.get()
            estado = entry_estado.get()

            if tipo and capacidad and estado:
                try:
                    #capacidad = int(capacidad)
                    crear_barril(tipo, capacidad, estado)
                    messagebox.showinfo("Éxito", f"Barril '{tipo}' creado correctamente.")
                    cargar_barriles()
                    top.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Capacidad debe ser un número.")
            else:
                messagebox.showwarning("Campos vacíos", "Complete todos los campos.")

        top = tk.Toplevel(ventana)
        top.title("Cargar Nuevo Barril")
        top.geometry("300x250")

        tk.Label(top, text="Tipo:").pack(pady=5)
        entry_tipo = tk.Entry(top)
        entry_tipo.pack()

        tk.Label(top, text="Capacidad (L):").pack(pady=5)
        entry_capacidad = tk.Entry(top)
        entry_capacidad.pack()

        tk.Label(top, text="Estado:").pack(pady=5)
        entry_estado = tk.Entry(top)
        entry_estado.pack()

        tk.Button(top, text="Guardar", command=guardar_barril).pack(pady=20)

    # Función para eliminar el barril seleccionado
    def eliminar_barril():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un barril para eliminar.")
            return

        valores = tree.item(seleccionado, "values")
        barril_id = valores[0]

        confirmacion = messagebox.askyesno("Eliminar", f"¿Está seguro de eliminar este barril?")
        if confirmacion:
            borrar_barril(barril_id)
            cargar_barriles()
            messagebox.showinfo("Éxito", f"Barril eliminado.")

    # Función para abrir la ventana emergente de "Actualizar"
    def abrir_ventana_actualizar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un barril para actualizar.")
            return

        valores = tree.item(seleccionado, "values")
        barril_id = valores[0]
        tipo_actual = valores[1]
        capacidad_actual = valores[2]
        estado_actual = valores[3]

        def guardar_actualizacion():
            nuevo_tipo = entry_tipo.get()
            nueva_capacidad = entry_capacidad.get()
            nuevo_estado = entry_estado.get()

            if nuevo_tipo and nueva_capacidad and nuevo_estado:
                try:
                    #nueva_capacidad = int(nueva_capacidad)
                    actualizar_barril(barril_id, nuevo_tipo, nueva_capacidad,  nuevo_estado)
                    messagebox.showinfo("Éxito", f"Barril actualizado correctamente.")
                    cargar_barriles()
                    top.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Capacidad debe ser un número.")
            else:
                messagebox.showwarning("Campos vacíos", "Complete todos los campos.")

        top = tk.Toplevel(ventana)
        top.title(f"Actualizar Barril ID {barril_id}")
        top.geometry("300x250")

        tk.Label(top, text="Tipo:").pack(pady=5)
        entry_tipo = tk.Entry(top)
        entry_tipo.insert(0, tipo_actual)
        entry_tipo.pack()

        tk.Label(top, text="Capacidad (L):").pack(pady=5)
        entry_capacidad = tk.Entry(top)
        entry_capacidad.insert(0, capacidad_actual)
        entry_capacidad.pack()

        tk.Label(top, text="Estado:").pack(pady=5)
        entry_estado = tk.Entry(top)
        entry_estado.insert(0, estado_actual)
        entry_estado.pack()

        tk.Button(top, text="Guardar Cambios", command=guardar_actualizacion).pack(pady=20)

    # ===================
    # Tabla de Barriles (Treeview)
    # ===================
    columnas = ("ID", "Tipo", "Capacidad (L)", "Estado")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    # Definimos los encabezados
    tree.heading("ID", text="ID")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Capacidad (L)", text="Capacidad (L)")
    tree.heading("Estado", text="Estado")

    # Configuramos el ancho de las columnas
    tree.column("ID", width=5)
    tree.column("Tipo", width=150)
    tree.column("Capacidad (L)", width=120)
    tree.column("Estado", width=150)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollbar vertical para el treeview
    scrollbar = ttk.Scrollbar(ventana, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    # ===================
    # Botones de acción
    # ===================
    contenedor_botones = tk.Frame(ventana)
    contenedor_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

    btn_cargar = tk.Button(contenedor_botones, text="Cargar Barril", width=20, command=abrir_ventana_cargar)
    btn_cargar.pack(pady=10)

    btn_eliminar = tk.Button(contenedor_botones, text="Eliminar Barril", width=20, command=eliminar_barril)
    btn_eliminar.pack(pady=10)

    btn_actualizar = tk.Button(contenedor_botones, text="Actualizar Barril", width=20, command=abrir_ventana_actualizar)
    btn_actualizar.pack(pady=10)

    # Cargar la tabla al iniciar
    cargar_barriles()

    ventana.mainloop()
