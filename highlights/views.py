from django.shortcuts import render
from django.http import HttpResponse
from highlights.models import VideoList
from datetime import datetime
import requests
import json

# Create your views here.

KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"
PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'
VIDEO_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"



class YouTubePlaylist:
    def __init__(self, playlist_id, api_key):
        """
        Initializes the YouTubePlaylist class.

        Parameters:
        - playlist_id (str): The ID of the YouTube playlist.
        - api_key (str): Your API key for the YouTube Data API.
        """
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
        - title (str): The title of the YouTube video.
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
        """
        Parse the JSON response and extract relevant video data.

        Parameters:
        - data (dict): The JSON response containing video data.
        - title (str, optional): If specified, only videos with titles containing this string will be included.

        Returns:
        A list of dictionaries containing video data.
        """
        data_list = []
        for i in data.get("items", []):
            if not title or title in i["snippet"]["title"]:
                data_dict = {"thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                             "videoid": i["snippet"]["resourceId"]["videoId"],
                             "title": i["snippet"]["title"].split("|", 1)[0]}
                data_list.append(data_dict)
        return data_list


# Homepage
def index(request):
    """
    Renders the index.html template for the homepage.

    If a POST request is received, performs a search based on the submitted form data and returns the search results.

    Returns:
    - If the request method is POST, renders the search.html template with the search results.
    - If the request method is GET, renders the index.html template.
    """
    if request.method == "POST":
        search = request.POST.get('search', '').split(' ')
        # Query the database for titles that include the list of search terms
        matching_videos = VideoList.objects.filter(title__icontains=search[0])
        for term in search[1:]:
            matching_videos = matching_videos.filter(title__icontains=term)
        return render(request, "highlights/search.html", {'vidlist': matching_videos})
    else:
        return render(request, "highlights/index.html")


# Get premier league playlist data
PL_PLAYLIST_ID = "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj"
playlist = YouTubePlaylist(playlist_id=PL_PLAYLIST_ID, api_key=KEY)
# Only get videos from playlist that has the specific title
video_data_pl = playlist.get_video_data(title="| PREMIER LEAGUE HIGHLIGHTS |")

SPORTS_INFO = {
    "PL": {"video_data": video_data_pl, "params": {"key": KEY, "part": "snippet"}},
    # Add more sports here
}


def get_pl_video_info(latest_video):
    """
    Returns a tuple containing the title and description of the video.
    """
    title = latest_video["snippet"]["title"].split("|", 1)[0]
    description = latest_video["snippet"]["description"].split("#", 1)[0]
    return title, description


# Add more functions here for each sport
SPORT_FUNCTIONS = {
    "PL": get_pl_video_info,
    # Add more sports here
}


def sport_highlights(request, sport):
    """
    Renders the playepisode.html template with the highlights for the specified sport.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - sport (str): The sport for which to display highlights.

    Returns:
    - If the specified sport is valid, renders the playepisode.html template with the relevant data.
    - If the specified sport is invalid, returns an HTTP response with an error message.
    """
    if sport not in SPORTS_INFO:
        # Handle invalid sport error
        return HttpResponse("Invalid sport")

    sport_info = SPORTS_INFO[sport]
    video_data = sport_info["video_data"]
    video_link = video_data[0]["videoid"]  # Get the latest video from the playlist
    params = sport_info["params"]
    params["id"] = video_link

    response = requests.get(VIDEO_ENDPOINT, params=params)
    data = response.json()
    latest_video = data["items"][0]

    # Call the appropriate function based on the sport parameter
    title, description = SPORT_FUNCTIONS[sport](latest_video)

    publish_date = datetime.strptime(latest_video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")

    context = {
        "link": video_link,
        "data": video_data,
        "maintitle": title,
        "maindescription": description,
        "publishdate": publish_date,
        "page": sport.upper(),
    }

    return render(request, "highlights/playepisode.html", context)


def coming_soon(request):
    """
    Returns coming soon page for a sport/tournament that does not have highlights yet.
    """
    return render(request, "highlights/comingsoon.html")


# Get the details only for specific video clicked by user / request comes with the help of JS.
def watch(request, video_link):
    """
    Retrieves the details of specific video and returns the data as Json.
    """
    video_info = video_link.split('-', 2)
    prefix, video_id = video_info[0], video_info[1]
    params = {"key": KEY, "part": "snippet", "id": video_id}
    response = requests.get(VIDEO_ENDPOINT, params=params)
    data = response.json()
    video_detail = data["items"][0]
    title, description = "", ""
    if prefix == 'PL':
        title, description = get_pl_video_info(video_detail)
    else:
        pass  # Call another sport function to get the title and description

    publish_date = datetime.strptime(video_detail["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
    data_dict = {"title": title, "date": publish_date, "description": description}

    return HttpResponse(json.dumps(data_dict))
