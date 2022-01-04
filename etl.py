import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
      Description: This function will read the JSON files in the path (data/song_data) to get the artist and song data, 
      load them into pandas, filter/update them if necessary and insert the relevent data into the songs and artists dim tables.

      Arguments:
          cur: the cursor object. 
          filepath: the file path to song data. 

      Returns:
          None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0]

    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]]\
        .rename(columns={"artist_name": "name",
                         "artist_location": "location",
                         "artist_latitude": "latitude",
                         "artist_longitude": "longitude"
                         }).values[0]
    
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
      Description: This function will read the JSON files in the path (data/log_data) to get the user and time data, 
      load them into pandas, filter/update them if necessary and insert the relevent data into the users and time dim tables.

      Arguments:
          cur: the cursor object. 
          filepath: the file path to log data. 

      Returns:
          None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    time_data = {'start_time': t,
                 'hour': t.dt.hour,
                 'day': t.dt.day,
                 'week': t.dt.week,
                 'month': t.dt.month,
                 'year': t.dt.year,
                 'weekday': t.dt.weekday}
    
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(data=time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # # load user table
    user_df = df[["userId", 
                  "firstName", 
                  "lastName", 
                  "gender", 
                  "level"]].rename(columns={
        "userId": "user_id", 
        "firstName": "first_name", 
        "lastName": "last_name"})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), 
                         row.userId, 
                         row.level, 
                         songid, 
                         artistid, 
                         row.sessionId,
                         row.location, 
                         row.userAgent)
        
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
      Description: This function will get ahold of all the files that are in the provided file path, 
      determine the number of files to be processed, calls the relevent data processing function to process data while keeping 
      the user updated with the number of files that had been processed.
      
      Arguments:
          cur: the cursor object.
          conn: the database connection object.
          filepath: the file path to the data that is to be processed. 
          func: the reference to the data processing function. 
          
      Returns:
          None

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
       Description: Establish a connection to the database with appropriate credentials, creates a cursor to be referenced
       and calls data processing functions. Closes the database connection after all is done.
       
       Arguments:
           None
           
       Returns:
           None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()