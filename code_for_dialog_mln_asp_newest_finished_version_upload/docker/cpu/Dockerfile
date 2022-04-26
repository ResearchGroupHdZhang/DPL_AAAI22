FROM tensorflow/tensorflow:1.14.0
# ADD file:d2abb0e4e7ac1773741f51f57d3a0b8ffc7907348842d773f8c341ba17f856d5 in / 
WORKDIR /pydial/
COPY ./requirements.txt /tmp/requirements.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN apt-get update --fix-missing 
RUN apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion vim &&     apt-get clean
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh &&     /bin/bash ~/anaconda.sh -b -p /opt/conda &&     rm ~/anaconda.sh &&     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh &&     echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc &&     echo "conda activate base" >> ~/.bashrc &&     find /opt/conda/ -follow -type f -name '*.a' -delete &&     find /opt/conda/ -follow -type f -name '*.js.map' -delete &&     /opt/conda/bin/conda clean -afy
RUN conda init bash
RUN yes | conda create -n py2 python=2.7
SHELL [ "conda" , "run", "-n", "py2", "/bin/bash", "-c"]
RUN ls -al
RUN pwd
RUN yes | conda install -c potassco clingo

RUN yes | pip install -r /tmp/requirements.txt


ENTRYPOINT ["conda" , "run", "-n", "py2", "python", "pydial.py"]