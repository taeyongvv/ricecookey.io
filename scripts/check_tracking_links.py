"""Run locally, or pass https://www.ricecookey.com to verify deployed bytes."""
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from urllib.request import urlopen

root = Path(__file__).resolve().parents[1]
count = 0
for app, package, apple_id in (
    ('plants', 'com.ricecookey.plantskeeper', '6793824278'),
    ('gyeomsa', 'com.ricecookey.gyeomsa', '6805783865'),
):
    for channel in ('', 'x/'):
        for platform in ('aos', 'ios'):
            path = f'go/{app}/{channel}{platform}/index.html'
            local = (root / path).read_text(encoding='utf-8')
            text = local
            if len(sys.argv) > 1:
                with urlopen(sys.argv[1].rstrip('/') + '/' + path.removesuffix('index.html'), timeout=30) as response:
                    assert response.status == 200, path
                    text = response.read().decode()
                assert text == local, f'deployed content differs: {path}'
            js_url = re.search(r'location.replace\("([^"]+)"\)', text).group(1)
            href = unescape(re.search(r'<a href="([^"]+)"', text).group(1))
            meta = unescape(re.search(r'content="3;url=([^"]+)"', text).group(1))
            assert js_url == href == meta, path
            url = urlsplit(js_url)
            params = parse_qs(url.query)
            assert url.scheme == 'https'
            if platform == 'aos':
                assert url.netloc == 'play.google.com' and params['id'] == [package]
                if channel:
                    assert set(params) == {'id', 'referrer'}
                    assert parse_qs(params['referrer'][0]) == {
                        'utm_source': ['x'], 'utm_medium': ['social'], 'utm_campaign': ['x']}
                else:
                    assert set(params) == {'id'}
            else:
                assert url.netloc == 'apps.apple.com' and url.path.endswith('/id' + apple_id)
                # No invented provider token: iOS download attribution is pending.
                assert not params
            assert 'defer src="/_vercel/insights/script.js"' in text
            assert '"load"' in text and '),350)' in text
            assert '<meta name="robots" content="noindex">' in text
            count += 1
            print('PASS', path, '->', js_url)
assert count == 8
print(f'PASS: {count} routes; redirects, campaign encoding, analytics script, and fallbacks')
