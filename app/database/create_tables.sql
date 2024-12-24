
CREATE TABLE bp_release (
    release_id INTEGER PRIMARY KEY,
    release_title TEXT,
    release_date DATE,
    release_url TEXT,
    updated_on INTEGER
);

CREATE TABLE bp_genre (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT,
    song_count INTEGER,
    genre_url TEXT,
    updated_on TIMESTAMP(0)
);

CREATE TABLE bp_artist (
    artist_id INTEGER PRIMARY KEY,
    artist_name TEXT,
    artist_url TEXT,
    updated_on TEXT
);

CREATE TABLE bp_track (
    track_id INTEGER PRIMARY KEY,
    title TEXT,
    mix TEXT,
    release_date DATE,
    genre_id INTEGER,
    track_url TEXT,
    bpm TEXT,
    duration TIME,
    release_id INTEGER,
    FOREIGN KEY (genre_id) REFERENCES bp_genre(genre_id)
    FOREIGN KEY (release_id) REFERENCES bp_release(release_id)
);

CREATE TABLE artist_track (
    artist_id INTEGER,
    track_id INTEGER,
    updated_on TIMESTAMP(0),
    FOREIGN KEY (artist_id) REFERENCES bp_artist(artist_id),
    FOREIGN KEY (track_id) REFERENCES bp_track(track_id)
);

CREATE TABLE artist_release (
    artist_id INTEGER,
    release_id INTEGER,
    updated_on TIMESTAMP(0),
    FOREIGN KEY (artist_id) REFERENCES bp_artist(artist_id),
    FOREIGN KEY (release_id) REFERENCES bp_release(release_id)
);

CREATE TABLE release_media (
    release_id INTEGER,
    release_img_id INTEGER,
    release_img_uuid TEXT,
    updated_on TIMESTAMP(0),
    FOREIGN KEY (release_id) REFERENCES bp_release(release_id)
);