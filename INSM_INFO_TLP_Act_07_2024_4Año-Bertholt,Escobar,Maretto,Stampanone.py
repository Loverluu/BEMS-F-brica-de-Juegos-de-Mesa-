import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import re
import tkinter as tk

Inicio = Tk()
Inicio.title("BEMS-Fábrica de Juegos de Mesa")
Inicio.resizable(1, 1)
app_width = 600
app_height = 200
screen_width = Inicio.winfo_screenwidth()
screen_height = Inicio.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
Inicio.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
# Añadir título
titulo_label = Label(Inicio, text="Bienvenidos", font=("Helvetica", 24, "bold"), bg="pink")
titulo_label.grid(row=0, column=2, columnspan=5)
Nombre = Label(Inicio, text="BEMS-Juegos de Mesa", font=("Helvetica", 24, "bold"), bg="lightblue")
Nombre.grid(row=1,column=2, columnspan=5)


def crear_Inventario1():
    connection = sqlite3.connect("Bienvenidos.db")
    return connection
# Creo la Tabla
def crear_inventario():
    connection = sqlite3.connect("Bienvenidos.db")
    cursor = connection.cursor()

    # Crear la primera tabla (LISTA)
    sql_lista = """CREATE TABLE IF NOT EXISTS LISTA (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Producto VARCHAR(50) NOT NULL,
                    Tipo VARCHAR(50) NOT NULL,
                    Precio_Unitario VARCHAR(50) NOT NULL
                   )"""
    cursor.execute(sql_lista)

    # Crear la segunda tabla (gets) con columnas Id y Producto de LISTA
    sql_gets = """CREATE TABLE IF NOT EXISTS gets (
                    Id INTEGER,
                    Cantidad_en_local VARCHAR(50) NOT NULL,
                    Stock_en_depósito VARCHAR(50) NOT NULL,
                    FOREIGN KEY (Id) REFERENCES LISTA(Id)
                  )"""
    cursor.execute(sql_gets)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    connection.close()

def Listadeproductos():
    Página = Toplevel()
    Página.title("BEMS-Lista de Productos")
    Página.resizable(1, 1)
    app_width = 545
    app_height = 550
    screen_width = Página.winfo_screenwidth()
    screen_height = Página.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    Página.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
    
        
    # Esta función es para ejecutar la sentencia que haga el usuario de sql y mostrar los resultados
    def execute_query():
        query = entry_sentencia.get().strip()
        if not query:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una sentencia SQL.")
            return
        try: 
            connection = sqlite3.connect("Bienvenidos.db")
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            # Para limpiar el treeview
            for item in tree.get_children():
                tree.delete(item)
            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                tree["columns"] = columns
                tree["show"] = "headings"
                for col in columns:
                    tree.heading(col, text=col)
                for row in rows:
                    tree.insert("", "end", values=row)
            connection.close()
            messagebox.showinfo("Resultado", "La consulta se ejecutó correctamente.")
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))

    def funcion_c():
        conexion = crear_Inventario1()
        cursor = conexion.cursor()
        sql = "SELECT * FROM LISTA ORDER BY Id DESC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for item in tree.get_children():
            tree.delete(item)
        tree.grid(column=0, row=2, columnspan=5)
        for row in rows:
            tree.insert("", index=1, text=row[0], values=[row[1], row[2], row[3]])
        conexion.commit()

    def Crear_R(Producto, Tipo, PrecioU):
        if (Reg_Muestra(Producto) and Reg_Muestra(Tipo) and int(PrecioU)):
            conexion = crear_Inventario1()
            cursor = conexion.cursor()
            data = (Producto.upper(), Tipo.capitalize(), PrecioU)
            sql = "INSERT INTO LISTA (Producto, Tipo, Precio_Unitario) VALUES (?, ?, ?)"
            try:
                cursor.execute(sql, data)
                conexion.commit()
                funcion_c()
                messagebox.showinfo(title="Producto agregado", message=f"El producto {Producto} tipo {Tipo} con un costo Unitario de ${PrecioU} fue agregado correctamente")
                FieldCleaning()
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Se ha producido un error: {e}")
        else:
            messagebox.showerror(title="Error", message="Caracteres de los campos incorrectos. Revise!")

    def Borrar_R():
        try:
            Reg_Borrar = tree.selection()
            if not Reg_Borrar:
                messagebox.showwarning("Selección requerida", "Por favor, seleccione una casilla para eliminar.")
                return
            item = tree.item(Reg_Borrar)
            id_del = item["text"]
            Rta = messagebox.askquestion("Eliminar producto", f"¿Está seguro que desea eliminar el producto {id_del}?")
            if Rta == "yes":
                conexion = crear_Inventario1()
                cursor = conexion.cursor()
                sql = "DELETE FROM LISTA WHERE Id = ?;"
                data = (id_del,)
                cursor.execute(sql, data)
                conexion.commit()
                tree.delete(Reg_Borrar)
                messagebox.showinfo("Producto eliminado con éxito", f"El producto {id_del} fue borrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")

    def Mod_R(Producto, Tipo, PrecioU, mi_Id):
        if (Reg_Muestra(Producto) and Reg_Muestra(Tipo) and int(PrecioU)):
            conexion = crear_Inventario1()
            cursor = conexion.cursor()
            data = (Producto.upper(), Tipo.capitalize(), PrecioU, mi_Id)
            sql = "UPDATE LISTA SET Producto=?, Tipo=?, Precio_Unitario=? WHERE Id=?;"
            try:
                cursor.execute(sql, data)
                conexion.commit()
                funcion_c()
                FieldCleaning()
                messagebox.showinfo(title="Producto modificado", message=f"El producto {Producto} tipo {Tipo} de costo unitario de ${PrecioU} fue modificado correctamente")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Se ha producido un error: {e}")
        else:
            messagebox.showerror(title="Error", message="Caracteres de los campos incorrectos. Revise!")

    def Reg_Muestra(cadena):
        patron_Muestra = r"[a-zA-Z\s]+(-[^\W\d_]+)?$"
        return bool(re.match(patron_Muestra, cadena))

    def FieldCleaning():   
        entry_Producto.delete(0, END)
        entry_Tipo.delete(0, END)
        entry_PrecioU.delete(0, END)
        entry_Codi.delete(0, END)

    def Sel_Reg_Clic(event):
        item = tree.selection()
        if item:
            item = tree.item(item)
            var_indu = item["text"]
            item_values = item["values"]
            var_prod = item_values[0]
            var_ti = item_values[1]
            var_pre = item_values[2]
            var_Producto.set(var_prod)
            var_Tipo.set(var_ti)
            var_PrecioU.set(var_pre)
            var_prdus.set(var_indu)

    var_Producto = StringVar()
    var_Tipo = StringVar()
    var_PrecioU = IntVar()
    var_prdus = IntVar()
    var_sentencia = StringVar()

    Producto = Label(Página, text="Producto")
    Producto.grid(row=4, column=0, sticky=W + E)
    Tipo = Label(Página, text="Tipo")
    Tipo.grid(row=5, column=0, sticky=W + E)
    Precio = Label(Página, text="Precio Unitario")
    Precio.grid(row=6, column=0, sticky=W + E)
    Elementos = Label(Página, text="Número del producto encontrado")
    Elementos.grid(row=7, column=0, sticky=W + E)
    sentencia = Label(Página, text="Sentencia SQL")
    sentencia.grid(row=8, column=0, sticky=W + E)

    entry_Producto = Entry(Página, textvariable=var_Producto, width=25)
    entry_Producto.config(fg="red", justify="center")
    entry_Producto.grid(row=4, column=1)
    entry_Tipo = Entry(Página, textvariable=var_Tipo, width=25)
    entry_Tipo.config(fg="red", justify="center")
    entry_Tipo.grid(row=5, column=1)
    entry_PrecioU = Entry(Página, textvariable=var_PrecioU, width=15)
    entry_PrecioU.config(fg="red", justify="center")
    entry_PrecioU.grid(row=6, column=1)
    entry_Codi = Entry(Página, textvariable=var_prdus, state=DISABLED, width=5)
    entry_Codi.config(justify="center")
    entry_Codi.grid(row=7, column=1)
    entry_sentencia = Entry(Página, textvariable=var_sentencia, width=25)
    entry_sentencia.config(justify="center")
    entry_sentencia.grid(row=8, column=1)

    textTest = Text(Página, height=0, width=50)
    textTest.insert("1.0", "Selecciona qué hacer con la información")
    textTest["state"] = "disabled"
    textTest.grid(row=3, column=0, columnspan=3)

    titulo = Label(Página, text="BEMS-Productos", bg="DeepPink", fg="black", height=1, width=70)
    titulo.grid(row=0, column=0, columnspan=5, padx=1, pady=1, sticky=W + E)

    boton_create = Button(Página, text="Create", command=lambda: Crear_R(var_Producto.get(), var_Tipo.get(), var_PrecioU.get()))
    boton_create.grid(row=3, column=4, sticky="e", padx=10, pady=10)
    boton_read = Button(Página, text="Read", command=funcion_c)
    boton_read.grid(row=4, column=4, sticky="e", padx=10, pady=10)
    boton_update = Button(Página, text="Update", command=lambda: Mod_R(var_Producto.get(), var_Tipo.get(), var_PrecioU.get(), var_prdus.get()))
    boton_update.grid(row=5, column=4, sticky="e", padx=10, pady=10)
    boton_delete = Button(Página, text="Delete", command=Borrar_R)
    boton_delete.grid(row=6, column=4, sticky="e", padx=10, pady=10)
    boton_clean = Button(Página, text="Clean", command=FieldCleaning)
    boton_clean.grid(row=7, column=4, sticky="e", padx=10, pady=10)
    boton_sentencia = Button(Página, text="Aceptar Sentencia", command=execute_query)
    boton_sentencia.grid(row=8, column=4, sticky="e", padx=10, pady=10)

    tree = ttk.Treeview(Página)
    tree["columns"] = ("Producto", "Tipo", "Precio Unitario")
    tree.column("#0", width=50, minwidth=50, anchor=W)
    tree.column("Producto", width=80, minwidth=50, anchor=W)
    tree.column("Tipo", width=80, minwidth=80, anchor=W)
    tree.column("Precio Unitario", width=60, minwidth=60, anchor=W)
    tree.heading("#0", text="Id")
    tree.heading("Producto", text="Producto")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.grid(column=0, row=2, columnspan=5)
    tree.bind('<ButtonRelease-1>', Sel_Reg_Clic)

    # Creo Funciones Auxiliares
    # ------------------------------------------------------------------------
    def SMS_Clean():
        for item in tree.get_children():
            tree.delete(item)
            tree.grid(column=0, row=2, columnspan=5)
            FieldCleaning()

    def AppExit():
        Rta = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la app?")
        if Rta == "yes":
            Página.destroy()  # So as you just want to quit the program so you should use root.destroy() as it will it stop the mainloop()

    boton_cerrar = ttk.Button(Página, text="Cerrar ventana", command=Página.destroy)
    boton_cerrar.grid(row=9, column=4)

def GestionCantidadStock():
    Página = Toplevel()
    Página.title("BEMS-Gestión de Cantidad y Stock")
    Página.resizable(1, 1)
    app_width = 500
    app_height = 400
    screen_width = Página.winfo_screenwidth()
    screen_height = Página.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    Página.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    notebook = ttk.Notebook(Página)
    notebook.pack(expand=True, fill="both")

    tab1 = Frame(notebook)
    tab2 = Frame(notebook)
    tab3 = Frame(notebook)
    tab4= Frame(notebook)

    notebook.add(tab1, text='Gestión de Stock')
    notebook.add(tab2, text='Pedidos y ventas')
    notebook.add(tab3, text='Compras')
    notebook.add(tab4, text="Local y depósito")
    

    # Definir las funciones para actualizar y mostrar datos
    def funcion_c():
            try:
                conexion = sqlite3.connect("Bienvenidos.db")
                cursor = conexion.cursor()
                # Consulta para obtener los datos de LISTA y gets
                sql = """SELECT l.Id, l.Producto, COALESCE(g.Cantidad_en_local, ''), COALESCE(g.Stock_en_depósito, '')
                        FROM LISTA l LEFT JOIN gets g ON l.Id = g.Id ORDER BY l.Id DESC"""
                cursor.execute(sql)
                rows = cursor.fetchall()

                # Limpiar el treeview
                for item in tree.get_children():
                    tree.delete(item)

                # Mostrar datos en el treeview
                for row in rows:
                    tree.insert("", "end", values=row)

                conexion.close()  # Cerrar conexión después de usarla

            except Exception as e:
                messagebox.showerror("Error", f"Error al leer datos: {e}")
    def actualizar_stock():
        id_producto = entry_id_producto.get()
        cantidad_local = entry_cantidad_local.get()
        stock_deposito = entry_stock_deposito.get()

        if not id_producto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto.")
            return

        try:
            cantidad_local = int(cantidad_local) if cantidad_local else None
            stock_deposito = int(stock_deposito) if stock_deposito else None

            connection = sqlite3.connect("Bienvenidos.db")
            cursor = connection.cursor()

            # Verificar si el producto ya existe en la tabla gets
            cursor.execute("SELECT Id FROM gets WHERE Id = ?", (id_producto,))
            exists = cursor.fetchone()

            if exists:
                if cantidad_local is not None:
                    cursor.execute("UPDATE gets SET Cantidad_en_local = ? WHERE Id = ?", (cantidad_local, id_producto))
                if stock_deposito is not None:
                    cursor.execute("UPDATE gets SET Stock_en_depósito = ? WHERE Id = ?", (stock_deposito, id_producto))
            else:
                if cantidad_local is not None and stock_deposito is not None:
                    cursor.execute("INSERT INTO gets (Id, Cantidad_en_local, Stock_en_depósito) VALUES (?, ?, ?)", 
                                   (id_producto, cantidad_local, stock_deposito))
                elif cantidad_local is not None:
                    cursor.execute("INSERT INTO gets (Id, Cantidad_en_local) VALUES (?, ?)", 
                                   (id_producto, cantidad_local))
                elif stock_deposito is not None:
                    cursor.execute("INSERT INTO gets (Id, Stock_en_depósito) VALUES (?, ?)", 
                                   (id_producto, stock_deposito))

            connection.commit()
            messagebox.showinfo("Actualización exitosa", "La cantidad y el stock se han actualizado correctamente.")

            # Refrescar los datos en el treeview después de la actualización
            funcion_c()

        except ValueError:
            messagebox.showerror("Error", "La cantidad y el stock deben ser números enteros.")
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            connection.close()

    # Widgets de la primera pestaña (Gestión de Stock)
    Label(tab1, text="ID del Producto:").grid(row=0, column=0, sticky=W + E)
    Label(tab1, text="Cantidad en Local:").grid(row=1, column=0, sticky=W + E)
    Label(tab1, text="Stock en Depósito:").grid(row=2, column=0, sticky=W + E)

    entry_id_producto = Entry(tab1)
    entry_id_producto.grid(row=0, column=1)
    entry_cantidad_local = Entry(tab1)
    entry_cantidad_local.grid(row=1, column=1)
    entry_stock_deposito = Entry(tab1)
    entry_stock_deposito.grid(row=2, column=1)

    Button(tab1, text="Actualizar", command=actualizar_stock, bg="pink", fg="black").grid(row=3, column=0, columnspan=2, sticky=W + E)

    tree = ttk.Treeview(tab1)
    tree["columns"] = ("Id", "Producto", "Cantidad_en_local", "Stock_en_depósito")
    tree.column("#0", width=0, stretch=NO)
    tree.column("Id", width=50, minwidth=50, anchor=W)
    tree.column("Producto", width=150, minwidth=80, anchor=W)
    tree.column("Cantidad_en_local", width=120, minwidth=80, anchor=W)
    tree.column("Stock_en_depósito", width=120, minwidth=80, anchor=W)
    tree.heading("#0", text="", anchor=W)
    tree.heading("Id", text="Id", anchor=W)
    tree.heading("Producto", text="Producto", anchor=W)
    tree.heading("Cantidad_en_local", text="Cantidad en Local", anchor=W)
    tree.heading("Stock_en_depósito", text="Stock en Depósito", anchor=W)
    tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    funcion_c()  # Mostrar datos al abrir la página

    boton_cerrar = ttk.Button(tab1, text="Cerrar ventana", command=Página.destroy)
    boton_cerrar.grid(row=5, column=1, sticky="e", padx=10, pady=10)
    
    # Contenido de la Pestaña 2
    def calcular_precio_total_tab2():
        id_producto = entry_id_producto_tab2.get()
        cantidad = entry_cantidad_tab2.get()
        if not id_producto or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto y la cantidad.")
            return

        try:
            cantidad = int(cantidad)

            conexion = sqlite3.connect("Bienvenidos.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT Producto, Precio_Unitario FROM LISTA WHERE Id = ?", (id_producto,))
            producto = cursor.fetchone()

            if producto:
                nombre_producto, precio_unitario = producto
                precio_unitario = float(precio_unitario)  # Asegúrate de que precio_unitario sea un número
                precio_total = cantidad * precio_unitario

                etiqueta_pedido_tab2.config(text=f"Su pedido del producto {nombre_producto} de {cantidad} unidades, tiene un precio total de {precio_total:.2f}")

            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto con el ID ingresado.")
            
            conexion.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            conexion.close()

    # Función para realizar la venta en la pestaña 2
    def realizar_venta_tab2():
        id_producto = entry_id_producto_tab2.get()
        cantidad = entry_cantidad_tab2.get()
        if not id_producto or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto y la cantidad.")
            return

        try:
            cantidad = int(cantidad)

            conexion = sqlite3.connect("Bienvenidos.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT Cantidad_en_local FROM gets WHERE Id = ?", (id_producto,))
            stock_actual = cursor.fetchone()

            if stock_actual:
                stock_actual = int(stock_actual[0])  # Convertir a entero

                if stock_actual >= cantidad:
                    nuevo_stock = stock_actual - cantidad
                    cursor.execute("UPDATE gets SET Cantidad_en_local = ? WHERE Id = ?", (nuevo_stock, id_producto))
                    messagebox.showinfo("Venta exitosa", f"Venta realizada. Nuevo stock en local: {nuevo_stock} unidades.")
                else:
                    messagebox.showwarning("Advertencia", "Stock insuficiente para realizar la venta.")

            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto con el ID ingresado.")
            
            conexion.commit()
            funcion_c()  # Actualizar datos en el treeview después de la venta
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            conexion.close()
            calcular_precio_total_tab2()

    Label(tab2, text="ID del Producto:").grid(row=0, column=0, sticky=W + E)
    Label(tab2, text="Cantidad:").grid(row=1, column=0, sticky=W + E)

    entry_id_producto_tab2 = Entry(tab2)
    entry_id_producto_tab2.grid(row=0, column=1)
    entry_cantidad_tab2 = Entry(tab2)
    entry_cantidad_tab2.grid(row=1, column=1)

    Button(tab2, text="Calcular Precio", command=calcular_precio_total_tab2,bg="pink", fg="black").grid(row=2, column=0, columnspan=2, sticky=W + E)
    Button(tab2, text="Realizar Venta", command=realizar_venta_tab2,bg="pink", fg="black").grid(row=3, column=0, columnspan=2, sticky=W + E)

    etiqueta_pedido_tab2 = Label(tab2, text="")
    etiqueta_pedido_tab2.grid(row=4, column=0, columnspan=2, sticky=W + E)

   # Contenido de la Pestaña 3 (Realiza compra)
    def calcular_precio_total1():
        id_producto1 = entry_id_producto_pedido.get()
        cantidad1 = entry_cantidad_pedido.get()

        if not id_producto1 or not cantidad1:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto y la cantidad.")
            return

        try:
            cantidad1 = int(cantidad1)

            conexion = sqlite3.connect("Bienvenidos.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT Producto, Precio_Unitario FROM LISTA WHERE Id = ?", (id_producto1,))
            producto = cursor.fetchone()

            if producto:
                nombre_producto, precio_unitario = producto
                precio_unitario = float(precio_unitario)  # Asegúrate de que precio_unitario sea un número
                precio_total = cantidad1 * precio_unitario

                etiqueta_pedido.config(text=f"La posible compra del producto {nombre_producto} de {cantidad1} unidades, tendrá un precio total de {precio_total:.2f}")

            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto con el ID ingresado.")
            
            conexion.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            conexion.close()

    def realizar_compra():
        id_producto = entry_id_producto_pedido.get()
        cantidad = entry_cantidad_pedido.get()

        if not id_producto or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto y la cantidad.")
            return

        try:
            cantidad = int(cantidad)

            conexion = sqlite3.connect("Bienvenidos.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT Stock_en_depósito FROM gets WHERE Id = ?", (id_producto,))
            stock_actual = cursor.fetchone()

            if stock_actual:
                stock_actual = int(stock_actual[0])  # Convertir a entero
                nuevo_stock = stock_actual + cantidad

                cursor.execute("UPDATE gets SET Stock_en_depósito = ? WHERE Id = ?", (nuevo_stock, id_producto))
                messagebox.showinfo("Compra realizada", f"Se han obtenido {cantidad} unidades del producto {id_producto}. Nuevo stock: {nuevo_stock}")
            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto con el ID ingresado.")
            
            conexion.commit()
            funcion_c()  # Actualizar datos en el treeview después de la venta

        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            conexion.close()

    tk.Label(tab3, text="ID del Producto:").grid(row=0, column=0, sticky=tk.W)
    tk.Label(tab3, text="Cantidad:").grid(row=1, column=0, sticky=tk.W)

    entry_id_producto_pedido = tk.Entry(tab3)
    entry_id_producto_pedido.grid(row=0, column=1)
    entry_cantidad_pedido = tk.Entry(tab3)
    entry_cantidad_pedido.grid(row=1, column=1)

    tk.Button(tab3, text="Calcular Precio", command=calcular_precio_total1,bg="pink", fg="black").grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)
    tk.Button(tab3, text="Realizar Compra", command=realizar_compra,bg="pink", fg="black").grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

    etiqueta_pedido = tk.Label(tab3, text="")
    etiqueta_pedido.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E)
    
    # Definir tree_tab4 globalmente
    tree_tab4 = None

    # Contenido de la Pestaña 4
    def transferir_stock():
        global tree_tab4  # Acceder a la variable global tree_tab4
        
        id_producto = entry_id_producto_tab4.get()
        cantidad_transferir = entry_cantidad_transferir.get()

        if not id_producto or not cantidad_transferir:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del producto y la cantidad a transferir.")
            return

        try:
            cantidad_transferir = int(cantidad_transferir)

            conexion = sqlite3.connect("Bienvenidos.db")
            cursor = conexion.cursor()

            # Verificar si el producto existe en la tabla gets y obtener el stock en depósito
            cursor.execute("SELECT Stock_en_depósito FROM gets WHERE Id = ?", (id_producto,))
            stock_deposito = cursor.fetchone()

            if stock_deposito:
                stock_deposito = int(stock_deposito[0])  # Convertir a entero

                # Verificar si hay suficiente stock en depósito para la transferencia
                if stock_deposito >= cantidad_transferir:
                    # Actualizar la cantidad en local y en depósito
                    cursor.execute("UPDATE gets SET Stock_en_depósito = Stock_en_depósito - ?, Cantidad_en_local = Cantidad_en_local + ? WHERE Id = ?", 
                                (cantidad_transferir, cantidad_transferir, id_producto))
                    messagebox.showinfo("Transferencia realizada", f"Se han transferido {cantidad_transferir} unidades del producto {id_producto} al local.")
                    funcion_c()  # Actualizar datos en el treeview después de la transferencia
                else:
                    messagebox.showwarning("Advertencia", "Stock insuficiente en depósito para la transferencia.")

            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto con el ID ingresado.")

            conexion.commit()
        except ValueError:
            messagebox.showerror("Error", "La cantidad a transferir debe ser un número entero.")
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error: {e}")
        finally:
            conexion.close()

    # Resto del código de la pestaña 4
    Label(tab4, text="ID del Producto:").grid(row=0, column=0, sticky=W + E)
    Label(tab4, text="Cantidad a Transferir:").grid(row=1, column=0, sticky=W + E)

    entry_id_producto_tab4 = Entry(tab4)
    entry_id_producto_tab4.grid(row=0, column=1)
    entry_cantidad_transferir = Entry(tab4)
    entry_cantidad_transferir.grid(row=1, column=1)

    Button(tab4, text="Transferir Stock", command=transferir_stock,bg="pink", fg="black").grid(row=2, column=0, columnspan=2, sticky=W + E)

    Button(tab4, text="Actualizar", command=funcion_c,bg="red", fg="black").grid(row=3, column=1, sticky="e", padx=10, pady=10)
    boton_cerrar_tab4 = ttk.Button(tab4, text="Cerrar ventana", command=Página.destroy)
    boton_cerrar_tab4.grid(row=4, column=1, sticky="e", padx=10, pady=10)
    
    Página.mainloop()

prod=Label(Inicio, text="Lista de Productos")
prod.grid(row=6, column=1)
ges=Label(Inicio, text="Sistema de Inventario")
ges.grid(row=7, column=1)

boton_listaproduc = ttk.Button(Inicio, text="Productos", command=Listadeproductos)
boton_listaproduc.grid(row=6, column=2, sticky="e", padx=15, pady=15)
boton_inven = ttk.Button(Inicio, text="Inventario", command=GestionCantidadStock)
boton_inven.grid(row=7, column=2, sticky="e", padx=15, pady=15)

Inicio.mainloop()