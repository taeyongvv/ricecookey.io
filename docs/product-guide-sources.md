# Product guide sources

Evidence for `games/last-castle/`, `games/wakbu-ball/` and `games/tingle-tingle/`, checked 2026-10-20.
Store pages win over design docs; game source (read-only) was used only for UI names, controls and rules.
Re-check stores before changing versions, editions or prices. Validate with `python3 scripts/check_product_pages.py`.

## Store listings

| Game | Store | URL | Checked fact |
| --- | --- | --- | --- |
| Last Castle | App Store | https://apps.apple.com/kr/app/id6786145722 | 1.7.3, 2026-10-17, free, iOS 15.0+, 12+, KO/EN/JA/FR/ES; auto attack, 1 of 3 cards per wave, effects list, permanent upgrades, challenge modes |
| Last Castle | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.lastcastle | updated 2026-10-17 (1.7.3 notes), "Contains ads"; 15 heroes, recruit/train, season pass free+premium, six battlefields, Hard/Nightmare, weekly + ranked Endless |
| Last Castle | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0001006556 | listing exists (title only) |
| Wakbu Ball | App Store | https://apps.apple.com/kr/app/id6786132527 | 1.5.1, 2026-08-18, paid, ad-free text, iOS 15.0+, 4+; press/crack/roll, 80-color Dex, textures, ranking, haptics/sound; 1.5.1 notes: plaza nickname, Today's Picks |
| Wakbu Ball | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.wakbuball | updated 2026-08-18, no ads label, "광고 없는 버전", Workshop creation (shape/shell/core/finale/feel) |
| Wakbu Ball | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0001007182 | listing exists (title only) |
| Tingle Tingle (free) | Google Play | https://play.google.com/store/apps/details?id=com.RiceCookey.dongle | updated 2026-07-28, "Contains ads"; v2.2: global ranking, revive, retry interstitial removed, Play Games sign-in |
| Tingle Tingle (free) | App Store | https://apps.apple.com/kr/app/id6796646984 | 1.0, 2026-08-19, free, iOS 15.0+, 4+; tap/swipe to drop, merge, overflow ends, leaderboard. Ad display not confirmed |
| Tingle Tingle (free) | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0000761967 | title "팅글 팅글 - 합치기 게임" |
| Tingle Tingle (ad-free) | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0000763243 | title "팅글 팅글 : 수박게임 (광고제거)" |
| Tingle Tingle (ad-free) | Google Play | https://play.google.com/store/apps/details?id=com.RiceCookey.donglepaid | **404 with hl=ko&gl=KR and hl=en&gl=US** — not linked from the guide; the home catalog link is unchanged pending owner review |

## Claims from game source (read-only, may differ per store build)

- Last Castle (`translations/main.csv`): Tutorial, Castle Upgrade, Codex menus; gold/free/ad reroll and "After reroll" preview; pause menu items and run loss on exit; ad revive at 50% HP once per run; 20-wave clear; Endless unlocks after Stage 1 and gives no diamonds; Hard modifiers; Nightmare after all Hard clears plus one challenge; hero tactics note; card/stage English names.
- Wakbu Ball (`autoloads/Loc.gd`, `docs/specs/03-input-score-audio.md`): hold-still squish vs drag roll with inertia; settings (sound, volume, vibration intensity, Endless Mode, language); free odds-based color collection; tap Dex color; Planet unlock at 80 colors; ranking nickname max 12; Workshop material-first and Test It; Plaza rules agreement and temporary closure message; silent-mode help text.
- Tingle Tingle (`Assets/1.Scripts/GameMgr.cs`, `Dongle.cs`, `BombCtrl.cs`), read at Google Play v2.2 release commit `2acb86a49e65726975299a71f8f56fa880439508` (2026-07-28); local source HEAD is `d14c5e872a4bf571b1555f29be4c456da18fbe1e` (2026-08-20, unreleased): touch-drag-release drop; gray after 2 s over the line, game over after 5 s (unchanged since 2023 code `4bd0bf1`); pause-menu exit skips revive; revive once per game clears only Tingles above the danger line (`clearHeight = line.y` at `2acb86a`), cleared pieces score nothing; bombs (v2.2 `FREE_VERSION`, matches in-game "1 Game = 2 Ads" and App Store screenshot x1→x0): free starts 1 + up to 2 ad bombs per game; best score stored on device and submitted to the leaderboard.
  - Omitted, unreleased: `d14c5e8` changes revive to clear the upper half; it postdates both public builds (Google Play v2.2 2026-07-28, App Store 1.0 2026-08-19).
  - Omitted, unverified: paid-edition starting bomb count (`#else` branch first added in `2acb86a`; no paid build shown released with it).

## Screenshots

Official App Store iPhone screenshots, KR storefront, from `https://itunes.apple.com/lookup?id=<id>&country=kr` `screenshotUrls[n]`, fetched at `540x0w.jpg`. Pixels inspected before captioning. Full URLs and sizes are in `.task/screenshot-manifest.json` (untracked).

| File | App / index | SHA-256 |
| --- | --- | --- |
| assets/games/last-castle/battle.jpg | id6786145722 #0 | 5206a32eacf04675abeac52965e471333bbc87ef2b2d5a181e7ee28f8fb86ea2 |
| assets/games/last-castle/upgrade-cards.jpg | id6786145722 #2 | 2868615bacacbe3d92238b7ad8fa5fc6ad70a97c212d7dfa88998d2c76f357b0 |
| assets/games/last-castle/stage-select.jpg | id6786145722 #8 | 7fffa0ce63d70fcc88b617011739ed6223093b47cf993a15f74f25243692cec9 |
| assets/games/wakbu-ball/main-screen.jpg | id6786132527 #0 | ffe15819cebaa8668cdaf93cdcf740564982ccb083a657841ed70eab4fb1c817 |
| assets/games/wakbu-ball/workshop.jpg | id6786132527 #4 | 7c224c4d24adcb18ae628c00e288273bd87944ab4a52dc14ab1617e7215633c0 |
| assets/games/wakbu-ball/slime-broken-count.jpg | id6786132527 #5 | a578d01404c8ccd70c0a762ffbe2700a953b2f87164cbc578b3b11528cb68207 |
| assets/games/tingle-tingle/merge-score.jpg | id6796646984 #2 | 8b8b5d37584e24538b5a251a7f5a700fada30bab734f198ccca6f1471d04a6b6 |
| assets/games/tingle-tingle/bomb.jpg | id6796646984 #3 | 349296cd59a21488b214a5f4753ab35209c6b9dada622c8368475204797ef438 |
| assets/games/tingle-tingle/how-to-play.jpg | id6796646984 #8 | 6a8c4c43b588175d5d392498cc58ffa09dbbd3b4d6badaf38d8ba00d5c2a41a8 |
