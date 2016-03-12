# coding: utf-8
from __future__ import unicode_literals

import re
import base64
import socket

from .common import InfoExtractor
from ..utils import (
    RegexNotFoundError,
    ExtractorError
)
from ..compat import (
    compat_urllib_request,
    compat_http_client,
    compat_urllib_error
)

class KissAnimeIE(InfoExtractor):
    IE_NAME = 'kissanime.to'
    _VALID_URL = r'https?://kissanime\.to/Anime/.+\?id=(?P<id>[0-9]+)'

    _TEST = {
        'url': 'https://kissanime.to/Anime/Sakurasou-no-Pet-na-Kanojo/Episode-002?id=284',
        'md5': '280444729039609b6588b7719edda0b3',
        'info_dict': {
            'id': '284',
            'ext': 'mp4',
            'title': 'Sakurasou no Pet na Kanojo Episode 002'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id, note='Downloading video page ...')
        title = self._search_regex(r'<title>\s*([^\r\n]+)\s*([^\r\n]+)', webpage, 'title', group = 1) + ' ' + self._search_regex(r'<title>\s*([^\r\n]+)\s*([^\r\n]+)', webpage, 'title', group = 2)

        base64_urls = re.findall(r'value="(.*?)".*?(?:[0-9]p)', webpage)
        if not base64_urls:
            raise RegexNotFoundError('Unable to extract video URL')

        formats = []
        for url in base64_urls:
            height = self._search_regex(r'' + url + r'.*?([0-9]+)p', webpage, 'video quality')
            url = base64.b64decode(url)

            request = compat_urllib_request.Request(url)
            request.get_method = lambda : 'HEAD'
            try:
                response = compat_urllib_request.urlopen(request)
            except (compat_urllib_error.URLError, compat_http_client.HTTPException, socket.error) as err:
                raise ExtractorError('Unable send HEAD request')

            formats.append({
                'url': response.geturl(),
                'height': height,
                'ext': 'mp4',
                'vcodec': 'h264'
            })
        formats.reverse()

        return {
            'id': video_id,
            'title': title,
            'formats': formats
        }
