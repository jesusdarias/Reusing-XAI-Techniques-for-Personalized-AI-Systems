## Using the API with Postman

This quick guide illustrates how to launch the Flask server and make requests to any of the explanation methods in the API using Postman. The code, requirements, Dockerfile, and example use cases are available in the project's repository.

### Launching the Server

##### Using Python

1) Clone the repository.

2) From the root folder, create a virtual environment for the installation of the required libraries with:

           
```console
python -m venv .
```
                
            
3) Use pip to install the dependencies from the requirements file.

```console
pip -r requirements.txt
```
            
4) Once all the dependencies have been installed, access the XAI API folder and execute the script with:

```console
python app.py
```
    

##### Using Docker

1) Clone the repository.
2) From the root folder, execute the following command to build a Docker Image using the Dockerfile:
    
```console
docker build -t <tag_name> .
```
The associated tag name you choose will be used to refer to the docker image that will be generated.

3) Run the container to launch the server. The -p option maps the port from the container to the real system, to allow making requests to the server.

```console
docker run -p 5000:5000 <tag_name>
```
    
### Making Requests

If the server was launched correctly, a similar message to the one in the image should appear, meaning that it is ready to receive requests to the specified address and port.

![ServerLaunched](https://user-images.githubusercontent.com/71895708/170830447-760dce21-69b3-4538-ab37-22f6d058ed1f.PNG)

1) To make requests, open Postman and go to *My Workspace > File > New Tab*.
2) item To get information about how to use a specific method, we can make a GET request. In the URL bar, specify the address and port of the server, followed by the name of the method, and send the request. The response is displayed in the bottom part of the console. For example, for Tabular/Importance:
    
![GetPostman](https://user-images.githubusercontent.com/71895708/170830521-5fa44c83-c121-4903-9621-d04feb94e121.PNG)
    
3) To execute the methods, we have to make a POST request. To do so, change the request type to POST and go to *Body > form-data*. Here is where we specify the required parameters, such as the *model* and *data* files, and the *params* object. In this example, I am using the cancer use case model and data. The only parameters included in the *params* object were the *backend* (sklearn) and the *model\_task* (classification).

![PostPostman](https://user-images.githubusercontent.com/71895708/170830600-62e2fdea-dc15-4dee-b0eb-9e2c24942b3b.PNG)


### Visualizing Explanations

The responses to the HTTP requests are given in JSON format. However, most of the methods return responses that also contain the URLs to plots or graphs of the explanations in HTML or PNG format. Before accessing the explanations, it is necessary to change the default JSON mime-type.

1) To visualize these explanations, click on the URL in the response. It will open a new request tab with the specified URL.
2) Go to *Headers* and disable the *Accept* attribute.
3) Add a new header with the same name, *Accept*, as key and specify the value according to the type of file you are trying to access. For .png files, specify *image/png*. For .html files, specify *text/html*. Finally, send the request.
    
![ViewerPostman](https://user-images.githubusercontent.com/71895708/170830655-23bb69f2-321d-4851-acb9-d8012b51ae2c.PNG)
    
## Using the CBR system functions

The instructions are similar to using just the API, but to test the Retriever and Retainer functionalities of the CBR system, it is necessary to install MongoDB and import the case base and explainers description.

1) Follow steps 1 through 3 of launching the server for the API using python.
2) Install MongoDB. Please, refer to https://www.mongodb.com/docs/manual/installation/. **Note:** by default, MongoDB uses port 27017. Please, do not change this port. Once you have installed it, make sure the service is running. Otherwise, launch it with the *mongod* command.
3) From a command line instance (not Mongo), access the CBR system folder and execute the following commands to import the database collections:
```console
mongoimport --collection=caseBase --db=xai caseBase.json
mongoimport --collection=explainers --db=xai explainers.json
```
4) Launch the server with:

```console
python app.py
``` 
5) To use the Retriever function, the approach is similar to making POST requests to the explainer methods. However, the only parameter that is passed in the body of the requests is *params*, which is representative of a target case. Here is an example using Postman:

![Retriever](https://user-images.githubusercontent.com/71895708/170833985-e65b1336-b8e6-4bfc-8a5b-6a83436c1c25.PNG)
