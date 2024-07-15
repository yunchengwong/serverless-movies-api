## SERVERLESS-MOVIES-API

An API with serverless functions that display movie information.

#### 0. PREREQUISITES

- **Google Cloud Account:** You must have a Google Cloud account with active billing. [Create free account](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjv4rag0YiHAxWL4RYFHelWBqoYABABGgJ0bA&co=1&ase=2&gclid=CjwKCAjwyo60BhBiEiwAHmVLJcA7TabY8sV7owWMwhfaBI9U_3A1qSMIimrhMpXi4HVE5Gx-oI-LjhoCo0wQAvD_BwE&ei=yheEZpDINLeF4-EPwvaCiAE&ohost=www.google.com&cid=CAESVeD2brbPcj_YXbA6und6jqaPM94VVZu70iyOdtc6jG8nz_HwuVI3QFrinlciXwXvocM485XEMkE9HPx8hmXk4bhd5ZSuS2M580J4Dw9ApjvAN3ZOnYo&sig=AOD64_2zm-TBrPQGuwtu9BNoMLZM2qPAlg&q&sqi=2&nis=6&adurl&ved=2ahUKEwiQ1ayg0YiHAxW3wjgGHUK7ABEQqyQoAHoECBEQDA).
- **Google Cloud APIs**: You must enable the Cloud Functions, Cloud Build, Artifact Registry, Cloud Run, and Cloud Logging APIs. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=cloudfunctions.googleapis.com,%20%20%20%20%20cloudbuild.googleapis.com,artifactregistry.googleapis.com,%20%20%20%20%20run.googleapis.com,logging.googleapis.com&redirect=https://cloud.google.com/functions/docs/create-deploy-http-python&_ga=2.58149219.834821017.1720511681-1686645962.1716954818&_gac=1.154398410.1719932891.CjwKCAjwyo60BhBiEiwAHmVLJcA7TabY8sV7owWMwhfaBI9U_3A1qSMIimrhMpXi4HVE5Gx-oI-LjhoCo0wQAvD_BwE)

- **Bash:** You need a bash terminal to run the installation script.

#### 1. INSTALLATION

create your cloud infrastructure by running the installation script: `setup` in a bash terminal:

```
git clone https://github.com/yunchengwong/serverless-movies-api.git
cd serverless-movies-api
chmod 755 setup
./setup
```

#### 2. EXAMPLE DATA

you can use the sample data in `example_data.json` or create your own using the same format. to store the movie cover images in cloud storage and store the finalize movie data in firestore, run:

```
cd prepare-your-data
python3 main.py
```

> **note:** you can run the file `prepare-your-data/main.py` multiple times to load more data.

#### 3. DEPLOY THE FUNCTION 

to deploy the function with an HTTP trigger, run:

```
cd create-serverless-functions

gcloud functions deploy serverless-movies-api \
	--gen2 \
	--runtime=python312 \
	--source=. \
	--entry-point=my_function \
	--trigger-http \
	--allow-unauthenticated

gcloud functions describe serverless-movies-api \
    --gen2 \
    --format="value(serviceConfig.uri)"
```

#### 4. TRIGGER THE FUNCTION (HTTP) (EXAMPLE API ENDPOINTS)

- **getmovies:** `https://<REGION>-<PROJECT_ID>.cloudfunctions.net/serverless-movies-api/getmovies`
- **getmoviesbyyear:** `https://<REGION>-<PROJECT_ID>.cloudfunctions.net/serverless-movies-api/getmoviesbyyear/<INT:YEAR>`
- **getmoviesummary:** `https://<REGION>-<PROJECT_ID>.cloudfunctions.net/serverless-movies-api/getmoviesummary/<STRING:TITLE>`
