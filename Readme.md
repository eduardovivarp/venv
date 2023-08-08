<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

# <h1 align=center>**`Eduardo Vivar Pomiano`**</h1>
# <h1 align=center>**`Agosto - 2023`**</h1>
<hr>  

## **Analisis de data sobre juegos en plataforma STEAM**

Steam es un software gratuito que instalado en una computadora permite usarla como una consola de juegos como una Xbox o PlayStation. A traves de STEAM se pueden comprar y disfrutar los juegos.


## Contexto

Nuestra fuente de datos es un archivo json con 32135 registros, disponemos del diccionario de datos. 

[Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj?usp=drive_link)
[Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link)

Es importante conocer el concepto de cada termino para darle el tratamiento adecuado durante las transformaciones y el EDA.

Columna	    : Descripción
publisher	: Empresa publicadora del contenido
genres	: Genero del contenido
app_name	: Nombre del contenido
title	: Titulo del contenido
url	: URL de publicación del contenido
release_date : Fecha de lanzamiento
tags	: etiquetas de contenido
discount_price  : precio de descuento
reviews_url	: Reviews de contenido
specs	: Especificaciones
price	: Precio del contenido
early_access	: acceso temprano
id	identificador:  : unico de contenido
developer	: Desarrollador
sentiment	: Análisis de sentimiento
metascore	: Score por metacritic


## Data Engineering 
## Transformaciones

Cargamos la informacion del archivo json en un dataframe para asi poder tener una visión detallada del contenido de cada columna.

Columna por columna explicamos las transformaciones realizadas, estos cambios figuran en el archivo TRANSF_Y_EDA.jpynb.

+ Valores Nulos: Haciendo uso de la funcion isnull e info, pudimos notar la cantidad de valores nulos en cada columna.Destacando entre ellos la columna publisher (8052 reg.), genre (3283 reg.), sentiment (7182 reg.) y metascore (29458 reg.).
+ Publisher: Elegimos colocarle el texto "Unknown" para los registros que tienen publisher en NaN o nulo.
+ Genre: Elegimos colocarle el texto "Unknown" para los registros que tienen genre en NaN o nulo, notar que aqui usamos una lista, pues la columna contiene listas. Luego estas columnas de genero se explotaron en en n generos dando lugar a columnas con valores 0/1 (hotencoding). 
+ App_name y title: Notamos que en la mayoria de registros(>29k) app_name y title tienen el mismo valor, sin embargo title tiene alrededor de 2k Nulos, por ello decidimos colocar en los casos de title nulo el valor de app_name, esta asignacion la colocamos en una nueva columna llamada title_fixed.
+ Price: Esta columna tenia datos de tipo string como Soon, Free, Free to play. Lo que se aplico el cero para todos esos casos.
+ Sentiment: Los valores nulos le asignamos el texto "None", nos parece necesario que exista un valor que represente a aquellos registros que aun no cumplen con las consideraciones para recibir un sentiment, para quienes consuman la data sera mas claro. Asimismo la columna sentiment la explotamos en n columnas de sentiment con valores 0/1(hotencoding).
+ Year: Extrajimos el dato año de la columna release_date, notando que las FECHAS eran String y con formatos diversos como "Apr 2014" o "Soon..". Sin embargo logramos obtener el numero del año usando la funcion contains.

## Desarrollo API:

Para el desarrollo de esta API estos fueron los pasos:

1. Creamos un entorno virtual, que nos va a servir para aislar las librerias y los programas y demas componentes de este proyecto.
2. Enlazamos el entorno virtual con un repositorio en github
3. Desarrollamos el programa de transformacion y EDA en jupiter notebooks
4. Desarrollamos las funciones de las API y EDA en jupiter notebooks
5. Una vez que los programas en jupiter notebooks estaban listos los colocamos en el programa Main.py del proyecto. Aqui destaca el uso de FASTAPI.
6. Utilizando uvicorn levantamos y probamos la Api de manera local
7. Utilizando render.com, enlazamos un servicio web a nuestro repositorio en github.

Se debe prestar especial atencion al archivo requirements.txt que si bien es cierto contiene las librerias a descargarse, se debe retirar la info de las versiones.
Igualmente se debe prestar atencion a que las librerias a instalarse aplicarse en el entorno virtual, es decir tener el entorno virtual activado.

Hecho ese trabajo de desarrollo tenemos disponible la Api con las 6 funciones.

Se aplicaron validaciones para el ingreso de año correcto

+ def **genero( *`Año`: str* )**:
    Se ingresa un año y devuelve una lista con los 5 géneros más vendidos en el orden correspondiente.

+ def **juegos( *`Año`: str* )**:
    Se ingresa un año y devuelve una lista con los juegos lanzados en el año.

+ def **specs( *`Año`: str* )**:
    Se ingresa un año y devuelve una lista con los 5 specs que más se repiten en el mismo en el orden correspondiente. 

+ def **earlyacces( *`Año`: str* )**:
    Cantidad de juegos lanzados en un año con early access.

+ def **sentiment( *`Año`: str* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros que se encuentren categorizados con un análisis de sentimiento. 

+ def **metascore( *`Año`: str* )**:
    Top 5 juegos según año con mayor metascore.



## Análisis exploratorio de datos:

Observaciones respecto al analisis exploratorio:
Si bien Steam se viene desde el 2003, segun la data hay un crecimiento de lanzamiento de juegos desde el 2014 hacia el 2017, tenemos data solamente hasta el 2018.
De entre todos los generos si bien el de "design illustration" tiene mas correlacion con el precio que los demas.
Asimismo podemos notar que la correlacion entre sentiment positive y precio tambien resalta sobre las otras como podria ser Mostly Positive y Overwhelming Positive.
No se aprecia una correlacion entre precio y metascore, pues la mayor cantidad de puntajes altos de metascore tiene precios menores a 40, incluso a 20. Por otro lado la cantidad de informacion que no supera los 3k registros en la columna metascore hace necesario que los datasets que tomemos tomen solo esa cantidad.  

## Modelo de predicción:

Estoy utilizando solamente año y metascore para el modelo, con un archivo que considera solamente los valores existentes de metascore(2K registros aprox), sin embargo la estructura de los programas de este proyecto permitirán en adelante agregarle más variables y continuar analizando con diversas variantes, entre las mas interesantes pueden ser generos, tags, sentiment.

El RMSE resultante es de 13.55, que esta expresado en la misma unidad de la variable objetivo precio. Como proximos pasos es necesario utilizar variables que mejoren(disminuyan) este indicador de precision del modelo.


+ def **prediccion( *`year, metascore`* )**:
    Ingresando estos parámetros, deberíamos recibir el precio y **RMSE**.
