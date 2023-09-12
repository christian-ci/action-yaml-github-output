FROM python:3.11-alpine

COPY requirements.txt entrypoint.sh main.py /

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -r requirements.txt && chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
