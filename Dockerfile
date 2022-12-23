from python:3.8

workdir /src

# First install dependencies as they change less frequently than code
COPY requirements.txt /src
RUN pip install -Ur requirements.txt

copy . /src


entrypoint ["python", "main.py"]
