import os
import requests
import re
import urllib


directory = '../saved_page/photos'

# Create directory to save results
if not os.path.exists(directory):
    os.makedirs(directory)


def get_albums_list(user_id, secret_key):
    print("Getting photo albums...")
    photos_albums_response = requests.get("https://api.vk.com/method/photos.getAlbums?owner_id=" + user_id +
                                  "&need_system=1&access_token="+ secret_key).json()
    #print "Got {0} albums from UID {1}.".format(len(music_response[u'response'])-1, user_id)
    albums_list = []
    rx = '[' + re.escape('><\/:|?"*') + ']'
    for album in photos_albums_response[u'response']:
        # Remove characters that are forbidden in Windows filenames
        title = re.sub(rx, '', album[u'title'])
        folder = '{0}/{1}'.format(directory, title.encode('cp1251'))
        if not os.path.exists(folder):
            os.makedirs(folder)
        albums_list.append([title, album[u'aid']])
    print("Got {0} photo albums.".format(len(albums_list)))
    return albums_list

def get_photos_from_album(albums_list, user_id, secret_key):
    print("Getting photos...")
    c = 1
    sizes = [u'src',u'src_big',u'src_xbig', u'src_xxbig',u'src_xxxbig']
    for album in albums_list:
        print("{0}/{1}. Downloading {2}...".format(c,len(albums_list), album[0].encode("utf-8")))
        photos_response = requests.get("https://api.vk.com/method/photos.get?owner_id=" + user_id +
                                  "&album_id="+ str(album[1]) +"&access_token="+ secret_key).json()[u'response']
        for photo in photos_response:
            # Choosing the largest image available
            for size in sizes:
                try:
                    url = photo[size]
                except:
                    break
            picture = "{0}/{1}/{2}.jpg".format(directory, album[0].strip().encode("cp1251"),
                                                                      photo[u'pid'])
            if not os.path.isfile(picture):
                urllib.URLopener().retrieve(url, picture)
        c+=1


def get_photos(user_id, secret_key):
    albums_list = get_albums_list(user_id, secret_key)
    get_photos_from_album(albums_list, user_id, secret_key)
