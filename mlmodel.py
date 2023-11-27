import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import database


def liked_movies(title):
    movies = database.get_all_type_title_loose(title)
    for i in movies:
        i['Likes'] = 1
    return movies


def disliked_movies(title):
    movies = database.get_all_type_title_loose(title)
    for i in movies:
        i['Likes'] = 0
    return movies


def find_best(liked, disliked):
    # print(movies)
    # Sample movie data in dictionary format
    movie_data = liked + disliked
    for i in movie_data:
        if 'Description' not in i:
            i['Description'] = []
        if 'Genre' not in i:
            i['Genre'] = []
        if 'Director' not in i:
            i['Director'] = []
        if 'Rating' not in i:
            i['Rating'] = []
        if 'Original Language' not in i:
            i['Original Language'] = []
        if 'Cast' not in i:
            i['Cast'] = []
    # Create a DataFrame from the sample data
    df = pd.DataFrame(movie_data)

    # Create one-hot encodings for genres and age_rating
    mlb = MultiLabelBinarizer()
    genre_encoded = mlb.fit_transform(df['Genre'])
    age_rating_encoded = mlb.fit_transform(df['Rating'])
    lang_encoded = mlb.fit_transform(df['Original Language'])
    cast_encoded = mlb.fit_transform(df['Cast'])

    # Vectorize movie descriptions using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    description_encoded = tfidf_vectorizer.fit_transform(df['Description'].apply(lambda x: ' '.join(x)))

    # Combine all features
    features = (description_encoded.toarray(), genre_encoded, age_rating_encoded, lang_encoded, cast_encoded)
    X = np.hstack(features)
    y = df['Likes']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)

    # Create a Linear Regression model
    lr_model = LinearRegression()

    # Fit the model on the training data
    lr_model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = lr_model.predict(X_test)

    # Evaluate the model using Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    # print(f"Mean Squared Error: {mse:.2f}")

    # Now you can use the trained Linear Regression model to predict whether a user would like a new movie.

    # Define a new movie as a dictionary with the same features
    new_movies = database.get_all_enteries()
    new_movies = database.slim_list(movie_data)

    highest_value = 0
    highest_movie = ""
    # Fill missing values for genres and directors, and "Not Rated" for age_rating
    for new_movie in new_movies:
        if 'Description' not in new_movie:
            new_movie['Description'] = []
        if 'Genre' not in new_movie:
            new_movie['Genre'] = []
        if 'Director' not in new_movie:
            new_movie['Director'] = []
        if 'Rating' not in new_movie:
            new_movie['Rating'] = []
        if 'Original Language' not in new_movie:
            new_movie['Original Language'] = []
        if 'Cast' not in new_movie:
            new_movie['Cast'] = []

        # Vectorize the description of the new movie
        new_movie_description_encoded = tfidf_vectorizer.transform(new_movie['Description'])
        # Convert genres and age rating to one-hot encodings
        new_movie_genre_encoded = mlb.transform([new_movie['Genre']])
        new_movie_age_rating_encoded = mlb.transform([new_movie['Rating']])
        new_movie_lang_encoded = mlb.transform([new_movie['Original Language']])
        new_movie_cast_encoded = mlb.transform([new_movie['Cast']])
        # print(new_movie_director_encoded)

        # Combine features for the new movie
        features = (new_movie_description_encoded.toarray(), new_movie_genre_encoded, new_movie_age_rating_encoded,
                    new_movie_lang_encoded, new_movie_cast_encoded)
        new_movie_features = np.hstack(features)

        # Ensure that the number of features matches the trained model by adding zero columns for missing features
        expected_num_features = X_train.shape[1]  # Get the number of features from the training data
        # print("EXPECTED:", expected_num_features)
        # print("FEATURES:", new_movie_features.shape[1])
        if new_movie_features.shape[1] < expected_num_features:
            missing_features = np.zeros((new_movie_features.shape[0], expected_num_features - new_movie_features.shape[1]))
            new_movie_features = np.hstack((new_movie_features, missing_features))
        elif new_movie_features.shape[1] > expected_num_features:
            # In case the new movie's feature vector has more features than expected (unlikely), you may need to trim it.
            new_movie_features = new_movie_features[:, :expected_num_features]

        # Predict whether the user would like or dislike the new movie using the Linear Regression model
        prediction = lr_model.predict(new_movie_features)

        if prediction[0] > highest_value:
            highest_value = prediction[0]
            highest_movie = new_movie

    print(highest_movie)
    return highest_movie
