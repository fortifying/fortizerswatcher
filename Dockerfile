FROM heinzdf/fortizerswxtcher:skyfall

# Set timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
#
# Clone repo and prepare working directory
#
RUN git clone https://github.com/fortifying/fortizerswatcher.git /skyfall/fortizers
RUN mkdir /skyfall/bin/
WORKDIR /skyfall/fortizers/

CMD ["python3","-m","fortizers"]
