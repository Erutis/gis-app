FROM python

COPY ./ .

ENV POSTGRES_USER nyc
ENV POSTGRES_PASSWORD gis
ENV POSTGRES_DB nyc

RUN pip install -r ../requirements.txt

CMD [python db_setup.py]

