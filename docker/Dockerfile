FROM python:3.10.12-slim-bullseye
WORKDIR /flask
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "flask", "--app" ,"src", "run", "--host=0.0.0.0"]