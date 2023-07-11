import sqlite3

DATABASE = 'inventario3.db'

def get_db_connection():
    print("Obteniendo conexion...")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    print("Creando tabla de libros...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
        codigo INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ejemplar INTEGER NOT NULL,
        prestados INTEGER NOT NULL
        )''')
    conn.commit()
    cursor.close()
    conn.close()

def create_database():
    print("Creando la BD...")
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

create_database()

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
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor() #Lista de libros en el inventario3 (variable de clase)
    # Este metodo permite crear objetos de la clase "Producto" agregarlos al imventario
    def agregar_libro(self, codigo, titulo, autor, ejemplar, prestados):
        libro_existente = self.consultar_libro(codigo)
        if libro_existente:
            print("Ya existe un libro con ese nombre") 
            return False
        nuevo_libro = Libro(codigo, titulo, autor, ejemplar, prestados)
        sql = f'INSERT INTO libros VALUES ({codigo}, "{titulo}", "{autor}", {ejemplar}, {prestados});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
    
    def consultar_libro(self, codigo):
        sql = f'SELECT * FROM libros WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, titulo, autor, ejemplar, prestados = row
            return Libro(codigo, titulo, autor, ejemplar, prestados)
        return False    

    # Este metodo permite modificar datos de libros que estan en el invetario
    # uitliza el metodo consultar_libro del invetario y modifica del libro

    def modificar_libro(self, codigo, nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados):
        libro = self.consultar_libro(codigo)
        if libro:
            libro.modificar(nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados)
            sql = f'UPDATE libros SET titulo = "{nuevo_titulo}", autor = "{nuevo_autor}", ejemplar = {nuevo_ejemplar}, prestados = {nuevo_prestados} WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()

    # Este metodo eliminara el libro indicado por codigo de la lista mantenida en el inventario3
    
    def eliminar_libro(self, codigo):
        sql = f'DELETE FROM libros WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Libro {codigo} elminado')
            self.conexion.commit()
        else:
            print(f'libro {codigo} no encontrado')

    # Este metodo imprime en la temrinal una lista con los datos de los libros que figuran en el inventario3.
    def listar_libros(self):
        print("-"*50)
        print("lista de libros en el inventario3:")
        print("Codigo\tTitulo\t\tAutor\tEjemplar\tPrestados")
        self.cursor.execute("SELECT * FROM libros")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, titulo, autor, ejemplar, prestados = row
            print(f'{codigo}\t{titulo}\t{autor}\t{ejemplar}\t{prestados}')
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
        self.conexion = sqlite3.connect('inventario3.db')
        self.cursor = self.conexion.cursor()
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
                sql = f'UPDATE libros SET ejemplar = ejemplar - {ejemplar} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True
            
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Libro(codigo, libro.titulo, libro.autor, ejemplar, libro.prestados)
        self.items.append(nuevo_item)

        # Actualizamos la cantidad en el inventario
        sql = f'UPDATE libros SET ejemplar = ejemplar - {ejemplar} WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
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
                sql = f'UPDATE libros SET ejemplar = ejemplar + {ejemplar} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True
        


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

print(mi_inventario.consultar_libro(3))
print(mi_inventario.consultar_libro(4))
mi_inventario.listar_libros()

mi_listaSalida.agregar(1,2, mi_inventario)
mi_listaSalida.agregar(3,4, mi_inventario)


mi_listaSalida.quitar(1,1, mi_inventario)
mi_listaSalida.quitar(3,1, mi_inventario)

mi_listaSalida.mostrar()
mi_inventario.listar_libros()