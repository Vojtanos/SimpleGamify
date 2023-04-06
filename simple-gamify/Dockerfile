FROM python:3.10
RUN mkdir /simple-gamify
WORKDIR /simple-gamify
COPY requirements.txt /simple-gamify/requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"] 