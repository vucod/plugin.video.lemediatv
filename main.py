## -*- coding: utf-8 -*-
import urlparse
import sys,urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver
import requests

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

_addon = xbmcaddon.Addon()
_icon = _addon.getAddonInfo('icon')
print(_icon)


def scrap_url_yt():
    """
    Scrap the website of lemediatv.fr to get the playlist of videos.
    """
    url = "https://cms.inscreen.tv/Api/program/list/95/undefined"
    r = requests.get(url)
    playlist = r.json()
    videoid = playlist[0]['videoid']
    title = playlist[0]['title']
    url = 'https://www.youtube.com/watch?v='+videoid
    return url,title

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url    

class MyPlayer(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def onPlayBackEnded(self):
        xbmc.executebuiltin("XBMC.PlayMedia(plugin://plugin.video.lemediatv/?mode=play)")

def play_video():
    """
    Scrap and play a video from the website
    """
    path,title = scrap_url_yt()
    stream_url = resolve_url(path)
    play_item = xbmcgui.ListItem(path=path)
    # Can't read accent in title
    play_item.setInfo('video', {'Title': str('Lemediatv.fr : '+title), 'Genre': 'Video', 'plot': 'Regardez Le Media en direct'})
    custplay = MyPlayer()
    custplay.play(stream_url, listitem=play_item)
    xbmc.sleep(500)  # Wait until playback starts
    while custplay.isPlaying():
            xbmc.sleep(500)

xbmc.log("[plugin.video.lemedia]: Started Running")

if sys.argv[2] == '':
    url = build_url({'mode' :'play'})
    li = xbmcgui.ListItem('Regardez Le Media en direct')
    li.setProperty('IsFolder' , 'False')
    li.setArt({'thumb': 'https://www.lemediatv.fr/sites/default/files/media-logo.png'})
    li.setContentLookup(False)
    li.addStreamInfo('audio', {'language': 'fr'})
    li.setInfo('video', {'Title': 'Lemediatv.fr', 'Genre': 'Video', 'plot': 'Regardez Le Media en direct'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

else:
    play_video()

xbmc.log("[plugin.video.lemedia] : Finished Running")
