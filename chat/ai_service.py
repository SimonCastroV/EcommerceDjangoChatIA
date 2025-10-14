import os
import google.generativeai as genai
from django.conf import settings

class GeminiService:
    def __init__(self):
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            raise ValueError("⚠️ GEMINI_API_KEY no configurada en el archivo .env")

        genai.configure(api_key=api_key)

    
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def generate_response(self, user_message, products, context):
        product_text = "\n".join(
            [f"- {p.name} ({p.brand}) {p.category}, color {p.color}, talla {p.size}, ${p.price}"
             for p in products]
        ) or "No hay productos disponibles."

        context_text = "\n".join([
            f"{m.role.capitalize()}: {m.message}" for m in context
        ])

        prompt = f"""
Eres un asistente de ventas para una tienda de ropa y calzado.
Usa el catálogo de productos para responder preguntas y sugerir prendas.

Catálogo:
{product_text}

Historial:
{context_text}

Cliente: {user_message}
Asistente:
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error al conectar con la IA: {e}"
