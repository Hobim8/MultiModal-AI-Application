FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

# Install CPU only PyTorch to avoid massive CUDA downloads
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]