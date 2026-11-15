"""Homepage catalog check (stdlib only): python3 scripts/check_catalog.py

Every card's store links must equal the verified URLs below (source: evidence inventory, 2026-11-15).
Unverified stores are omitted, never rendered as disabled buttons.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

root = Path(__file__).resolve().parents[1]
GP = 'https://play.google.com/store/apps/details?id='
AS = 'https://apps.apple.com/kr/app/id'
ONE = 'https://m.onestore.co.kr/v2/ko-kr/app/'
CATALOG = {  # id -> exact outbound links, in page order
    'lc': [GP + 'com.ricecookey.lastcastle', AS + '6786145722', ONE + '0001006556'],
    'gs': [GP + 'com.ricecookey.gyeomsa', AS + '6805783865'],
    'at': [AS + '6813819414'],
    'gr': [GP + 'com.ricecookey.berritz2048', AS + '6811958719'],
    'cc': [GP + 'com.wajangchang.chakchak', AS + '6821259190'],
    'hl': [GP + 'com.ricecookey.homealllocked', AS + '6819195900'],
    'ai': [GP + 'com.alieninvasion.rpg'],
    'td': ['https://ricecookeytodayis.vercel.app'],
    'dm': [GP + 'com.ricecookey.ductmate', AS + '6816418338'],
    'pp': [GP + 'com.ricecookey.poppop'],
    'fm': [GP + 'com.ricecookey.focusmylady', AS + '6819981098'],
    'pk': [GP + 'com.ricecookey.plantskeeper', 'https://apps.apple.com/kr/app/plants-keeper/id6793824278'],
    'br': [GP + 'com.ricecookey.brrrp', AS + '6793560139'],
    'sw': [GP + 'com.ricecookey.todaysafeweather', AS + '6793529210'],
    'wb': [GP + 'com.ricecookey.wakbuball', AS + '6786132527', ONE + '0001007182'],
    'tt': [GP + 'com.RiceCookey.dongle', AS + '6796646984', ONE + '0000761967', ONE + '0000763243'],
    'bp': [GP + 'com.ricecookey.ricecookey_2048', ONE + '0000761443'],
    'bm': [GP + 'com.dreamy.bangmandarin.google', ONE + '0001000460'],
    'rb': [ONE + '0001000448'],
    'ti': [GP + 'com.ricecookey.puzzle1010i', 'https://apps.apple.com/us/app/brain-puzzle-game-1010i/id6795572711',
           ONE + '0001000954'],
    # Not publicly listed: identity only, no buttons, no status copy.
    'co': [], 'lg': [], 'kh': [], 'rn': [], 'cu': [], 'ml': [],
}
NEW_ART = ('gyeomsa', 'atelier-of-starlight', 'berritz2048', 'chakchak', 'home-all-locked', 'alien-invasion')
PRESERVED = ('./games/last-castle/', './journal/last-castle-builds/', './journal/wakbu-ball-tactile-design/',
             './journal/multistore-catalog/', './privacy/', './rakunovel/privacy/', './rakunovel/terms/',
             './apps/ductmong/', './apps/focus-my-lady/', './apps/plants-keeper/', './apps/brrrp/',
             './apps/today-safe-weather/', './games/today-dungeon/', './games/poppop/', './games/wakbu-ball/',
             './games/tingle-tingle/', './games/beep-2048/', './games/bang-mandarin/', './games/puzzle-1010i/',
             'mailto:ricecookey.official@gmail.com')
PRESERVED_FILES = ('berritz2048/privacy/index.html', 'go/plants/ios/index.html', 'go/gyeomsa/x/aos/index.html',
                   'ads.txt', 'app-ads.txt')
STATUS = re.compile(r'준비중|출시 예정|Coming soon|\bbeta\b|베타|store-link--disabled|preparing|webBeta|betaGuide', re.I)
VERSION = re.compile(r'\b(?:v|ver\.?\s?)?\d+\.\d+(?:\.\d+)?\b')


class Cards(HTMLParser):
    """Collects (id, img src, outbound hrefs) per catalog card (featured article or game-row li)."""
    def __init__(self, text):
        super().__init__()
        self.cards, self.cur, self.depth = [], None, 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get('class', '')
        if self.cur is None and (tag == 'article' and 'game-feature' in cls or tag == 'li' and 'game-row' in cls):
            self.cur, self.depth = {'tag': tag, 'id': None, 'img': None, 'hrefs': []}, 0
        if self.cur is None:
            return
        if tag == self.cur['tag']:
            self.depth += 1
        m = re.fullmatch(r'g-([a-z]+)-title', a.get('id', ''))
        if m:
            self.cur['id'] = m.group(1)
        if tag == 'img' and not self.cur['img']:
            self.cur['img'] = a
        if tag == 'a' and a.get('href', '').startswith('https://'):
            self.cur['hrefs'].append(a['href'])
            assert a.get('target') == '_blank' and set(a.get('rel', '').split()) >= {'noopener', 'noreferrer'}, a

    def handle_endtag(self, tag):
        if self.cur and tag == self.cur['tag']:
            self.depth -= 1
            if self.depth == 0:
                self.cards.append(self.cur)
                self.cur = None


def webp_size(path):
    d = path.read_bytes()
    assert d[:4] == b'RIFF' and d[8:12] == b'WEBP', f'not WebP: {path}'
    if d[12:16] == b'VP8 ':
        return int.from_bytes(d[26:28], 'little') & 0x3fff, int.from_bytes(d[28:30], 'little') & 0x3fff
    if d[12:16] == b'VP8X':
        return int.from_bytes(d[24:27], 'little') + 1, int.from_bytes(d[27:30], 'little') + 1
    raise AssertionError(f'unsupported WebP chunk in {path}')


index = (root / 'index.html').read_text(encoding='utf-8')
i18n = (root / 'i18n.js').read_text(encoding='utf-8')
games = index[index.index('id="games"'):index.index('id="journal"')]

cards = Cards(games).cards
ids = [c['id'] for c in cards]
assert len(ids) == len(set(ids)) == len(CATALOG), f'catalog count {len(ids)} != {len(CATALOG)}'
assert set(ids) == set(CATALOG), set(ids) ^ set(CATALOG)
for c in cards:
    assert c['hrefs'] == CATALOG[c['id']], f"{c['id']}: links {c['hrefs']} != {CATALOG[c['id']]}"
    src = c['img']['src']
    img = root / src.split('?')[0]
    assert img.is_file() and img.stat().st_size > 0, f"{c['id']}: missing image {src}"
    assert c['img'].get('data-i18n-alt') == f"game.{c['id']}.alt", c['id']
for name in NEW_ART:
    assert webp_size(root / f'assets/games/{name}.webp') == (256, 256), name
    assert f'./assets/games/{name}.webp" width="256" height="256"' in games, name

# No per-app status, release or version copy anywhere in the catalog or its translations.
assert not STATUS.search(index) and not STATUS.search(i18n), STATUS.search(index + i18n)
assert not VERSION.search(re.sub(r'<[^>]+>', ' ', games)), VERSION.search(re.sub(r'<[^>]+>', ' ', games))

# KO/EN parity: same keys, every homepage key present, catalog text keys non-empty in both.
ko_block, en_block = i18n.split('\n  en: {')
dicts = [dict(re.findall(r'^\s*"([^"]+)": "((?:[^"\\]|\\.)*)"', b, re.M)) for b in (ko_block, en_block)]
assert dicts[0].keys() == dicts[1].keys(), dicts[0].keys() ^ dicts[1].keys()
for key in re.findall(r'data-i18n(?:-aria|-alt|-html)?="([^"]+)"', index):
    assert all(d.get(key) for d in dicts), f'i18n key missing/empty: {key}'
for cid in CATALOG:
    for part in ('name', 'desc', 'alt'):
        assert all(d.get(f'game.{cid}.{part}') for d in dicts), f'game.{cid}.{part}'

for href in PRESERVED:
    assert f'href="{href}"' in index, f'preserved link missing: {href}'
for rel in PRESERVED_FILES:
    assert (root / rel).is_file(), rel
assert 'i18n.js?v=20261115-title1' in index and 'styles.css?v=20261115-catalog1' in index, 'cache keys'
print(f'PASS: {len(cards)} catalog cards, {sum(map(len, CATALOG.values()))} exact store links, '
      f'{len(NEW_ART)} new 256px WebP icons, no status/version copy, KO/EN parity, preserved links')
