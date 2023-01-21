from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
# Create your views here.

KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"
PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'
VIDEO_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
PL_PLAYLISTID = "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj"
WC_PLAYLISTID = "PLKHdj0BT9oN6PyrNURqyIt7zcvULLfglZ"

def datalistwc():

    PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": WC_PLAYLISTID , "maxResults": "64"}

    response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
    data = response.json()
    data_list = []
    nextPage = True
    while nextPage:
        for i in data["items"]:
            data_dict = {"thumbnail": i["snippet"]["thumbnails"]["maxres"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"]}
            data_list.append(data_dict)
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": WC_PLAYLISTID , "maxResults": "20", "pageToken": token}
                response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
                data = response.json()
            else:
                pass
        except KeyError:
            nextPage = False
    return data_list


def datalistpl():

    PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": PL_PLAYLISTID, "maxResults": "64"}
    response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
    data = response.json()
    data_list = []
    nextPage = True
    while nextPage:
        for i in data["items"]:
            if "| PREMIER LEAGUE HIGHLIGHTS |" in i["snippet"]["title"]:
                data_dict = {"thumbnail": i["snippet"]["thumbnails"]["maxres"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"]}
                data_list.append(data_dict)
            else:
                pass
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": PL_PLAYLISTID,
                                   "maxResults": "64", "pageToken": token}
                response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
                data = response.json()
            else:
                pass
        except KeyError:
            nextPage = False
    return data_list


def videolist():
    viddict = {worldcup: {'title': 'World Cup 2022 Qatar', 'link': 'worldcup/KokKw1esPL8', 'image': '/static/highlights/WC2022.jpg'},
               premierleague: {'title': 'Premier League 2022/23', 'link': 'premierleague/U0bndsJANvk', 'image': '/static/highlights/PL2223.png'}}
    return viddict


def index(request):
    if request.GET.get('search', None):
        search = request.GET.get('search').split()
        titles = videolist()
        vidlist = []
        for term in search:
            for title in titles:
                if term in titles[title]['title']:
                    vidlist.append({"title": titles[title]['title'], "link": titles[title]['link'], "image": titles[title]['image']})
                else:
                    pass
        if vidlist:
            return render(request, "highlights/search.html", {'vidlist': vidlist})
        else:
            return render(request, "highlights/search.html", {'vidlist': vidlist})
    else:
        return render(request, "highlights/index.html")


def worldcup(request, videolink):
    maintitle = "Qatar vs. Ecuador"
    maindesc = "Qatar and Ecuador kicked off the 2022 FIFA World Cup in style! Ecuador showed urgency and notched a penalty kick goal by Enner Valencia in the 16th minute. Valencia wasn’t done there, as he scored his second goal in the 31st minute. Both teams had chances in the second half but the score would stand at 2-0 in favor of Ecuador."
    date = "Nov 20, 2022"
    infolist = datalistwc()
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "publishdate": date, "page": "worldcup"})


def premierleague(request, videolink):
    maintitle = "Crystal Palace v. Arsenal"
    maindesc = "Gabriel Martinelli netted the first goal of the 2022-23 Premier League campaign to lift Arsenal to a season-opening victory against Crystal Palace."
    infolist = datalistpl()
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "page": "premierleague"})


def comingsoon(request):
    return render(request, "highlights/comingsoon.html")


def worldcuptest(request, videolink):


    YOUTUBE_PARAMS = {"key": KEY, "part": "snippet", "id": videolink}

    response = requests.get(VIDEO_ENDPOINT, params=YOUTUBE_PARAMS)
    data = response.json()
    data_dict = {}
    for i in data["items"]:
        test_desc = i["snippet"]["description"].split("#", 1)
        description = test_desc[0]
        test_title = i["snippet"]["title"].split("Highlights", 1)
        title = test_title[0]
        data_dict = {"title": title, "date": i["snippet"]["publishedAt"], "description": description}

    return HttpResponse(json.dumps(data_dict))


def premierleaguetest(request, videolink):

    YOUTUBE_PARAMS = {"key": KEY, "part": "snippet", "id": videolink}
    response = requests.get(VIDEO_ENDPOINT, params=YOUTUBE_PARAMS)
    data = response.json()
    data_dict = {}
    for i in data["items"]:
        if "| PREMIER LEAGUE HIGHLIGHTS |" in i["snippet"]["title"]:
            test_title = i["snippet"]["title"].split("|", 1)
            title = test_title[0]
            test_desc = i["snippet"]["description"].split("#", 1)
            description = test_desc[0]
            data_dict = {"title": title, "date": i["snippet"]["publishedAt"], "description": description}

    return HttpResponse(json.dumps(data_dict))

