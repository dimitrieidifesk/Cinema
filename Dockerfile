FROM python:3.10

WORKDIR /opt/api


COPY requirements.txt .

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_api.sh .
COPY src .

RUN chmod +x /opt/api/run_api.sh
ENTRYPOINT [ "/opt/api/run_api.sh" ]