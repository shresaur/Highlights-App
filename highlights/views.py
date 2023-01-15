from django.shortcuts import render
import requests
# Create your views here.

def datalistwc():

    YOUTUBE_ENDPOINT = "https://www.googleapis.com/youtube/v3/playlists"

    KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"

    YOUTUBE_PARAMS = {"key": KEY, "part": "snippet", "channelId": "UCooTLkxcpnTNx6vfOovfBFA"}

    response = requests.get(YOUTUBE_ENDPOINT, params=YOUTUBE_PARAMS)
    data = response.json()
    playlistId = ""

    for i in data['items']:
        if i["snippet"]["title"] == "FIFA World Cup Game Highlights | FOX SOCCER":
            playlistId = (i["id"])
        else:
            pass


    PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'

    PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": playlistId, "maxResults": "64"}

    response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
    data = response.json()
    data_list = []
    nextPage = True
    while nextPage:
        for i in data["items"]:
            test_desc = i["snippet"]["description"].split("#", 1)
            description = test_desc[0]
            test_title = i["snippet"]["title"].split("Highlights", 1)
            title = test_title[0]
            data_dict = {"title": title, "date": i["snippet"]["publishedAt"],
                         "thumbnail": i["snippet"]["thumbnails"]["high"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"], "description": description}
            data_list.append(data_dict)
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": playlistId, "maxResults": "20", "pageToken": token}
                response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
                data = response.json()
            else:
                pass
        except KeyError:
            nextPage = False
    return data_list

def datalistpl():

    KEY = "AIzaSyBs2ThvW9nFTDV4nr90t6_v2eReVoZHgbU"

    PLAYLIST_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems'

    PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj",
                       "maxResults": "64"}

    response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
    data = response.json()
    data_list = []
    nextPage = True
    while nextPage:
        for i in data["items"]:
            if "| PREMIER LEAGUE HIGHLIGHTS |" in i["snippet"]["title"]:
                test_title = i["snippet"]["title"].split("|", 1)
                title = test_title[0]
                test_desc = i["snippet"]["description"].split("#", 1)
                description = test_desc[0]
                data_dict = {"title": title, "date": i["snippet"]["publishedAt"],
                             "thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                             "videoid": i["snippet"]["resourceId"]["videoId"], "description": description}
                data_list.append(data_dict)
            else:
                pass
        try:
            if data["nextPageToken"]:
                token = data["nextPageToken"]
                PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": "PLXEMPXZ3PY1hjUnuEJqxxYoRQLOEw6WFj",
                                   "maxResults": "64",
                                   "pageToken": token}
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
    global maintitle
    global maindesc
    infolist = datalistwc()
    for list in infolist:
        if videolink == list["videoid"]:
            maintitle = list["title"]
            maindesc = list["description"]
        else:
            pass
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "page": "worldcup"})

def premierleague(request, videolink):
    global maintitle
    global maindesc
    infolist = datalistpl()
    for list in infolist:
        if videolink == list["videoid"]:
            maintitle = list["title"]
            maindesc = list["description"]
        else:
            pass
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist, "maintitle": maintitle, "maindescription": maindesc, "page": "premierleague"})

def comingsoon(request):
    return render(request, "highlights/comingsoon.html")

