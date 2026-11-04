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
# Last Castle is an editorial decision guide (2026-11-05 approved copy): no controls/FAQ sections,
# two decision sections and a loss-review section instead. Every other guide keeps SECTIONS.
SECTIONS_BY_SLUG = {
    'last-castle': ('loop', 'tips', 'reroll', 'review', 'start', 'gallery', 'stores', 'help', 'refs'),
}
# The homepage reading entry intentionally adds a second link to these guides (catalog + reading entry).
HOME_GUIDE_LINKS = {'games/last-castle/': 2}
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
ko_keys, en_keys = (set(re.findall(r'^\s*"([^"]+)":', b, re.M)) for b in (ko_block, en_block))
assert ko_keys == en_keys, f'i18n.js KO/EN key sets differ: {ko_keys ^ en_keys}'


def has(text, where, *phrases):
    for s in phrases:
        assert s in text, f'{where}: missing approved text {s!r}'


def lacks(text, where, *phrases):
    for s in phrases:
        assert s not in text, f'{where}: superseded or overbroad text {s!r}'


# Approved 2026-11-05 content: limitations, discovery entry and corrections must not regress.
lc = (root / 'games/last-castle/index.html').read_text(encoding='utf-8')
has(lc, 'last-castle', '이 글은 실제 클리어 공략이 아닙니다', 'This is not a tested clear strategy',
    '촬영 빌드는 미확인', 'capture build unconfirmed', '소환 궁수 공격력 +35%', 'Summoned archer attack +35%',
    '리롤 후: 1251', '1251 remaining afterward', '앱에 이 기록 양식이 있다는 뜻은 아닙니다',
    'not a form provided by the game', '<table>', '다시 확인했다는 뜻이 아닙니다',
    'does not mean later store changes were re-checked', '실제 플레이 검증이 아닙니다', 'not a verified run')
lacks(lc, 'last-castle', 'HP 50%', '50% HP', '20웨이브', 'A stage has 20 waves', '런당 1회', 'once per run',
      '적 HP +100%', 'enemy HP +100%', '엔드리스 모드는 스테이지 1', 'Endless Mode unlocks', '영웅에게 적용되지 않습니다',
      'do not apply to heroes', 'Healing Spring', 'Archer Drill', '성 HP부터 보세요', 'Check castle HP first',
      '버전 1.7.3 기준, 홍보 문구 포함', '확인일 2026년 10월 20일', 'https://www.ricecookey.com/assets')
jr = (root / 'journal/last-castle-builds/index.html').read_text(encoding='utf-8')
has(jr, 'journal', '제작자의 과거 의도를 대신 말하는 회고가 아닙니다', "not a retrospective claiming to know the creator's past intentions",
    '아래 1.7.3 변경 공지와 같은 빌드의 화면이라고 단정하지 않습니다', 'The capture build of this promotional image is unconfirmed',
    '이번 글은 그 실험을 했다고 주장하지 않습니다', 'This article does not claim that experiment has happened',
    '공지는 변경 항목을 알려 주며, 효과 측정을 대신하지 않습니다', 'it is not an effect measurement',
    'href="../../games/last-castle/"', 'pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2103625263346419',
    '다시 확인했다는 뜻이 아닙니다')
lacks(jr, 'journal', 'RICECookey는', 'At RICECookey', 'Our design approach', 'We approach a build', '성을 지키는 선택의 설계',
      'Designing choices that defend the castle', 'https://www.ricecookey.com/assets', 'href="/')
journal_path = root / 'journal/last-castle-builds/index.html'
journal = load(journal_path)
assert not {i for i in journal.ids if journal.ids.count(i) > 1}, 'journal duplicate ids'
check_links(journal_path, journal)
# Homepage reading entry: exact audit KO/EN text, after the brand hero, before the catalog, not an install control.
entry = re.search(r'<aside class="read-entry".*?</aside>', index_text, re.S)
assert entry, 'index.html: reading entry'
assert index_text.index('class="hero-wrap"') < entry.start() < index_text.index('id="games"'), 'reading entry position'
e = entry.group(0)
has(e, 'reading entry', '게임에서 막혔나요?', '라스트캐슬 — 카드 효과를 읽고 패배를 복기하기',
    '제작 분석 — 선택 화면이 알려 주는 것과 남기는 것', 'href="./games/last-castle/"', 'href="./journal/last-castle-builds/"')
lacks(e, 'reading entry', 'store-link', 'btn', 'https://')
has(en_block, 'i18n en', '"read.title": "Stuck in a game?"', '"read.guide": "Last Castle — read card effects and review a loss"',
    '"read.journal": "Production analysis — what a choice screen tells you and leaves open"')
lacks(index_text + i18n, 'homepage journal teaser', '성을 지키는 선택의 설계', 'Designing choices that defend the castle')
assert re.search(r'i18n\.js\?v=2026110[5-9]', index_text), 'i18n.js cache bump'
tt = (root / 'games/tingle-tingle/index.html').read_text(encoding='utf-8')
lacks(tt, 'tingle-tingle', '무료 버전은 광고가 있고', '게임 규칙은 같고', '무료 버전(광고 포함)', 'The free edition has ads',
      'The rules are the same', 'Free edition (contains ads)')
has(tt, 'tingle-tingle', 'Google Play 무료 버전에는 광고가 포함되어 있고, App Store 판의 광고 여부는 확인하지 못했습니다',
    'The Google Play free edition contains ads; whether the App Store build shows ads was not confirmed',
    '기능이 같은지는 이 페이지에서 확인하지 못했습니다', 'this page did not confirm that their features match')

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
        for s in SECTIONS_BY_SLUG.get(slug, SECTIONS[kind]):
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
    assert hrefs.count(f'./{guide}') == HOME_GUIDE_LINKS.get(guide, 1), f'catalog link for {guide}'
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
