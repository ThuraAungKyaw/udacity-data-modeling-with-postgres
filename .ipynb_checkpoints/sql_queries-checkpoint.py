# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
                            songplay_id SERIAL PRIMARY KEY NOT NULL,
                            level varchar(4) NOT NULL, 
                            song_id varchar REFERENCES songs(song_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            artist_id varchar REFERENCES artists(artist_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            session_id int NOT NULL, 
                            location varchar, 
                            user_agent varchar NOT NULL,
                            start_time timestamp REFERENCES time(start_time) ON DELETE CASCADE ON UPDATE CASCADE,
                            user_id varchar REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE);
                        """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                        user_id varchar PRIMARY KEY NOT NULL, 
                        first_name varchar NOT NULL, 
                        last_name varchar NOT NULL, 
                        gender varchar(1) NOT NULL, 
                        level varchar(4) NOT NULL);
                    """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                        song_id varchar PRIMARY KEY NOT NULL, 
                        title varchar NOT NULL, 
                        artist_id varchar NOT NULL,
                        year smallint NOT NULL, 
                        duration numeric NOT NULL);
                    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                          artist_id varchar PRIMARY KEY NOT NULL, 
                          name varchar NOT NULL, 
                          location varchar, 
                          latitude numeric, 
                          longitude numeric);
                      """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                        start_time timestamp PRIMARY KEY NOT NULL, 
                        hour smallint NOT NULL, 
                        day smallint NOT NULL, 
                        week smallint NOT NULL, 
                        month smallint NOT NULL, 
                        year smallint NOT NULL, 
                        weekday smallint NOT NULL);
                    """)

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (
                            start_time, 
                            user_id, 
                            level, 
                            song_id, 
                            artist_id, 
                            session_id, 
                            location, 
                            user_agent) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                        """)

user_table_insert = ("""INSERT INTO users (
                        user_id, 
                        first_name, 
                        last_name, 
                        gender, 
                        level) 
                        VALUES(%s, %s, %s, %s, %s) 
                        ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;
                    """)

song_table_insert = ("""INSERT INTO songs (
                        song_id, 
                        title, 
                        artist_id, 
                        year, 
                        duration) 
                        VALUES(%s, %s, %s, %s, %s) 
                        ON CONFLICT (song_id) DO NOTHING;
                    """)

artist_table_insert = ("""INSERT INTO artists (
                          artist_id, 
                          name, 
                          location, 
                          latitude, 
                          longitude) 
                          VALUES(%s, %s, %s, %s, %s) 
                          ON CONFLICT (artist_id) DO NOTHING;
                       """)


time_table_insert = ("""INSERT INTO time (
                        start_time, 
                        hour, 
                        day, 
                        week, 
                        month, 
                        year, 
                        weekday) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (start_time) DO NOTHING;
                    """)

# FIND SONGS

song_select = ("""SELECT songs.song_id as songid, artists.artist_id AS artistid FROM songs 
                  JOIN artists ON songs.artist_id = artists.artist_id 
                  WHERE songs.title = (%s) AND artists.name = (%s) AND songs.duration=(%s)
                """)

# QUERY LISTS
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]