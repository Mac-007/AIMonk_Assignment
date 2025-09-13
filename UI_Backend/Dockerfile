# UI_Backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and templates/static
COPY ui_backend.py /app/ui_backend.py
COPY templates/ /app/templates/
COPY static/ /app/static/

EXPOSE 5000

CMD ["python", "ui_backend.py"]
