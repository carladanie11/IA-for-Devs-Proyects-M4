# IA-for-Devs-Proyects-M4
# ChatBot con OpenAI y Búsqueda Web

Este proyecto es un chatbot en consola que responde preguntas del usuario utilizando la API de OpenAI (GPT-3.5/4) y realiza búsquedas en internet usando Serper.dev para enriquecer sus respuestas con información actualizada.

## Requisitos

- Python 3.8 o superior
- Una API Key de [OpenAI](https://platform.openai.com/)
- Una API Key de [Serper.dev](https://serper.dev/)
- Entorno virtual recomendado (`venv`)

## Instalación

1. **Clona el repositorio o descarga los archivos.**

2. **Crea y activa un entorno virtual:**
   ```bash
   python3 -m venv bot_venv
   source bot_venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   Si no tienes `requirements.txt`, instala manualmente:
   ```bash
   pip install openai requests beautifulsoup4
   ```

4. **Configura tus claves API:**
   - Abre el archivo `chatbotOpenAI.py`.
   - Reemplaza los valores de `SERPER_API_KEY` y `OPENAI_API_KEY` por tus claves reales.

## Uso

Ejecuta el chatbot desde la terminal:

```bash
python chatbotOpenAI.py
```

- Escribe tu pregunta y presiona Enter.
- El bot buscará información relevante en internet y generará una respuesta usando OpenAI.
- Escribe `salir`, `exit` o `quit` para terminar la conversación.

## Ejemplo de interacción

```
Usuario: ¿Qué es una abeja?
Chatbot: ** Búsqueda en internet **
Chatbot: He encontrado los siguientes enlaces relevantes:
- Abeja - Wikipedia: https://es.wikipedia.org/wiki/Abeja
...
Chatbot: Las abejas son insectos himenópteros conocidos por...
Referencias:
- Abeja - Wikipedia: https://es.wikipedia.org/wiki/Abeja
...
```

## Notas

- Si ves errores de cuota o autenticación, revisa tus claves y el estado de tu cuenta en OpenAI y Serper.dev.
- El bot limita la cantidad de texto extraído de cada página para optimizar el uso de tokens en la API de OpenAI.

## Dependencias

Incluye en tu `requirements.txt`:

```
openai
requests
beautifulsoup4
```

---
