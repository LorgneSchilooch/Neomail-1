# Set the base image using miniconda 
FROM continuumio/anaconda3

# Create environnement Python 3.7
RUN conda update -n base -c defaults conda
RUN conda create -n envPython37 python=3.7

# Install packages in environnement workflow
# Run one environment workflow from env of anaconda
RUN echo "source activate envPython37" > ~/.bashrc

# redirection of environment
ENV PATH /opt/conda/envs/envPython37/bin:$PATH
RUN pip install --upgrade pip
RUN pip install -U --upgrade protobuf && \
pip install numpy && \
pip install h5py && \
pip install jupyter && \
pip install graphviz && \
pip install pandas && \
pip install pandas-gbq -U && \
pip install sklearn && \
pip install matplotlib && \
pip install ipyparallel && \
pip install seaborn && \
pip install opencv-contrib-python && \
pip install Pillow && \
pip install wordcloud && \
pip install gensim && \
pip install google-cloud-storage && \
pip install nltk && \
pip install tensorflow
# Use Kernel
RUN python -m ipykernel install --user --name envPython37 --display-name "Python (envPython37)"


copy jupyter_notebook_config.py /root/.jupyter/

# Set working directory 
WORKDIR /home/4aibd-s1-project-ml

EXPOSE 8888

CMD jupyter-lab --notebook-dir=/home/4aibd-s1-project-ml --no-browser --port=8888 --ip=0.0.0.0 --allow-root