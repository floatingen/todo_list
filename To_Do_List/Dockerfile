# pull official base image
FROM python:3.11

# create the appropriate directories
# ENV HOME=/home/app
ENV APP_HOME=/usr/src/main
# RUN mkdir -p $APP_HOME
# RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]