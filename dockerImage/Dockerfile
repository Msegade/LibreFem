FROM centos:7

MAINTAINER miguelrsegade@gmail.com  

# Update and prerequisites
RUN yum clean all   && \
    yum -y update   && \
    yum -y install wget \
                   gawk \
                   make cmake \
                   gdb ddd \
                   gcc g++ gfortran \
                   python python-devel python-numpy python-qt4 \
                   tk \
                   bison flex \
                   liblapack-devel \
                   zlib-devel \
                   gnuplot \
                   sudo && \
    yum clean all       && \
    rm -rf /var/cache/*

# Default user without password and sudo
ARG USER=librefem
RUN adduser $USER
RUN passwd -d $USER
RUN usermod -aG wheel $USER

# Set permissions and enviromental variables
RUN chown -R $USER:$USER /home/$USER
USER $USER
ENV HOME /home/$USER
ENV USER $USER
WORKDIR $HOME


