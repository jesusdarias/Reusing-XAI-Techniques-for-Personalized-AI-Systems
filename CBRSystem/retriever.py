from flask_restful import Resource,reqparse
from pymongo import MongoClient
import json
import numpy as np
import pandas 

def similarity_fn(usercase, case):
    return (0.2*int(usercase["Domain"]==case["Domain"])
           +0.2*int(usercase["DomainKnowledgeLevel"]==case["DomainKnowledgeLevel"])
           +0.2*int(usercase["MLKnowledge"]==case["MLKnowledge"])
           +0.2*int(usercase["AITask"]==case["AITask"])
           +0.1*int(usercase["ModelBackend"]==case["ModelBackend"])
           +0.1*int(usercase["ModelType"]==case["ModelType"]))

class Retriever(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("params")
        args = parser.parse_args()
        
        usercase = json.loads(args.get("params"))
       
        #database connection
        client = MongoClient('localhost', 27017)  
        db = client.xai                 
        collection = db.explainers

        query={}
        query.update(usercase)
        query.pop("Domain") 
        query.pop("DomainKnowledgeLevel") 
        query.pop("MLKnowledge")
        if query["ModelBackend"] != "Other":
            query.update(ModelBackend={"$in":["Any",query["ModelBackend"]]})
        else:
            query.update(ModelBackend="Any")
        if query["ModelType"] != "Other":
            query.update(ModelType={"$in":["Any",query["ModelType"]]})
        else:
            query.update(ModelType="Any")
        if query["TrainingData"] == "Yes":  
            query.pop("TrainingData")
        if query["DataType"] == "Image" and query["Black&White"]=="No":  
            query.pop("Black&White")
        
        explainers=[]
        for explainer in collection.find(query,{"_id":0,"ExplainerName":1}):
            explainers.append(explainer["ExplainerName"])

        #Switch to cases collection
        collection = db.caseBase

        solutions=[]
        for explainer in explainers:
            existent_cases=collection.find({"Solution":explainer})
            sim_and_scores=[]
    
            for case in existent_cases:
                sim=similarity_fn(usercase,case["Description"])
                sim_and_scores.append((sim,case["UserScore"]))
        
            sim_and_scores=np.array(sim_and_scores,dtype=[('similarity', np.float64), ('score', np.float64)])
            df = pandas.DataFrame(sim_and_scores)
            result = df.groupby('similarity').mean()
            sorted_sim_scores=result.to_records()
            if sorted_sim_scores.size != 0:
                affinity, predScore = sorted_sim_scores[-1]
            else: 
                affinity, predScore = (0.0,0.0)
    
            solutions.append({"ExplainerName":explainer, "ExpectedScore":predScore,"Similarity":affinity})
        solutions= sorted(solutions,key = lambda x: (-x["ExpectedScore"],-x["Similarity"],x["ExplainerName"]))    
            
        return solutions


    def get(self):
        return {
        "_method_description": "This method retrieves a set of explainers that are compatible with the description of a given model, along with a" 
                               "predicted user satisfaction score and the level of similarity of the user's case with previous cases in the database. The description"
                               "of the user case is depicted in the argument 'params' which is a string representing a json object with the following fields:",
        "params": { 
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
                "Black&White": "(Optional) Only used if DataType is Image to indicate whether the image to be explained is black and white ('Yes' or 'No')."
                },

        "params_example":{
                              "Domain": "Medicine",
                              "DataType": "Tabular",
                              "TrainingData": "Yes",
                              "AITask": "Classification",
                              "ModelBackend": "Sklearn",
                              "ModelType": "ANN",
                              "DomainKnowledgeLevel": "Expert",
                              "ExplanationScope": "Local"
                           }
         }
    