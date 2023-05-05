from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests
import json

# Create your views here.

KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"
PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'
VIDEO_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
PL_PLAYLIST_ID = "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj"


class YouTubePlaylist:
    def __init__(self, playlist_id, api_key):
        self.playlist_id = playlist_id
        self.api_key = api_key
        self.playlist_endpoint = 'https://www.googleapis.com/youtube/v3/playlistItems'

    def get_video_data(self, title=None):
        """
        Retrieve video data for a YouTube playlist.

        Parameters:
        title (str, optional): If specified, only videos with titles containing this string will be included.

        Returns:
        A list of dictionaries, where each dictionary contains information about a single video in the playlist.
        Each dictionary contains the following keys:
        - thumbnail (str): The URL of the video's thumbnail image.
        - videoid (str): The ID of the YouTube video.
        """
        playlist_params = {"key": self.api_key, "part": "snippet", "playlistId": self.playlist_id, "maxResults": "64"}
        response = requests.get(self.playlist_endpoint, params=playlist_params)
        data = response.json()
        video_data = self._parse_data(data, title)
        while "nextPageToken" in data:
            token = data["nextPageToken"]
            playlist_params["pageToken"] = token
            response = requests.get(self.playlist_endpoint, params=playlist_params)
            data = response.json()
            video_data += self._parse_data(data, title)
        return video_data

    def _parse_data(self, data, title=None):
        data_list = []
        for i in data.get("items", []):
            if not title or title in i["snippet"]["title"]:
                data_dict = {"thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                             "videoid": i["snippet"]["resourceId"]["videoId"]}
                data_list.append(data_dict)
        return data_list

# Get premier league playlist data
playlist = YouTubePlaylist(playlist_id=PL_PLAYLIST_ID, api_key=KEY)
video_data_pl = playlist.get_video_data(title="| PREMIER LEAGUE HIGHLIGHTS |")



def video_list():
    vid_dict = {premier_league: {'title': 'Premier League 2022/23', 'link': 'premierleague/U0bndsJANvk',
                               'image': '/static/highlights/PL2223.png'}}
    return vid_dict


# Homepage
def index(request):
    if request.GET.get('search', None):
        search = request.GET.get('search').split()
        titles = video_list()
        vid_list = []
        for term in search:
            for title in titles:
                if term in titles[title]['title']:
                    vid_list.append({"title": titles[title]['title'], "link": titles[title]['link'],
                                    "image": titles[title]['image']})
                else:
                    pass
        if vid_list:
            return render(request, "highlights/search.html", {'vidlist': vid_list})
        else:
            return render(request, "highlights/search.html", {'vidlist': vid_list})
    else:
        return render(request, "highlights/index.html")


# Landing page for specific sport/tournament.
def premier_league(request, videolink):
    main_title = "Crystal Palace v. Arsenal"
    main_desc = "Gabriel Martinelli netted the first goal of the 2022-23 Premier League campaign to lift Arsenal" \
                " to a season-opening victory against Crystal Palace."
    date = "Aug 5, 2022"
    info_list = video_data_pl
    return render(request, "highlights/playepisode.html",
                  {"link": videolink, "data": info_list, "maintitle": main_title, "maindescription": main_desc,
                   "publishdate": date, "page": "PL"})


# Returns coming soon page for a sport/tournament that does not have highlights yet.
def coming_soon(request):
    return render(request, "highlights/comingsoon.html")


# Get the details only for specific video clicked by user / request comes with the help of JS.
def watch(request, videolink):
    video_link_temp = videolink.split('-', 2)
    prefix = video_link_temp[0]
    video_link_test = video_link_temp[1]
    YOUTUBE_PARAMS = {"key": KEY, "part": "snippet", "id": video_link_test}

    response = requests.get(VIDEO_ENDPOINT, params=YOUTUBE_PARAMS)
    data = response.json()
    data_dict = {}
    for i in data["items"]:
        if prefix == 'PL':
            test_title = i["snippet"]["title"].split("|", 1)
            title = test_title[0]
        else:
            test_title = i["snippet"]["title"].split("Highlights", 1)
            title = test_title[0]
        test_desc = i["snippet"]["description"].split("#", 1)
        description = test_desc[0]
        date_string = i["snippet"]["publishedAt"]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        publish_date = date_object.strftime("%B %d, %Y")
        data_dict = {"title": title, "date": publish_date, "description": description}

    return HttpResponse(json.dumps(data_dict))
