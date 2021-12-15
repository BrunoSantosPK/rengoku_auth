FROM python:3.8-slim-buster
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:3636", "wsgi"]