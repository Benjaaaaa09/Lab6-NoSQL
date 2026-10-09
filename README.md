# Laboratorio Neo4j TechLib - Python CRUD

Proyecto para la digitalización y gestión de la biblioteca universitaria **"TechLib"** utilizando la base de datos de grafos **Neo4j** y una aplicación de consola con operaciones **CRUD** desarrollada en **Python**.

---

## Estructura del Proyecto

```text
├── crud_techlib.py                     # Script principal de Python con el menú y operaciones CRUD
├── comandos_cypher_laboratorio_techlib.md # Script Cypher con creación de nodos, relaciones y consultas
├── guialab6-2026-10-09T01-20-31.dump   # Volcado (Dump) oficial de la base de datos Neo4j
├── Lab6 (1).pdf                        # Guía y enunciado del laboratorio
├── .env.example                        # Plantilla de variables de entorno
├── .env                                # Credenciales locales de conexión (ignorado en git)
├── .gitignore                          # Configuración de exclusión para git
└── README.md                           # Documentación general del proyecto
```

---

## Requisitos Previos

- **Python 3.10+**
- **Neo4j Desktop** (o Neo4j Server v4/v5)
- Dependencias de Python:
  ```bash
  pip install neo4j python-dotenv
  ```

---

## Carga de la Base de Datos

Puedes inicializar la base de datos de **dos formas diferentes**:

### Opción A: A partir del archivo `.dump` (Recomendado)
1. En **Neo4j Desktop**, selecciona tu proyecto.
2. Haz clic en **Add** > **File**.
3. Selecciona el archivo `guialab6-2026-10-09T01-20-31.dump` incluido en este repositorio.
4. En el archivo cargado, haz clic en los tres puntos **`...`** y selecciona **Create DBMS from dump**.
5. Inicia el nuevo DBMS.

### Opción B: Ejecutar el script Cypher
1. Inicia tu DBMS en **Neo4j Desktop** y abre **Neo4j Browser**.
2. Copia y ejecuta los bloques de creación y relaciones incluidos en el archivo `comandos_cypher_laboratorio_techlib.md`.

---

## Configuración del Entorno (.env)

1. Crea tu archivo `.env` a partir de la plantilla:
   ```bash
   cp .env.example .env
   ```
2. Configura los parámetros según tu instalación de Neo4j Desktop:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=tu_contraseña
   NEO4J_DATABASE=guialab6
   ```

---

## Ejecución del Sistema CRUD

Para iniciar la aplicación de consola interactiva, ejecuta:

```bash
python crud_techlib.py
```

### Operaciones Disponibles:

- **1. Registrar nuevo libro (Create):** Permite ingresar títulos, copias disponibles, año, ubicación y palabras clave, vinculando automáticamente sus relaciones `[:ESCRITO_POR]` y `[:PERTENECE_A]`.
- **2. Listar todos los libros (Read):** Muestra el catálogo completo con autor, categoría, stock y ubicación en formato limpio.
- **3. Buscar libro (Read):** Búsqueda flexible que normaliza y descarta tildes y mayúsculas, permitiendo buscar tanto por título como por autor o género (ej. *"fundacion"*, *"orwell"*, *"clinica"*).
- **4. Actualizar libro (Update):** Modifica el stock de copias disponibles y/o la ubicación física del libro en estanterías.
- **5. Eliminar libro (Delete):** Borra el libro y desvincula de forma segura todas sus relaciones asociadas mediante `DETACH DELETE`.
- **0. Salir:** Cierra la conexión de manera segura con el driver de Neo4j.

---

## Consultas de Análisis (Cypher)

En el archivo `comandos_cypher_laboratorio_techlib.md` se encuentran implementadas y documentadas las consultas analíticas solicitadas en el laboratorio, tales como:

- Autor correspondiente a cada libro.
- Libros prestados por cada usuario.
- Categorías y conteo de libros asociados.
- Préstamos activos (`devuelto = false`).
- Total de préstamos realizados por usuario.
- Libros disponibles de "Ciencia Ficción" o "Programación".
- Cálculo del promedio de multas pendientes de usuarios activos.
