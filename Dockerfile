FROM eclipse-temurin:21

# install apt packages
RUN apt update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y python3
RUN apt-get install -y unzip
RUN apt-get install -y curl

# set working directory
WORKDIR /code

# create and start python virtual environment, install python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt

# install sirius 
RUN curl -L -o sirius.zip https://github.com/sirius-ms/sirius/releases/download/v6.1.1/sirius-6.1.1-linux-x64.zip \
    && unzip sirius.zip -d /opt/sirius \
    && rm sirius.zip

# update PATH to include sirius and python venv
ENV PATH="/opt/sirius/sirius/bin:/opt/venv/bin:${PATH}"

COPY ./ /code

EXPOSE 80
CMD ["uvicorn", "sirius.main:app", "--host", "0.0.0.0", "--port", "80"]
