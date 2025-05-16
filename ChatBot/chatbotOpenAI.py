from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def buscar_en_google(pregunta):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": pregunta
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        resultados = response.json()
        enlaces = []
        for item in resultados.get("organic", [])[:5]:
            enlaces.append({
                "titulo": item.get("title"),
                "url": item.get("link")
            })
        return enlaces
    except Exception as e:
        print(f"Chatbot: Error al buscar en Google: {e}")
        return []

def extraer_texto_de_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        texto = " ".join([p.get_text() for p in soup.find_all("p")])
        return texto[:1000]
    except Exception as e:
        return f"No se pudo extraer texto de {url}: {e}"

def generar_respuesta_llm(historial, textos_fuentes, pregunta):
    mensajes = []
    for mensaje in historial:
        rol = "user" if mensaje["rol"] == "usuario" else "assistant"
        mensajes.append({"role": rol, "content": mensaje["contenido"]})
    contexto = "Información encontrada en internet:\n"
    for fuente in textos_fuentes:
        contexto += f"- {fuente['titulo']}: {fuente['texto']}\n"
    mensajes.append({"role": "system", "content": contexto})
    mensajes.append({"role": "user", "content": pregunta})

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensajes,
            max_tokens=300,
            temperature=0.7
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar respuesta con OpenAI: {e}"

# Inicializa la memoria de conversación como una lista vacía
historial_conversacion = []

while True:
    try:
        mensaje_usuario = input("Usuario: ")
        if mensaje_usuario.lower() in ["salir", "exit", "quit"]:
            print("Chatbot: ¡Hasta luego!")
            break

        historial_conversacion.append({"rol": "usuario", "contenido": mensaje_usuario})

        print("Chatbot: ** Búsqueda en internet **")
        enlaces = buscar_en_google(mensaje_usuario)

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

        respuesta_bot = generar_respuesta_llm(historial_conversacion, textos_fuentes, mensaje_usuario)

        if textos_fuentes and not respuesta_bot.startswith("Error al generar respuesta"):
            respuesta_bot += "\n\nReferencias:\n"
            for fuente in textos_fuentes:
                respuesta_bot += f"- {fuente['titulo']}: {fuente['url']}\n"

        historial_conversacion.append({"rol": "bot", "contenido": respuesta_bot})

        print(f"Chatbot: {respuesta_bot}")
    except Exception as e:
        print(f"Chatbot: Error inesperado: {e}")
        break