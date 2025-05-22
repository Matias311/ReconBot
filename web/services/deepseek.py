import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def consultar_deepseek(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek/deepseek-prover-v2:free",
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente útil que responde en español, cada respuesta tiene que ser con esta estructura: Respuesta:  y ahi recien escribes tu respuesta",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 5000,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=70)

        # Manejar errores HTTP con claridad
        if response.status_code == 402:
            return "Tu cuenta de DeepSeek no tiene crédito o acceso habilitado. Verifica tu plan en https://platform.deepseek.com"

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "Tiempo de espera agotado al contactar DeepSeek."

    except requests.exceptions.ConnectionError as conn_err:
        return f"No se pudo establecer conexión con DeepSeek. {str(conn_err)}"

    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err.response.status_code} - {http_err.response.text}"

    except requests.exceptions.RequestException as req_err:
        return f"Error de solicitud: {str(req_err)}"

    except Exception as e:
        return f"Error inesperado: {str(e)}"
