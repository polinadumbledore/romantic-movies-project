import sqlite3
import pandas as pd
from pymorphy2 import MorphAnalyzer
from nltk.tokenize import wordpunct_tokenize
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt


morph = MorphAnalyzer()


con = sqlite3.connect('imdb_small_indexed.db') 
cur = con.cursor()  

romance_films = """
SELECT title
from titles
	JOIN film_types ON titles.type = film_types.id
	JOIN film_genres ON titles.title_id = film_genres.title_id
	JOIN genre_types ON film_genres.genre_id = genre_types.id
WHERE genre_name = "Romance"
"""
# делаем табличку, где один столбец - романтические фильмы, чтобы сделать из названий word cloud

df = pd.read_sql_query(romance_films, con=con)

stops = set(stopwords.words('english'))

def lemmatize(x):
    if type(x) != str:
        return ""
    text = wordpunct_tokenize(x)
    result = []
    for word in text:
        if word.isalpha():
            nf = morph.parse(word)[0].normal_form
            if nf not in stops:
                result.append(nf)
    return " ".join(result)

 
wordcloud = WordCloud(
    background_color ='white',
    width = 800,
    height = 800, 
).generate(text)


plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud)
plt.axis("off") 
plt.title('Облако слов (включая стоп-слова)')
plt.show()
# сделали word cloud

year_ratings = """
SELECT premiered,
ROUND(AVG(rating), 2) as average_rating
FROM titles
    JOIN crew ON titles.title_id = crew.title_id
    JOIN people ON crew.person_id = people.person_id
    JOIN rating ON titles.title_id = rating.title_id
    JOIN film_genres ON titles.title_id = film_genres.title_id
    JOIN genre_types ON film_genres.genre_id = genre_types.id
WHERE genre_name = "Romance"
GROUP BY premiered
ORDER BY premiered DESC 
"""
# делаем табличку, где один столбец — год выпуска романтических фильмов, а другой — средний рейтинг фильмов в этом году, чтобы понять тенденцию

df2 = pd.read_sql_query(year_ratings, con=con)


X = df2['premiered']
Y = df2['average_rating']

plt.plot(X, Y) 
plt.title('Рейтинг романтических фильмов по популярности') 
plt.ylabel('Рейтинг') 
plt.xlabel('Год') 
plt.show()
# делаем график по данным year_ratings


male_actors = """
SELECT name, premiered, born, (premiered - born) as age, AVG(premiered - born) as aveg_age_male
FROM titles
    JOIN film_genres ON titles.title_id = film_genres.title_id
    JOIN genre_types ON film_genres.genre_id = genre_types.id
    JOIN crew ON titles.title_id = crew.title_id
    JOIN people ON crew.person_id = people.person_id
WHERE genre_name = "Romance" AND category = "1"
LIMIT 50
"""

female_actors = """
SELECT name, premiered, born, (premiered - born) as age, AVG(premiered - born) as aveg_age_female
FROM titles
    JOIN film_genres ON titles.title_id = film_genres.title_id
    JOIN genre_types ON film_genres.genre_id = genre_types.id
    JOIN crew ON titles.title_id = crew.title_id
    JOIN people ON crew.person_id = people.person_id
WHERE genre_name = "Romance" AND category = "2"
LIMIT 50
"""


