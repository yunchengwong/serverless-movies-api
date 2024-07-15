from flask import Flask, jsonify, request, redirect, url_for
import functions_framework
from google.cloud import firestore, aiplatform
from google.cloud.firestore_v1.base_query import FieldFilter
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig


movies = []
moviesbyyear = []

app = Flask("internal")

@app.route('/getmovies', methods=['GET', 'POST'])
def getmovies():
    db = firestore.Client()

    docs = db.collection("movies").stream()
    
    for doc in docs:
        movies.append(doc.to_dict())

    return jsonify(movies)

@app.route('/getmoviesbyyear/<int:id>', methods=['GET', 'POST'])
def getmoviesbyyear(id):
    db = firestore.Client()

    docs = (
        db.collection("movies")
        .where(filter=FieldFilter("releaseYear", "==", str(id)))
        .stream()
    )
    
    for doc in docs:
        moviesbyyear.append(doc.to_dict())
            
    return jsonify(moviesbyyear)

@app.route('/getmoviesummary/<string:id>', methods=['GET', 'POST'])
def getmoviesummary(id):
    db = firestore.Client()

    doc = (
        db.collection("movies")
        .document(id.replace("-", ""))
        .get()
    )
    
    if doc.exists:
        movie = doc.to_dict()
        prompt = f"Create a one-sentence summary of the movie '{movie['title']}' released in '{movie['releaseYear']}'."
        model = GenerativeModel("gemini-1.5-flash-001")
        generation_config = GenerationConfig(max_output_tokens=100)
        response = model.generate_content(prompt, generation_config=generation_config)
        movie['generatedSummary'] = response.text
        
        return jsonify(movie)
    else:
        return f'movie "{id}" not found'


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
