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


def data_playlist(playlist_id, title=None):
    playlist_params = {"key": KEY, "part": "snippet", "playlistId": playlist_id, "maxResults": "64"}
    response = requests.get(PLAYLIST_ENDPOINT, params=playlist_params)
    data = response.json()
    data_list = []
    next_page = True
    while next_page:
        for i in data["items"]:
            if title:
                if title in i["snippet"]["title"]:
                    data_dict = {"thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                                 "videoid": i["snippet"]["resourceId"]["videoId"]}
                    data_list.append(data_dict)
                else:
                    pass
            else:
                data_dict = {"thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                             "videoid": i["snippet"]["resourceId"]["videoId"]}
                data_list.append(data_dict)
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                playlist_params = {"key": KEY, "part": "snippet", "playlistId": playlist_id, "maxResults": "64",
                                   "pageToken": token}
                response = requests.get(PLAYLIST_ENDPOINT, params=playlist_params)
                data = response.json()
            else:
                pass
        except KeyError:
            next_page = False
    return data_list


# To get Premier League data
data_list_pl = data_playlist(PL_PLAYLIST_ID, "| PREMIER LEAGUE HIGHLIGHTS |")


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
    infolist = data_list_pl
    return render(request, "highlights/playepisode.html",
                  {"link": videolink, "data": infolist, "maintitle": main_title, "maindescription": main_desc,
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
