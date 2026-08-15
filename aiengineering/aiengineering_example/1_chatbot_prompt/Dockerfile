FROM python:3.11-slim

# Set working directory di dalam kontainer
WORKDIR /app

# Install dependensi Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy kode aplikasi
COPY 1_chatbot_terminal.py .

# Pastikan output Python langsung keluar ke terminal (tanpa buffering)
ENV PYTHONUNBUFFERED=1

# Command default untuk menjalankan chatbot
CMD ["python", "1_chatbot_terminal.py"]
