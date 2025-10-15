FROM python:3.13-slim

# Instalar Tesseract y el modelo en español
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libtesseract-dev \
    libleptonica-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Agregar al PATH tanto el binario de UV como el entorno virtual que creará UV
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

WORKDIR /app

# Copiar solo archivos necesarios primero (para aprovechar cache)
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen

# Copiar el resto del proyecto
COPY . .

EXPOSE 8000

# Ejecutar la app usando uv dentro del entorno virtual
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]