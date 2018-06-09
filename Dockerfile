FROM tensorflow/tensorflow:1.5.1-py3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD python app.py

WORKDIR /var/work