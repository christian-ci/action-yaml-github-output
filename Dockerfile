FROM python:3.11-slim

COPY action_requirements.txt action_entrypoint.sh main_action.py /

RUN pip install -r action_requirements.txt && chmod +x action_entrypoint.sh

ENTRYPOINT ["/action_entrypoint.sh"]