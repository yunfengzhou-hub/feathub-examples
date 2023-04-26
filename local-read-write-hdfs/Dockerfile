FROM apache/spark:v3.3.1

USER root

WORKDIR /opt/spark

RUN apt-get update && apt-get install -y vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip

# Install Feathub to allow submitting Feathub programs
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install 'feathub-nightly[spark]'
