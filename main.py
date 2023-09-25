from movies import MovieAPI
import database

if __name__ == "__main__":
    movie = MovieAPI()

    print("Loose Title Search")
    database.get_all_type_title_loose("the first movie")
    print("\nStrict Title Search")
    database.get_all_type_title_strict("the first movie")

    print("\nLoose Description Search")
    database.get_all_type_description_loose("ash, goh and dawn")
    print("\nStrict Description Search")
    database.get_all_type_description_strict("ash, goh and dawn")

    # print("\nSearch Movie/Show Into Database")
    # query = str(input("Insert Query...: "))
    # database.add_list_to_db(movie.query_movie(query))

    # print("\nDelete Movie/Show From Database")
    # database.delete_title("Broaden Your Horizons")
