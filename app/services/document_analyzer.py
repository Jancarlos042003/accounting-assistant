import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from typing import Dict
from app.services.ai_analyzer import AIAnalyzer
import base64


class DocumentAnalyzer:
    def __init__(self):
        """Inicializa el analizador de documentos"""
        # Configurar Tesseract para español
        self.tesseract_config = '--oem 3 --psm 6'
        self.lang = 'spa'

    def extract_pdf_text(self, pdf_doc: fitz.Document) -> str:
        """Extrae texto de PDF, detectando automáticamente si necesita OCR"""
        complete_text = ""

        # Extraer texto directamente
        for page in pdf_doc:
            complete_text += page.get_text() + "\n\n"

        # También extraer texto de imágenes incrustadas
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            images = page.get_images()

            if images:
                print(f"Encontradas {len(images)} imágenes en página {page_num + 1}")
                for img_index, img in enumerate(images):
                    try:
                        xref = img[0]
                        base_image = pdf_doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))

                        # Aplicar OCR a la imagen
                        img_text = pytesseract.image_to_string(
                            image,
                            lang=self.lang,
                            config=self.tesseract_config
                        )
                        if img_text.strip():
                            complete_text += f"\n[Texto de imagen {img_index + 1}]\n{img_text}\n"
                    except Exception as e:
                        print(f"   Error procesando imagen {img_index + 1}: {e}")

        return complete_text

    def analyze_document(self, pdf_doc: fitz.Document) -> Dict:
        """
        Analiza un documento PDF y extrae la información relevante

        Args:
            pdf_doc: Objeto fitz.Document ya abierto

        Returns:
            Diccionario con los datos extraídos
        """
        analyzer = AIAnalyzer()

        if is_scanned_pdf(pdf_doc):
            images = process_pdf_with_images(pdf_doc)
            data = analyzer.analyze_invoice_data_with_images(images)
        else:
            text = self.extract_pdf_text(pdf_doc)
            data = analyzer.analyze_invoice_data(text)

        return {
            'extracted_data': data,
        }


def is_scanned_pdf(pdf_doc: fitz.Document) -> bool:
    """Detecta si el PDF es escaneado o tiene texto seleccionable"""
    total_text = ""

    for page in pdf_doc:
        total_text += page.get_text()

    # Si tiene poco texto, probablemente es escaneado
    return len(total_text.strip()) < 50


def process_pdf_with_images(pdf_doc):
    """
    Procesa el PDF y guarda las imágenes de cada página
    """
    images_base64 = []

    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        # Renderizar página como imagen (300 DPI para mejor calidad)
        pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
        img_bytes = pix.tobytes("png")

        # Convertir a base64 para enviar a OpenAI
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        images_base64.append(img_base64)

    return images_base64
