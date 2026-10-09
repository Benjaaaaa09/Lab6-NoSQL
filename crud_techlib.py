import os
import sys
import unicodedata
from dotenv import load_dotenv
from neo4j import GraphDatabase, exceptions

def normalizar(texto):
    """Quita tildes, diacriticos y pasa a minusculas para busquedas flexibles."""
    if not texto:
        return ""
    nfd = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower().strip()


# Cargar configuracion desde .env
load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")


class BibliotecaCRUD:
    def __init__(self, uri, user, password, database):
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver = None

    def conectar(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            print("Conectado exitosamente a Neo4j.")
            return True
        except exceptions.AuthError:
            print("Error: usuario o contrasena incorrectos.")
            return False
        except exceptions.ServiceUnavailable:
            print(f"Error: no se pudo conectar al servidor en {self.uri}. Revisa que este iniciado en Neo4j Desktop.")
            return False
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def cerrar(self):
        if self.driver:
            self.driver.close()

    def _get_session(self):
        if self.database:
            return self.driver.session(database=self.database)
        return self.driver.session()

    # 1. Crear nuevo libro
    def crear_libro(self, titulo, anio_publicacion, disponibles, ubicacion, palabras_clave, autor=None, genero=None):
        query = """
        MERGE (l:Libro {titulo: $titulo})
        ON CREATE SET 
            l.añoPublicacion = $anio,
            l.disponibles = $disponibles,
            l.ubicacion = $ubicacion,
            l.`palabras Clave` = $palabras_clave,
            l.palabrasClave = $palabras_clave
        ON MATCH SET
            l.añoPublicacion = $anio,
            l.disponibles = $disponibles,
            l.ubicacion = $ubicacion,
            l.`palabras Clave` = $palabras_clave,
            l.palabrasClave = $palabras_clave
        WITH l
        FOREACH (_ IN CASE WHEN $autor IS NOT NULL AND $autor <> '' THEN [1] ELSE [] END |
            MERGE (a:Autor {nombre: $autor})
            MERGE (l)-[:ESCRITO_POR]->(a)
        )
        WITH l
        FOREACH (_ IN CASE WHEN $genero IS NOT NULL AND $genero <> '' THEN [1] ELSE [] END |
            MERGE (g:Genero {nombre: $genero})
            MERGE (l)-[:PERTENECE_A]->(g)
        )
        RETURN l.titulo AS titulo
        """
        params = {
            "titulo": titulo,
            "anio": int(anio_publicacion),
            "disponibles": int(disponibles),
            "ubicacion": ubicacion,
            "palabras_clave": palabras_clave if isinstance(palabras_clave, list) else [p.strip() for p in palabras_clave.split(",")],
            "autor": autor,
            "genero": genero
        }

        with self._get_session() as session:
            result = session.run(query, params)
            record = result.single()
            if record:
                print(f"Libro '{record['titulo']}' guardado correctamente.")
                return True
        return False

    # 2. Leer libros
    def listar_libros(self):
        query = """
        MATCH (l:Libro)
        OPTIONAL MATCH (l)-[:ESCRITO_POR]->(a:Autor)
        OPTIONAL MATCH (l)-[:PERTENECE_A]->(g:Genero)
        RETURN 
            l.titulo AS titulo,
            l.añoPublicacion AS anio,
            l.disponibles AS disponibles,
            l.ubicacion AS ubicacion,
            coalesce(l.`palabras Clave`, []) AS palabrasClave,
            coalesce(a.nombre, "Sin autor") AS autor,
            coalesce(g.nombre, "Sin categoria") AS genero
        ORDER BY l.titulo
        """
        with self._get_session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    def buscar_libro(self, termino):
        termino_norm = normalizar(termino)
        if not termino_norm:
            return []

        todos = self.listar_libros()
        resultados = []
        for l in todos:
            titulo_norm = normalizar(l.get("titulo"))
            autor_norm = normalizar(l.get("autor"))
            genero_norm = normalizar(l.get("genero"))
            if termino_norm in titulo_norm or termino_norm in autor_norm or termino_norm in genero_norm:
                resultados.append(l)
        return resultados

    # 3. Actualizar libro
    def actualizar_libro(self, titulo, nuevos_disponibles=None, nueva_ubicacion=None):
        set_clauses = []
        params = {"titulo": titulo}

        if nuevos_disponibles is not None:
            set_clauses.append("l.disponibles = $disponibles")
            params["disponibles"] = int(nuevos_disponibles)

        if nueva_ubicacion is not None and nueva_ubicacion.strip() != "":
            set_clauses.append("l.ubicacion = $ubicacion")
            params["ubicacion"] = nueva_ubicacion

        if not set_clauses:
            print("No se indicaron cambios para actualizar.")
            return False

        query = f"""
        MATCH (l:Libro {{titulo: $titulo}})
        SET {', '.join(set_clauses)}
        RETURN l.titulo AS titulo, l.disponibles AS disponibles, l.ubicacion AS ubicacion
        """

        with self._get_session() as session:
            result = session.run(query, params)
            record = result.single()
            if record:
                print(f"Libro '{record['titulo']}' actualizado. (Disponibles: {record['disponibles']}, Ubicacion: {record['ubicacion']})")
                return True
            else:
                print(f"No se encontro el libro '{titulo}'.")
                return False

    # 4. Eliminar libro
    def eliminar_libro(self, titulo):
        query = """
        MATCH (l:Libro {titulo: $titulo})
        DETACH DELETE l
        RETURN count(l) AS eliminados
        """
        with self._get_session() as session:
            result = session.run(query, {"titulo": titulo})
            record = result.single()
            if record and record["eliminados"] > 0:
                print(f"Libro '{titulo}' eliminado de la base de datos.")
                return True
            else:
                print(f"No se encontro el libro '{titulo}'.")
                return False


def mostrar_libro(libro):
    palabras = ", ".join(libro.get("palabrasClave", [])) if libro.get("palabrasClave") else "Ninguna"
    print(f"- Titulo: {libro.get('titulo')}")
    print(f"  Autor: {libro.get('autor')} | Genero: {libro.get('genero')}")
    print(f"  Año: {libro.get('anio')} | Disponibles: {libro.get('disponibles')}")
    print(f"  Ubicacion: {libro.get('ubicacion')}")
    print(f"  Palabras clave: {palabras}")
    print("-" * 45)


def menu_interactivo(crud: BibliotecaCRUD):
    while True:
        print("\n--- MENU BIBLIOTECA TECHLIB ---")
        print("1. Registrar nuevo libro")
        print("2. Listar todos los libros")
        print("3. Buscar libro por titulo")
        print("4. Actualizar libro (stock o ubicacion)")
        print("5. Eliminar libro")
        print("0. Salir")

        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            print("\n>> Registrar Libro")
            titulo = input("Titulo: ").strip()
            if not titulo:
                print("El titulo no puede estar vacio.")
                continue

            try:
                anio = int(input("Año de publicacion: ").strip())
                disponibles = int(input("Copias disponibles: ").strip())
            except ValueError:
                print("El año y las copias deben ser numeros enteros.")
                continue

            ubicacion = input("Ubicacion (ej: Seccion A - Estante 1): ").strip()
            palabras = input("Palabras clave (separadas por coma): ").strip()
            autor = input("Autor (opcional): ").strip()
            genero = input("Genero (opcional): ").strip()

            lista_palabras = [p.strip() for p in palabras.split(",") if p.strip()]
            crud.crear_libro(titulo, anio, disponibles, ubicacion, lista_palabras, autor or None, genero or None)

        elif opcion == "2":
            print("\n>> Lista de Libros:")
            libros = crud.listar_libros()
            if not libros:
                print("No hay libros registrados.")
            else:
                print(f"Total: {len(libros)} libros\n")
                for l in libros:
                    mostrar_libro(l)

        elif opcion == "3":
            print("\n>> Buscar Libro")
            termino = input("Titulo a buscar: ").strip()
            if not termino:
                print("Debes ingresar un titulo.")
                continue

            libros = crud.buscar_libro(termino)
            if not libros:
                print(f"No se encontraron libros con '{termino}'.")
            else:
                print(f"\nResultados ({len(libros)} encontrados):\n")
                for l in libros:
                    mostrar_libro(l)

        elif opcion == "4":
            print("\n>> Actualizar Libro")
            titulo = input("Titulo del libro a modificar: ").strip()
            if not titulo:
                continue

            existentes = crud.buscar_libro(titulo)
            if not existentes:
                print(f"No se encontro el libro '{titulo}'.")
                continue

            actual = existentes[0]
            titulo_real = actual.get("titulo")
            print(f"Libro encontrado: {titulo_real}")
            print(f"(Deja en blanco para no cambiar el valor actual)")
            disp_input = input(f"Nuevas copias disponibles (actual: {actual.get('disponibles')}): ").strip()
            nuevos_disp = int(disp_input) if disp_input else None

            ubic_input = input(f"Nueva ubicacion (actual: {actual.get('ubicacion')}): ").strip()
            nueva_ubic = ubic_input if ubic_input else None

            crud.actualizar_libro(titulo_real, nuevos_disponibles=nuevos_disp, nueva_ubicacion=nueva_ubic)

        elif opcion == "5":
            print("\n>> Eliminar Libro")
            titulo = input("Titulo del libro a eliminar: ").strip()
            if not titulo:
                continue

            existentes = crud.buscar_libro(titulo)
            if not existentes:
                print(f"No se encontro el libro '{titulo}'.")
                continue

            titulo_real = existentes[0].get("titulo")
            confirmar = input(f"¿Seguro que deseas eliminar '{titulo_real}'? (s/n): ").strip().lower()
            if confirmar == 's':
                crud.eliminar_libro(titulo_real)
            else:
                print("Eliminacion cancelada.")

        elif opcion == "0":
            print("Cerrando aplicacion...")
            break
        else:
            print("Opcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    crud = BibliotecaCRUD(URI, USER, PASSWORD, DATABASE)
    if crud.conectar():
        try:
            menu_interactivo(crud)
        finally:
            crud.cerrar()
    else:
        sys.exit(1)
