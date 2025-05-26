# Please see README file for instructions.

FROM python:3.8
WORKDIR /opt/ev_share_predictor

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir templates
COPY ev_data.csv .
COPY model.py .
RUN python3 model.py

COPY templates/index.html templates/
COPY templates/result.html templates/
COPY flaskapp.py .

ENTRYPOINT ["python3", "flaskapp.py"]
