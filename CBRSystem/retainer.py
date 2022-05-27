from flask_restful import Resource,reqparse
from pymongo import MongoClient
import json
import numpy as np
import pandas 
from bson.json_util import dumps

class Retainer(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("params")
        args = parser.parse_args()
        
        newcase = json.loads(args.get("params"))
       
        #database connection
        client = MongoClient('localhost', 27017)  
        db = client.xai                 
        collection = db.caseBase

        _id=collection.insert_one(newcase)
  
        return json.loads(dumps(collection.find_one({"_id":_id.inserted_id})))


    def get(self):
        return {
        "_method_description": "This method stores a complete user case in the cases database." 
                               " The description"
                               " of this case is depicted in the argument 'params' which is a string representing a json object with the following fields:",
        "params": { 

            "Description": "A JSON dictionary with the following fields: ",
                            "Domain":"A string containing the domain of the AI model. For example, economics, medicine, security, etc.",
                            "DataType": "A string containing the type of data that the model works with. Supported values are: 'Tabular', 'Images','Text'.",
                            "TrainingData": "A string with 'Yes' or 'No' depending if you can provide the training data. Currently, the number of explainers that don't "
                                            "require training data is very limited",
                            "ModelBackend": "A string containing the backend of the prediction model. The supported values are: 'Sklearn', 'TensorFlow1.0' "
                            "'TensorFlow2.0', 'Torch', and 'Other'.",
                            "AITask":  "A string containing 'Classification' or 'Regression' depending on the model's task.",
                            "ModelType": "A string representing the architecture of your model. Supported values are 'ANN'(Artificial Neural Network),'SVM'(Support Vector Machine),'RF'(Random Forest), "
                            "and 'Other'.",
                            "ExplanationScope": "A string with 'Local' or 'Global' depending on the desired explanation. Local explanations refer to specific instances or predictions, "
                            "while global explanations intend to explain the overall behavior of a model.",
                            "DomainKnowledgeLevel": "A string wih 'Low' or 'High' depending on the level of domain knowledge of the user receiving the explanation.",
                            "Black&White": "(Optional) Only used if DataType is Image to indicate whether the image to be explained is black and white ('Yes' or 'No').",
            "Solution": "The URL of the explainer used.",
            "UserScore": "The score the user gives to the explanation. Must be a number between 1 and 10."
                },

        "params_example":{ 
                            "Description": 
                                        {
                                            "Domain": "Medicine", 
                                            "DataType": "Tabular",
                                            "TrainingData": "Yes", 
                                            "AITask": "Classification",
                                            "ModelBackend": "Sklearn", 
                                            "ModelType": "ANN",
                                            "DomainKnowledgeLevel": "Expert",
                                            "ExplanationScope": "Local"
                                        }, 
                            "Solution": "Tabular/Anchors",
                            "UserScore": 7}
         }
    