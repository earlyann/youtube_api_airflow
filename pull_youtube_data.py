#
from googleapiclient.discovery import build
from datetime import date
import pandas as pd
import boto3
import io
import config
import time
from airflow.hooks.postgres_hook import PostgresHook
from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from sqlalchemy import create_engine

default_args = {
    'owner': 'Lacey',
    'depends_on_past': False,   
    'start_date': datetime(2023, 8, 1),
    'retries': 1,
    'provide_context': True
}

@dag(default_args=default_args, schedule_interval=timedelta(days=1), catchup=False, description='Calls for most popular videos in US, *pick 5 other countries where youtube is most popular and logs to db')
def youtube_database_builder():

    @task
    def pull_data(region_code):
        
        YOUTUBE_API_KEY = config.YOUTUBE_API_KEY
        api_service_name = "youtube"
        api_version = "v3"
        # create an API client
        youtube = build(
            api_service_name, api_version, developerKey=YOUTUBE_API_KEY)
        
        # make a request for the top videos
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=50
        )
        response = request.execute()

        # get current date
        today = date.today()

        # store response in a data frame
        df = pd.DataFrame(response['items'])
        df = pd.concat([df.drop('snippet', axis=1), pd.DataFrame(df['snippet'].tolist())], axis=1)
        df = pd.concat([df.drop('statistics', axis=1), pd.DataFrame(df['statistics'].tolist())], axis=1)

        # replace the category id with the name
        dict_category = {1 : 'Film & Animation', 2 : 'Autos & Vehicles', 10 : 'Music', 15 : 'Pets & Animals', 17 : 'Sports', 18 : 'Short Movies', 19 : 'Travel & Events',
                        20 : 'Gaming', 21 : 'Videoblogging', 22 : 'People & Blogs', 23 : 'Comedy', 24 : 'Entertainment', 25 : 'News & Politics', 26 : 'Howto & Style', 27 : 'Education',
                        28 : 'Science & Technology', 29 : 'Nonprofits & Activism', 30 : 'Movies', 31 : 'Anime/Animation', 32 : 'Action/Adventure', 33 : 'Classics', 34 : 'Comedy',
                        35 : 'Documentary', 36 : 'Drama', 37 : 'Family', 38 : 'Foreign', 39 : 'Horror', 40 : 'Sci-Fi/Fantasy', 41 : 'Thriller', 42 : 'Shorts', 43 : 'Shows', 44 : 'Trailers'}
        df['categoryId'] = df['categoryId'].astype(int)
        df['category'] = df['categoryId'].map(dict_category)
        df.insert(0, "date_of_extraction", today)
        df.insert(1, "country", region_code)

        # columns to keep
        columns = ['date_of_extraction', 'country','id', 'title', 'description', 'channelId', 'channelTitle', 'category', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount']
        df = df[columns]
        df = df.dropna()
        
        # identify data types for each column
        int_col = df.columns[-4:]
        for col in int_col:
            df[col] = df[col].astype(int)
        str_col = df.columns[:-4]
        for col in str_col:
            df[col] = df[col].astype(str)
        
        # keep desired columns
        df = df[['date_of_extraction',  'country','id', 'title',  'channelId','channelTitle', 'category', 'viewCount', 'likeCount', 'commentCount']]
        
        return df

    # Save the data to a postgres db/table that has already been created
    @task
    def save_to_postgresql(df: pd.DataFrame):
        
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5433/youtube_data_db"
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            df.to_sql('youtube_data', con=conn, if_exists='append', index=False)
                       
        return None
    
    countries = ["US", "IN", "BR", "RU", "JP", "DE"]  # countries where YouTube is popular

    save_tasks = []
    for country in countries:
        data_task = pull_data(country)  # Corrected this line
        save_task = save_to_postgresql(data_task)
        save_tasks.append(save_task)

        data_task >> save_task

    return save_tasks

youtube_database_builder_dag = youtube_database_builder()
