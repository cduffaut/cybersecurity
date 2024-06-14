FROM python:3.11

RUN apt-get update && apt-get install -y \
    git \
    libpcap-dev \
    && apt-get clean

RUN python3 -m pip install scapy
RUN python3 -m pip install libpcap

WORKDIR /app

COPY inquisitor.py .

CMD ["tail", "-f", "/dev/null"]
