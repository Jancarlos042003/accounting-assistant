"""
Servicio de extracción de datos usando OpenAI
Procesa texto extraído de documentos y devuelve JSON estructurado
"""

from openai import OpenAI
from typing import Dict, List, Any
from app.schemas.ai_response import InvoiceDataSchema
from app.services.prompt_library import PromptLibrary

prompt_lib = PromptLibrary()


class AIAnalyzer:
    def __init__(self):
        """Inicializa el cliente de OpenAI"""
        self.client = OpenAI()

    def _parse_response(
            self,
            content: Any,
            text_format: Any,
            system_message: str = "Eres un experto en analizar documentos oficiales peruanos de facturas electrónicas. "
                                  "Extraes datos de forma precisa y validas la autenticidad de los documentos.",
            model: str = "gpt-4o-mini"
    ) -> Any:
        """Ejecuta el parsing con OpenAI"""
        response = self.client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            text_format=text_format,
            temperature=0.1
        )
        return response.output_parsed

    def analyze_invoice_data(self, text: str) -> Dict:
        """
        Extrae datos de una factura usando OpenAI

        Args:
            text: Texto extraído del PDF

        Returns:
            Dict con datos estructurados y validación
        """
        prompt = f"""Analiza el siguiente texto extraído de una factura electrónica del Perú

{prompt_lib.render("get_invoice_prompt.txt")}

Texto del documento:
{text}
"""

        try:
            return self._parse_response(
                content=prompt,
                text_format=InvoiceDataSchema,
            )
        except Exception as e:
            return _get_error_response(e)

    def analyze_invoice_data_with_images(self, images_base64: List[str]) -> Dict:
        """
        Extrae datos de una factura usando OpenAI

        Args:
            images_base64: Lista de imágenes en base64

        Returns:
            Dict con datos estructurados y validación
        """
        content = [
            {
                "type": "input_text",
                "text": f"Analiza las siguientes imágenes de una factura electrónica del Perú."
                        f"\n{prompt_lib.render("get_invoice_prompt.txt")}"
            }
        ]

        for img_base64 in images_base64:
            content.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{img_base64}",
                "detail": "high"
            })

        try:
            return self._parse_response(
                content=content,
                text_format=InvoiceDataSchema,
                model="gpt-4.1-mini"
            )
        except Exception as e:
            return _get_error_response(e)


def _get_error_response(error: Exception) -> Dict:
    """Retorna respuesta de error estandarizada"""
    base_response = {
        "is_valid": False,
        "validation_message": "Error al procesar el documento con IA.",
        "error": str(error)
    }

    return base_response
