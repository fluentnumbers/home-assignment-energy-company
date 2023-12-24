FROM python:3.10.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/
COPY task1.py /app/
COPY app.py /app/

COPY tools /app/tools
COPY models /app/models

EXPOSE 5000

CMD ["python", "app.py"]
