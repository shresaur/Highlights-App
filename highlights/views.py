from django.shortcuts import render
import requests
# Create your views here.

def datalist():

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
        title = i["snippet"]["title"]
        data_dict = {"title": title.replace('Highlights | 2022 FIFA World Cup', ''), "date": i["snippet"]["publishedAt"],
                     "thumbnail": i["snippet"]["thumbnails"]["high"]["url"], "videoid": i["snippet"]["resourceId"]["videoId"]}
        data_list.append(data_dict)
    return data_list


def index(request):
    return render(request, "highlights/index.html")


def playepisode(request, videolink):
    infolist = datalist()
    return render(request, "highlights/playepisode.html", {"link": videolink, "data": infolist})

