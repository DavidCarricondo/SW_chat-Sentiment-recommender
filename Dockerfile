FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3 python3-pip

COPY . .

RUN pip3 install -r requirements.txt


EXPOSE 3500


RUN python3 -c "import nltk; nltk.download('vader_lexicon', download_dir='/usr/local/share/nltk_data')" 
RUN python3 -c "import nltk; nltk.download('stopwords', download_dir='/usr/local/share/nltk_data')" 


ENTRYPOINT ["python3"]
CMD ["api.py"]