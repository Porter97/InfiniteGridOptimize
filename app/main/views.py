from flask import render_template, request, current_app
from . import main
from .. import cache
from ..utils import make_cache_key
import requests


@main.route('/')
def index():
    return render_template("templates/index.html")


@main.route('/images')
@cache.cached(key_prefix=make_cache_key, timeout=60)
def get_images():

    page = request.args.get('page', 1, type=int)

    query = {
        "client_id": current_app.config['UNSPLASH_CLIENT_ID'],
        "page": page,
        "per_page": current_app.config['RESULTS_PER_PAGE'],
    }

    u_query = request.args.get('query')
    if u_query and u_query != 'null':
        query['query'] = u_query
        r = requests.get('https://api.unsplash.com/search/photos', params=query)
        res = r.json()
        return {'body': [{'image': x['urls']['small'],
                         'hash': x['blur_hash']} for x in res['results']]}, 200
    else:
        r = requests.get('https://api.unsplash.com/photos', params=query)
        return {'body': [{'image': x['urls']['small'],
                         'hash': x['blur_hash']} for x in r.json()]}, 200