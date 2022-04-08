from billboard_song_scrapping import *
from spotify_web_api import *
from datetime import date

if __name__ == "__main__":
    song_list_ids = []  # track ID holder
    not_found_songs = list()    # Just to see what songs were not found

    date_scraped = "2022-04-08"
    playlist_name = f"Billboard 100 - {date_scraped}"
    playlist_description = f"The playlist was created by a python script on {str(date.today())}"
    year_searched = "2022"  # to specify the search for Spotify - now disabled
    sp = SpotifyWebAccess()
    sc = SongChartScrapper(date_scraped)
    playlist_id = sp.create_playlist(playlist_name, playlist_description)
    song_list = sc.get_song_titles()

    for song in song_list:
        track = sp.find_id_for_song_name(song, year=year_searched)
        if track is not None:
            song_list_ids.append(track)
        else:
            not_found_songs.append(song)

    sp.add_tracks_to_playlist(playist_id=playlist_id, tracks_list=song_list_ids)

