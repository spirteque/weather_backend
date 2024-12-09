FROM python:3.12.8-alpine


#ENV OPEN_METEO_BASE_URL=https://api.open-meteo.com
#ENV MIN_LATITUDE=-90
#ENV MAX_LATITUDE=90
#ENV MIN_LONGITUDE=-180
#ENV MAX_LONGITUDE=180
#ENV INSTALLATION_POWER_KW=2.5
#ENV INSTALLATION_EFFICIENCY=0.2
#ENV PRODUCTION=1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
