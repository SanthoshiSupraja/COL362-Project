CREATE TABLE  IF NOT EXISTS artists (
    artist_popularity bigint,
    followers bigint,
    genres text [],
    id text NOT NULL,
    name text,
    track_id text,
    track_name_prev text,
    CONSTRAINT ar_id PRIMARY KEY (id)
);

CREATE TABLE  IF NOT EXISTS albums (
    album_type text,
    artist_id text NOT NULL,
    external_url text,
    href text,
    id text NOT NULL,
    images text [],
    name text,
    release_date text,
    total_tracks bigint,
    track_id text,
    track_name_prev text,
    uri text,
    CONSTRAINT al_id PRIMARY KEY (id)
);
CREATE TABLE  IF NOT EXISTS tracks (
    acousticness decimal(12,8),
    album_id text NOT NULL,
    analysis_url text,
    artists_id text NOT NULL,
    country text,
    danceability decimal(12,8),
    disc_number bigint,
    duration_ms bigint,
    href text,
    id text NOT NULL,
    liveness decimal(12,8),
    loudness decimal(12,8),
    name text,
    CONSTRAINT tr_id PRIMARY KEY (id),
    CONSTRAINT artists_id FOREIGN KEY (artists_id) references artists(id),
    CONSTRAINT album_id FOREIGN KEY (album_id) references albums(id)
);
CREATE TABLE IF NOT EXISTS users(
   username text,
   emailid text,
   password text,
   CONSTRAINT eml_id PRIMARY KEY (emailid)
)
