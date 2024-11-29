FROM python:3.12

RUN python -m pip install flask sqlalchemy==2.0.35 pymysql==1.1.1 cryptography==43.0.1 pandas

RUN mkdir /app

WORKDIR /app

ENTRYPOINT ["/bin/bash", "-c", "python app.py"]
