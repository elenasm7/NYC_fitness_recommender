# NYC_fitness_recommender

An NYC based application to provide you with the best recommendations for fitness class, studios, and gyms. From yoga to cycling, swimming to energy healing, its got you covered. I hope you enjoy the final product as much as I have! 

## Overview:

Fitness is something that is super important to me, so as someone new to NYC it seemed like the perfect opportunity to create a recommender system to find my perfect new class(es). In this project I work to add more details and features into the recommender system to give better results than the ones I've found thus far. 

To add more depth to the reviews, NLP was used for the reviews left and descriptions given by the classes themselves. This project makes use of the python recommender system library _**Surprise**_. In a separate jupyter [notebook]() you can find some information to help with your own project with the library.

All reviews were scraped from **Yelp**, and other information about the classes were scraped from **ClassPass**. This data was then used to make our preidction using different algorithms in Surprise such as: co-clustering and slopeone for collaborative fitering.

**add here about the creation/combination of collobrative and content based filtering.**

## Steps Taken:

|Part One:|
|-------------|
|1. Data aquisition using Selenium and Beautifulsoup to scrape from Yelp and ClassPass.|
|2. Exploratory Data Analysis and Data Cleaning|
|3. Create baseline collaborative filtering models with SlopeOne and Co-Clustering|


