FROM python:3

WORKDIR /app
ENV FLASK_APP =./app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
