FROM python:3.5.6

MAINTAINER xuyong@gintong.com

RUN git clone https://github.com/xuyonggit/uploadfile.git && \
		cd uploadfile &&\
		pip3 install -r requirements

WORKDIR /uploadfile/uploadfile

CMD ["python", "uploadfile.py"]
