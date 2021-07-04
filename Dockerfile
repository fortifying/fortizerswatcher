FROM heroku/heroku:18

RUN apt install ca-certificates

RUN apt update

# Set timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
#
# Clone repo and prepare working directory
#
RUN git clone https://github.com/fortifying/fortizerswatcher.git -b is-wip /root/fortizers

WORKDIR /root/fortizers

RUN apt install -y \
    curl \
    figlet \
    gcc \
    g++ \
    git \
    aria2 \
    libpq-dev \
    python3-pip \
    postgresql \
    postgresql-client \
    openssl \
    pv \
    jq \
    wget \
    python3 \
    python3-dev \
    sqlite \
    ffmpeg \
    sudo

RUN pip3 install -r requirements.txt
RUN pip3 install tswift
RUN pip3 install gTTS
RUN pip3 install pynewtonmath

CMD ["python3","-m","fortizers"]
