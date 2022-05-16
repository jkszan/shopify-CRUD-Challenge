FROM ubuntu:18.04

# Installing python3 and upgrading pip
RUN apt-get update -y && \
    apt-get install -y python3.8 python3-pip && \
    pip3 install --upgrade pip


# We are going to paramaterize this to make it easy to change in the future
ARG appdir=/opt/app

COPY ./requirements.txt ${appdir}/requirements.txt

WORKDIR $appdir

# We want to get all of our downloads and requirement installations done before we touch any application files, this is to leverage
# the Docker image layering system to avoid redownloading dependencies in response to any change in source code
RUN pip3 install -r requirements.txt

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Copying all source into our application directory
COPY  . $appdir

EXPOSE 5000

CMD [ "flask", "run" ]