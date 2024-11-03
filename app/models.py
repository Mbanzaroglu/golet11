from . import db
# Burada class olarak tanımlıyoruz çünkü kodun içerisindeki CRUD işlemleri için direkt class yapısını verimli bir şekilde kullanabiliriz.
# Tablolar üzerinde yapacağımız sütun ekle-çıkar ya da yeni tablo ekleme işlemlerini yine burada yapacağız

# bp_release tablosunu temsil eden sınıf
class Release(db.Model):
    __tablename__ = 'bp_release'
    release_id = db.Column(db.Integer, primary_key=True)
    release_title = db.Column(db.Text)
    release_date = db.Column(db.Date)
    release_url = db.Column(db.Text)
    label_id = db.Column(db.Integer, db.ForeignKey('label.label_id'))
    updated_on = db.Column(db.TIMESTAMP)

# bp_genre tablosunu temsil eden sınıf
class Genre(db.Model):
    __tablename__ = 'bp_genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.Text)
    song_count = db.Column(db.Integer)
    genre_url = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)

# bp_artist tablosunu temsil eden sınıf
class Artist(db.Model):
    __tablename__ = 'bp_artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.Text)
    artist_url = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)

# bp_track tablosunu temsil eden sınıf
class Track(db.Model):
    __tablename__ = 'bp_track'
    track_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    mix = db.Column(db.Text)
    is_remixed = db.Column(db.Boolean)
    release_date = db.Column(db.Date)
    genre_id = db.Column(db.Integer, db.ForeignKey('bp_genre.genre_id'))
    subgenre_id = db.Column(db.Integer, db.ForeignKey('subgenre.subgenre_id'))
    track_url = db.Column(db.Text)
    bpm = db.Column(db.Text)
    duration = db.Column(db.Integer)

# subgenre tablosunu temsil eden sınıf
class SubGenre(db.Model):
    __tablename__ = 'subgenre'
    subgenre_id = db.Column(db.Integer, primary_key=True)
    subgenre_name = db.Column(db.Text)
    song_count = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('bp_genre.genre_id'))
    subgenre_url = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)
    genre_url = db.Column(db.Text)

# label tablosunu temsil eden sınıf
class Label(db.Model):
    __tablename__ = 'label'
    label_id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.Text)
    label_url = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)

# release_media tablosunu temsil eden sınıf
class ReleaseMedia(db.Model):
    __tablename__ = 'release_media'
    release_id = db.Column(db.Integer, primary_key=True)
    release_img_id = db.Column(db.Integer)
    release_img_uuid = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)

# label_media tablosunu temsil eden sınıf
class LabelMedia(db.Model):
    __tablename__ = 'label_media'
    label_id = db.Column(db.Integer, primary_key=True)
    label_img_id = db.Column(db.Integer)
    label_img_uuid = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP)

# artist_release tablosunu temsil eden sınıf
class ArtistRelease(db.Model):
    __tablename__ = 'artist_release'
    artist_id = db.Column(db.Integer, db.ForeignKey('bp_artist.artist_id'), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('bp_release.release_id'), primary_key=True)
    updated_on = db.Column(db.TIMESTAMP)

# artist_track tablosunu temsil eden sınıf
class ArtistTrack(db.Model):
    __tablename__ = 'artist_track'
    artist_id = db.Column(db.Integer, db.ForeignKey('bp_artist.artist_id'), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('bp_track.track_id'), primary_key=True)
    updated_on = db.Column(db.TIMESTAMP)
    is_remixer = db.Column(db.Boolean)

# label_artist tablosunu temsil eden sınıf
class LabelArtist(db.Model):
    __tablename__ = 'label_artist'
    label_id = db.Column(db.Integer, db.ForeignKey('label.label_id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('bp_artist.artist_id'), primary_key=True)
    updated_on = db.Column(db.TIMESTAMP)
