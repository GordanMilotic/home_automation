FROM python:3.10.7
WORKDIR /main
ADD . /main
COPY requirements.txt req.txt
RUN pip install --no-cache-dir -r req.txt
EXPOSE 8080
CMD ["python", "main.py"]