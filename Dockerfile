FROM python:3.7-buster

COPY req /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY main.py /app/webapp.py
COPY calc.py /app/calc.py

WORKDIR /app
EXPOSE 8000
CMD ["python", "webapp.py"]