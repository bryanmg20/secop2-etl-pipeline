# SECOP II ETL Pipeline

Pipeline ETL que extrae los datos públicos de contratación del SECOP II, los transforma y los carga en PostgreSQL siguiendo un modelo dimensional (esquema estrella), proporcionando una base de datos optimizada para análisis y consultas.

---

## Cómo ejecutar
1. Clonar el repositorio
2. `pip install -r requirements.txt`
3. Configurar `.env` con credenciales basandose en el .env.example
4. `docker compose up -d`
5. `python main.py`


## Arquitectura

```mermaid
graph LR
    A[API SECOP II] --> B[extraction]
    B --> C[transformation]
    C --> D[loading]
    D --> E[(PostgreSQL)]
```

## Modelo de datos
![Modelo de datos](assets/database_model.png)


## Tecnologías
Python · Pandas · PostgreSQL · SQLAlchemy · Power BI · Docker · Git

## Recursos

- Documentación técnica: [`docs/`](docs/)
- Dashboards y diagramas: [`assets/`](assets/)