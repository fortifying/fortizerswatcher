FROM heinzdf/fortizerswxtcher:skyfall

#
# Clone repo and prepare working directory
#
RUN git clone https://github.com/fortifying/fortizerswatcher.git /skyfall/fortizers
RUN mkdir /skyfall/bin/
WORKDIR /skyfall/fortizers/

CMD ["python3","-m","fortizers"]
