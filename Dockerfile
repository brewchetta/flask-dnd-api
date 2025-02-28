FROM PYTHON:latest
# TODO: double check python version
# TODO: see if pip needs to be added

COPY /server/routes/ /app/
COPY /server/app.py /app/
COPY /server/config.py /app/
COPY /server/create_app.py /app/
COPY /server/damage_types.py /app/
COPY /server/helpers.py /app/
COPY /server/models.py /app/
COPY /requirements.txt /app/

WORKDIR /app

RUN pip install requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "app:app"]