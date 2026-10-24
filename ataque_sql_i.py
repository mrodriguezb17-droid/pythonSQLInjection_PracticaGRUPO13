import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser

# Direcciones de las aplicaciones de prueba
URL_VULNERABLE = "http://127.0.0.1:5000"
URL_SEGURA = "http://127.0.0.1:5001"

# Entradas utilizadas para simular SQL Injection
PAYLOAD_LOGIN = "' OR '1'='1' -- "
PAYLOAD_BUSQUEDA = "' OR 1=1 -- "


class LectorHTML(HTMLParser):
    """Extrae el texto visible de una página HTML."""

    def __init__(self):
        super().__init__()
        self.textos = []
        self.omitir = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.omitir += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self.omitir > 0:
            self.omitir -= 1

    def handle_data(self, data):
        texto = data.strip()
        if texto and self.omitir == 0:
            self.textos.append(texto)

    def obtener_texto(self):
        return " ".join(self.textos)


def enviar_prueba(url, ruta, datos, metodo="POST"):
    """Envía datos mediante GET o POST y devuelve la respuesta."""

    try:
        if metodo == "GET":
            parametros = urllib.parse.urlencode(datos)
            destino = f"{url}{ruta}?{parametros}"

            solicitud = urllib.request.Request(
                destino,
                method="GET"
            )
        else:
            formulario = urllib.parse.urlencode(datos).encode("utf-8")

            solicitud = urllib.request.Request(
                f"{url}{ruta}",
                data=formulario,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                method="POST"
            )

        with urllib.request.urlopen(solicitud, timeout=5) as respuesta:
            codigo = respuesta.status
            contenido = respuesta.read().decode(
                "utf-8", errors="replace"
            )

    except urllib.error.HTTPError as error:
        codigo = error.code
        contenido = error.read().decode(
            "utf-8", errors="replace"
        )

    except urllib.error.URLError as error:
        print(f"No se pudo conectar con {url}: {error.reason}")
        return None, ""

    except TimeoutError:
        print(f"Tiempo de espera agotado al conectar con {url}.")
        return None, ""

    lector = LectorHTML()
    lector.feed(contenido)

    return codigo, lector.obtener_texto()


def probar_login(nombre, url):
    print("\nPrueba de autenticación:")

    codigo, respuesta = enviar_prueba(
        url,
        "/login",
        {
            "usuario": PAYLOAD_LOGIN,
            "contrasena": "prueba123"
        },
        metodo="POST"
    )

    if codigo is None:
        print("No se pudo completar la prueba de autenticación.")
        return

    print(f"Estado HTTP: {codigo}")

    if "Acceso concedido:" in respuesta:
        print("Resultado: la aplicación permitió el acceso.")
        if nombre == "VULNERABLE":
            print("Observación: posible bypass de autenticación.")
    elif "Acceso autorizado." in respuesta:
        print("Resultado: acceso autorizado por la aplicación.")
    elif "Acceso denegado." in respuesta:
        print("Resultado: acceso rechazado por la aplicación segura.")
    else:
        print("Resultado: revisa el mensaje mostrado por la aplicación.")

    if respuesta:
        print("Respuesta:", respuesta[:350])


def probar_busqueda(nombre, url):
    print("\nPrueba de búsqueda:")

    # La aplicación vulnerable utiliza GET.
    # La aplicación segura utiliza POST.
    if nombre == "VULNERABLE":
        metodo = "GET"
    else:
        metodo = "POST"

    codigo, respuesta = enviar_prueba(
        url,
        "/buscar",
        {"nombre": PAYLOAD_BUSQUEDA},
        metodo=metodo
    )

    if codigo is None:
        print("No se pudo completar la prueba de búsqueda.")
        return

    print(f"Estado HTTP: {codigo}")

    if codigo != 200:
        print("La solicitud no se completó correctamente.")
        if respuesta:
            print("Respuesta:", respuesta[:350])
        return

    if respuesta.count("Usuario:") >= 2:
        print("Resultado: se mostraron varios registros.")
        print("Observación: posible extracción mediante SQL Injection.")
    elif "No se encontraron usuarios." in respuesta:
        print("Resultado: no se encontraron registros.")
        print("La consulta segura no devolvió coincidencias.")
    elif "Usuario encontrado:" in respuesta:
        print("Resultado: la aplicación devolvió una coincidencia.")
    else:
        print("Resultado: revisa la respuesta de la búsqueda.")

    if respuesta:
        print("Respuesta:", respuesta[:350])


def ejecutar_pruebas():
    print("=" * 55)
    print(" SIMULACIÓN DE SQL INJECTION")
    print(" Materia: Seguridad Informática")
    print("=" * 55)

    aplicaciones = [
        ("VULNERABLE", URL_VULNERABLE),
        ("SEGURA", URL_SEGURA)
    ]

    for nombre, url in aplicaciones:
        print("\n" + "-" * 55)
        print(f"APLICACIÓN {nombre}")
        print("-" * 55)

        probar_login(nombre, url)
        probar_busqueda(nombre, url)

    print("\n" + "=" * 55)
    print("FIN DE LAS PRUEBAS")
    print("=" * 55)
    print("Compara los resultados de ambas aplicaciones.")
    print("Esta simulación debe ejecutarse únicamente en local.")


if __name__ == "__main__":
    ejecutar_pruebas()
