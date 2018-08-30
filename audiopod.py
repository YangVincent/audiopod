"""
Notes:
    Dropbox links don't work
    Google drive links don't work
    Both m4a and m4b do work
    Host on a webserver
"""
import sys
import os
from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route("/")
def get_podcast():
    return send_from_directory('skeleton', 'rss.xml')

@app.route("/files/<path:path>")
def send_files(path):
    print('path is ' + str(path))
    return send_from_directory('files', path)

def generate_podcast_xml(base, books):
    from podgen import Podcast, Episode
    from datetime import timedelta
    from podgen import Media
    
    p = Podcast()
    
    p.name = "AeonNeo's Audiobooks"
    p.description = "Description"
    p.website = "www.yangvincent.com"
    p.explicit = False
    
    # create episode
    for book_name in books:
        ep = Episode()
        ep.title = book_name[:-4]
        full_path = base + '/files/' + book_name
        dev_path = 'files/' + book_name
        try:
            book_size = os.path.getsize(dev_path)
        except OSError as e:
            print(e)
            book_size = 0

        ep.media = Media(full_path, type = 'audio/mp4a', size=book_size)
        p.episodes.append(ep)
    
    # Generate rss
    p.rss_file('skeleton/rss.xml', minimize=True)

def get_books():
    books = []
    for entry in os.scandir('files/'):
        if entry.is_file():
            print(entry.path)
            books.append(entry.path[6:])
    return(books)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        books = get_books()
        generate_podcast_xml(sys.argv[1], books)
    else:
        print("Usage: python3.7 create_podcast.py ngrok_public_route")
