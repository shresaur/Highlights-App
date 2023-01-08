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
    for i in data["items"]:
        test_desc = i["snippet"]["description"].split("#", 1)
        description = test_desc[0]
        title = i["snippet"]["title"]
        rep_title = {"Highlights": "", "|": "", "2022 FIFA World Cup": "", "Round of 16": "", "Highlight": "", "Quarterfinals": "", "Semifinals": "", "Third Place Game": "", "Final": ""}
        for key, value in rep_title.items():
            title = title.replace(key, value)
        data_dict = {"title": title, "date": i["snippet"]["publishedAt"],
                     "thumbnail": i["snippet"]["thumbnails"]["high"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"], "description": description}
        data_list.append(data_dict)
    if data["nextPageToken"]:
        token = data["nextPageToken"]
        PLAYLIST_PARAMS = {"key": KEY, "part": "snippet", "playlistId": playlistId, "maxResults": "20", "pageToken": token}
        response = requests.get(PLAYLIST_ENDPOINT, params=PLAYLIST_PARAMS)
        data = response.json()
        for i in data["items"]:
            test_desc = i["snippet"]["description"].split("#", 1)
            description = test_desc[0]
            title = i["snippet"]["title"]
            rep_title = {"Highlights": "", "|": "", "2022 FIFA World Cup": "", "Round of 16": "", "Highlight": "", "Third Place Game": "", "Final": "",
                         "Quarterfinals": "", "Semifinals": ""}
            for key, value in rep_title.items():
                title = title.replace(key, value)
            data_dict = {"title": title, "date": i["snippet"]["publishedAt"],
                         "thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
                         "videoid": i["snippet"]["resourceId"]["videoId"], "description": description}
            data_list.append(data_dict)
    else:
        pass

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


def index(request):
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

