# Comandos Cypher - Laboratorio TechLib

A continuación se presentan los comandos para crear los nodos y relaciones en la base de datos "Biblioteca" de Neo4j, así como las consultas solicitadas en el laboratorio.

## 1. Creación de Nodos

Puedes ejecutar cada uno de estos bloques por separado en Neo4j Desktop.

### Géneros
```cypher
CREATE 
  (g1:Genero {nombre: "Ciencia Ficción"}),
  (g2:Genero {nombre: "Programación"}),
  (g3:Genero {nombre: "Fantasía"}),
  (g4:Genero {nombre: "Literatura Clásica"});
```

### Autores
```cypher
CREATE 
  (a1:Autor {nombre: "Isaac Asimov", nacionalidad: "Ruso-Estadounidense", fechaNacimiento: "1920-01-02"}),
  (a2:Autor {nombre: "Robert C. Martin", nacionalidad: "Estadounidense", fechaNacimiento: "1952-12-05"}),
  (a3:Autor {nombre: "J.R.R. Tolkien", nacionalidad: "Británico", fechaNacimiento: "1892-01-03"}),
  (a4:Autor {nombre: "George Orwell", nacionalidad: "Británico", fechaNacimiento: "1903-06-25"}),
  (a5:Autor {nombre: "Martin Fowler", nacionalidad: "Británico", fechaNacimiento: "1963-12-18"});
```

### Libros
```cypher
CREATE 
  (l1:Libro {titulo: "Fundación", añoPublicacion: 1951, disponibles: 3, ubicacion: "Sección A - Estante 1", `palabras Clave`: ["espacio", "imperio", "psicohistoria"]}),
  (l2:Libro {titulo: "Yo, Robot", añoPublicacion: 1950, disponibles: 2, ubicacion: "Sección A - Estante 2", `palabras Clave`: ["robots", "leyes", "futuro"]}),
  (l3:Libro {titulo: "Clean Code", añoPublicacion: 2008, disponibles: 5, ubicacion: "Sección P - Estante 1", `palabras Clave`: ["desarrollo", "buenas prácticas", "código"]}),
  (l4:Libro {titulo: "Clean Architecture", añoPublicacion: 2017, disponibles: 4, ubicacion: "Sección P - Estante 2", `palabras Clave`: ["arquitectura", "software", "diseño"]}),
  (l5:Libro {titulo: "El Señor de los Anillos", añoPublicacion: 1954, disponibles: 1, ubicacion: "Sección F - Estante 1", `palabras Clave`: ["anillo", "aventura", "magia"]}),
  (l6:Libro {titulo: "El Hobbit", añoPublicacion: 1937, disponibles: 3, ubicacion: "Sección F - Estante 2", `palabras Clave`: ["dragón", "enanos", "viaje"]}),
  (l7:Libro {titulo: "1984", añoPublicacion: 1949, disponibles: 6, ubicacion: "Sección C - Estante 1", `palabras Clave`: ["distopía", "vigilancia", "totalitarismo"]}),
  (l8:Libro {titulo: "Rebelión en la granja", añoPublicacion: 1945, disponibles: 4, ubicacion: "Sección C - Estante 2", `palabras Clave`: ["sátira", "política", "animales"]}),
  (l9:Libro {titulo: "Refactoring", añoPublicacion: 1999, disponibles: 2, ubicacion: "Sección P - Estante 3", `palabras Clave`: ["código", "optimización", "patrones"]}),
  (l10:Libro {titulo: "Patrones de Arquitectura de Aplicaciones Empresariales", añoPublicacion: 2002, disponibles: 3, ubicacion: "Sección P - Estante 4", `palabras Clave`: ["arquitectura", "empresa", "patrones"]});
```

### Usuarios
```cypher
CREATE 
  (u1:Usuario {nombreCompleto: "Ana Gómez", carrera: "Ingeniería Civil Informática", fechaRegistro: "2023-03-10", `multa Pendiente`: 0}),
  (u2:Usuario {nombreCompleto: "Luis Martínez", carrera: "Arquitectura", fechaRegistro: "2024-05-20", `multa Pendiente`: 1500}),
  (u3:Usuario {nombreCompleto: "Carla Silva", carrera: "Medicina", fechaRegistro: "2025-01-15", `multa Pendiente`: 0}),
  (u4:Usuario {nombreCompleto: "Diego Rojas", carrera: "Derecho", fechaRegistro: "2025-08-05", `multa Pendiente`: 3000}),
  (u5:Usuario {nombreCompleto: "Sofía Castro", carrera: "Ingeniería Civil Informática", fechaRegistro: "2026-02-01", `multa Pendiente`: 0});
```

---

## 2. Creación de Relaciones

### Relaciones: Libro -> Autor
```cypher
MATCH (l:Libro {titulo: "Fundación"}), (a:Autor {nombre: "Isaac Asimov"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Yo, Robot"}), (a:Autor {nombre: "Isaac Asimov"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Clean Code"}), (a:Autor {nombre: "Robert C. Martin"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Clean Architecture"}), (a:Autor {nombre: "Robert C. Martin"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "El Señor de los Anillos"}), (a:Autor {nombre: "J.R.R. Tolkien"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "El Hobbit"}), (a:Autor {nombre: "J.R.R. Tolkien"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "1984"}), (a:Autor {nombre: "George Orwell"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Rebelión en la granja"}), (a:Autor {nombre: "George Orwell"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Refactoring"}), (a:Autor {nombre: "Martin Fowler"}) CREATE (l)-[:ESCRITO_POR]->(a);
MATCH (l:Libro {titulo: "Patrones de Arquitectura de Aplicaciones Empresariales"}), (a:Autor {nombre: "Martin Fowler"}) CREATE (l)-[:ESCRITO_POR]->(a);
```

### Relaciones: Libro -> Género
```cypher
MATCH (l:Libro {titulo: "Fundación"}), (g:Genero {nombre: "Ciencia Ficción"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Yo, Robot"}), (g:Genero {nombre: "Ciencia Ficción"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Clean Code"}), (g:Genero {nombre: "Programación"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Clean Architecture"}), (g:Genero {nombre: "Programación"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "El Señor de los Anillos"}), (g:Genero {nombre: "Fantasía"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "El Hobbit"}), (g:Genero {nombre: "Fantasía"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "1984"}), (g:Genero {nombre: "Ciencia Ficción"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Rebelión en la granja"}), (g:Genero {nombre: "Literatura Clásica"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Refactoring"}), (g:Genero {nombre: "Programación"}) CREATE (l)-[:PERTENECE_A]->(g);
MATCH (l:Libro {titulo: "Patrones de Arquitectura de Aplicaciones Empresariales"}), (g:Genero {nombre: "Programación"}) CREATE (l)-[:PERTENECE_A]->(g);
```

### Relaciones: Usuario -> Libro (Préstamos)
```cypher
MATCH (u:Usuario {nombreCompleto: "Ana Gómez"}), (l:Libro {titulo: "Clean Code"}) CREATE (u)-[:PRESTO {devuelto: false}]->(l);
MATCH (u:Usuario {nombreCompleto: "Luis Martínez"}), (l:Libro {titulo: "1984"}) CREATE (u)-[:PRESTO {devuelto: false}]->(l);
MATCH (u:Usuario {nombreCompleto: "Carla Silva"}), (l:Libro {titulo: "Fundación"}) CREATE (u)-[:PRESTO {devuelto: true}]->(l);
MATCH (u:Usuario {nombreCompleto: "Diego Rojas"}), (l:Libro {titulo: "El Señor de los Anillos"}) CREATE (u)-[:PRESTO {devuelto: false}]->(l);
MATCH (u:Usuario {nombreCompleto: "Sofía Castro"}), (l:Libro {titulo: "Clean Architecture"}) CREATE (u)-[:PRESTO {devuelto: true}]->(l);
MATCH (u:Usuario {nombreCompleto: "Ana Gómez"}), (l:Libro {titulo: "Refactoring"}) CREATE (u)-[:PRESTO {devuelto: true}]->(l);
```

---

## 3. Consultas y Operaciones (Análisis de Datos)

**Obtener el autor de cada libro:**
```cypher
MATCH (l:Libro)-[:ESCRITO_POR]->(a:Autor)
RETURN l.titulo AS Libro, a.nombre AS Autor;
```

**Obtener todos los libros prestados por cada usuario:**
```cypher
MATCH (u:Usuario)-[:PRESTO]->(l:Libro)
RETURN u.nombreCompleto AS Usuario, collect(l.titulo) AS LibrosPrestados;
```

**Mostrar todos los libros con su categoría correspondiente:**
```cypher
MATCH (l:Libro)-[:PERTENECE_A]->(g:Genero)
RETURN l.titulo AS Libro, g.nombre AS Categoria;
```

**Mostrar los préstamos activos junto con los datos del usuario y del libro:**
```cypher
MATCH (u:Usuario)-[p:PRESTO {devuelto: false}]->(l:Libro)
RETURN u, p, l;
```

**Calcular cuántos préstamos ha realizado cada usuario:**
```cypher
MATCH (u:Usuario)-[p:PRESTO]->(:Libro)
RETURN u.nombreCompleto AS Usuario, count(p) AS TotalPrestamos;
```

**Mostrar cuántos libros pertenecen a cada categoría:**
```cypher
MATCH (l:Libro)-[:PERTENECE_A]->(g:Genero)
RETURN g.nombre AS Categoria, count(l) AS TotalLibros;
```

**Listar los libros disponibles cuyo género sea "Ciencia Ficción" o "Programación":**
```cypher
MATCH (l:Libro)-[:PERTENECE_A]->(g:Genero)
WHERE l.disponibles > 0 AND g.nombre IN ["Ciencia Ficción", "Programación"]
RETURN l.titulo, l.disponibles, g.nombre;
```

**Calcular el promedio de multas pendientes de los usuarios activos (con préstamos no devueltos):**
```cypher
MATCH (u:Usuario)-[:PRESTO {devuelto: false}]->(:Libro)
RETURN avg(u.`multa Pendiente`) AS PromedioMultas;
```
