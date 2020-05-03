FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3 python3-pip

COPY . .

EXPOSE 3500

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["api.py"]