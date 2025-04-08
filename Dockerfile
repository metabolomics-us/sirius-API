FROM eclipse-temurin:21
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt update
RUN apt install -y pthon3-pip python3-venv python3
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code
EXPOSE 80
CMD ["uvicorn", "sirius.main:app", "--host", "0.0.0.0", "--port", "80"]
