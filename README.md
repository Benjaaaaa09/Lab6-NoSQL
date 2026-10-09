# Laboratorio Neo4j TechLib - Python CRUD

Proyecto para la gestión de la biblioteca universitaria "TechLib" utilizando la base de datos de grafos **Neo4j** y un sistema de operaciones **CRUD** desarrollado en **Python**.

## Requisitos previos

- Python 3.10+
- Neo4j Desktop o Neo4j Community Server
- Dependencias de Python:
  ```bash
  pip install neo4j python-dotenv
  ```

## Estructura del Proyecto

```text
├── crud_techlib.py                     # Script principal con operaciones CRUD y menú
├── comandos_cypher_laboratorio_techlib.md # Comandos Cypher de creación y consultas
├── .env.example                        # Plantilla para variables de entorno
├── .env                                # Archivo de configuración local (ignorado en git)
├── .gitignore                          # Archivos ignorados por git
└── README.md                           # Documentación del proyecto
```

## Configuración

1. Copiar el archivo `.env.example` y renombrarlo a `.env`:
   ```bash
   cp .env.example .env
   ```
2. Editar el archivo `.env` con las credenciales de tu base de datos:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=tu_contraseña
   NEO4J_DATABASE=guialab6
   ```

## Ejecución

1. Iniciar la base de datos en **Neo4j Desktop**.
2. Ejecutar los comandos Cypher de creación inicial que se encuentran en `comandos_cypher_laboratorio_techlib.md`.
3. Ejecutar el script interactivo:
   ```bash
   python crud_techlib.py
   ```

## Funcionalidades CRUD

- **Crear (Create):** Registro de nuevos libros vinculados a autores y categorías.
- **Leer (Read):** Listado general y búsqueda flexible (insensible a tildes y mayúsculas por título, autor o género).
- **Actualizar (Update):** Modificación de ejemplares disponibles y ubicación física en estantes.
- **Eliminar (Delete):** Eliminación de libros y desvinculación segura de relaciones (`DETACH DELETE`).
