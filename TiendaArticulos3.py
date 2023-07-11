import sqlite3
from flask import Flask, jsonify, request

DATABASE = 'inventario3.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
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
            return jsonify({'message':' ya existe un libro con ese codigo'}), 4000
        nuevo_libro = Libro(codigo, titulo, autor, ejemplar, prestados)
        sql = f'INSERT INTO libros VALUES ({codigo}, "{titulo}", "{autor}", {ejemplar}, {prestados});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message':'Producto agregado correctamente.'}), 200
    
    def consultar_libro(self, codigo):
        sql = f'SELECT * FROM libros WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, titulo, autor, ejemplar, prestados = row
            return Libro(codigo, titulo, autor, ejemplar, prestados)
        return None    

    # Este metodo permite modificar datos de libros que estan en el invetario
    # uitliza el metodo consultar_libro del invetario y modifica del libro

    def modificar_libro(self, codigo, nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados):
        libro = self.consultar_libro(codigo)
        if libro:
            libro.modificar(nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados)
            sql = f'UPDATE libros SET titulo = "{nuevo_titulo}", autor = "{nuevo_autor}", ejemplar = {nuevo_ejemplar}, prestados = {nuevo_prestados} WHERE codigo = {codigo};'
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Libro modificado correctamente.'}), 200
        return jsonify({'message': 'Libro no encontrado.'}), 404
    # Este metodo eliminara el libro indicado por codigo de la lista mantenida en el inventario3
    
    def eliminar_libro(self, codigo):
        sql = f'DELETE FROM libros WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Libro eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404


    # Este metodo imprime en la temrinal una lista con los datos de los libros que figuran en el inventario3.
    def listar_libros(self):
        self.cursor.execute("SELECT * FROM libros")
        rows = self.cursor.fetchall()
        libros = []
        for row in rows:
            codigo, titulo, autor, ejemplar, prestados = row
            libro = {'codigo': codigo, 'titulo': titulo, 'autor': autor, 'ejemplar': ejemplar, 'prestados': prestados}
            libros.append(libro)
        return jsonify(libros), 200
            # print(f'{codigo}\t{titulo}\t{autor}\t{ejemplar}\t{prestados}')
            # print("-"*50)
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
        # self.conexion = sqlite3.connect('inventario3.db')
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.items = []

    def agregar(self, codigo, ejemplar, inventario):
        
        libro = inventario.consultar_libro(codigo)
        if libro is None:
            return jsonify({'message': 'El libro no existe.'}), 404
        if libro.ejemplar < ejemplar:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400
        
        # Verificamos que la ejemplar en stock sea suficiente
        
        # Si existe y hay stock, vemos si ya existe en el carrito
        for item in self.items:
            if item.codigo == codigo:
                item.ejemplar += ejemplar
                sql = f'UPDATE libros SET ejemplar = ejemplar - {ejemplar} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'LIbro agregado al carrito correctamente.'}), 20
            
        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Libro(codigo, libro.titulo, libro.autor, ejemplar, libro.prestados)
        self.items.append(nuevo_item)

        # Actualizamos la cantidad en el inventario
        sql = f'UPDATE libros SET ejemplar = ejemplar - {ejemplar} WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'LIbro agregado al carrito correctamente.'}), 200
    
    # Este metodo quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, ejemplar, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if ejemplar > item.ejemplar:
                    return jsonify({'message': 'Ejemplar a quitar mayor a la ejemplar en el listaSalida.'}), 400
                item.ejemplar -= ejemplar
                if item.ejemplar == 0:
                    self.items.remove(item)
                # Actualizamos la ejemplar en el inventario
                sql = f'UPDATE libros SET ejemplar = ejemplar + {ejemplar} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Libro quitado del listaSalida correctamente.'}), 200
        return jsonify({'message': 'El libro no se encuentra en el ListaSalida.'}), 404
        

    def mostrar(self):
        # print("-"*50)
        # print("Lista de libros en el carrito")
        # print("Codigo\tTitulo\t\tAutor\t\tEjemplar\tPrestados")
        libros_listaSalida = []
        for item in self.items:
            libro = {'codigo': item.codigo, 'titulo': item.titulo, 'autor': item.autor, 'ejemplar': item.ejemplar, 'prestados': item.prestados}
            libros_listaSalida.append(libro)
        return jsonify(libros_listaSalida), 200
            # print(f'{item.codigo}\t{item.titulo}\t{item.autor}\t{item.ejemplar}\t{item.prestados}')
            # print("-"*50)


app = Flask(__name__)

listaSalida = ListaSalida()
inventario = Inventario()

@app.route('/libros/<int:codigo>', methods=['GET'])
def obtener_libro(codigo):
    libro = inventario.consultar_libro(codigo)
    if libro:
        return jsonify({
            'codigo': libro.codigo, 
            'titulo': libro.titulo, 
            'autor': libro.autor, 
            'ejemplar': libro.ejemplar, 
            'prestados': libro.prestados
        }), 200
    return jsonify({'message': 'Libro no encontrado.'}), 404

@app.route('/')
def index():
    return 'API de inventario'

@app.route('/libros', methods=['GET'])
def obtener_libros():
    return inventario.listar_libros()

@app.route('/libros', methods=['POST'])
def agregar_libro():
    codigo = request.json.get('codigo')
    titulo = request.json.get('titulo')
    autor = request.json.get('autor')
    ejemplar = request.json.get('ejemplar')
    prestados = request.json.get('prestados')
    return inventario.agregar_libro(codigo, titulo, autor, ejemplar, prestados)

@app.route('/libros/<int:codigo>', methods=['PUT'])
def modificar_libro(codigo):
    nuevo_titulo = request.json.get('titulo')
    nuevo_autor = request.json.get('autor')
    nuevo_ejemplar = request.json.get('ejemplar')
    nuevo_prestados = request.json.get('prestados')
    return inventario.modificar_libro(codigo, nuevo_titulo, nuevo_autor, nuevo_ejemplar, nuevo_prestados)

@app.route('/libros/<int:codigo>', methods=['DELETE'])
def eliminar_libro(codigo):
    return inventario.eliminar_libro(codigo)

@app.route('/listaSalida', methods=['POST'])
def agregar_listaSalida():
    codigo = request.json.get('codigo')
    ejemplar = request.json.get('ejemplar')
    inventario = Inventario()
    return listaSalida.agregar(codigo, ejemplar, inventario)

@app.route('/listaSalida', methods=['DELETE'])
def quitar_listaSalida():
    codigo = request.json.get('codigo')
    ejemplar = request.json.get('ejemplar')
    inventario = Inventario()
    return listaSalida.quitar(codigo, ejemplar, inventario)

@app.route('/listaSalida', methods=['GET'])
def obtener_listaSalida():
    return listaSalida.mostrar()

if __name__ == '__main__':
    app.run()