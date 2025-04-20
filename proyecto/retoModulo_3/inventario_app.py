import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox, ttk

class Producto:
    def __init__(self, nombre, cantidad, precio, categoria):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria

class GestionInventario:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.conectar()
    
    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='gestion_inventario',
                user='root',
                password='123456'  # Coloca tu contraseña si es necesario
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.crear_tabla()
        except Error as e:
            messagebox.showerror("Error", f"Error al conectar a MySQL: {e}")
            self.connection = None
            self.cursor = None
    
    def verificar_conexion(self):
        if not self.connection or not self.connection.is_connected():
            self.conectar()
        return self.connection and self.connection.is_connected()
    
    def crear_tabla(self):
        if not self.verificar_conexion():
            return False
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) UNIQUE,
                    cantidad INT,
                    precio DECIMAL(10, 2),
                    categoria VARCHAR(50)
            """)
            self.connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error al crear tabla: {e}")
            return False

    def agregar_producto(self, producto):
        if not self.verificar_conexion():
            return False
        try:
            query = "INSERT INTO productos (nombre, cantidad, precio, categoria) VALUES (%s, %s, %s, %s)"
            values = (producto.nombre, producto.cantidad, producto.precio, producto.categoria)
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "El producto con este nombre ya existe")
            return False
        except Error as e:
            messagebox.showerror("Error", f"Error al agregar producto: {e}")
            return False

    def mostrar_productos(self):
        if not self.verificar_conexion():
            return []
        try:
            self.cursor.execute("SELECT nombre, cantidad, precio, categoria FROM productos")
            return self.cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")
            return []

    def buscar_producto(self, nombre):
        if not self.verificar_conexion():
            return None
        try:
            query = "SELECT nombre, cantidad, precio, categoria FROM productos WHERE nombre = %s"
            self.cursor.execute(query, (nombre,))
            result = self.cursor.fetchone()
            if result:
                return Producto(result[0], result[1], result[2], result[3])
            return None
        except Error as e:
            messagebox.showerror("Error", f"Error al buscar producto: {e}")
            return None

    def actualizar_producto(self, nombre_original, producto):
        if not self.verificar_conexion():
            return False
        try:
            query = """
                UPDATE productos 
                SET nombre = %s, cantidad = %s, precio = %s, categoria = %s 
                WHERE nombre = %s
            """
            values = (producto.nombre, producto.cantidad, producto.precio, producto.categoria, nombre_original)
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {e}")
            return False

    def eliminar_producto(self, nombre):
        if not self.verificar_conexion():
            return False
        try:
            query = "DELETE FROM productos WHERE nombre = %s"
            self.cursor.execute(query, (nombre,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")
            return False

    def __del__(self):
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            self.connection.close()

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")
        
        self.gestion = GestionInventario()
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        
        self.crear_menu_principal()
    
    def crear_menu_principal(self):
        self.limpiar_pantalla()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=50)
        
        Label(main_frame, text="Sistema de Gestión de Inventario", 
              font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=20)
        
        buttons = [
            ("Agregar Producto", self.mostrar_agregar_producto),
            ("Mostrar Productos", self.mostrar_lista_productos),
            ("Buscar Producto", self.mostrar_buscar_producto),
            ("Actualizar Producto", self.mostrar_actualizar_producto),
            ("Eliminar Producto", self.mostrar_eliminar_producto),
            ("Salir", self.root.quit)
        ]
        
        for text, command in buttons:
            ttk.Button(main_frame, text=text, command=command, width=20).pack(pady=5)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_agregar_producto(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Agregar Nuevo Producto", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        labels = ["Nombre:", "Cantidad:", "Precio:", "Categoría:"]
        self.entries = []
        
        for i, label in enumerate(labels):
            Label(frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky='e')
            entry = Entry(frame)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.entries.append(entry)
        
        ttk.Button(frame, text="Agregar", command=self.agregar_producto).grid(row=5, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=6, columnspan=2, pady=5)
    
    def agregar_producto(self):
        nombre = self.entries[0].get()
        cantidad = self.entries[1].get()
        precio = self.entries[2].get()
        categoria = self.entries[3].get()
        
        if not all([nombre, cantidad, precio, categoria]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser entero y precio debe ser número")
            return
        
        producto = Producto(nombre, cantidad, precio, categoria)
        if self.gestion.agregar_producto(producto):
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.crear_menu_principal()
    
    def mostrar_lista_productos(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20, fill=BOTH, expand=True)
        
        Label(frame, text="Lista de Productos", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Crear Treeview
        columns = ("Nombre", "Cantidad", "Precio", "Categoría")
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Obtener y mostrar productos
        productos = self.gestion.mostrar_productos()
        for prod in productos:
            tree.insert('', 'end', values=prod)
        
        tree.pack(fill=BOTH, expand=True)
        
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).pack(pady=10)
    
    def mostrar_buscar_producto(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Buscar Producto", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        Label(frame, text="Nombre del producto:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.buscar_entry = Entry(frame)
        self.buscar_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Buscar", command=self.buscar_producto).grid(row=2, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=3, columnspan=2, pady=5)
    
    def buscar_producto(self):
        nombre = self.buscar_entry.get()
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre para buscar")
            return
        
        producto = self.gestion.buscar_producto(nombre)
        if producto:
            self.mostrar_resultado_busqueda(producto)
        else:
            messagebox.showinfo("No encontrado", "No se encontró el producto")
    
    def mostrar_resultado_busqueda(self, producto):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Resultado de Búsqueda", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        info = [
            ("Nombre:", producto.nombre),
            ("Cantidad:", producto.cantidad),
            ("Precio:", producto.precio),
            ("Categoría:", producto.categoria)
        ]
        
        for i, (label, value) in enumerate(info):
            Label(frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky='e')
            Label(frame, text=value).grid(row=i+1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=5, columnspan=2, pady=10)
    
    def mostrar_actualizar_producto(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Actualizar Producto", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        Label(frame, text="Nombre del producto a actualizar:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.actualizar_nombre_entry = Entry(frame)
        self.actualizar_nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Buscar", command=self.buscar_para_actualizar).grid(row=2, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=3, columnspan=2, pady=5)
    
    def buscar_para_actualizar(self):
        nombre = self.actualizar_nombre_entry.get()
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre para buscar")
            return
        
        producto = self.gestion.buscar_producto(nombre)
        if producto:
            self.mostrar_formulario_actualizar(producto)
        else:
            messagebox.showinfo("No encontrado", "No se encontró el producto")
    
    def mostrar_formulario_actualizar(self, producto_original):
        self.limpiar_pantalla()
        self.producto_original = producto_original
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Actualizar Producto", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        labels = ["Nombre:", "Cantidad:", "Precio:", "Categoría:"]
        valores = [
            producto_original.nombre,
            producto_original.cantidad,
            producto_original.precio,
            producto_original.categoria
        ]
        
        self.actualizar_entries = []
        for i, (label, valor) in enumerate(zip(labels, valores)):
            Label(frame, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky='e')
            entry = Entry(frame)
            entry.insert(0, valor)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.actualizar_entries.append(entry)
        
        ttk.Button(frame, text="Actualizar", command=self.actualizar_producto).grid(row=5, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=6, columnspan=2, pady=5)
    
    def actualizar_producto(self):
        nombre = self.actualizar_entries[0].get()
        cantidad = self.actualizar_entries[1].get()
        precio = self.actualizar_entries[2].get()
        categoria = self.actualizar_entries[3].get()
        
        if not all([nombre, cantidad, precio, categoria]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser entero y precio debe ser número")
            return
        
        producto = Producto(nombre, cantidad, precio, categoria)
        if self.gestion.actualizar_producto(self.producto_original.nombre, producto):
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.crear_menu_principal()
    
    def mostrar_eliminar_producto(self):
        self.limpiar_pantalla()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Eliminar Producto", font=('Arial', 14, 'bold')).grid(row=0, columnspan=2, pady=10)
        
        Label(frame, text="Nombre del producto a eliminar:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.eliminar_entry = Entry(frame)
        self.eliminar_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Eliminar", command=self.eliminar_producto).grid(row=2, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=3, columnspan=2, pady=5)
    
    def eliminar_producto(self):
        nombre = self.eliminar_entry.get()
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre para eliminar")
            return
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {nombre}?")
        if confirmar:
            if self.gestion.eliminar_producto(nombre):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.crear_menu_principal()
            else:
                messagebox.showinfo("Error", "No se pudo eliminar el producto")

def configurar_base_datos():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Coloca tu contraseña si es necesario
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_inventario")
        connection.commit()
        cursor.close()
        connection.close()
        print("Base de datos configurada correctamente")
    except Error as e:
        print(f"Error al configurar la base de datos: {e}")

if __name__ == "__main__":
    configurar_base_datos()
    root = Tk()
    app = InventarioApp(root)
    root.mainloop()