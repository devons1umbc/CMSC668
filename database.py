from pymongo import MongoClient
import pandas as pd

# from time import sleep

user = "group668"
password = "v3VWOj434w7zXyWj"

cluster = MongoClient(
    "mongodb+srv://" + user + ":" + password + "@movies.93uecwx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["MoviesAndTV"]
collection = db["Dataset"]


# Adds a list of dictionaries to the database
def add_list_to_db(dictionary_array):
    # seconds = 1
    for site in dictionary_array:
        title = site['Title'][0]
        description = site['Description'][0]
        if collection.find_one({"Title": title}) is not None and collection.find_one({"Description": description}) is not None:
            print("ALREADY EXISTS")
            print(site)
        else:
            print("ADDED")
            print(site)
            collection.insert_one(site)
            # sleep(seconds)


# Deletes a title in the database. Title must be exact.
def delete_title(title):
    if collection.find_one({"Title": title}) is not None:
        collection.delete_one({"Title": title})
        print("DELETED")
        print(title)
        return 1
    else:
        print("FAILED TO DELETE")
        print(title)
        return 0


# Returns all movies and shows relating to a query by title. Returns more results, less accuracy
def get_all_type_title_loose(title):
    movie_set = []
    desc = title.split()
    for i in desc:
        for j in collection.find({"Title": {"$regex": i, "$options": "i"}}, {'_id': False}):
            if j not in movie_set:
                movie_set.append(j)
    return movie_set


# Returns all movies and shows relating to a query by description. Returns more results, less accuracy
def get_all_type_description_loose(desc):
    movie_set = []
    desc = desc.split()
    for i in desc:
        for j in collection.find({"Description": {"$regex": i, "$options": "i"}}, {'_id': False}):
            if j not in movie_set:
                movie_set.append(j)
    return movie_set


# Returns all movies and shows relating to a query by title. Returns fewer results, more accuracy
def get_all_type_title_strict(title):
    movie_set = []
    for i in collection.find({"Title": {"$regex": title, "$options": "i"}}, {'_id': False}):
        movie_set.append(i)
    return movie_set


# Returns all movies and shows relating to a query by description. Returns fewer results, more accuracy
def get_all_type_description_strict(desc):
    movie_set = []
    for i in collection.find({"Description": {"$regex": desc, "$options": "i"}}, {'_id': False}):
        movie_set.append(i)
    return movie_set


def get_all_enteries():
    array = []
    for i in collection.find({}, {'_id': False}):
        array.append(i)
    return array


def export_cv(name):
    df = pd.DataFrame(list(collection.find({}, {'_id': False})))
    df.to_csv(name, index=False)


def slim_list(name):
    titles = []
    returns = []
    for i in name:
        titles.append(i['Title'][0])
    print(titles)
    stuff = collection.find({}, {'_id': False})
    for i in stuff:
        if i['Title'][0] not in titles:
            returns.append(i)
            print(i)
    return returns


def delete_title(title):
    print(collection.delete_many({"Title": {"$regex": title, "$options": "i"}}))
