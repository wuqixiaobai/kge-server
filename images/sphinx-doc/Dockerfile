FROM continuumio/miniconda3

MAINTAINER Víctor Fernández <vfrico@gmail.com>

USER root

# Install some dependencies and updates
RUN apt-get update && \
    apt-get install -y gcc g++ make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add user for run server
ENV CONDA_USER_UID 1001
ENV CONDA_USER kgeserver
RUN useradd -m -s /bin/bash -N -u $CONDA_USER_UID $CONDA_USER && \
    chown $CONDA_USER_UID:users -R /opt/conda

# Install some conda dependencies
RUN conda install --yes scikit-learn scipy cython &&\
    conda clean -tipsy

# Install kge-server and its dependencies
RUN pip install --upgrade pip
RUN pip install setuptools requests nose falcon
RUN cd /home/$CONDA_USER/ && git clone https://github.com/vfrico/kge-server.git && \
    cd kge-server/ && python3 setup.py install

# Once tools to build Annoy are used, uninstall them
RUN apt-get remove gcc g++ -y && \
    apt-get autoremove -y

# Init system and launch script
ENTRYPOINT ["/bin/bash", "launch_docs.sh"]

COPY launch_docs.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/launch_docs.sh

# Exit from root user
USER $CONDA_USER
ENV PATH /opt/conda/bin:$PATH
