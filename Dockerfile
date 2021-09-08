FROM ubuntu:20.04

# ENV
ENV DEBIAN_FRONTEND noninteractive

# Package
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update \
  && apt-get install -y python3.8 python3-pip python3-dev \
  && apt-get install -y git vim apt-utils nano  \
  && apt-get install -y build-essential xorg libssl-dev libxrender-dev wget \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3.8 python \
  && ln -s /usr/bin/python3.8 python3

# Set timezone for this container(CST)
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Installsshd
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:systex123!' | chpasswd
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so @g' -i /etc/pam.d/sshd

# Install OpenJDK-8  for dbconnect driver
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# Install Python 3.8
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 0

# Python pip initial & install requirements
COPY requirements.txt /requirements.txt
RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN pip3 install -r requirements.txt
RUN mkdir /var/lib/jupyter/

#CMD ["jupyter", "notebook", "--allow-root", "--port", "8888"]

# Ports
#EXPOSE 8888