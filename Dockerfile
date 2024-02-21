FROM python:3.11-slim

WORKDIR /device_statistic_analysis
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
