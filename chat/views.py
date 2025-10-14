import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import ChatMessage
from products.models import Product
from .ai_service import GeminiService


def chat_ui(request):
    """Muestra la interfaz del chat"""
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    return render(request, "chat/chat.html", {"session_id": session_id})


@require_POST
def chat_message_api(request):
    """Recibe el mensaje del usuario y devuelve la respuesta de Gemini"""
    try:
        # Leer datos del cuerpo de la solicitud
        data = json.loads(request.body)
        session_id = data.get("session_id")
        user_text = data.get("message", "").strip()

        if not user_text:
            return JsonResponse({"error": "Mensaje vacío"}, status=400)

        # Guardar el mensaje del usuario
        ChatMessage.objects.create(session_id=session_id, role="user", message=user_text)

        # Obtener historial de la sesión
        context = list(ChatMessage.objects.filter(session_id=session_id).order_by("created_at")[:6])

        products = Product.objects.all()

        # Generar respuesta de la IA
        try:
            ai = GeminiService()
            ai_response = ai.generate_response(user_text, products, context)
        except Exception as e:
            # Error interno al llamar a Gemini
            traceback.print_exc()
            ai_response = f"⚠️ Error al conectar con la IA: {e}"

        # Guardar respuesta de la IA
        ChatMessage.objects.create(session_id=session_id, role="assistant", message=ai_response)

        # Responder con JSON al frontend
        return JsonResponse({
            "session_id": session_id,
            "user_message": user_text,
            "assistant_message": ai_response,
            "timestamp": timezone.now().isoformat(),
        })

    except Exception as e:
        # Captura de cualquier otro error inesperado
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
