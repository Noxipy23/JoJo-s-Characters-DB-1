# JoJo DB

Base de datos de personajes de JoJo's Bizarre Adventure. Puedes añadir, buscar, filtrar y eliminar personajes desde el navegador. Los datos se guardan en un archivo SQLite (`jojo.db`).

**Tecnologías:** Python · Flask · SQLite · HTML + JavaScript

---

## Cómo funciona (en 30 segundos)

```
Navegador (HTML + JS)  ⇄  Flask (app.py)  ⇄  SQLite (jojo.db)
```

- **SQLite** guarda los datos en un archivo.
- **Flask** es el intermediario: el navegador no puede leer el `.db` directamente, así que Flask ofrece una API (URLs que reciben y devuelven JSON).
- **HTML + JavaScript** pide datos a esa API con `fetch()` y dibuja la página.

> **Importante:** la página debe abrirse a través del servidor (`http://127.0.0.1:5000`). Si haces doble clic en `index.html`, la dirección empieza por `file://`, no hay servidor detrás y no se guardará nada.

---

## Estructura del proyecto

```
jojo-flask/
├── app.py            ← servidor Flask + base de datos
├── README.md         ← este archivo
└── static/
    └── index.html    ← la interfaz
```

`index.html` **debe** estar dentro de la carpeta `static`, porque `app.py` lo busca ahí.

Después de la primera ejecución aparecerán dos elementos más: la carpeta `venv/` (entorno virtual) y el archivo `jojo.db` (tus datos).

---

## Requisitos

Necesitas **Python 3.8 o superior**. Comprueba si lo tienes:

| Sistema | Comando |
|---|---|
| Linux | `python3 --version` |
| Windows | `py --version` |

### Si no lo tienes

- **Arch Linux:** `sudo pacman -S python`
- **Debian / Ubuntu:** `sudo apt install python3 python3-venv python3-pip`
- **Fedora:** `sudo dnf install python3`
- **Windows:** descarga el instalador desde <https://www.python.org/downloads/>. **Marca la casilla "Add python.exe to PATH"** en la primera pantalla del instalador.

---

## Instalación y ejecución en Linux

Abre una terminal y sigue los pasos en orden.

### 1. Entrar a la carpeta del proyecto

```bash
cd ~/jojo-flask
```

### 2. Crear el entorno virtual (solo la primera vez)

```bash
python -m venv venv
```

> Si `python` no existe, usa `python3`.

**¿Por qué?** Muchas distribuciones (Arch incluida) no permiten instalar paquetes con `pip` en el Python del sistema, para no chocar con el gestor de paquetes. El entorno virtual es una carpeta aislada con su propio Python y sus propios paquetes.

### 3. Activar el entorno virtual

Depende de la shell que uses. Si no sabes cuál es, ejecuta `echo $SHELL`.

| Shell | Comando |
|---|---|
| bash / zsh | `source venv/bin/activate` |
| fish | `source venv/bin/activate.fish` |

Verás `(venv)` al inicio de la línea. Eso indica que está activo.

> **Error típico en fish:** `'case' builtin not inside of switch block`. Ocurre por usar `activate` (escrito para bash) en fish. Usa `activate.fish`.

### 4. Instalar Flask (solo la primera vez)

```bash
pip install flask
```

### 5. Arrancar el servidor

```bash
python app.py
```

Debe aparecer algo como `Running on http://127.0.0.1:5000`. **Deja esta terminal abierta**: si la cierras, el servidor se apaga.

### 6. Abrir en el navegador

```
http://127.0.0.1:5000
```

---

## Instalación y ejecución en Windows

Puedes usar **PowerShell** (recomendado) o **CMD**. Para abrir PowerShell: tecla Windows, escribe `PowerShell` y pulsa Enter.

### 1. Entrar a la carpeta del proyecto

Ajusta la ruta a donde guardaste el proyecto:

```powershell
cd C:\Users\TuUsuario\jojo-flask
```

> Truco: en el Explorador de archivos, abre la carpeta, haz clic derecho en un espacio vacío y elige **"Abrir en Terminal"**.

### 2. Crear el entorno virtual (solo la primera vez)

```powershell
py -m venv venv
```

> Si `py` no funciona, prueba con `python -m venv venv`.

### 3. Activar el entorno virtual

| Terminal | Comando |
|---|---|
| PowerShell | `venv\Scripts\Activate.ps1` |
| CMD | `venv\Scripts\activate.bat` |

Verás `(venv)` al inicio de la línea.

> **Error típico en PowerShell:** *"la ejecución de scripts está deshabilitada en este sistema"*. Windows bloquea por defecto los scripts `.ps1`. Se arregla una sola vez con:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
>
> Responde `S` (o `Y`) y vuelve a activar el entorno. El parámetro `-Scope CurrentUser` limita el cambio a tu usuario, sin afectar a todo el equipo.

### 4. Instalar Flask (solo la primera vez)

```powershell
pip install flask
```

### 5. Arrancar el servidor

```powershell
python app.py
```

Deja la ventana abierta mientras uses la aplicación. Si Windows muestra un aviso del Firewall, puedes permitir el acceso en redes privadas.

### 6. Abrir en el navegador

```
http://127.0.0.1:5000
```

---

## Usar el proyecto otro día

El entorno y Flask ya están instalados. Solo repite estos pasos:

**Linux (bash/zsh)**
```bash
cd ~/jojo-flask
source venv/bin/activate
python app.py
```

**Linux (fish)**
```fish
cd ~/jojo-flask
source venv/bin/activate.fish
python app.py
```

**Windows (PowerShell)**
```powershell
cd C:\Users\TuUsuario\jojo-flask
venv\Scripts\Activate.ps1
python app.py
```

Para **apagar** el servidor, pulsa `Ctrl + C` en su terminal. Para **salir del entorno virtual**, escribe `deactivate`.

---

## Cómo ver los datos directamente en SQLite

Con el servidor apagado o encendido, desde otra terminal en la carpeta del proyecto:

```bash
sqlite3 jojo.db
```

Y dentro:

```sql
.headers on
.mode box
SELECT * FROM personajes;
.quit
```

En Windows necesitas tener instalado `sqlite3` (<https://www.sqlite.org/download.html>) o usar la herramienta gráfica **DB Browser for SQLite**.

---

## Copia de seguridad y reinicio

Todos tus datos están en **un solo archivo**: `jojo.db`.

- **Copia de seguridad:** copia `jojo.db` a otro lugar.
- **Empezar de cero:** apaga el servidor y borra `jojo.db`. Se creará uno vacío al arrancar de nuevo.

---

## La API (para curiosos)

Estas son las rutas que Flask expone y que usa el HTML:

| Método | Ruta | Qué hace | SQL equivalente |
|---|---|---|---|
| GET | `/api/personajes` | Lista y busca (admite `?q=` y `?parte=`) | `SELECT` |
| POST | `/api/personajes` | Crea un personaje | `INSERT` |
| DELETE | `/api/personajes/<id>` | Elimina un personaje | `DELETE` |

Puedes probarla sin navegador. Por ejemplo, en Linux:

```bash
curl http://127.0.0.1:5000/api/personajes
```

---

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| Pulso "Añadir" y no pasa nada | Abriste `index.html` con doble clic (`file://`) | Entra por `http://127.0.0.1:5000` con el servidor corriendo |
| `Not Found` en el navegador | `index.html` no está dentro de `static/` | Revisa la estructura del proyecto |
| `ModuleNotFoundError: No module named 'flask'` | Entorno sin activar o Flask sin instalar | Activa el entorno y ejecuta `pip install flask` |
| `python: command not found` (Linux) | El comando se llama distinto | Usa `python3` |
| `python` no se reconoce (Windows) | Python no está en el PATH | Usa `py`, o reinstala Python marcando "Add to PATH" |
| `'case' builtin not inside of switch block` | Usaste `activate` en fish | Usa `activate.fish` |
| Scripts deshabilitados (PowerShell) | Política de ejecución de Windows | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Address already in use` | Otro programa usa el puerto 5000 | Cierra el otro programa, o cambia el puerto en la última línea de `app.py`: `app.run(debug=True, port=5001)` |

### Dos herramientas para depurar

- **La terminal del servidor.** Cada petición se imprime, por ejemplo `"POST /api/personajes HTTP/1.1" 201`. Si no aparece ninguna línea `POST`, la petición nunca llegó a Flask.
- **F12 en el navegador.** La pestaña *Console* muestra errores de JavaScript, y *Network* muestra cada petición con su código de respuesta.

---

## Notas de seguridad

- `app.run(debug=True)` es cómodo para aprender (se reinicia solo al editar), pero **no** debe usarse en un servidor público.
- Las consultas SQL usan `?` en lugar de insertar texto directamente. Así se evita la **inyección SQL**.
- El HTML usa `textContent` al mostrar datos. Así se evita que un nombre con `<script>` se ejecute (**XSS**).

---

## Ideas para seguir aprendiendo

1. Añadir **editar** personajes (ruta `PUT` con `UPDATE`).
2. Añadir **imágenes** a cada personaje.
3. Añadir una columna nueva (por ejemplo `edad`) y ver qué cambios pide en `app.py` y en el HTML.
4. Separar los datos en dos tablas (`personajes` y `stands`) y relacionarlas con una clave foránea.
