FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8501

COPY . /app

#ENTRYPOINT ["streamlit","run"]

#CMD ["CCRIS_Uploading.py"]

CMD ["streamlit","run","CCRIS_Uploading.py"]

