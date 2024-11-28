FROM python:3.12

RUN python -m pip install flask==2.3.2 sqlalchemy==2.0.35 pymysql==1.1.1 cryptography==43.0.1 pandas 

WORKDIR ./

ENTRYPOINT ["/bin/bash", "-c", "python app.py"]