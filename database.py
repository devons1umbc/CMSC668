from pymongo import MongoClient
# from time import sleep

user = "PLACEHOLDER"
password = "PLACEHOLDER"

cluster = MongoClient("mongodb+srv://" + user + ":" + password + "@movies.93uecwx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["MoviesAndTV"]
collection = db["Dataset"]


# Adds a list of dictionaries to the database
def add_list_to_db(dictionary_array):
    # seconds = 1
    for site in dictionary_array:
        title = site['Title'][0]
        if collection.find_one({"Title": title}) is not None:
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
        for j in collection.find({"Title": {"$regex": i, "$options": "i"}}):
            if j not in movie_set:
                movie_set.append(j)
    for i in movie_set:
        print(i)


# Returns all movies and shows relating to a query by description. Returns more results, less accuracy
def get_all_type_description_loose(desc):
    movie_set = []
    desc = desc.split()
    for i in desc:
        for j in collection.find({"Description": {"$regex": i, "$options": "i"}}):
            if j not in movie_set:
                movie_set.append(j)
    for i in movie_set:
        print(i)


# Returns all movies and shows relating to a query by title. Returns fewer results, more accuracy
def get_all_type_title_strict(title):
    for i in collection.find({"Title": {"$regex": title, "$options": "i"}}):
        print(i)


# Returns all movies and shows relating to a query by description. Returns fewer results, more accuracy
def get_all_type_description_strict(desc):
    for i in collection.find({"Description": {"$regex": desc, "$options": "i"}}):
        print(i)

