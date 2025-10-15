import fitz  # PyMuPDF
import requests
from fastapi import APIRouter, HTTPException
from app.services.document_analyzer import DocumentAnalyzer
from app.services.signed_url import generate_signed_url

documents_router = APIRouter()


@documents_router.post("/validate")
def validate_document(blob_name: str):
    try:
        # Generar una URL firmada
        signed_url = generate_signed_url(blob_name)

        # Obtener el archivo desde la URL firmada
        response = requests.get(signed_url)
        response.raise_for_status()  # Lanza excepción si el status code no es 200

        content = response.content

        # Abrir el PDF
        with fitz.open(stream=content, filetype="pdf") as pdf_doc:
            # Inicializar el analizador
            analyzer = DocumentAnalyzer()

            # Analizar el documento
            result = analyzer.analyze_document(pdf_doc=pdf_doc, )

            return {
                "status": "success",
                "data": result
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el documento: {str(e)}")
