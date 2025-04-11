import re
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font

class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

class GestionContactos:
    def __init__(self):
        self.contactos = []
        self.archivo = "contactos.txt"
        self.cargar_contactos()
    
    def agregar_contacto(self, contacto):
        if not self.validar_email(contacto.email):
            raise ValueError("Formato de email inválido")
        
        if not contacto.nombre or not contacto.telefono:
            raise ValueError("Nombre y teléfono son campos requeridos")
        
        self.contactos.append(contacto)
        self.guardar_contactos()
    
    def mostrar_contactos(self):
        return self.contactos
    
    def buscar_contacto(self, nombre):
        return [c for c in self.contactos if nombre.lower() in c.nombre.lower()]
    
    def eliminar_contacto(self, contacto):
        self.contactos.remove(contacto)
        self.guardar_contactos()
    
    def validar_email(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None
    
    def guardar_contactos(self):
        try:
            with open(self.archivo, 'w') as f:
                for contacto in self.contactos:
                    f.write(f"{contacto.nombre},{contacto.telefono},{contacto.email}\n")
        except IOError as e:
            messagebox.showerror("Error", f"Error al guardar contactos: {str(e)}")
    
    def cargar_contactos(self):
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r') as f:
                    lineas = f.readlines()
                    for linea in lineas:
                        datos = linea.strip().split(',')
                        if len(datos) == 3:
                            self.contactos.append(Contacto(datos[0], datos[1], datos[2]))
        except IOError as e:
            messagebox.showerror("Error", f"Error al cargar contactos: {str(e)}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Contactos - Neomorfismo")
        self.attributes('-fullscreen', True)  # Pantalla completa
        self.gestion = GestionContactos()
        
        # Configuración de estilos neomorfismo mejorados
        self.bg_color = "#e0e5ec"
        self.button_bg = "#e0e5ec"
        self.button_active = "#d1d7e0"
        self.text_color = "#4a4a4a"
        self.highlight = "#7d8da3"
        self.entry_bg = "#ffffff"
        self.font_large = ('Helvetica', 16)
        self.font_medium = ('Helvetica', 14)
        self.font_small = ('Helvetica', 12)
        
        self.configure(bg=self.bg_color)
        self.estilo = ttk.Style()
        
        # Configurar estilos mejorados
        self.estilo.configure("TFrame", background=self.bg_color)
        self.estilo.configure("TLabel", 
                            background=self.bg_color, 
                            foreground=self.text_color, 
                            font=self.font_medium)
        self.estilo.configure("TButton", 
                            background=self.button_bg,
                            foreground=self.text_color,
                            font=self.font_medium,
                            borderwidth=0,
                            relief="flat",
                            padding=10)
        self.estilo.map("TButton",
                       background=[('active', self.button_active)],
                       relief=[('active', 'sunken')])
        
        # Crear widgets
        self.crear_widgets()
        
        # Configurar tecla ESC para salir de pantalla completa
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))
    
    def crear_widgets(self):
        # Frame principal con padding aumentado
        main_frame = ttk.Frame(self, padding=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título con fuente más grande
        titulo = ttk.Label(main_frame, 
                          text="SISTEMA DE GESTIÓN DE CONTACTOS", 
                          font=('Helvetica', 24, 'bold'))
        titulo.pack(pady=(0, 30))
        
        # Frame de botones con mayor espaciado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        # Botones más grandes con mejor padding
        btn_agregar = ttk.Button(btn_frame, text="AGREGAR CONTACTO", command=self.agregar_contacto)
        btn_agregar.pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        btn_buscar = ttk.Button(btn_frame, text="BUSCAR CONTACTO", command=self.buscar_contacto)
        btn_buscar.pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        btn_eliminar = ttk.Button(btn_frame, text="ELIMINAR CONTACTO", command=self.eliminar_contacto)
        btn_eliminar.pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        # Botón para salir
        btn_salir = ttk.Button(btn_frame, text="SALIR", command=self.destroy)
        btn_salir.pack(side=tk.RIGHT, padx=15, ipadx=20, ipady=10)
        
        # Treeview con fuentes más grandes
        self.tree = ttk.Treeview(main_frame, 
                                columns=("Nombre", "Teléfono", "Email"), 
                                show="headings",
                                height=20)
        self.tree.heading("Nombre", text="NOMBRE", anchor=tk.CENTER)
        self.tree.heading("Teléfono", text="TELÉFONO", anchor=tk.CENTER)
        self.tree.heading("Email", text="EMAIL", anchor=tk.CENTER)
        self.tree.column("Nombre", width=300, anchor=tk.CENTER)
        self.tree.column("Teléfono", width=200, anchor=tk.CENTER)
        self.tree.column("Email", width=400, anchor=tk.CENTER)
        
        # Configurar estilo del Treeview mejorado
        self.estilo.configure("Treeview", 
                            background=self.entry_bg,
                            foreground=self.text_color,
                            fieldbackground=self.entry_bg,
                            font=self.font_small,
                            rowheight=35)
        self.estilo.configure("Treeview.Heading", 
                            background=self.highlight,
                            foreground="Black",
                            font=('Helvetica', 18, 'bold'),
                            padding=10)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Actualizar lista
        self.actualizar_lista()
    
    def actualizar_lista(self, contactos=None):
        self.tree.delete(*self.tree.get_children())
        contactos = contactos if contactos else self.gestion.mostrar_contactos()
        for contacto in contactos:
            self.tree.insert("", tk.END, values=(contacto.nombre, contacto.telefono, contacto.email))
    
    def agregar_contacto(self):
        # Ventana emergente para agregar contacto
        dialog = tk.Toplevel(self)
        dialog.title("Agregar Nuevo Contacto")
        dialog.geometry("600x400")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.grab_set()
        
        # Frame principal del diálogo
        dialog_frame = ttk.Frame(dialog, padding=30)
        dialog_frame.pack(fill=tk.BOTH, expand=True)
        
        # Función para centrar la ventana
        self.centrar_ventana(dialog)
        
        # Campos del formulario con etiquetas más grandes
        ttk.Label(dialog_frame, text="Nombre:", font=self.font_medium).pack(pady=(10, 5))
        nombre_entry = ttk.Entry(dialog_frame, font=self.font_medium)
        nombre_entry.pack(fill=tk.X, padx=20, pady=5, ipady=8)
        
        ttk.Label(dialog_frame, text="Teléfono:", font=self.font_medium).pack(pady=(15, 5))
        telefono_entry = ttk.Entry(dialog_frame, font=self.font_medium)
        telefono_entry.pack(fill=tk.X, padx=20, pady=5, ipady=8)
        
        ttk.Label(dialog_frame, text="Email:", font=self.font_medium).pack(pady=(15, 5))
        email_entry = ttk.Entry(dialog_frame, font=self.font_medium)
        email_entry.pack(fill=tk.X, padx=20, pady=5, ipady=8)
        
        # Frame para botones
        btn_frame = ttk.Frame(dialog_frame)
        btn_frame.pack(pady=20)
        
        # Botón para guardar
        def guardar():
            try:
                contacto = Contacto(
                    nombre_entry.get().strip(),
                    telefono_entry.get().strip(),
                    email_entry.get().strip()
                )
                self.gestion.agregar_contacto(contacto)
                self.actualizar_lista()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Contacto agregado correctamente")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        btn_guardar = ttk.Button(btn_frame, text="GUARDAR", command=guardar, style="TButton")
        btn_guardar.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=8)
        
        # Botón para cancelar
        btn_cancelar = ttk.Button(btn_frame, text="CANCELAR", command=dialog.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=10, ipadx=20, ipady=8)
        
        # Poner foco en el primer campo
        nombre_entry.focus_set()
    
    def buscar_contacto(self):
        nombre = simpledialog.askstring("Buscar Contacto", 
                                      "Ingrese el nombre a buscar:",
                                      parent=self,
                                      font=self.font_medium)
        if nombre:
            encontrados = self.gestion.buscar_contacto(nombre)
            if encontrados:
                self.actualizar_lista(encontrados)
                messagebox.showinfo("Resultados", f"Se encontraron {len(encontrados)} contactos")
            else:
                messagebox.showinfo("Resultados", "No se encontraron contactos")
                self.actualizar_lista()
    
    def eliminar_contacto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un contacto")
            return
        
        item = self.tree.item(seleccion[0])
        nombre = item['values'][0]
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro que desea eliminar a {nombre}?",
                             icon='warning'):
            contacto = Contacto(item['values'][0], item['values'][1], item['values'][2])
            self.gestion.eliminar_contacto(contacto)
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
    
    def centrar_ventana(self, ventana):
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    app = App()
    app.mainloop()