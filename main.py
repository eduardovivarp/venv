from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from flask import Flask, request, jsonify
import joblib

mi_app = FastAPI()

#@mi_app.get("/") #raiz
import ast
import pandas as pd    
# 1. Abrimos el archivo y lo cargamos en un dataframe
rows=[]
with open(r'steam_games.json') as f:
    for line in f.readlines():
        rows.append(ast.literal_eval(line))
df= pd.DataFrame(rows)

# 2.  detectamos los valores nulos en cada columna sobre 32135 regisros
#nulos_por_columna = df.isnull().sum()
#nulos_por_columna.info
    
# 3. Estandarizamos nombres publisher, generos y title   #  # 
# asignamos Unknown a publisher, son 8052 nulos
df['publisher'] = df['publisher'].fillna("Unknown")
# asignamos Unknown como una serie o lista a genres, son 3283 nulos
lista_unk = pd.Series(['Unknown'])  
df['genres'] = df['genres'].fillna("Unknown")
for i in range(32135):
    #print(df.loc[i, 'genres'])
    if str(df.loc[i, 'genres'])=='Unknown':
        df.loc[i, 'genres'] = ['Unknown']
# 29530 app_name y title son IGUALES
df[(df['app_name']!=df['title']) & (~df['title'].isnull())]
# agregamos 1 columna al dataframe para colocar asignarle el app_name en aquellos donde este nulo el title
df['title_fixed'] = df['title']
df['title_fixed'] = df['title_fixed'].fillna(df['app_name'])
#df['title_fixed']

@mi_app.get("/top_generos/{year_text}")

def top_generos(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]}
    # filtra el anio
    filtered_df = df[df['release_date'].str.contains(year_text, case=False, na=False)]
    # obtiene todos los generos
    all_genres = filtered_df['genres'].explode()
    # obtiene las ocurrencias por cada genero
    genre_counts = all_genres.value_counts()
    # obtiene los top x genero
    top_x_genres_year = genre_counts.head(5)
    return top_x_genres_year.to_dict()

@mi_app.get("/juegos/{year_text}")
def juegos(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]}
    filtered_df = df[df['release_date'].str.contains(year_text, case=False, na=False)]
    # Get all the juegos in the filtered DataFrame
    todos_juegos = filtered_df['title_fixed']
    # Count the occurrences of each titulo, en caso que hayan repetidos por nombre
    juegos_anio = todos_juegos.value_counts()
    return {year_text:juegos_anio.index.tolist()}

@mi_app.get("/specs/{year_text}")
def top_specs(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]}  
    filtered_df = df[df['release_date'].str.contains(year_text, case=False, na=False)]
    # Get all the specs in the filtered DataFrame
    all_specs = filtered_df['specs'].explode()
    # Count the occurrences of each spec
    specs_counts = all_specs.value_counts()
    # Get the top x genres
    top_x_specs = specs_counts.head(5)
    return {year_text:top_x_specs.index.tolist()}

@mi_app.get("/earlyaccess/{year_text}")
def earlyaccess(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]} 
    filtered_df = df[df['release_date'].str.contains(year_text, case=False, na=False)]
    # Get all the early_acccess in the filtered DataFrame
    solo_early = filtered_df[filtered_df['early_access']==True].shape[0]
    return {'Juegos con early access':solo_early} 

@mi_app.get("/sentiments/{year_text}")
def sentiments(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]} 
    # filtra el anio y retiramos los que contengan reviews, por que eso no califica como sentiment
    filtered_df = df[ ( df['release_date'].str.contains(year_text, case=False, na=False) ) & (~df['sentiment'].str.contains("reviews", case=False, na=False))]
    # obtiene todos los sentiment
    all_genres = filtered_df['sentiment'].explode()
    # obtiene las ocurrencias por cada sentiment
    genre_counts = all_genres.value_counts()
    return genre_counts.to_dict()

@mi_app.get("/metascores/{year_text}")
def top_metascores(year_text):
    if not year_text.isdigit():
     return {year_text + " no es válido":[]}
    filtered_df = df[df['release_date'].str.contains(year_text, case=False, na=False)]
    sorted_df = filtered_df.sort_values(by='metascore', ascending=False)
    # Tomar los primeros 5 registros con los mayores valores de 'metascore'
    top_5_records = sorted_df.head(5)
    # Convertir los datos en un diccionario
    result_dict = dict(zip(top_5_records['title'].to_list(),top_5_records['metascore'].to_list()))
    return result_dict

model = joblib.load('modelo_entrenado.pkl')

@mi_app.route('/predict')
def predict(year:str=None,metascore:float=None):
    data = request.json  # Datos enviados en la solicitud POST
    #genero = data['genre']
    year = data['year']
    metascore = data['metascore']
    #earlyaccess = data['earlyaccess']

    # Realizar la predicción
    input_data = [[year, metascore]]
    predicted_price,rmse = model.predict(input_data)[0]

    # Construir la respuesta
    response = {
        "predicted_price": predicted_price, "RMSE":rmse,
        "message": "Predicción exitosa"
    }

    return jsonify(response)