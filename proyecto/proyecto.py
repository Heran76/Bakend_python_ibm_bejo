import re
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class GestorContactosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contactos Profesional")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Configurar estilo moderno
        self.configurar_estilo()
        
        # Variables
        self.archivo_contactos = "contactos.txt"
        self.contactos = []
        
        # Cargar contactos existentes
        self.cargar_contactos()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores modernos
        self.color_principal = "#4a6fa5"
        self.color_secundario = "#166088"
        self.color_fondo = "#f8f9fa"
        self.color_superficie = "#ffffff"
        self.color_texto = "#212121"
        self.color_accento = "#4fc3f7"
        
        # Configurar estilos
        style.configure('TFrame', background=self.color_fondo)
        style.configure('TLabel', background=self.color_fondo, foreground=self.color_texto, font=('Segoe UI', 10))
        style.configure('TButton', background=self.color_principal, foreground='white', 
                       font=('Segoe UI', 10, 'bold'), padding=6, borderwidth=0)
        style.map('TButton', 
                 background=[('active', self.color_secundario)],
                 foreground=[('active', 'white')])
        style.configure('TEntry', fieldbackground=self.color_superficie, foreground=self.color_texto,
                      font=('Segoe UI', 10), padding=5)
        style.configure('TNotebook', background=self.color_fondo)
        style.configure('TNotebook.Tab', background=self.color_fondo, foreground=self.color_texto,
                       padding=[10, 5], font=('Segoe UI', 10))
        style.map('TNotebook.Tab', 
                background=[('selected', self.color_superficie)],
                expand=[('selected', [1, 1, 1, 0])])
        
        # Estilo para el Treeview
        style.configure('Treeview', background=self.color_superficie, fieldbackground=self.color_superficie,
                       foreground=self.color_texto, rowheight=25, font=('Segoe UI', 10), borderwidth=0)
        style.configure('Treeview.Heading', background=self.color_principal, foreground='white',
                        font=('Segoe UI', 10, 'bold'), padding=5)
        style.map('Treeview', background=[('selected', self.color_accento)],
                foreground=[('selected', 'white')])
    
    def crear_interfaz(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Lista de contactos
        self.tab_lista = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lista, text="Contactos")
        self.crear_tab_lista()
        
        # Pestaña 2: Añadir contacto
        self.tab_agregar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_agregar, text="Agregar")
        self.crear_tab_agregar()
        
        # Pestaña 3: Buscar
        self.tab_buscar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_buscar, text="Buscar")
        self.crear_tab_buscar()
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)
        self.status_var.set("Sistema listo. Contactos cargados.")
    
    def crear_tab_lista(self):
        # Treeview para mostrar contactos
        self.tree = ttk.Treeview(self.tab_lista, columns=('nombre', 'telefono', 'email'), show='headings')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('telefono', text='Teléfono')
        self.tree.heading('email', text='Email')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tab_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Posicionamiento
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Botón de actualizar
        btn_actualizar = ttk.Button(self.tab_lista, text="Actualizar", command=self.actualizar_lista)
        btn_actualizar.grid(row=1, column=0, pady=10)
        
        # Configurar grid
        self.tab_lista.columnconfigure(0, weight=1)
        self.tab_lista.rowconfigure(0, weight=1)
        
        # Cargar datos
        self.actualizar_lista()
    
    def crear_tab_agregar(self):
        # Título
        lbl_titulo = ttk.Label(self.tab_agregar, text="Nuevo Contacto", font=('Segoe UI', 12, 'bold'))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos del formulario
        ttk.Label(self.tab_agregar, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.nombre_entry = ttk.Entry(self.tab_agregar)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.tab_agregar, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.telefono_entry = ttk.Entry(self.tab_agregar)
        self.telefono_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.tab_agregar, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.email_entry = ttk.Entry(self.tab_agregar)
        self.email_entry.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Botón de enviar
        btn_agregar = ttk.Button(self.tab_agregar, text="Guardar Contacto", command=self.agregar_contacto)
        btn_agregar.grid(row=4, column=1, sticky=tk.E, pady=10)
        
        # Configurar grid
        self.tab_agregar.columnconfigure(1, weight=1)
    
    def crear_tab_buscar(self):
        # Campo de búsqueda
        ttk.Label(self.tab_buscar, text="Buscar contacto:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.buscar_entry = ttk.Entry(self.tab_buscar)
        self.buscar_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Botón de buscar
        btn_buscar = ttk.Button(self.tab_buscar, text="Buscar", command=self.buscar_contacto)
        btn_buscar.grid(row=0, column=2, padx=5)
        
        # Resultados
        self.tree_resultados = ttk.Treeview(self.tab_buscar, columns=('nombre', 'telefono', 'email'), show='headings')
        self.tree_resultados.heading('nombre', text='Nombre')
        self.tree_resultados.heading('telefono', text='Teléfono')
        self.tree_resultados.heading('email', text='Email')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tab_buscar, orient=tk.VERTICAL, command=self.tree_resultados.yview)
        self.tree_resultados.configure(yscroll=scrollbar.set)
        
        # Posicionamiento
        self.tree_resultados.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)
        scrollbar.grid(row=1, column=3, sticky='ns')
        
        # Configurar grid
        self.tab_buscar.columnconfigure(1, weight=1)
        self.tab_buscar.rowconfigure(1, weight=1)
    
    def cargar_contactos(self):
        try:
            if not os.path.exists(self.archivo_contactos):
                return
            
            with open(self.archivo_contactos, 'r') as f:
                self.contactos = []
                for linea in f:
                    datos = linea.strip().split(',')
                    if len(datos) == 3:
                        self.contactos.append({
                            'nombre': datos[0],
                            'telefono': datos[1],
                            'email': datos[2]
                        })
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los contactos: {e}")
    
    def guardar_contactos(self):
        try:
            with open(self.archivo_contactos, 'w') as f:
                for contacto in self.contactos:
                    f.write(f"{contacto['nombre']},{contacto['telefono']},{contacto['email']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los contactos: {e}")
    
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar contactos
        for contacto in self.contactos:
            self.tree.insert('', tk.END, values=(
                contacto['nombre'],
                contacto['telefono'],
                contacto['email']
            ))
    
    def agregar_contacto(self):
        nombre = self.nombre_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Validaciones
        if not nombre or not telefono or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Por favor ingrese un email válido")
            return
        
        # Agregar contacto
        self.contactos.append({
            'nombre': nombre,
            'telefono': telefono,
            'email': email
        })
        
        # Guardar y actualizar
        self.guardar_contactos()
        self.actualizar_lista()
        
        # Limpiar formulario
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Contacto agregado correctamente")
        self.status_var.set("Contacto agregado correctamente")
    
    def buscar_contacto(self):
        termino = self.buscar_entry.get().strip().lower()
        
        # Limpiar resultados anteriores
        for item in self.tree_resultados.get_children():
            self.tree_resultados.delete(item)
        
        # Buscar coincidencias
        resultados = [
            c for c in self.contactos 
            if termino in c['nombre'].lower() or 
               termino in c['telefono'].lower() or 
               termino in c['email'].lower()
        ]
        
        # Mostrar resultados
        for contacto in resultados:
            self.tree_resultados.insert('', tk.END, values=(
                contacto['nombre'],
                contacto['telefono'],
                contacto['email']
            ))
        
        # Actualizar estado
        self.status_var.set(f"Se encontraron {len(resultados)} contactos")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorContactosApp(root)
    root.mainloop()