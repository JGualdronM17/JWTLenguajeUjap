# API con JWT (2da parte - Lenguaje)

API REST con autenticacion por token JWT y control de acceso por rol.
FastAPI + passlib/bcrypt + python-jose.

## Requisitos

- Python 3.9 o superior

## Instalacion

```
pip install -r requirements.txt
```

## Ejecucion

```
uvicorn main:app --reload
```

La documentacion interactiva (Swagger) queda en: http://127.0.0.1:8000/docs

## Usuarios de prueba

| Correo | Contrasena | Rol |
|---|---|---|
| estudiante@ujap.edu.ve | estudiante123 | estudiante |
| maria@ujap.edu.ve | profesor123 | profesor |

Las contrasenas estan en el codigo a proposito: es una base de datos simulada para
poder probar los tres casos sin montar una base real. En un proyecto real se
guardaria solo el hash y la contrasena viviria en el usuario.

## Endpoints

| Metodo | Ruta | Acceso | Resultado |
|---|---|---|---|
| POST | `/login` | publico | 200 con token, 401 si las credenciales fallan |
| GET | `/publico` | publico | 200 |
| GET | `/privado` | requiere token | 200, 401 sin token valido |
| GET | `/admin` | requiere rol profesor | 200 con maria, 403 con el estudiante |

## Como probarlo en Swagger

1. `POST /login` -> Try it out -> Execute. Salen 200 y el `access_token`.
2. Arriba a la derecha, Authorize -> escribe usuario y contrasena -> Authorize.
3. `GET /privado` -> Execute. Salen 200 con el nombre y el rol del usuario.
4. `GET /admin` -> Execute. Sale 403 "Solo para profesores" porque el token es
   del estudiante.

Las capturas de esos tres casos estan en la carpeta `capturas/`.

## Estructura

- `auth.py` - `hash_password`, `verify_password`, `create_token`, `get_current_user`
- `main.py` - los cuatro endpoints
- `requirements.txt` - dependencias con versiones fijadas
- `capturas/` - evidencias de los tres casos
