# Inicializa la memoria de conversación como una lista vacía
historial_conversacion = []

while True:
    # Solicita la entrada del usuario
    mensaje_usuario = input("Usuario: ")
    if mensaje_usuario.lower() in ["salir", "exit", "quit"]:
        print("Chatbot: ¡Hasta luego!")
        break

    # Guarda el mensaje del usuario en el historial
    historial_conversacion.append({"rol": "usuario", "contenido": mensaje_usuario})

    # Aquí iría la lógica para generar la respuesta del bot (por ahora, respuesta de ejemplo)
    respuesta_bot = "Esta es una respuesta de ejemplo."

    # Guarda la respuesta del bot en el historial
    historial_conversacion.append({"rol": "bot", "contenido": respuesta_bot})

    # Muestra la respuesta del bot
    print(f"Chatbot: {respuesta_bot}")

# Si quieres ver el historial al final, puedes descomentar la siguiente línea:
# print(historial_conversacion)

from bs4 import BeautifulSoup
import requests

# Reemplaza esto con tu API Key real de Serper.dev
SERPER_API_KEY = "fdce4b4626734d8685d890b534a7d98ad484ebaa"

def buscar_en_google(pregunta):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": pregunta
    }
    response = requests.post(url, headers=headers, json=data)
    resultados = response.json()
    # Extrae los primeros 5 enlaces relevantes
    enlaces = []
    for item in resultados.get("organic", [])[:5]:
        enlaces.append({
            "titulo": item.get("title"),
            "url": item.get("link")
        })
    return enlaces

def extraer_texto_de_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extrae solo los párrafos como ejemplo simple
        texto = " ".join([p.get_text() for p in soup.find_all("p")])
        # Limita el texto a 1000 caracteres para no sobrecargar el modelo
        return texto[:1000]
    except Exception as e:
        return f"No se pudo extraer texto de {url}: {e}"

# Inicializa la memoria de conversación como una lista vacía
historial_conversacion = []

while True:
    # Solicita la entrada del usuario
    mensaje_usuario = input("Usuario: ")
    if mensaje_usuario.lower() in ["salir", "exit", "quit"]:
        print("Chatbot: ¡Hasta luego!")
        break

    # Guarda el mensaje del usuario en el historial
    historial_conversacion.append({"rol": "usuario", "contenido": mensaje_usuario})

    # Realiza la búsqueda en Google usando Serper.dev
    print("Chatbot: ** Búsqueda en internet **")
    enlaces = buscar_en_google(mensaje_usuario)

    # Extrae el texto de los enlaces encontrados
    textos_fuentes = []
    if enlaces:
        print("Chatbot: He encontrado los siguientes enlaces relevantes:")
        for enlace in enlaces:
            print(f"- {enlace['titulo']}: {enlace['url']}")
            texto = extraer_texto_de_url(enlace["url"])
            textos_fuentes.append({
                "titulo": enlace["titulo"],
                "url": enlace["url"],
                "texto": texto
            })
    else:
        print("Chatbot: No se encontraron resultados relevantes.")

    # (Opcional) Muestra un resumen del texto extraído para cada fuente
    for fuente in textos_fuentes:
        print(f"\nFuente: {fuente['titulo']} ({fuente['url']})")
        print(f"Texto extraído: {fuente['texto'][:300]}...")  # Solo muestra los primeros 300 caracteres

    # Respuesta de ejemplo (puedes mejorar esto en el siguiente paso)
    respuesta_bot = "Esta es una respuesta de ejemplo."

    # Guarda la respuesta del bot en el historial
    historial_conversacion.append({"rol": "bot", "contenido": respuesta_bot})

    # Muestra la respuesta del bot
    print(f"Chatbot: {respuesta_bot}")

# Si quieres ver el historial al final, puedes descomentar la siguiente línea:
# print(historial_conversacion)