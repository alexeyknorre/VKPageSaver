import os
import requests
import urllib


directory = '../saved_page/music'
output_txt = directory + "/audios.txt"

# Create directory to save results
if not os.path.exists(directory):
    os.makedirs(directory)


def get_music_list(user_id, secret_key):
    music_response = requests.get("https://api.vk.com/method/audio.get?owner_id=" + user_id +
                                  "&need_user=0&count=5000&access_token="+ secret_key).json()
    print "Got {0} audios from UID {1}.".format(len(music_response[u'response'])-1, user_id)
    return music_response[u'response'][1:]


def save_music_list(music_list, audios_txt):
    with open(directory+"/music_list.txt", 'wb') as f:
        f.write(u'artist'+" "+ u'title' +" "+ u'url'+"\n")
        for audiotrack in music_list:
            f.write("{0} - {1};URL:{2}\n".format(audiotrack[u'artist'].encode("UTF-8"),
                                                 audiotrack[u'title'].encode("UTF-8"),
                                                 audiotrack[u'url'].encode("UTF-8")))
def save_music_tracks(music_list, directory):
    c = 1
    for track in music_list:
        print("Downloading music files... {0}/{1}".format(c, len(music_list)))
        urllib.URLopener().retrieve(track[u'url'], "{0}/{1} - {2}.mp3".format(directory,
                                                                                   track[u'artist'].encode("cp1251"),
                                                                                   track[u'title'].encode("cp1251")))
        c += 1

def get_music(user_id, secret_key, directory=directory):
    print("Getting music...")
    music_list = get_music_list(user_id, secret_key)
    save_music_list(music_list, directory)
    save_music_tracks(music_list, directory)
    print("Music saved.")
