# NYC_fitness_recommender

An NYC based application to provide you with the best recommendations for fitness class, studios, and gyms. From yoga to cycling, swimming to energy healing, its got you covered. I hope you enjoy the final product as much as I have! 

## Overview:

Fitness is something that is super important to me, so as someone new to NYC it seemed like the perfect opportunity to create a recommender system to find my perfect new class(es). In this project I work to add more details and features into the recommender system to give better results than the ones I've found thus far. 

To add more depth to the reviews, NLP was used for the reviews left and descriptions given by the classes themselves. This project makes use of the python recommender system library _**Surprise**_. In a separate jupyter [notebook]() you can find some information to help with your own project with the library.

All reviews were scraped from **Yelp**, and other information about the classes were gathered using the API. This data was then used to make our preidction using different algorithms in Surprise such as: SVD, SDV++ and BaselineOnly for collaborative fitering.

The first part of this project, is all collaboratibve filtering although there were some models creating using **content based filtering**. The first (current) _final model_ of this project is a content based filtering model using Baseline only with the best hyper-parameters, and filtering for class category (i.e. Cycling, Cardio, Yoga, etc.).

The second part, I cleaned the text data and created a content based filtering model. The Surprise library lacks support for this type of recommender system, so for this I went through the NLP process and then used tf-idf and cosine similarity. This would return gyms/studios that were the most similar based on reviews. 

In the third section, I decided on my current model which takes the best BaselineOnly model from part one, and then filters the results based on the category it falls into (i.e. cycling, pilotes, yoga, etc.). I then created a simple Django webapp that would use some of the form inputs pass it into the serialized model, and query the results with the rest of the user inputs. 

In the next sections, I will outline the steps taken, report findings and share images of the final product--the django web app.

## Steps Taken:

|Part One|
|-------------|
|1. Yelp and ClassPass Data aquisition (Selenium and Beautifulsoup)|
|2. Exploratory Data Analysis (EDA) and Data Cleaning|
|3. Create baseline collaborative-filtering models using _Surprise_|

|Part Two|
|--------|
|1. EDA and Cleaning for Text Data                                                     |
|2. feature engineering, lemming, tokenizing, vectorization, etc.                      |
|3. Create a content based filtering model                                             |

|Part Three|
|----------|
|1. Serialize the model |
|2. Create Django WebApp|
|2. Embed model in WebApp|


