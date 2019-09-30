FROM python:3.7.4-alpine

WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements/dev.txt
EXPOSE 8000
ENV ENVIRONMENT dev

CMD ["python3", "app/app.py"]