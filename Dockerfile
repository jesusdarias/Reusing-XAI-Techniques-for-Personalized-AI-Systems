FROM ubuntu
RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install joblib
RUN pip3 install dice_ml
RUN pip3 install json5
RUN pip3 install jsonpickle
RUN pip3 install jsonschema
RUN pip3 install Werkzeug
RUN pip3 install h5py
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install lime
RUN pip3 install shap
RUN pip3 install alibi
RUN pip3 install dalex
RUN pip3 install tensorflow
RUN pip3 install torch
RUN pip3 install html2image
RUN pip3 install pillow
RUN pip3 install matplotlib
RUN pip3 install kaleido
RUN pip3 install pymongo
COPY . .
CMD ["python3","XAI API/app.py"]