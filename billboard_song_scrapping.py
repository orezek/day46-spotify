import requests
from bs4 import BeautifulSoup as soup


class SongChartScrapper:
    """
    This class will get you first 100 songs from the billboard chart for any period you specify.
    You can get list of song titles, band names or a dictionary with the song position and song title and band name.
    """

    URL_LINK = "https://www.billboard.com/charts/hot-100"
    date = "2000-08-12"  # default value for easy use

    def __init__(self, date=date):
        """
        Date format YYYY-MM-DD
        :param date:
            specify date to be scrapped
        """
        response = requests.get(url=self.URL_LINK + "/" + date + "/")
        self.html_content = response.text
        self.song_titles = self.get_song_titles()
        self.band_titles = self.get_band_name()
        self.complete_chart = self.generate_chart_list()

    def get_song_titles(self) -> list:
        """
        Gets song title names list
        :return:
        List of song title
        """
        html_soup = soup(self.html_content, "html.parser")
        all_title_songs_raw = html_soup.findAll("h3", id="title-of-a-story", class_="a-no-trucate")
        song_titles = [s.text.strip(" ").strip("\n\t") for s in all_title_songs_raw]
        return song_titles

    def get_band_name(self) -> list:
        """
        Gets band names list
        :return:
        List of band names
        """
        html_soup = soup(self.html_content, "html.parser")
        all_bands_raw = html_soup.findAll("span", class_="a-no-trucate")
        band_titles = [b.text.strip(" ").strip("\n\t") for b in all_bands_raw]
        return band_titles

    def generate_chart_list(self) -> dict:
        """
        Gets song titles and band names in a dictionary along with the song position in the chart
        :return:
        Returns a dictionary
        """
        chart_dict = dict()
        try:
            for i in range(len(self.song_titles)):
                chart_dict.update({i + 1: {self.song_titles[i]: self.band_titles[i]}})
        except IndexError:
            raise IndexError
        return chart_dict




