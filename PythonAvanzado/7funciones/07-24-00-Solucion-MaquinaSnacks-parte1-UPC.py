# Programa de Máquina de Snacks

# Definicion de la lista de snacks
snacks = [
    {'id': 1, 'nombre': 'Papas', 'precio': 30},
    {'id': 2, 'nombre': 'Refresco', 'precio': 50},
    {'id': 3, 'nombre': 'Sandwich', 'precio': 120}
]

# Lista de productos (vacia). Son los snacks que queremos comprar
productos = []


# Falta agregar las funciones de la máquina de snacks
def mostrar_snacks():
    pass


def comprar_snack():
    pass


def mostrar_ticket():
    pass


# Programa principal
if __name__ == '__main__':
    print('*** Máquina de Snacks ***')
    # Cramos el menú
    while True:
        print(f'''Menú:
        1. Mostrar Snacks
        2. Comprar Snack
        3. Mostrar ticket
        4. Salir''')
        opcion = int(input('Escoge una opción: '))
        if opcion == 1:
            mostrar_snacks()
        elif opcion == 2:
            comprar_snack()
        elif opcion == 3:
            mostrar_ticket()
        elif opcion == 4:
            print('Regresa pronto!')
            break
        else:
            print('Opción inválida, selecciona otra opción!')