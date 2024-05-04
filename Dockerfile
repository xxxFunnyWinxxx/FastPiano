FROM python
WORKDIR /app
COPY requirements.txt /app/requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python3 -m pip install --upgrade pip 
RUN python3 -m pip install --upgrade -r requirements.txt


COPY . .
CMD ["python", "manage.py", "runserver"]