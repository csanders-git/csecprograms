FROM fedora:25
MAINTAINER Chaim Sanders chaim.sanders@gmail.com

RUN dnf install -y python-pip

COPY . /opt/csecprogram

RUN cd /opt/csecprogram && \
    pip install -r requirments.txt

EXPOSE 80

CMD ["python","/opt/csecprogram/app.py"]


