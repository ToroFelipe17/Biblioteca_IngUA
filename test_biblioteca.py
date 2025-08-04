import pytest
from biblioteca import Libro, Usuario, Prestamo, RepositorioLibrosEnMemoria, Biblioteca

@pytest.fixture
def biblioteca_vacia():
    # Crea una biblioteca vacía con repositorio en memoria para cada test.
    return Biblioteca(RepositorioLibrosEnMemoria())

def test_registrar_usuario(biblioteca_vacia):
    usuario = Usuario(1, "Felipe Toro")
    biblioteca_vacia.registrar_usuario(usuario)
    assert usuario in biblioteca_vacia.usuarios

def test_agregar_libro(biblioteca_vacia):
    libro = Libro(10, "El Quijote", "Miguel de Cervantes")
    biblioteca_vacia.agregar_libro(libro)
    assert libro in biblioteca_vacia.repo_libros.libros

def test_buscar_libro(biblioteca_vacia):
    libro = Libro(20, "Cien años de soledad", "Gabriel García Márquez")
    biblioteca_vacia.agregar_libro(libro)
    resultados = biblioteca_vacia.buscar_libro("soledad")
    assert libro in resultados

def test_prestar_y_devolver_libro(biblioteca_vacia):
    usuario = Usuario(2, "Sebastián")
    libro = Libro(30, "1984", "George Orwell")
    biblioteca_vacia.registrar_usuario(usuario)
    biblioteca_vacia.agregar_libro(libro)
    prestamo = biblioteca_vacia.prestar_libro(2, 30)
    assert prestamo is not None
    assert not libro.disponible

    # Devolución inmediata, no debería tener multa
    multa = biblioteca_vacia.devolver_libro(2, 30)
    assert libro.disponible
    assert multa == 0

def test_calculo_multa_prestamo_atrasado(monkeypatch, biblioteca_vacia):
    usuario = Usuario(3, "Pedro González")
    libro = Libro(40, "Python Pro", "Alguien Pro")
    biblioteca_vacia.registrar_usuario(usuario)
    biblioteca_vacia.agregar_libro(libro)
    prestamo = biblioteca_vacia.prestar_libro(3, 40)

    # Simula que pasan 10 días (más que DIAS_MAXIMO)
    from datetime import datetime, timedelta
    fecha_futura = prestamo.fecha_prestamo + timedelta(days=10)
    # Parchea la fecha actual solo para este test (usando monkeypatch)
    monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: fecha_futura)
    prestamo.devuelto = True
    prestamo.fecha_devolucion = fecha_futura
    multa = prestamo.calcular_multa()
    assert multa == (10 - Prestamo.DIAS_MAXIMO) * Prestamo.MULTA_POR_DIA
