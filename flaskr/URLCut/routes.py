from flask import Blueprint, jsonify, request, abort, redirect
from flaskr.Models.models import ShortURL
import re


shorten = Blueprint('shorten', __name__)


@shorten.route('/api/shorten')
def get_urls():
    urls = ShortURL.query.all()

    if not urls:
        abort(404, 'No URL\'s Available!')

    urls = [u.display() for u in urls]

    return jsonify({
        'urls': urls,
        'success': True
    })


@shorten.route('/api/shorten/<short_url>')
def redirect_to_url(short_url):
    link = ShortURL.query.filter_by(short_url=short_url).first()

    if not link:
        abort(400, 'This Link is Not Available!')

    return jsonify({
        'url': link.original_url,
        'success': True
    })


@shorten.route('/api/shorten', methods=['POST'])
def create_short_url():

    req = request.get_json()
    original_url = req.get('original_url')
    url_key = req.get('url_key')

    if not req or not original_url:
        abort(400, 'You Should Provide A URL First!')

    if url_key:
        if url_key in [u.short_url for u in ShortURL.query.all()] or not url_key.isalnum():
            abort(400, 'URL Key Is Used!')

    try:
        validation = validate_url(original_url)

        if not validation:
            raise Exception('URL is Not Valid')

        link = ShortURL(original_url=original_url, short_url=url_key)
        link.insert()

        return jsonify({
            'short_url': link.short_url,
            'full_data': link.display(),
            'success': True
        })

    except Exception as e:
        print(e)
        abort(400, e)


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url)
