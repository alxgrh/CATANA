import os

DB_NAME = os.environ.get( 'CATANA_DB_NAME' , 'catana')
DB_USER = os.environ.get( 'CATANA_DB_USER' , 'catana')
DB_PASSWORD = os.environ.get( 'CATANA_DB_PASSWORD' , 'somesecret')
DB_HOST = os.environ.get( 'CATANA_DB_HOST' , '127.0.0.1')
DB_PORT = os.environ.get( 'CATANA_DB_PORT' , '33306')

DB_ENGINE = os.environ.get( 'CATANA_DB_ENGINE' , 'mysql')

YOUTUBE_API_KEY =  os.environ.get('YOUTUBE_API_KEY', 'AIzaSyDda_-kZe4i0U_gUwoFkHmlG8UAIUv2c1o')
YOUTUBE_CHANNEL_LIST =  os.environ.get('YOUTUBE_CHANNEL_LIST', 'test_channels.json')