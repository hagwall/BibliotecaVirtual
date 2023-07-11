

class Libro:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, titulo, autor, ejemplar, prestados):
        self.codigo = codigo           # Código 
        self.titulo = titulo # Descripción
        self.autor = autor # Descripción
        self.ejemplar = ejemplar       # Cantidad disponible (stock)
        self.prestados = prestados           # Precio 


    # Este método permite modificar un libro.
    def modificar(self, nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados):
        self.titulo = nuevo_titulo  # Modifica la descripción
        self.autor = nuevo_autor  # Modifica la descripción
        self.ejemplar = nuevo_ejemplar        # Modifica la cantidad
        self.prestados = nuevo_prestados            # Modifica el precio

# libro = Libro(1, 'harry poter', 'jhoson ha', 10, 2)

# print(f'{libro.codigo} | {libro.titulo} | {libro.autor} |  {libro.ejemplar} | {libro.prestados}')

# libro.modificar('Juegos del hambre','fredery j', 10, 5)
# print(f'{libro.codigo} | {libro.titulo} | {libro.autor} | {libro.ejemplar} | {libro.prestados}')


class Inventario:
    # Definimos el consctructor e inicialzamos los atributos de instancia
    def __init__(self):
        self.libros = []
         #Lista de libros en el inventario (variable de clase)
    # Este metodo permite crear objetos de la clase "Producto" agregarlos al imventario
    def agregar_libro(self, codigo, titulo, autor, ejemplar, prestados):
        nuevo_libro = Libro(codigo, titulo, autor, ejemplar, prestados)
        self.libros.append(nuevo_libro)
    
    def consultar_libro(self, codigo):
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro
        return False    

    # Este metodo permite modificar datos de libros que estan en el invetario
    # uitliza el metodo consultar_libro del invetario y modifica del libro

    def modificar_libro(self, codigo, nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados):
        libro = self.consultar_libro(codigo)
        if libro:
            libro.modificar(nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados)
           

    # Este metodo eliminara el libro indicado por codigo de la lista mantenida en el inventario
    
    def eliminar_libro(self, codigo):
        eliminar = False
        for libro in self.libros:
            if libro.codigo == codigo:
                eliminar = True
                libro_eliminar = libro
        if eliminar == True:
            self.libros.remove
            libro_eliminar(f'Libro {codigo} elminado')
        else: 
            print(f'Libro {codigo} no encontrado')


    # Este metodo imprime en la temrinal una lista con los datos de los libros que figuran en el inventario.
    def listar_libros(self):
        print("-"*50)
        print("lista de libros en el inventario:")
        print("Codigo\tTitulo\t\tAutor\tEjemplar\tPrestados")
        for libro in self.libros:
            print(f'{libro.codigo}\t{libro.titulo}\t{libro.autor}\t{libro.ejemplar}\t{libro.prestados}')
            print("-"*50)
# Principal programa

# mi_inventario = Inventario()
# mi_inventario.agregar_libro(1, 'harry usb','jhosn so', 10, 2)
# mi_inventario.agregar_libro(2, 'psico vm', 'san fede', 8, 1)
# mi_inventario.agregar_libro(3, 'ojos tc', 'arthit si', 6, 3)
# mi_inventario.agregar_libro(4, 'velero btp','sanches s', 9, 2)
# mi_inventario.agregar_libro(5, 'fisica xwo', 'ramirez son', 18, 3)


# # # # Consultar un libro
# libro = mi_inventario.consultar_libro(3)
# if libro != False:
#     print(f'libro encontrado:\nCodigo: {libro.codigo}\nTitulo:{libro.titulo}\nAutor:{libro.autor}\nEjemplar:{libro.ejemplar}\nPrestados:{libro.prestados}')
# else:
#     print("libro no encontrado")

# mi_inventario.modificar_libro(3, 'Jake al psico','Jhon kasenbas', 10, 3)

# mi_inventario.listar_libros()

# mi_inventario.eliminar_libro(4)
# mi_inventario.listar_libros()


class ListaSalida:

    def __init__(self):
        self.items = []


    def agregar(self, codigo, ejemplar, inventario):
        
        libro = inventario.consultar_libro(codigo)
        if libro is False:
            print("El libro no existe")
            return False
        
        # Verificamos que la cantidad en stock sea suficiente
        if libro.ejemplar < ejemplar:
            print("Cantidad en stock insuficiente")
            return False
        
        # Si existe y hay stock, vemos si ya existe en el carrito
        for item in self.items:
            if item.codigo == codigo:
                item.ejemplar += ejemplar
                # actualizamos la cantidad inventario
                libro = inventario.consultar_libro(codigo)
                libro.modificar(libro.titulo, libro.autor, libro.ejemplar - ejemplar, libro.prestados)
                return True
            
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Libro(codigo, libro.titulo, libro.autor, ejemplar, libro.prestados)
        self.items.append(nuevo_item)

        # Actualizamos la cantidad en el inventario
        libro = inventario.consultar_libro(codigo)
        libro.modificar(libro.titulo, libro.autor,libro.ejemplar - ejemplar, libro.prestados)
        return True
    
    # Este metodo quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, ejemplar, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if ejemplar > item.ejemplar:
                    print("Cantidad a quitar mayor a la ejemplar en el carrito")
                    return False
                item.ejemplar -= ejemplar
                if item.ejemplar == 0:
                    self.items.remove(item)
                # Actualizamos la ejemplar en el inventario
                libro = inventario.consultar_libro(codigo)
                libro.modificar(libro.titulo, libro.autor, libro.ejemplar + ejemplar, libro.prestados)
                return True
        
        print("EL producto no se encuentra en el carrito")
        return False    

    def mostrar(self):
        print("-"*50)
        print("Lista de libros en el carrito")
        print("Codigo\tTitulo\t\tAutor\t\tEjemplar\tPrestados")
        for item in self.items:
            print(f'{item.codigo}\t{item.titulo}\t{item.autor}\t{item.ejemplar}\t{item.prestados}')
            print("-"*50)

mi_inventario = Inventario()

mi_listaSalida = ListaSalida()

mi_inventario.agregar_libro(1, 'harry poter', 'jhon lennon', 10, 2)
mi_inventario.agregar_libro(2, 'luna de apolo', 'kasenbech', 20, 5)
mi_inventario.agregar_libro(3, 'historia de un loco','frank jose', 15, 3)

mi_inventario.listar_libros()

# mi_listaSalida.agregar(1,2, mi_inventario)
# mi_listaSalida.agregar(3,4, mi_inventario)


# mi_listaSalida.quitar(1,1, mi_inventario)
# mi_listaSalida.quitar(3,1, mi_inventario)

# mi_listaSalida.mostrar()
# mi_inventario.listar_libros()