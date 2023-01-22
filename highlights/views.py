from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests
import json
# Create your views here.

KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"
PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'
VIDEO_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
PL_PLAYLISTID = "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj"
WC_PLAYLISTID = "PLKHdj0BT9oN6PyrNURqyIt7zcvULLfglZ"

def datalist(playlistId, title=None):
    PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": playlistId, "maxResults": "64"}
    response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
    data = response.json()
    data_list = []
    nextPage = True
    while nextPage:
        for i in data["items"]:
            if title:
                if title in i["snippet"]["title"]:
                    data_dict = {"thumbnail": i["snippet"]["thumbnails"]["maxres"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"]}
                    data_list.append(data_dict)
                else:
                    pass
            else:
                data_dict = {"thumbnail": i["snippet"]["thumbnails"]["maxres"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"]}
                data_list.append(data_dict)
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": playlistId, "maxResults": "64", "pageToken": token}
                response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
                data = response.json()
            else:
                pass
        except KeyError:
            nextPage = False
    return data_list

# To get World Cup data
data_listwc = datalist(WC_PLAYLISTID)

# To get Premier League data
data_listpl = datalist(PL_PLAYLISTID, "| PREMIER LEAGUE HIGHLIGHTS |")


def videolist():
    viddict = {worldcup: {'title': 'World Cup 2022 Qatar', 'link': 'worldcup/KokKw1esPL8', 'image': '/static/highlights/WC2022.jpg'},
               premierleague: {'title': 'Premier League 2022/23', 'link': 'premierleague/U0bndsJANvk', 'image': '/static/highlights/PL2223.png'}}
    return viddict


# Homepage
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


# Landing page for specific sport/tournament
def worldcup(request, videolink):
    maintitle = "Qatar vs. Ecuador"
    maindesc = "Qatar and Ecuador kicked off the 2022 FIFA World Cup in style! Ecuador showed urgency and notched a penalty kick goal by Enner Valencia in the 16th minute. Valencia wasn’t done there, as he scored his second goal in the 31st minute. Both teams had chances in the second half but the score would stand at 2-0 in favor of Ecuador."
    date = "Nov 20, 2022"
    infolist = data_listwc
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "publishdate": date, "page": "WC"})


def premierleague(request, videolink):
    maintitle = "Crystal Palace v. Arsenal"
    maindesc = "Gabriel Martinelli netted the first goal of the 2022-23 Premier League campaign to lift Arsenal to a season-opening victory against Crystal Palace."
    date = "Aug 5, 2022"
    infolist = data_listpl
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "publishdate": date, "page": "PL"})


# Returns coming soon page for a sport/tournament that does not have highlights yet
def comingsoon(request):
    return render(request, "highlights/comingsoon.html")


# Get the details only for specific video clicked by user / request comes with the help of JS
def watch(request, videolink):
    videolink_temp = videolink.split('-', 2)
    prefix = videolink_temp[0]
    videolinktest = videolink_temp[1]
    YOUTUBE_PARAMS = {"key": KEY, "part": "snippet", "id": videolinktest}

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
        publishdate = date_object.strftime("%B %d, %Y")
        data_dict = {"title": title, "date": publishdate, "description": description}

    return HttpResponse(json.dumps(data_dict))


