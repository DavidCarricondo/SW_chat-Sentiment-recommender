FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3 python3-pip

COPY . .

RUN pip3 install -r requirements.txt


EXPOSE 3500


RUN python3 -c "import nltk; nltk.download('vader_lexicon')" 
RUN python3 -c "import nltk; nltk.download('stopwords')" 


ENTRYPOINT ["python3"]
CMD ["api.py"]