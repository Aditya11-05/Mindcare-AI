# MindCare AI — Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose FastAPI on 8000 and Streamlit on 8501
EXPOSE 8000 8501

# Default env
ENV API_URL=http://localhost:8000/chat
ENV DB_URL=sqlite:///mindcare.db

# Start both services
# Note: in single container, we'll run backend in background then Streamlit
CMD bash -lc 'uvicorn src.api:app --host 0.0.0.0 --port 8000 & streamlit run app/ui_streamlit.py --server.port 8501 --server.address 0.0.0.0'
