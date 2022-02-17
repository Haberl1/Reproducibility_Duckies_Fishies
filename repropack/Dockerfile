# SPDX-License-Identifier: MIT-0

# Start off of a long-term maintained base distribution
FROM ubuntu:20.04

MAINTAINER Sabrina Haberl <sabrina.haberl@st.oth-regensburg.de>

ENV DEBIAN_FRONTEND noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
		build-essential \
		ca-certificates \
		python3 \
		python3-dev \
		python3-pip \
		r-base \
		r-cran-ggplot2 \
		r-cran-reticulate \
		r-cran-reshape2 \
		r-cran-knitr \
		r-cran-tinytex \ 
		sudo \
		texlive-base \
		texlive-bibtex-extra \
		texlive-fonts-recommended \
		texlive-latex-extra \
		texlive-publishers 

# Add user
RUN useradd -m -G sudo -s /bin/bash repro && echo "repro:repro" | chpasswd
RUN usermod -a -G staff repro
USER repro
WORKDIR /home/repro

# Add res directory to container
ADD --chown=repro:repro res/ res/

# Run pip install commands for python script
RUN pip install pandas
RUN pip install matplotlib
RUN pip install scipy

# Convert Report.Rnw to PDF
RUN Rscript -e "require ('knitr'); knit2pdf ('./res/scripts/Report.Rnw')"