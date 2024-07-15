#### step 1: create your cloud infrastructure

setup: https://cloud.google.com/functions/docs/create-deploy-http-python#before_you_begin

- select a google cloud project with billing
- enable apis
    - [cloud storage]
    - [firestore]
    - [cloud functions](https://console.cloud.google.com/flows/enableapi?apiid=cloudfunctions,cloudbuild.googleapis.com,artifactregistry.googleapis.com,run.googleapis.com,logging.googleapis.com&redirect=https://cloud.google.com/functions/docs/create-deploy-gcloud&_ga=2.162545781.834821017.1720511681-1686645962.1716954818&_gac=1.62079326.1719932891.CjwKCAjwyo60BhBiEiwAHmVLJcA7TabY8sV7owWMwhfaBI9U_3A1qSMIimrhMpXi4HVE5Gx-oI-LjhoCo0wQAvD_BwE)
- install and initialize gcloud cli
- prepare your development environment: https://cloud.google.com/python/docs/setup
    - install python
    - (optional) use venv to isolate dependencies
    - install cloud client libraries for python
        - search libraries: https://cloud.google.com/python/docs/reference
        - example code:
            - cloud storage
            - firestore
            - cloud functions
    - set up authentication: https://cloud.google.com/docs/authentication/client-libraries
        - application default credential (ADC): https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to

#### step 2: prepare your data

cloud storage: 

- quickstart: https://cloud.google.com/storage/docs/reference/libraries#client-libraries-usage-python

firestore:

- quickstart: https://cloud.google.com/firestore/docs/create-database-server-client-library#python_1
- query: https://cloud.google.com/firestore/docs/query-data/get-data#python_1

## STEP 3: CREATE SERVERLESS FUNCTIONS

#### Create your function

https://medium.com/google-cloud/use-multiple-paths-in-cloud-functions-python-and-flask-fc6780e560d3

> **cloud function limitation:**
> Only one path is suitable. No subpath configuration, no path routing definition.

> **solution:**
> Manual Flask invocation - The principle is to reuse only the routing part, without the listen and serve; this part is performed by the Cloud Functions runtime.

```
from flask import Flask, request
#Define an internal Flask app
app = Flask("internal")
#Define the internal path, idiomatic Flask definition
@app.route('/user/<string:id>', methods=['GET', 'POST'])
def users(id):
    print(id)
    return id, 200
#Comply with Cloud Functions code structure for entry point
def my_function(request):
    #Create a new app context for the internal app
    internal_ctx = app.test_request_context(path=request.full_path,
                                            method=request.method)
    
    #Copy main request data from original request
    #According to your context, parts can be missing. Adapt here!
    internal_ctx.request.data = request.data
    internal_ctx.request.headers = request.headers
    
    #Activate the context
    internal_ctx.push()
    #Dispatch the request to the internal app and get the result 
    return_value = app.full_dispatch_request()
    #Offload the context
    internal_ctx.pop()
    
    #Return the result of the internal app routing and processing      
    return return_value

curl https://<region>-<projectID>.cloudfunctions.net/<functionName>/user/123
```

#### Specify dependencies

https://cloud.google.com/functions/docs/writing/specifying-dependencies-python

```
functions-framework==3.*
```

ERROR: (gcloud.functions.deploy) OperationError: code=3, message=Could not create or update Cloud Run service serverless-movies-api, Container Healthcheck failed. Revision 'serverless-movies-api-00001-cej' is not ready and cannot serve traffic. The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable. Logs for this revision might contain more information.

"ImportError: cannot import name 'firestore' from 'google.cloud' (unknown location)"

#### Build and test your function locally

#### Deploy your function

```

```
