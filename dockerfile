FROM python:3.7-alpine
RUN apk add git

RUN git clone https://github.com/MSDS698/2021-product-analytics-group-project-group_4_readthesign /MSDS698/2021-product-analytics-group-project-group_4_readthesign 
WORKDIR /MSDS698/2021-product-analytics-group-project-group_4_readthesign 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

# CMD python application.py