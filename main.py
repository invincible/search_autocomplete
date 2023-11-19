from flask import Flask, render_template, request
import requests as req

app = Flask(__name__)


def read_api():
    # https://rutube.ru/api/metainfo/tv/28/video?sort=random
    r = req.get('https://rutube.ru/api/tags/video/5994/?noSubs=true').json()
    return r['results']


videos = read_api()


def find_video(query):
    result = []
    for video in videos:
        if query.lower() in video['title'].lower():
            result.append(video)
    return result


@app.route("/")
def index():
    # videos = read_api()
    # print(videos)
    return render_template('index.html', videos=videos, found=len(videos))


@app.route("/autocomplete")
def autocomplete():
    term = request.values['term']
    found_videos = find_video(term)
    video_titles = []
    for video in found_videos:
        video_titles.append(video['title'])
    return video_titles


@app.route("/search")
def search():
    query = request.values['search_text'].lower()
    result = []
    for video in videos:
        if query in video['title'].lower():
            result.append(video)

    return render_template('index.html', videos=result, found=len(result), query=query)


if __name__ == "__main__":
    app.run(debug=True)
