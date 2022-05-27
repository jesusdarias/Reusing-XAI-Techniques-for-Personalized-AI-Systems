from flask_restful import Resource,reqparse
import tensorflow as tf
import torch
import numpy as np
import pandas as pd
import joblib
import werkzeug
import h5py
import json
from alibi.explainers import AnchorText

class AnchorsText(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("model", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("model", type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('params')
        args = parser.parse_args()
        
      
        params_json = json.loads(args.get("params"))
        instance=params_json["instance"]
        backend = params_json["backend"]

        model = args.get("model")
        
        if backend=="TF1" or backend=="TF2":
            model=h5py.File(model, 'w')
            mlp = tf.keras.models.load_model(model)
            predic_func=mlp.predict
        elif backend=="sklearn":
            mlp = joblib.load(model)
            if hasattr(mlp,'predict_proba'):
                predic_func=mlp.predict_proba
            else:
                predic_func=mlp.predict
        elif backend=="PYT":
            mlp = torch.load(model)
            predic_func=mlp.predict
        else:
            mlp = joblib.load(model)
            predic_func=mlp.predict

        kwargsData = dict(threshold=0.95)
        if "threshold" in params_json:
            kwargsData["threshold"] = params_json["threshold"]

        # Create explainer
        explainer = AnchorText(predic_func)
        explanation = explainer.explain(instance, **{k: v for k, v in kwargsData.items()})
        
        return explanation.to_json()


    def get(self):
        return {
        "_method_description": "This method provides local explanations in the form of simple boolean rules with a precision score and a "
                            "coverage value which represents the scope in which that rules applies to similar instances. Requires 3 arguments: " 
                           "the 'params' string, the 'model' which is a file containing the trained model, and " 
                           "the 'data', containing the training data used for the model. These arguments are described below.",

        "params": { 
                "instance": "Array representing a row with the feature values of an instance not including the target class.",
                "backend": "A string containing the backend of the prediction model. The supported values are: 'sklearn' (Scikit-learn), 'TF1' "
                "(TensorFlow 1.0), 'TF2' (TensorFlow 2.0), 'PYT' (PyTorch).",
                "threshold": "(Optional) The minimum level of precision required for the anchors. Default is 0.95"
                },

        "params_example":{
                  "instance": [
                    1966,
                    62,
                    8,
                    2,
                    0,
                    0,
                    0,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                  ],
                  "backend": "sklearn",
                  "feature_names": [
                    "construction_year",
                    "surface",
                    "floor",
                    "no_rooms",
                    "district_Bemowo",
                    "district_Bielany",
                    "district_Mokotow",
                    "district_Ochota",
                    "district_Praga",
                    "district_Srodmiescie",
                    "district_Ursus",
                    "district_Ursynow",
                    "district_Wola",
                    "district_Zoliborz"
                  ],
                  "categorical_names": {
                    "4": [ "0", "1" ],
                    "5": [ "0", "1" ],
                    "6": [ "0", "1" ],
                    "7": [ "0", "1" ],
                    "8": [ "0", "1" ],
                    "9": [ "0", "1" ],
                    "10": [ "0", "1" ],
                    "11": [ "0", "1" ],
                    "12": [ "0", "1" ],
                    "13": [ "0", "1" ]
                  },
                  "ohe": False,
                  "threshold": 0.8

        },

        "model": "The trained prediction model given as a file. The extension must match the backend being used i.e.  a .pkl " 
             "file for Scikit-learn (use Joblib library), .pt for PyTorch or .h5 for TensorFlow models. For models with different backends, also upload "
             "a .pkl, and make sure that the prediction function of the model is called 'predict'. This can be achieved by using a wrapper class.",
        }
    
