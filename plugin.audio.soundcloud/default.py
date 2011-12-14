# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2010
@author: Zsolt Török, Vanhoutteghem Pieter

Copyright (C) 2010 Zsolt Török
 
This file is part of XBMC SoundCloud Plugin.

XBMC SoundCloud Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XBMC SoundCloud Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XBMC SoundCloud Plugin.  If not, see <http://www.gnu.org/licenses/>.

'''
import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import xbmcsc.client as client
import urllib

from xbmcsc.client import SoundCloudClient

plugin="SoundCloud"
REMOTE_DBG = False
dbg = True # Set to false if you don't want debugging
dbglevel = 3 # Do NOT change from 3

import CommonFunctions
common = CommonFunctions.CommonFunctions()
common.plugin = plugin

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
        
# plugin related constants
PLUGIN_URL = u'plugin://music/SoundCloud/'
PLUGIN_ID = u'plugin.audio.soundcloud'

# XBMC plugin modes
MODE_GROUPS = 0
MODE_GROUPS_MENU = 1
MODE_GROUPS_FAVORITES = 2
MODE_GROUPS_SEARCH = 3
MODE_GROUPS_HOTTEST = 4
MODE_GROUPS_TRACKS = 5
MODE_GROUPS_FAVORITES = 6

MODE_TRACKS = 10
MODE_TRACKS_MENU = 11
MODE_TRACKS_FAVORITES = 12
MODE_TRACKS_SEARCH = 13
MODE_TRACKS_HOTTEST = 14
MODE_TRACK_PLAY = 15
MODE_TRACKS_DASH = 16
MODE_TRACKS_PRIVATE = 17

MODE_USERS = 20
MODE_USERS_MENU = 21
MODE_USERS_FAVORITES = 22
MODE_USERS_SEARCH = 23
MODE_USERS_HOTTEST = 24
MODE_USERS_TRACKS = 25
MODE_USERS_FOLLOWINGS = 26
MODE_USERS_FOLLOWERS = 27

# Parameter keys
PARAMETER_KEY_OFFSET = u'offset'
PARAMETER_KEY_LIMIT = u'limit'
PARAMETER_KEY_MODE = u'mode'
PARAMETER_KEY_URL = u'url'
PARAMETER_KEY_PERMALINK = u'permalink'
PARAMETER_KEY_TOKEN = u'oauth_token'

# Plugin settings
SETTING_USERNAME = u'username'
SETTING_PASSWORD = u'password'
SETTING_LOGIN = u'login_to_soundcloud'


loginerror = False
params = common.getParameters(sys.argv[2])
url = urllib.unquote_plus(params.get(PARAMETER_KEY_URL, ""))
name = urllib.unquote_plus(params.get("name", ""))
mode = int(params.get(PARAMETER_KEY_MODE, "0"))
nexturl = params.get("nexturl","")
query = urllib.unquote_plus(params.get("q", ""))
oauth_token = urllib.unquote_plus(params.get(PARAMETER_KEY_TOKEN,""))

handle = int(sys.argv[1])

username = xbmcplugin.getSetting(handle, SETTING_USERNAME)
password = xbmcplugin.getSetting(handle, SETTING_PASSWORD)
login = xbmcplugin.getSetting(handle, SETTING_LOGIN)
if login=="true" and (not username or not password):
    xbmcaddon.Addon(id=PLUGIN_ID).openSettings()

soundcloud_client = SoundCloudClient(login, username, password, oauth_token)

if oauth_token=="":
    oauth_token = soundcloud_client.oauth_token
    
if login=="true" and oauth_token=="":
    #error login failed
    login="false"
    loginerror="true"
    common.log("Login Failed", 2)
   

def addDirectoryItem(name, label2='', infoType="Music", infoLabels={}, isFolder=True, parameters={}, url=""):
    ''' Add a list item to the XBMC UI.'''
    li = xbmcgui.ListItem(name, label2)
    if not infoLabels:
        infoLabels = {"Title": name }

    li.setInfo(infoType, infoLabels)
    if url=="":
        url = sys.argv[0] + '?' + urllib.urlencode(parameters) 
    else:
        #activities next url
        url = sys.argv[0] + '?' + urllib.urlencode(parameters) + '&' + "nexturl=" + url
    print(url)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)

def show_tracks_menu():
    ''' Show the Tracks menu. '''
    if login == 'true':
        addDirectoryItem(name='Favorites', parameters={PARAMETER_KEY_URL: PLUGIN_URL + "favorites", PARAMETER_KEY_MODE: MODE_TRACKS_FAVORITES, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
        addDirectoryItem(name='New in Dashboard', parameters={PARAMETER_KEY_URL: PLUGIN_URL + "dashboard", PARAMETER_KEY_MODE: MODE_TRACKS_DASH, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
        addDirectoryItem(name='Shared Private', parameters={PARAMETER_KEY_URL: PLUGIN_URL + "private", PARAMETER_KEY_MODE: MODE_TRACKS_PRIVATE, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Hottest", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "tracks/hottest", PARAMETER_KEY_MODE: MODE_TRACKS_HOTTEST, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Search", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "tracks/search", PARAMETER_KEY_MODE: MODE_TRACKS_SEARCH, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_users_menu():
    ''' Show the Users menu. '''
    if login == 'true':
        addDirectoryItem(name="Followings", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "followings", PARAMETER_KEY_MODE: MODE_USERS_FOLLOWINGS, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
        addDirectoryItem(name="Followers", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "followers", PARAMETER_KEY_MODE: MODE_USERS_FOLLOWERS, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Hottest", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "users/hottest", PARAMETER_KEY_MODE: MODE_USERS_HOTTEST, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Search", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "users/search", PARAMETER_KEY_MODE: MODE_USERS_SEARCH, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_groups_menu():
    ''' Show the Groups menu. '''
    if login == 'true':
        addDirectoryItem(name="My Groups", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "mygroups", PARAMETER_KEY_MODE: MODE_GROUPS_FAVORITES, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Hottest", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "groups/hottest", PARAMETER_KEY_MODE: MODE_GROUPS_HOTTEST, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name="Search", parameters={PARAMETER_KEY_URL: PLUGIN_URL + "groups/search", PARAMETER_KEY_MODE: MODE_GROUPS_SEARCH, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_tracks(tracks, parameters={}):
    ''' Show a list of tracks. A 'More...' item is added, 
        if there are more items available, then what is currently listed. '''
    xbmcplugin.setContent(handle, "songs")
    for track in tracks:
        li = xbmcgui.ListItem(label=track[client.TRACK_TITLE], thumbnailImage=track[client.TRACK_ARTWORK_URL])
        li.setInfo("music", { "title": track[client.TRACK_TITLE], "genre": track.get(client.TRACK_GENRE, "") })
        li.setProperty("mimetype", 'audio/mpeg')
        li.setProperty("IsPlayable", "true")
        trackid = str(track[client.TRACK_ID])
        track_parameters = {PARAMETER_KEY_MODE: MODE_TRACK_PLAY, PARAMETER_KEY_URL: PLUGIN_URL + "tracks/" + trackid, "permalink": trackid, PARAMETER_KEY_TOKEN: oauth_token}
        url = sys.argv[0] + '?' + urllib.urlencode(track_parameters)
        #url = track['stream_url']
        ok = xbmcplugin.addDirectoryItem(handle, url=url, listitem=li, isFolder=False)
    if not len(tracks) < parameters[PARAMETER_KEY_LIMIT]:
        modified_parameters = parameters.copy()
        modified_parameters[PARAMETER_KEY_OFFSET] = str(int(parameters[PARAMETER_KEY_OFFSET]) + int(parameters[PARAMETER_KEY_LIMIT]))
        addDirectoryItem(name="More...", parameters=modified_parameters, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_activity_tracks(tracks, nexturl, parameters={}):
    ''' Show a list of tracks. A 'More...' item is added, 
        if there are more items available, then what is currently listed. '''
    xbmcplugin.setContent(handle, "songs")
    for track in tracks:
        li = xbmcgui.ListItem(label=track[client.TRACK_TITLE], thumbnailImage=track[client.TRACK_ARTWORK_URL])
        li.setInfo("music", { "title": track[client.TRACK_TITLE], "genre": track.get(client.TRACK_GENRE, "") })
        li.setProperty("mimetype", 'audio/mpeg')
        li.setProperty("IsPlayable", "true")
        trackid = str(track[client.TRACK_ID])
        track_parameters = {PARAMETER_KEY_MODE: MODE_TRACK_PLAY, PARAMETER_KEY_URL: PLUGIN_URL + "tracks/" + trackid, "permalink": trackid, PARAMETER_KEY_TOKEN: oauth_token}
        url = sys.argv[0] + '?' + urllib.urlencode(track_parameters)
        ok = xbmcplugin.addDirectoryItem(handle, url=url, listitem=li, isFolder=False)
    if nexturl != "":
        addDirectoryItem(name="More...", parameters=parameters, isFolder=True, url=nexturl)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


def play_track(id):
    ''' Start to stream the track with the given id. '''
    track = soundcloud_client.get_track(id)
    li = xbmcgui.ListItem(label=track[client.TRACK_TITLE], thumbnailImage=track.get(client.TRACK_ARTWORK_URL, ""), path=track[client.TRACK_STREAM_URL])
    li.setInfo("music", { "title": track[client.TRACK_TITLE], "genre": track.get(client.TRACK_GENRE, "") })
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
    

def show_users(users, parameters):
    ''' Show a list of users. A 'More...' item is added, 
        if there are more items available, then what is currently listed. '''
    for user in users:
        li = xbmcgui.ListItem(label=user.get(client.USER_NAME, ""), thumbnailImage=user.get(client.USER_AVATAR_URL, ""))
        user_parameters = {PARAMETER_KEY_MODE: MODE_USERS_TRACKS, PARAMETER_KEY_URL: PLUGIN_URL + "users/" + user[client.USER_PERMALINK], "user_permalink": user[client.USER_PERMALINK], PARAMETER_KEY_TOKEN: oauth_token}
        url = sys.argv[0] + '?' + urllib.urlencode(user_parameters)
        ok = xbmcplugin.addDirectoryItem(handle, url=url, listitem=li, isFolder=True)
    if not len(users) < parameters[PARAMETER_KEY_LIMIT]:
        more_item_parameters = parameters.copy()
        more_item_parameters[PARAMETER_KEY_OFFSET] = str(int(parameters[PARAMETER_KEY_OFFSET]) + int(parameters[PARAMETER_KEY_LIMIT]))
        addDirectoryItem(name="More...", parameters=more_item_parameters, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_groups(groups, parameters):
    ''' Show a list of groups. A 'More...' item is added, 
        if there are more items available, then what is currently listed. '''
    for group in groups:
        li = xbmcgui.ListItem(label=group.get(client.GROUP_NAME, ""), thumbnailImage=group.get(client.GROUP_ARTWORK_URL, ""))
        group_parameters = {PARAMETER_KEY_MODE: MODE_GROUPS_TRACKS, PARAMETER_KEY_URL: PLUGIN_URL + "groups/" + group[client.GROUP_PERMALINK], "group_id": group[client.GROUP_ID], PARAMETER_KEY_TOKEN: oauth_token}
        url = sys.argv[0] + '?' + urllib.urlencode(group_parameters)
        ok = xbmcplugin.addDirectoryItem(handle, url=url, listitem=li, isFolder=True)
    if not len(groups) < parameters[PARAMETER_KEY_LIMIT]:
        more_item_parameters = parameters.copy()
        more_item_parameters[PARAMETER_KEY_OFFSET] = str(int(parameters[PARAMETER_KEY_OFFSET]) + int(parameters[PARAMETER_KEY_LIMIT]))
        addDirectoryItem(name="More...", parameters=more_item_parameters, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def _show_keyboard(default="", heading="", hidden=False):
    ''' Show the keyboard and return the text entered. '''
    search = common.getUserInput(heading, default)
    return search

def show_root_menu():
    ''' Show the plugin root menu. '''
    addDirectoryItem(name='Groups', parameters={PARAMETER_KEY_URL: PLUGIN_URL + 'groups', PARAMETER_KEY_MODE: MODE_GROUPS, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name='Tracks', parameters={PARAMETER_KEY_URL: PLUGIN_URL + 'tracks', PARAMETER_KEY_MODE: MODE_TRACKS, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    addDirectoryItem(name='Users', parameters={PARAMETER_KEY_URL: PLUGIN_URL + 'users', PARAMETER_KEY_MODE: MODE_USERS, PARAMETER_KEY_TOKEN: oauth_token}, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
##################################################################

# Depending on the mode, call the appropriate function to build the UI.
if not sys.argv[ 2 ] or not url:
    # new start
    ok = show_root_menu()
elif mode == MODE_GROUPS:
    ok = show_groups_menu()
elif mode == MODE_TRACKS:
    ok = show_tracks_menu()
elif mode == MODE_USERS:
    ok = show_users_menu()
elif mode == MODE_TRACKS_SEARCH:
    if (not query):
        query = _show_keyboard()
    tracks = soundcloud_client.get_tracks(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, query)
    ok = show_tracks(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url, "q":query}, tracks=tracks)
elif mode == MODE_TRACKS_HOTTEST:
    tracks = soundcloud_client.get_tracks(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_tracks(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, tracks=tracks)
elif mode == MODE_TRACKS_FAVORITES:
    tracks = soundcloud_client.get_favorite_tracks(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_tracks(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, tracks=tracks)
elif mode == MODE_TRACKS_DASH:
    tracks,nexturl = soundcloud_client.get_dash_tracks(int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, nexturl)
    ok = show_activity_tracks(parameters={PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, tracks=tracks, nexturl=nexturl)
elif mode == MODE_TRACKS_PRIVATE:
    tracks,nexturl = soundcloud_client.get_private_tracks(int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, nexturl)
    ok = show_activity_tracks(parameters={PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, tracks=tracks, nexturl=nexturl)
elif mode == MODE_GROUPS_SEARCH:
    if (not query):
        query = _show_keyboard()
    groups = soundcloud_client.get_normal_groups(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, query)
    ok = show_groups(groups=groups, parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url, "q":query})
elif mode == MODE_GROUPS_HOTTEST:
    groups = soundcloud_client.get_normal_groups(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_groups(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, groups=groups)
elif mode == MODE_GROUPS_TRACKS:
    tracks = soundcloud_client.get_group_tracks(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, int(params.get("group_id", "1")))
    ok = show_tracks(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL: url}, tracks=tracks)
elif mode == MODE_GROUPS_FAVORITES:
    groups = soundcloud_client.get_following_groups(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_groups(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, groups=groups)
elif mode == MODE_USERS_SEARCH:
    if (not query):
        query = _show_keyboard()
    users = soundcloud_client.get_users(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, query)
    ok = show_users(users=users, parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url, "q":query})
elif mode == MODE_USERS_HOTTEST:
    users = soundcloud_client.get_users(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_users(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, users=users)
elif mode == MODE_USERS_FOLLOWINGS:
    users = soundcloud_client.get_following_users(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_users(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, users=users)
elif mode == MODE_USERS_FOLLOWERS:
    users = soundcloud_client.get_follower_users(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_users(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, users=users)
elif mode == MODE_USERS_HOTTEST:
    users = soundcloud_client.get_users(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url)
    ok = show_users(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL:url}, users=users)
elif mode == MODE_USERS_TRACKS:
    tracks = soundcloud_client.get_user_tracks(int(params.get(PARAMETER_KEY_OFFSET, "0")), int(params.get(PARAMETER_KEY_LIMIT, "50")), mode, url, params.get("user_permalink"))
    ok = show_tracks(parameters={PARAMETER_KEY_OFFSET: int(params.get(PARAMETER_KEY_OFFSET, "0")), PARAMETER_KEY_LIMIT: int(params.get(PARAMETER_KEY_LIMIT, "50")), PARAMETER_KEY_MODE: mode, PARAMETER_KEY_URL: url}, tracks=tracks)
elif mode == MODE_TRACK_PLAY:
    play_track(params.get(PARAMETER_KEY_PERMALINK, "1"))
    
if loginerror=="true":
    xbmc.executebuiltin("Notification(%s,%s,%i)" % ("warning", "Login Failed", 5000))
    