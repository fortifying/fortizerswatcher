FROM heroku/heroku:18

RUN apt install ca-certificates

RUN apt update

#
# Clone repo and prepare working directory
#
RUN git clone https://github.com/fortifying/fortizerswatcher.git /root/emilia
RUN mkdir /root/emilia/bin/
WORKDIR /root/emilia/
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt
RUN pip3 install tswift
RUN pip3 install gTTS
RUN pip3 install pynewtonmath

CMD ["python3","-m","emilia"]
