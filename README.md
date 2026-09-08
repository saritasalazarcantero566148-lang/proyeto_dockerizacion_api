# Gestor de Tareas — API REST (Flask + PostgreSQL)

API sencilla de gestión de tareas (CRUD), pensada para desplegarse fácilmente con Docker.

## Endpoints

| Método | Ruta                  | Descripción              |
|--------|-----------------------|---------------------------|
| GET    | /api/salud            | Verifica que la API responde |
| GET    | /api/tareas            | Lista todas las tareas   |
| GET    | /api/tareas/\<id>      | Obtiene una tarea        |
| POST   | /api/tareas            | Crea una tarea           |
| PUT    | /api/tareas/\<id>      | Actualiza una tarea      |
| DELETE | /api/tareas/\<id>      | Elimina una tarea        |

## Modelo `Tarea`

```json
{
  "id": 1,
  "titulo": "Comprar leche",
  "descripcion": "Ir al supermercado",
  "completada": false,
  "fecha_creacion": "2026-09-07T10:00:00"
}
```

## Ejecución local (sin Docker)

1. Crear entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copiar `.env.example` a `.env` y ajustar los valores de conexión a PostgreSQL.

3. Ejecutar la app:
   ```bash
   python app.py
   ```

La API quedará disponible en `http://localhost:5000`.

## Variables de entorno

Definidas en `.env` (ver `.env.example`):

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

## Notas

- La app crea las tablas automáticamente al iniciar (`db.create_all()`).
- El contenedor de la base de datos debe estar accesible en el host/puerto configurados en las variables de entorno (por ejemplo, el nombre del servicio en `docker-compose.yml`).
