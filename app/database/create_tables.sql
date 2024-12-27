CREATE TABLE bp_release (
    release_id INTEGER,
    release_title text,
    release_date DATE,
    release_url text
);

CREATE TABLE bp_genre (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT,
    song_count INTEGER,
    genre_url TEXT
);

CREATE TABLE bp_artist (
    artist_id INTEGER PRIMARY KEY,
    artist_name TEXT,
    artist_url TEXT
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
    release_id INTEGER
    
);

CREATE TABLE artist_track (
    artist_id INTEGER,
    track_id INTEGER
);


CREATE TABLE artist_release (
    artist_id INTEGER,
    release_id INTEGER
);


-- Adding primary keys (already defined in CREATE TABLE statements)
ALTER TABLE bp_release ADD CONSTRAINT pk_bp_release PRIMARY KEY (release_id);
ALTER TABLE bp_genre ADD CONSTRAINT pk_bp_genre PRIMARY KEY (genre_id);
ALTER TABLE bp_artist ADD CONSTRAINT pk_bp_artist PRIMARY KEY (artist_id);
ALTER TABLE bp_track ADD CONSTRAINT pk_bp_track PRIMARY KEY (track_id);
ALTER TABLE artist_track ADD CONSTRAINT pk_artist_track PRIMARY KEY (artist_id, track_id);
ALTER TABLE artist_release ADD CONSTRAINT pk_artist_release PRIMARY KEY (artist_id, release_id);

use golet11;
-- Adding foreign keys to bp_track
ALTER TABLE bp_track
ADD CONSTRAINT fk_bp_track_genre_id FOREIGN KEY (genre_id) REFERENCES bp_genre(genre_id),
ADD CONSTRAINT fk_bp_track_release_id FOREIGN KEY (release_id) REFERENCES bp_release(release_id);

-- Adding foreign keys to artist_track
ALTER TABLE artist_track
ADD CONSTRAINT fk_artist_track_artist_id FOREIGN KEY (artist_id) REFERENCES bp_artist(artist_id),
ADD CONSTRAINT fk_artist_track_track_id FOREIGN KEY (track_id) REFERENCES bp_track(track_id);

-- Adding foreign keys to artist_release
ALTER TABLE artist_release
ADD CONSTRAINT fk_artist_release_artist_id FOREIGN KEY (artist_id) REFERENCES bp_artist(artist_id),
ADD CONSTRAINT fk_artist_release_release_id FOREIGN KEY (release_id) REFERENCES bp_release(release_id);