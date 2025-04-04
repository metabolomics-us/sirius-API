FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code
EXPOSE 80
# TODO, launch service with uvicorn. Is "sirius-api.web.main:app" correct here? And the port?
CMD ["uvicorn", "sirius.main:app", "--host", "0.0.0.0", "--port", "80"]
