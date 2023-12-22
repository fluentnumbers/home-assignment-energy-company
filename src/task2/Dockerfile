FROM python:3.10.13-alpine3.19
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

CMD ["python", "task2.py"]
