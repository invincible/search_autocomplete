from flask import Flask, render_template, request
import requests as req
import random
import time
import pickle
import numpy as np

from gensim.models.fasttext import FastText
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, OkapiBM25Model
from gensim.similarities import SparseMatrixSimilarity

ft_model = FastText.load('fastText/fasttext.model')
dictionary = Dictionary.load('fastText/dictionary_5M')

app = Flask(__name__)

def read_list():
    with open('fastText/corpus_5M', 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

corpus = read_list()

bm25_model = OkapiBM25Model(dictionary=dictionary)
bm25_corpus = bm25_model[list(map(dictionary.doc2bow, corpus))]
bm25_index = SparseMatrixSimilarity(bm25_corpus, num_docs=len(corpus), num_terms=len(dictionary),
                                   normalize_queries=False, normalize_documents=False)

tfidf_model = TfidfModel(dictionary=dictionary, smartirs='bnn')


def expand_query(query, wv, topn=10):
    expanded_query = [t for t in query]

    for t in query:
        expanded_query.extend(s for s, f in wv.most_similar(t, topn=topn))

    return expanded_query


def get_top_n(query, n=10):
    tfidf_query = tfidf_model[dictionary.doc2bow(query)]
    similarities = bm25_index[tfidf_query]

    idx = np.argpartition(similarities, -n)[-n:]
    topn = idx[np.argsort(-similarities[idx])]

    topk = []
    for i in topn:
        topk.append(' '.join(corpus[i]))

    return topk


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
    rnd_videos = random.sample(videos, 10) #10
    return render_template('index.html', videos=rnd_videos, found=len(rnd_videos))


@app.route("/autocomplete")
def autocomplete():
    # var data = [
    #     {label: "annhhx10", category: "Products"},
    #     {label: "andreas johnson", category: "People"}
    # ];
    term = request.values['term'].split()
    # prev = term[:-1]
    # term = term[-1]
    test_query_exp = expand_query(term, ft_model.wv)
    found_videos = get_top_n(test_query_exp, 10)
    #found_videos = ft_model.wv.most_similar(term, topn=10)
    # found_videos = find_video(term)
    video_titles = []
    for video in found_videos:
        # video_titles.append({'label': video['title'], 'category': video['category']['name']})
        video_titles.append({'label': video, 'category': ''})
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
    app.run()
    #app.run(host='0.0.0.0', port=80)
