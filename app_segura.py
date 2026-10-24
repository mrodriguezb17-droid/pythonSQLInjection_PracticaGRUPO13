import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB = "usuarios.db"


def conectar_db():
    conexion = sqlite3.connect(DB)
    conexion.row_factory = sqlite3.Row
    return conexion


HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Aplicación Segura | Seguridad Informática</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #e8f5e9, #f5faf5);
            color: #263b2d;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #14532d, #15803d);
            color: white;
            text-align: center;
            padding: 42px 20px 38px;
            box-shadow: 0 5px 18px rgba(20, 83, 45, 0.18);
        }

        .icono-principal {
            font-size: 42px;
            margin-bottom: 12px;
        }

        header h1 {
            font-size: clamp(24px, 4vw, 35px);
            margin-bottom: 12px;
        }

        header p {
            color: #dcfce7;
            font-size: 16px;
            margin-top: 7px;
        }

        .etiqueta {
            display: inline-block;
            margin-top: 18px;
            padding: 8px 16px;
            border: 1px solid #86efac;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 30px;
            font-size: 13px;
            font-weight: bold;
        }

        main {
            max-width: 1050px;
            margin: 35px auto;
            padding: 0 22px;
        }

        .introduccion {
            text-align: center;
            margin-bottom: 28px;
        }

        .introduccion h2 {
            color: #166534;
            font-size: 25px;
            margin-bottom: 10px;
        }

        .introduccion p {
            color: #607568;
            line-height: 1.6;
        }

        .contenedor-tarjetas {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 25px;
        }

        .tarjeta {
            background: #ffffff;
            border: 1px solid #d7eadb;
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 8px 25px rgba(22, 101, 52, 0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .tarjeta:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(22, 101, 52, 0.13);
        }

        .icono-tarjeta {
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dcfce7;
            border-radius: 14px;
            font-size: 27px;
            margin-bottom: 17px;
        }

        .tarjeta h3 {
            color: #166534;
            font-size: 22px;
            margin-bottom: 10px;
        }

        .descripcion {
            color: #718176;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 600;
            font-size: 14px;
            margin: 15px 0 7px;
            color: #344c3a;
        }

        input {
            display: block;
            width: 100%;
            padding: 13px 14px;
            border: 1px solid #cbdccf;
            border-radius: 10px;
            background: #fbfefb;
            font-size: 15px;
            outline: none;
            transition: border 0.2s, box-shadow 0.2s;
        }

        input:focus {
            border-color: #22a052;
            box-shadow: 0 0 0 3px rgba(34, 160, 82, 0.13);
        }

        button {
            display: block;
            width: 100%;
            padding: 13px;
            margin-top: 22px;
            background: linear-gradient(135deg, #15803d, #16a34a);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s;
        }

        button:hover {
            background: #166534;
            transform: translateY(-1px);
        }

        .mensaje {
            margin-top: 20px;
            padding: 14px;
            border-radius: 10px;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #166534;
            font-size: 14px;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .mensaje-error {
            background: #fff7ed;
            border-color: #fed7aa;
            color: #9a3412;
        }

        .estado-seguridad {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 28px;
            padding: 17px;
            background: #dcfce7;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            color: #166534;
            font-size: 14px;
            text-align: center;
        }

        footer {
            text-align: center;
            padding: 25px 15px;
            color: #718176;
            font-size: 13px;
        }

        @media (max-width: 700px) {
            .contenedor-tarjetas {
                grid-template-columns: 1fr;
            }

            header {
                padding: 32px 15px;
            }

            .tarjeta {
                padding: 22px;
            }
        }
    </style>
</head>

<body>

    <header>
        <div class="icono-principal">🛡️</div>

        <h1>Simulación y Mitigación de SQL Injection</h1>

        <p>Materia: Seguridad Informática</p>

        <p>Protección de consultas y datos de usuarios</p>

        <span class="etiqueta">✓ VERSIÓN SEGURA</span>
    </header>

    <main>
        <section class="introduccion">
            <h2>Centro de seguridad</h2>
            <p>
                Aplicación de demostración para validar credenciales
                y buscar usuarios mediante consultas SQL parametrizadas.
            </p>
        </section>

        <div class="contenedor-tarjetas">

            <section class="tarjeta">
                <div class="icono-tarjeta">🔐</div>

                <h3>Inicio de sesión</h3>

                <p class="descripcion">
                    Ingresa tus credenciales para verificar el acceso
                    de forma segura.
                </p>

                <form action="/login" method="post">
                    <label for="usuario">Nombre de usuario</label>
                    <input
                        id="usuario"
                        name="usuario"
                        type="text"
                        placeholder="Ejemplo: admin"
                        autocomplete="username"
                        required
                    >

                    <label for="contrasena">Contraseña</label>
                    <input
                        id="contrasena"
                        name="contrasena"
                        type="password"
                        placeholder="Ingresa tu contraseña"
                        autocomplete="current-password"
                        required
                    >

                    <button type="submit">Verificar acceso</button>
                </form>

                {% if mensaje_login %}
                    <div class="mensaje
                    {% if tipo_login == 'error' %}mensaje-error{% endif %}">
                        {{ mensaje_login }}
                    </div>
                {% endif %}
            </section>

            <section class="tarjeta">
                <div class="icono-tarjeta">🔎</div>

                <h3>Buscar usuario</h3>

                <p class="descripcion">
                    Consulta un usuario registrado en la base de datos
                    utilizando una búsqueda protegida.
                </p>

                <form action="/buscar" method="post">
                    <label for="nombre">Usuario que deseas buscar</label>
                    <input
                        id="nombre"
                        name="nombre"
                        type="text"
                        placeholder="Escribe el nombre de usuario"
                        required
                    >

                    <button type="submit">Buscar usuario</button>
                </form>

                {% if mensaje_busqueda %}
                    <div class="mensaje">
                        {{ mensaje_busqueda }}
                    </div>
                {% endif %}
            </section>

        </div>

        <div class="estado-seguridad">
            <span>✅</span>
            <span>
                <strong>Protección activa:</strong>
                consultas SQL parametrizadas para evitar la inyección SQL.
            </span>
        </div>
    </main>

    <footer>
        Proyecto académico | Seguridad Informática
    </footer>

</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(
        HTML,
        mensaje_login="",
        tipo_login="",
        mensaje_busqueda=""
    )


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "").strip()
    contrasena = request.form.get("contrasena", "")

    conexion = conectar_db()

    try:
        resultado = conexion.execute(
            """
            SELECT usuario
            FROM usuarios
            WHERE usuario = ? AND contrasena = ?
            """,
            (usuario, contrasena)
        ).fetchone()
    finally:
        conexion.close()

    if resultado:
        mensaje = "Acceso autorizado. Credenciales correctas."
        tipo = "ok"
    else:
        mensaje = "Acceso denegado. Verifica tu usuario y contraseña."
        tipo = "error"

    return render_template_string(
        HTML,
        mensaje_login=mensaje,
        tipo_login=tipo,
        mensaje_busqueda=""
    )


@app.route("/buscar", methods=["POST"])
def buscar():
    nombre = request.form.get("nombre", "").strip()

    conexion = conectar_db()

    try:
        resultados = conexion.execute(
            "SELECT usuario FROM usuarios WHERE usuario = ?",
            (nombre,)
        ).fetchall()
    finally:
        conexion.close()

    if resultados:
        nombres = ", ".join(fila["usuario"] for fila in resultados)
        mensaje = f"Usuario encontrado: {nombres}"
    else:
        mensaje = "No se encontraron usuarios."

    return render_template_string(
        HTML,
        mensaje_login="",
        tipo_login="",
        mensaje_busqueda=mensaje
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
