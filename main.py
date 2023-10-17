from movies import MovieAPI
import database


def printAll(input):
    for i in input:
        print(i)

if __name__ == "__main__":
    movie = MovieAPI()
    # database.export_cv("movielist.csv")
    # print(database.get_all_enteries())

    # print("Loose Title Search")
    # database.get_all_type_title_loose("hell")
    # print("\nStrict Title Search")
    # print(database.get_all_type_title_strict("batman"))
    # printAll(database.get_all_type_title_strict("Digimon"))

    # print("\nLoose Description Search")
    # database.get_all_type_description_loose("ash, goh and dawn")
    # print("\nStrict Description Search")
    # database.get_all_type_description_strict("ash, goh and dawn")

    # database.delete_title('yu-gi-oh')
    # print("\nSearch Movie/Show Into Database")
    query = str(input("Insert Query...: "))
    # print(movie.query_movie(query))
    database.add_list_to_db(movie.query_movie(query))
    # movie.query_movie(query)

    # print("\nDelete Movie/Show From Database")
    # database.delete_title("Broaden Your Horizons")

    # liked = database.get_all_type_title_loose("Pokemon")
    # dislike = database.get_all_type_title_loose("batman")
    # all = []
    # for i in liked:
    #     i["Likes"] = 1
    #     all.append(i)
    # for i in dislike:
    #     i["Likes"] = 0
    #     all.append(i)
    # print(all)

