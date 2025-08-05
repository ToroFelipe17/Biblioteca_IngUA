# GitHub Flow

from abc import ABC, abstractmethod
from datetime import datetime

# Constante para evitar duplicidad de literales
ID_LIBRO_LABEL = "ID del libro: "
ID_USUARIO_LABEL = "ID del usuario: "

# Clase Libro (SRP)
class Libro:
    """
    Representa un libro dentro de la biblioteca.
    Solo almacena y muestra la información del libro, cumpliendo así con el principio de responsabilidad única (SRP).
    """

    def __init__(self, id_libro, titulo, autor, disponible=True):
        """
        id_libro: int - Identificador único del libro.
        titulo: str - Título del libro.
        autor: str - Autor del libro.
        disponible: bool - Indica si el libro está disponible para préstamo.
        """
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def __str__(self):
        """
        Devuelve una representación legible del libro mostrando su estado.
        """
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.titulo} ({self.autor}) - {estado}"

# Clase Usuario (SRP)
class Usuario:
    """
    Modela un usuario del sistema de biblioteca.
    Se encarga solo de la información relacionada con el usuario.
    """
    def __init__(self, id_usuario, nombre):
        """
        id_usuario: int - Identificador único del usuario.
        nombre: str - Nombre completo del usuario.
        multas: int - Acumulado de multas a pagar (inicialmente 0).
        """
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.multas = 0

    def __str__(self):
        """
        Retorna la información relevante del usuario y sus multas acumuladas.
        """
        return f"{self.nombre} (ID: {self.id_usuario}), Multas: ${self.multas}"

# Clase base PrestamoBase (OCP, LSP)
class PrestamoBase(ABC):
    """
    Clase abstracta para definir el comportamiento básico de un préstamo.
    Se puede extender para distintos tipos de préstamo.
    """

    @abstractmethod
    def calcular_multa(self):
        """
        Calcula la multa asociada a un préstamo (si corresponde).
        """
        pass

# Clase Prestamo (hereda de PrestamoBase, SRP, OCP, LSP)
class Prestamo(PrestamoBase):
    """
    Modela el préstamo de un libro.
    Gestiona la información relacionada al préstamo, devolución y cálculo de multas.
    """
    DIAS_MAXIMO = 7  # Máximo de días permitidos para préstamo sin multa.
    MULTA_POR_DIA = 500  # Valor de la multa por día de atraso.

    def __init__(self, usuario, libro, fecha_prestamo=None):
        """
        usuario: Usuario - Usuario que realiza el préstamo.
        libro: Libro - Libro prestado.
        fecha_prestamo: datetime - Fecha del préstamo (si no se indica, usa la fecha actual).
        devuelto: bool - Indica si el libro fue devuelto.
        fecha_devolucion: datetime - Fecha real de devolución (None si aún no se devuelve).
        """
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.now()
        self.devuelto = False
        self.fecha_devolucion = None

    def devolver(self):
        """
        Marca el préstamo como devuelto, actualiza la fecha de devolución y disponibilidad del libro.
        """
        self.devuelto = True
        self.fecha_devolucion = datetime.now()
        self.libro.disponible = True

    def calcular_multa(self):
        """
        Calcula la multa basada en el atraso de la devolución.
        Si el préstamo no ha sido devuelto, calcula con la fecha actual.
        """
        if not self.devuelto:
            dias_prestados = (datetime.now() - self.fecha_prestamo).days
        else:
            dias_prestados = (self.fecha_devolucion - self.fecha_prestamo).days

        if dias_prestados > Prestamo.DIAS_MAXIMO:
            return (dias_prestados - Prestamo.DIAS_MAXIMO) * Prestamo.MULTA_POR_DIA
        return 0

# Interfaz abstracta para repositorio de libros (DIP)
class RepositorioLibros(ABC):
    """
    Define el contrato mínimo para cualquier repositorio de libros.
    """
    @abstractmethod
    def agregar_libro(self, libro):
        pass

    @abstractmethod
    def buscar_libro(self, criterio):
        pass

# Implementación concreta del repositorio (en memoria)
class RepositorioLibrosEnMemoria(RepositorioLibros):
    """
    Implementa el repositorio de libros usando una lista en memoria.
    """
    def __init__(self):
        """
        libros: list - Lista donde se almacenan los libros.
        """
        self.libros = []

    def agregar_libro(self, libro):
        """
        Añade un libro a la colección.
        """
        self.libros.append(libro)

    def buscar_libro(self, criterio):
        """
        Permite buscar libros por título o autor, de manera insensible a mayúsculas.
        criterio: str - Palabra clave para buscar coincidencias.
        """
        return [l for l in self.libros if criterio.lower() in l.titulo.lower() or criterio.lower() in l.autor.lower()]

# Clase principal Biblioteca (SRP, DIP)
class Biblioteca:
    """
    Orquesta la gestión de libros, usuarios y préstamos.
    Trabaja con el repositorio abstracto de libros.
    """
    def __init__(self, repo_libros):
        """
        repo_libros: RepositorioLibros - Repositorio para manejo de libros.
        usuarios: list - Lista de usuarios registrados.
        prestamos: list - Lista de préstamos realizados.
        """
        self.repo_libros = repo_libros
        self.usuarios = []
        self.prestamos = []

    def registrar_usuario(self, usuario):
        """
        Registra un nuevo usuario en la biblioteca.
        usuario: Usuario - Usuario a registrar.
        """
        self.usuarios.append(usuario)

    def agregar_libro(self, libro):
        """
        Añade un libro al sistema utilizando el repositorio.
        libro: Libro - Libro a añadir.
        """
        self.repo_libros.agregar_libro(libro)

    def buscar_libro(self, criterio):
        """
        Busca libros en el repositorio usando una palabra clave.
        criterio: str - Palabra clave para buscar.
        """
        return self.repo_libros.buscar_libro(criterio)

    def prestar_libro(self, id_usuario, id_libro):
        """
        Permite prestar un libro a un usuario, si está disponible.
        id_usuario: int - ID del usuario.
        id_libro: int - ID del libro.
        """
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        libro = next((l for l in self.repo_libros.libros if l.id_libro == id_libro and l.disponible), None)
        if usuario and libro:
            prestamo = Prestamo(usuario, libro)
            libro.disponible = False
            self.prestamos.append(prestamo)
            return prestamo
        return None

    def devolver_libro(self, id_usuario, id_libro):
        """
        Permite registrar la devolución de un libro.
        Calcula y asigna multa si corresponde.
        id_usuario: int - ID del usuario.
        id_libro: int - ID del libro.
        """
        prestamo = next((p for p in self.prestamos if p.usuario.id_usuario == id_usuario and 
                         p.libro.id_libro == id_libro and not p.devuelto), None)
        if prestamo:
            prestamo.devolver()
            multa = prestamo.calcular_multa()
            prestamo.usuario.multas += multa
            return multa
        return 0

# Menú por consola para interactuar con la biblioteca
if __name__ == "__main__":
    # Instanciación del repositorio y biblioteca
    repo = RepositorioLibrosEnMemoria()
    biblioteca = Biblioteca(repo)

    # Pre-carga de algunos datos de ejemplo (puedes modificar o quitar)
    biblioteca.registrar_usuario(Usuario(1, "Felipe Toro"))
    biblioteca.registrar_usuario(Usuario(2, "Gerardo Cerda"))
    biblioteca.agregar_libro(Libro(1, "Cien años de soledad", "Gabriel García Márquez"))
    biblioteca.agregar_libro(Libro(2, "1984", "George Orwell"))
    biblioteca.agregar_libro(Libro(3, "Python para todos", "Charles Severance"))

    def mostrar_menu():
        print("\n=== MENÚ BIBLIOTECA ===")
        print("1. Registrar usuario")
        print("2. Agregar libro")
        print("3. Buscar libro")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Mostrar usuarios")
        print("7. Mostrar libros")
        print("8. Mostrar préstamos")
        print("0. Salir")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                id_usuario = int(input(ID_USUARIO_LABEL))
                nombre = input("Nombre del usuario: ").strip()
                biblioteca.registrar_usuario(Usuario(id_usuario, nombre))
                print("Usuario registrado correctamente.")
            except Exception as e:
                print(f"Error al registrar usuario: {e}")

        elif opcion == "2":
            try:
                id_libro = int(input(ID_LIBRO_LABEL))
                titulo = input("Título del libro: ").strip()
                autor = input("Autor del libro: ").strip()
                biblioteca.agregar_libro(Libro(id_libro, titulo, autor))
                print("Libro agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar libro: {e}")

        elif opcion == "3":
            criterio = input("Buscar por título o autor: ").strip()
            resultados = biblioteca.buscar_libro(criterio)
            if resultados:
                print("\nResultados de la búsqueda:")
                for libro in resultados:
                    print(libro)
            else:
                print("No se encontraron libros con ese criterio.")

        elif opcion == "4":
            try:
                id_usuario = int(input(ID_USUARIO_LABEL))
                id_libro = int(input(ID_LIBRO_LABEL))
                prestamo = biblioteca.prestar_libro(id_usuario, id_libro)
                if prestamo:
                    print("Libro prestado correctamente.")
                else:
                    print("No se pudo prestar el libro (quizás no existe, ya está prestado, o el usuario no existe).")
            except Exception as e:
                print(f"Error al prestar libro: {e}")

        elif opcion == "5":
            try:
                id_usuario = int(input(ID_USUARIO_LABEL))
                id_libro = int(input(ID_LIBRO_LABEL))
                multa = biblioteca.devolver_libro(id_usuario, id_libro)
                if multa is not None:
                    print(f"Libro devuelto. Multa aplicada: ${multa}")
                else:
                    print("No se encontró el préstamo pendiente para esa combinación de usuario y libro.")
            except Exception as e:
                print(f"Error al devolver libro: {e}")

        elif opcion == "6":
            print("\nUsuarios registrados:")
            for usuario in biblioteca.usuarios:
                print(usuario)

        elif opcion == "7":
            print("\nLibros en biblioteca:")
            for libro in biblioteca.repo_libros.libros:
                print(libro)

        elif opcion == "8":
            print("\nPréstamos realizados:")
            for prestamo in biblioteca.prestamos:
                status = "Devuelto" if prestamo.devuelto else "Pendiente"
                print(f"{prestamo.libro.titulo} a {prestamo.usuario.nombre} el {prestamo.fecha_prestamo.strftime('%Y-%m-%d')} - {status}")

        elif opcion == "0":
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")
