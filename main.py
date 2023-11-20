from flask import Flask, render_template, request
import requests as req
import random
import time

app = Flask(__name__)


def read_api():
    # https://rutube.ru/api/metainfo/tv/28/video?sort=random
    # https://rutube.ru/api/tags/video/5994/?noSubs=true&page=2
    videos = []
    for i in range(10):
        url = "https://rutube.ru/api/tags/video/5994/?noSubs=true&page="+str(i+1)
        print(url)
        r = req.get(url).json()
        print(r)
        time.sleep(1)
        videos.extend(r['results'])
    return videos


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
    rnd_videos = random.sample(videos, 10)
    return render_template('index.html', videos=rnd_videos, found=len(rnd_videos))


@app.route("/autocomplete")
def autocomplete():
    # var data = [
    #     {label: "annhhx10", category: "Products"},
    #     {label: "andreas johnson", category: "People"}
    # ];
    term = request.values['term']
    found_videos = find_video(term)
    video_titles = []
    for video in found_videos:
        video_titles.append({'label': video['title'], 'category': video['category']['name']})
    return video_titles[:10]


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
    #app.run(host='0.0.0.0', port=80)
