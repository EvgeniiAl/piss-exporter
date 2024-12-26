FROM python:3.13.1-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED=TRUE
EXPOSE 8000
ADD src /app
RUN pip install --no-cache-dir --no-input -r requirements.txt
CMD [ "python", "piss_exporter.py" ]
