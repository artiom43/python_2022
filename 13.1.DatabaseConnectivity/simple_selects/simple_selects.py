import typing as tp
import sqlite3


class DataBaseHandler:
    def __init__(self, sqlite_database_name: str):
        """
        Initialize all the context for working with database here
        :param sqlite_database_name: path to the sqlite3 database file
        """
        self.connection = sqlite3.connect("chinook.db")
        pass

    def get_most_expensive_track_names(self, number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names sorted by UnitPrice descending.
        If the price is the same, sort by TrackId ascending.
        :param number_of_tracks: how many track names should be returned
        keywords: SELECT, ORDER BY, LIMIT
        :return:
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT Name FROM tracks  ORDER BY -UnitPrice  LIMIT :name", {'name': number_of_tracks})
        answer = cursor.fetchall()
        # print(answer)
        cursor.close()
        return answer
        pass

    def get_tracks_of_given_genres(self, set_genres: tp.Sequence[str],
                                   number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names that have one of the given genres
        sort asending by track duration and limit by number_of_tracks
        :param number_of_tracks:
        :param genres:
        keywords: JOIN, WHERE, IN
        :return:
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute('create table tablegenres (Name varchar(20) NOT NULL)')
        except sqlite3.OperationalError:
            pass
        # print([(genre,) for genre in set_genres], set_genres)
        cursor.executemany('INSERT INTO tablegenres (Name) VALUES (?)', [(genre,) for genre in set_genres])
        # .commit()
        cursor.execute("SELECT tracks.Name FROM tracks JOIN genres ON tracks.GenreId=genres.GenreId WHERE \
             genres.Name IN (SELECT Name FROM tablegenres) \
                        ORDER BY Milliseconds  LIMIT :name", {'name': number_of_tracks})
        answer = cursor.fetchall()
        # print(answer)[(genre) for genre in set_genres]
        cursor.execute('DROP TABLE tablegenres')
        # self.connection.commit()
        self.connection.rollback()
        cursor.close()
        return answer
        # return answer
        pass

    def get_tracks_that_belong_to_playlist_found_by_name(self, name_needle: str) -> tp.Sequence[tuple[str, str]]:
        """
        Return a sequence of track names and playlist names such that the track belongs to the playlist and
        the playlist's name contains `name_needle` (case sensitive).
        If the track belongs to more than one suitable playlist it
        should occur in the result for each playlist, but not just once
        :param name_needle:
        keywords: JOIN, WHERE, LIKE
        :return:
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT tracks.Name, playlists.Name FROM tracks, playlists JOIN playlist_track"
                       " ON tracks.TrackId=playlist_track.TrackId AND playlist_track.PlaylistId=playlists.PlaylistId"
                       " WHERE playlists.Name LIKE :name", {'name': f'%{name_needle}%'})
        answer = cursor.fetchall()
        # print(answer)
        cursor.close()
        return answer
        pass

    def teardown(self) -> None:
        """
        Cleanup everything after working with database.
        Do anything that may be needed or leave blank
        :return:
        """
        # self.connection.rollback()
        self.connection.close()
        pass
