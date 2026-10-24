import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_NAME = "usuarios.db"

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laboratorio de SQL Injection</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: "Segoe UI", Arial, sans-serif;
            color: #eaf0ff;
            background: linear-gradient(135deg, #0b1024, #172554, #312e81);
            padding: 35px 18px;
        }

        header {
            text-align: center;
            margin: 15px auto 30px;
            max-width: 850px;
        }

        .icono {
            font-size: 42px;
            margin-bottom: 10px;
        }

        .etiqueta {
            display: inline-block;
            color: #a5b4fc;
            border: 1px solid #6366f1;
            background: #312e8155;
            border-radius: 30px;
            padding: 7px 16px;
            font-size: 13px;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }

        h1 {
            font-size: clamp(27px, 4vw, 40px);
            margin: 5px 0 12px;
            color: white;
        }

        header p {
            color: #c7d2fe;
            font-size: 16px;
            margin: 8px 0;
        }

        .contenedor {
            max-width: 850px;
            margin: auto;
        }

        .aviso {
            text-align: center;
            padding: 12px;
            margin-bottom: 22px;
            background: #7c2d1233;
            border: 1px solid #fb923c;
            color: #fed7aa;
            border-radius: 10px;
            font-size: 13px;
        }

        .paneles {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
        }

        .tarjeta {
            background: #ffffff0d;
            border: 1px solid #ffffff20;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 12px 30px #0002;
            backdrop-filter: blur(8px);
        }

        .numero {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 43px;
            height: 43px;
            border-radius: 12px;
            background: #6366f133;
            font-size: 23px;
            margin-bottom: 12px;
        }

        h2 {
            font-size: 20px;
            margin: 5px 0 10px;
            color: white;
        }

        .descripcion {
            font-size: 14px;
            color: #cbd5e1;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-size: 13px;
            color: #dbeafe;
            margin: 14px 0 7px;
        }

        input {
            width: 100%;
            padding: 12px 14px;
            color: white;
            background: #0b1024aa;
            border: 1px solid #475569;
            border-radius: 9px;
            outline: none;
            font-size: 14px;
        }

        input:focus {
            border-color: #818cf8;
            box-shadow: 0 0 0 3px #6366f133;
        }

        input::placeholder {
            color: #94a3b8;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 18px;
            border: none;
            border-radius: 9px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            filter: brightness(1.15);
            transform: translateY(-1px);
        }

        .resultado {
            max-width: 850px;
            margin: 22px auto 0;
            padding: 20px;
            background: #0f172a;
            border: 1px solid #818cf8;
            border-radius: 12px;
            overflow-wrap: anywhere;
        }

        .resultado h2 {
            color: #a5b4fc;
        }

        pre {
            white-space: pre-wrap;
            font-family: Consolas, monospace;
            color: #e2e8f0;
        }

        footer {
            text-align: center;
            margin-top: 30px;
            color: #a5b4fc;
            font-size: 12px;
            line-height: 1.8;
        }

        @media (max-width: 500px) {
            body {
                padding: 20px 12px;
            }

            .tarjeta {
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <header>
        <div class="icono">🛡️</div>
        <div class="etiqueta">PROYECTO ACADÉMICO · 2026</div>

        <h1>Simulación y Mitigación de SQL Injection</h1>

        <p>Materia: Seguridad Informática</p>
        <p>Laboratorio de Seguridad de Aplicaciones Web</p>
    </header>

    <main class="contenedor">
        <div class="aviso">
            ⚠️ Entorno educativo local: versión vulnerable.
            Utilizar únicamente para pruebas autorizadas.
        </div>

        <section class="paneles">
            <div class="tarjeta">
                <div class="numero">🔐</div>
                <h2>Autenticación</h2>
                <p class="descripcion">
                    Verifica las credenciales de los usuarios
                    dentro del entorno de demostración.
                </p>

                <form method="post" action="/login">
                    <label for="usuario">Nombre de usuario</label>
                    <input id="usuario" name="usuario"
                           placeholder="Ingresa tu usuario" required>

                    <label for="contrasena">Contraseña</label>
                    <input id="contrasena" name="contrasena"
                           type="password"
                           placeholder="Ingresa tu contraseña" required>

                    <button type="submit">Iniciar sesión →</button>
                </form>
            </div>

            <div class="tarjeta">
                <div class="numero">🔎</div>
                <h2>Consulta de usuarios</h2>
                <p class="descripcion">
                    Permite consultar los registros ficticios
                    almacenados en la base de datos SQLite.
                </p>

                <form method="get" action="/buscar">
                    <label for="nombre">Usuario a buscar</label>
                    <input id="nombre" name="nombre"
                           placeholder="Ej. admin">

                    <button type="submit">Buscar registros →</button>
                </form>
            </div>
        </section>

        {% if mensaje %}
        <section class="resultado">
            <h2>📋 Resultado de la operación</h2>
            <pre>{{ mensaje }}</pre>
        </section>
        {% endif %}
    </main>

    <footer>
        Práctica experimental de Seguridad Informática<br>
        Python · Flask · SQLite<br>
        Proyecto académico — 2026
    </footer>
</body>
</html>
"""


def conectar_db():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


def preparar_db():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)

    conexion.executemany("""
        INSERT OR IGNORE INTO usuarios (usuario, contrasena)
        VALUES (?, ?)
    """, [
        ("admin", "AdminDemo2026"),
        ("fernanda", "ClaveDemo123"),
        ("estudiante", "PruebaDemo456")
    ])

    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return render_template_string(HTML, mensaje="")


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    contrasena = request.form.get("contrasena", "")

    conexion = conectar_db()

    try:
        consulta = (
            "SELECT usuario FROM usuarios "
            f"WHERE usuario = '{usuario}' "
            f"AND contrasena = '{contrasena}'"
        )

        resultado = conexion.execute(consulta).fetchone()

        if resultado:
            mensaje = f"Acceso concedido: {resultado['usuario']}"
        else:
            mensaje = "Acceso denegado. Credenciales incorrectas."

    except sqlite3.Error:
        mensaje = "Error al ejecutar la consulta SQL."

    finally:
        conexion.close()

    return render_template_string(HTML, mensaje=mensaje)


@app.route("/buscar")
def buscar():
    nombre = request.args.get("nombre", "")
    conexion = conectar_db()

    try:
        consulta = (
            "SELECT id, usuario FROM usuarios "
            f"WHERE usuario = '{nombre}'"
        )

        resultados = conexion.execute(consulta).fetchall()

        if resultados:
            mensaje = "\n".join(
                f"ID: {fila['id']} | Usuario: {fila['usuario']}"
                for fila in resultados
            )
        else:
            mensaje = "No se encontraron usuarios."

    except sqlite3.Error:
        mensaje = "Error al ejecutar la consulta SQL."

    finally:
        conexion.close()

    return render_template_string(HTML, mensaje=mensaje)


if __name__ == "__main__":
    preparar_db()
    print("Base de datos creada correctamente.")
    app.run(host="127.0.0.1", port=5000, debug=False)
