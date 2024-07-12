# SERVERLESS-MOVIES-API

## STEPS

#### Create Your Cloud Infrastructure

- gcloud cli
- google application default credential (ADC)
- python
- google cloud client libraries for python
    - cloud storage
    - firestore
    - cloud function

#### Prepare Your Data

1. search the movie on IMDb (https://www.imdb.com/)
2. right click on the poster to inspect its source on (https://www.imdb.com/title/*)
3. click on the `href` link in the `a` block to redirect to the movie album, previewing the poster, a level above the highlighted `div` block
4. right click again on the poster to view page source (inspect also works but cannot copy with CTRL+C), find the first http address with `.jpg`
5. (optional) confirm by visit the address copied

#### Create Serverless Functions

- GetMovies()
- GetMoviesByYear(year)
- GetMovieSummary(title)
