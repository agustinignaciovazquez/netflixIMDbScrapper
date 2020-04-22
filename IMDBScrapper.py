import imdb
import csv

from imdb import Movie

ia = imdb.IMDb()


def select_movie(suggested_movies, original_name):
    if len(suggested_movies) == 0:
        print("Not found " + original_name)
        return {'movie': None, 'keyword': original_name}
    if len(suggested_movies) == 1:
        return {'movie': suggested_movies[0], 'keyword': original_name}
    return {'movie': suggested_movies[0], 'keyword': original_name} #Olvidate no voy a hacer lo mismo para 1000 valores
    while True:
        print(">>")
        print(">>")
        print("SELECIONE UN VALOR")
        for i, suggested_movie in enumerate(suggested_movies):
            print("#" + str(i) + " " + suggested_movie.get('title') + "("+ str(suggested_movie.get('year')) +")")
        print(original_name)
        selected = int(input("Seleccionar un valor: "))
        if 0 <= selected < len(suggested_movies):
            return {'movie': suggested_movies[selected], 'keyword': original_name}


def search_movies(movies_keywords):
    results = []
    movies = []
    movies_keywords_no_duplicates = list(dict.fromkeys(movies_keywords))

    for index, movie_keyword in enumerate(movies_keywords_no_duplicates):
        print("(#" + str(index) + ") Searching keyword movies: " + movie_keyword)
        movie_results = ia.search_movie(movie_keyword)
        results.append({'keyword': movies_keywords_no_duplicates[index], 'movies_results': movie_results})

    for result in results:
        selected = select_movie(result['movies_results'], result['keyword'])
        movies.append(selected)

    for i, r in enumerate(movies):
        movie = r['movie']
        if(isinstance(movie, Movie.Movie)):
            print("Updating info from "+ movie['title'])
            ia.update(movie)

    return movies

def getCast(cast):
    r = []
    for person in cast:
        r.append(person.get('name'))
    return r

with open('NetflixViewingHistory.csv', encoding="utf8", newline='') as File:
    reader = csv.reader(File)
    movies_keywords = []
    for i, row in enumerate(reader):
        if i > 0:
            movies_keywords.append(row[1])
movies = search_movies(movies_keywords)

with open('moviesIMDB.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['keyword','title', 'year', 'director', 'cast', 'genres',
           'countries', 'rating',
           'languages', 'plot outline', 'kind', 'seasons',
           'cover url'])
    for r in movies:
        movie = r['movie']
        if (isinstance(movie, Movie.Movie)):
            print(movie.infoset2keys)
            cast = getCast(movie.get('cast'))
            row = [r['keyword'],movie.get('title'), movie.get('year'), movie.get('director'), cast, movie.get('genres'), movie.get('countries'), movie.get('rating'),
                   movie.get('languages'), movie.get('plot outline'), movie.get('kind'), movie.get('seasons'), movie.get('cover url')]
            print(row)
            writer.writerow(row)
        else:
            writer.writerow([r['keyword'], 'NOT FOUND', '', '', '',
                             '', '',
                             '', '', '', '',
                             '',''])


