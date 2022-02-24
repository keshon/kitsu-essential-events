FROM python:3.10-buster AS mybuildstage

RUN python3 -m venv /opt/venv

ADD src /usr/project

WORKDIR /usr/project

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Run the application:
CMD . /opt/venv/bin/activate && exec python main.py