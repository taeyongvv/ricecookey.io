"""Static checks for the product guide pages (stdlib only): python3 scripts/check_product_pages.py"""
import hashlib
import json
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
SITE = 'https://www.ricecookey.com/'
INVENTORY = json.loads((root / 'docs/product-guide-inventory.json').read_text(encoding='utf-8'))
GUIDED = [p for p in INVENTORY['products'] if p['state'] in ('existing', 'eligible')]
SECTIONS = {  # games/ guides describe a play loop and controls; apps/ guides describe purpose and features
    'games': ('loop', 'controls', 'start', 'tips', 'gallery', 'faq', 'stores', 'help', 'refs'),
    'apps': ('what', 'features', 'start', 'tips', 'gallery', 'faq', 'stores', 'help', 'refs'),
}
HELP = 'mailto:ricecookey.help@gmail.com'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.imgs, self.metas, self.scripts = [], [], [], {}, 0
        self.lang = None
        self.section = None  # current language section id
        self.count = {}      # (section, tag) -> n
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'section' and a.get('id') in ('korean', 'english'):
            self.section = a['id']
            assert a.get('lang') == {'korean': 'ko', 'english': 'en'}[a['id']], a
        if tag == 'script':
            self.scripts += 1
        if tag == 'meta' and 'name' in a:
            self.metas[a['name']] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.metas['canonical'] = a['href']
        if tag == 'link' and a.get('rel') == 'stylesheet':
            self.links.append((a['href'], a))
        if tag == 'a' and 'href' in a:
            self.links.append((a['href'], a))
        if tag == 'img':
            self.imgs.append((self.section, a))
        # The bare "English" heading (journal pattern) has no id and is not a content section.
        if self.section and tag in ('li', 'dt', 'dd', 'figure', 'figcaption', 'img', 'h2', 'h3', 'a') \
                and not (tag == 'h2' and 'id' not in a):
            key = (self.section, tag)
            self.count[key] = self.count.get(key, 0) + 1
            if tag == 'a' and a.get('href') == HELP:
                self.count[(self.section, 'help')] = self.count.get((self.section, 'help'), 0) + 1

    def handle_endtag(self, tag):
        if tag == 'section':
            self.section = None


def jpeg_size(path):
    data = path.read_bytes()
    assert data[:2] == b'\xff\xd8', f'not a JPEG: {path}'
    i = 2
    while i < len(data):
        marker, length = data[i + 1], struct.unpack('>H', data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack('>HH', data[i + 5:i + 9])
            return w, h
        i += 2 + length
    raise AssertionError(f'no JPEG size: {path}')


def target(page_path, href):
    """Resolve an internal href to (file, fragment)."""
    url = urlsplit(href)
    base = page_path.parent if url.path else page_path
    path = (base / url.path).resolve() if url.path else page_path
    if path.is_dir():
        path = path / 'index.html'
    return path, url.fragment


parsed = {}


def load(path):
    if path not in parsed:
        parsed[path] = Page(path.read_text(encoding='utf-8'))
    return parsed[path]


def check_links(path, page):
    for href, a in page.links:
        url = urlsplit(href)
        if url.scheme in ('http', 'https'):
            assert url.scheme == 'https', f'{path}: insecure {href}'
            if a.get('target') == '_blank':
                rel = set(a.get('rel', '').split())
                assert {'noopener', 'noreferrer'} <= rel, f'{path}: unsafe rel {href}'
            continue
        if url.scheme == 'mailto':
            continue
        assert not url.scheme and not url.netloc, f'{path}: unexpected link {href}'
        dest, frag = target(path, href)
        assert dest.exists(), f'{path}: broken link {href}'
        if frag and dest.suffix == '.html':
            assert frag in load(dest).ids, f'{path}: missing anchor {href}'


sources = (root / 'docs/product-guide-sources.md').read_text(encoding='utf-8')
sitemap = (root / 'sitemap.xml').read_text(encoding='utf-8')
index_path = root / 'index.html'
index_text = index_path.read_text(encoding='utf-8')
index = load(index_path)
shots = {s['file']: s for s in INVENTORY['screenshots']}

# Inventory covers the whole catalog exactly once; exclusions carry their failed checks.
catalog = re.findall(r'id="g-([a-z]+)-title"', index_text)
ids = [p['id'] for p in INVENTORY['products']]
assert len(catalog) == INVENTORY['catalog_count'] == len(ids), (len(catalog), INVENTORY['catalog_count'], len(ids))
assert sorted(catalog) == sorted(ids) and len(set(ids)) == len(ids), 'inventory ids must match the catalog'
for p in INVENTORY['products']:
    assert p['state'] in ('existing', 'eligible', 'excluded'), p
    if p['state'] == 'excluded':
        assert p.get('failed_checks') and p.get('reason') and 'guide' not in p, p
    else:
        assert re.fullmatch(r'(games|apps)/[a-z0-9-]+/', p['guide']), p

# Every listed screenshot exists with the recorded size and hash.
for rel, s in shots.items():
    img = root / rel
    assert jpeg_size(img) == (s['width'], s['height']), f'{rel}: size differs from inventory'
    assert hashlib.sha256(img.read_bytes()).hexdigest() == s['sha256'], f'{rel}: hash differs from inventory'
    assert s['original_url'].startswith('https://') and s['source_index'], rel

# Every i18n key used by the homepage exists in both languages.
i18n = (root / 'i18n.js').read_text(encoding='utf-8')
ko_block, en_block = i18n.split('\n  en: {')
for lang, block in (('ko', ko_block), ('en', en_block)):
    keys = set(re.findall(r'^\s*"([^"]+)":', block, re.M))
    for key in re.findall(r'data-i18n(?:-aria|-alt|-html)?="([^"]+)"', index_text):
        assert key in keys, f'i18n.js {lang}: missing key {key}'

for product in GUIDED:
    guide = product['guide']
    kind, slug = guide.strip('/').split('/')
    path = root / guide / 'index.html'
    page = load(path)
    text = path.read_text(encoding='utf-8')
    assert page.lang == 'ko', path
    assert page.metas.get('canonical') == f'{SITE}{guide}', path
    assert len(page.metas.get('description', '')) > 50, f'{path}: meta description'
    assert 'width=device-width' in page.metas.get('viewport', ''), path
    assert page.scripts == 0, f'{path}: primary content must not depend on JS'
    dupes = {i for i in page.ids if page.ids.count(i) > 1}
    assert not dupes, f'{path}: duplicate ids {dupes}'
    for lang, prefix in (('korean', 'ko'), ('english', 'en')):
        assert lang in page.ids, f'{path}: missing #{lang}'
        for s in SECTIONS[kind]:
            assert f'{prefix}-{s}' in page.ids, f'{path}: missing #{prefix}-{s}'
        assert page.count.get((lang, 'help'), 0) >= 2, f'{path}: help email in {lang}'
        assert page.count.get((lang, 'figure'), 0) >= 2, f'{path}: gallery in {lang}'
        assert page.count.get((lang, 'figcaption'), 0) == page.count.get((lang, 'figure')), path
    for tag in ('li', 'dt', 'dd', 'figure', 'img', 'h2', 'h3', 'a'):
        ko, en = page.count.get(('korean', tag), 0), page.count.get(('english', tag), 0)
        assert ko == en, f'{path}: KO/EN mismatch for <{tag}> ({ko} vs {en})'
    for section, a in page.imgs:
        assert len(a.get('alt', '')) > 20, f'{path}: weak alt {a.get("src")}'
        img = target(path, a['src'])[0]
        assert img.parent == root / 'assets/games' / slug, f'{path}: asset outside assets/games/{slug}'
        assert jpeg_size(img) == (int(a['width']), int(a['height'])), f'{path}: size attrs {img}'
        rel = img.relative_to(root).as_posix()
        if product['state'] == 'existing':
            assert rel in sources and hashlib.sha256(img.read_bytes()).hexdigest() in sources, \
                f'{rel}: missing from docs/product-guide-sources.md'
        else:
            assert rel in shots and rel in sources, f'{rel}: missing from inventory screenshots or sources doc'
    if product.get('beta'):
        for label in ('베타', 'beta'):
            assert label in text, f'{path}: beta status label {label}'
    # Editions are labelled in both languages.
    if slug in ('last-castle', 'tingle-tingle'):
        for label in ('무료 버전', 'Free edition'):
            assert label in text, f'{path}: edition label {label}'
    elif slug == 'wakbu-ball':
        for label in ('광고 없는 버전', 'Ad-free edition'):
            assert label in text, f'{path}: edition label {label}'
    else:
        ko_h3, en_h3 = (re.findall(r'<h3>([^<]+)</h3>', part) for part in text.split('<section id="english"'))
        assert ko_h3 and len(ko_h3) == len(en_h3), f'{path}: store card labels in both languages'
    if slug == 'tingle-tingle':
        for label in ('광고 제거 버전', 'Ad-free edition', '0000763243', '0000761967'):
            assert label in text, f'{path}: {label}'
        assert 'details?id=com.RiceCookey.donglepaid' not in text, 'unverified Google Play paid link'
    check_links(path, page)
    hrefs = [h for h, _ in index.links]
    assert hrefs.count(f'./{guide}') == 1, f'catalog link for {guide}'
    assert f'<loc>{SITE}{guide}</loc>' in sitemap, f'sitemap entry for {guide}'
    print('PASS', path.relative_to(root))

dupes = {i for i in index.ids if index.ids.count(i) > 1}
assert not dupes, f'index.html duplicate ids {dupes}'
check_links(index_path, index)
for loc in re.findall(r'<loc>([^<]+)</loc>', sitemap):
    assert loc.startswith(SITE), loc
    assert target(root / 'index.html', './' + loc[len(SITE):])[0].exists(), f'sitemap target missing: {loc}'
assert (root / '.task/screenshot-manifest.json').exists() or 'screenshot-manifest' in sources
counts = {s: sum(p['state'] == s for p in INVENTORY['products']) for s in ('existing', 'eligible', 'excluded')}
print(f'PASS: {len(GUIDED)} guide pages ({counts}) of {len(catalog)} catalog entries; inventory, '
      f'{len(shots)} screenshot hashes/sizes, i18n keys, KO/EN parity, links/anchors, catalog, sitemap, sources')
