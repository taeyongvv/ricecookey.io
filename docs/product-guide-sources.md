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

## Guides added for the full catalog

Ten guides added on 2026-10-20 under `apps/` (utilities) and `games/` (games and the web beta). The full catalog inventory, exclusion reasons and every screenshot's original URL, source index, size and SHA-256 are in `docs/product-guide-inventory.json`; raw fetched listings (Apple lookup KR/US JSON, Google Play hl=ko/gl=KR and hl=en/gl=US HTML, ONE Store HTML, web beta captures) are under `.task/evidence/` (untracked). No app source was read for these guides; every claim comes from public listings, official screenshots or the public web beta UI. iOS and Android editions are described separately where their listings differ.

| Product | Store | URL | Checked fact |
| --- | --- | --- | --- |
| Ductmong | App Store | https://apps.apple.com/kr/app/id6816418338 | 1.1.0, 2026-10-14, free, iOS 16.4+, 4+; KR storefront only (US lookup empty); hood/grill/ERV calcs, fan curve check, suppliers, site records; results after an ad; KRW 4,900/month ad-removal subscription; 1.1.0: ASHRAE comparison, fan first |
| Ductmong | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.ductmate | updated 2026-10-14, "광고 포함", "인앱 구매"; same feature text; app news notifications (My info > Notifications) |
| Plants Keeper | App Store | https://apps.apple.com/kr/app/plants-keeper/id6793824278 | 1.1.0, 2026-09-04, free, iOS 16.0+, 4+; photo species+condition, 5 free questions/day + ads, records, picture diary, discovery records, story care; 1.1.0 notes: asking watering reminders, pests, follow-up check, away checklist |
| Plants Keeper | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.plantskeeper | updated 2026-08-27 (1.0.2 notes), "광고 포함"; Greenhouse community, practice, encyclopedia, optional login, watering reminders, lucky plant |
| Brrrp | App Store | https://apps.apple.com/kr/app/id6793560139 | 1.6, 2026-09-15, free, iOS 26.0+, 4+; AlarmKit, silent/Focus, repeat days, sounds, Tutorial/Masterpiece/K-pop idol challenges, practice, badges, Emergency Exit, on-device; 1.6 fix: mission screen/alarm stopping |
| Brrrp | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.brrrp | updated 2026-09-15, no ads/IAP badge; face-only, silent mode, survives reboot, lock screen, 5 sounds, Tutorial (10) + Masterpiece (10); screenshots also show K-pop idol card |
| Today Safe Weather | App Store | https://apps.apple.com/kr/app/id6793529210 | 1.0.2, 2026-07-29, free, iOS 14.0+; KR storefront only (US lookup empty); same description as Google Play |
| Today Safe Weather | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.todaysafeweather | updated 2026-07-22, "광고 포함"; levels 평상~위험, worse-only alerts, evening forecast, typhoon/rain/wind warnings, 3 places, KMA + AirKorea, no sign-up, default area without location; notes: 시·군·구 search |
| Focus, My Lady | App Store | https://apps.apple.com/kr/app/id6819981098 | 1.0.3, 2026-10-19, free, iOS 15.0+, 4+, KO/EN/JA/ZH; gaze timer, escalating scolding, S~C report, calendar, 25/50/90 min, 3 tutors in text (screenshots show 4), on-device video; 1.0.3: lesson reminders, keep posture or recalibrate |
| Focus, My Lady | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.focusmylady | updated 2026-10-18, "광고 포함", "인앱 구매"; 4 tutors incl. Sir Cedric; Android phones/tablets; recalibrate option |
| PopPop | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.poppop | updated 2026-10-16, "광고 포함", "인앱 구매"; swipe-up draw, hold/auto/fast, same color +1, lucky +2, rainbow, 3 modes, golden card, missions, upgrades, skins, on-device save, coins not cashable, Remove Ads purchase |
| 1010i | App Store | https://apps.apple.com/kr/app/id6795572711 | 3.1.0, 2026-07-30, free, iOS 15.0+, 4+; place blocks, clear rows/columns; 3.1.0: faster clears, vibration toggle, EDIT nickname, English UI, ad continue fixes |
| 1010i | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.puzzle1010i | updated 2026-07-30, "광고 포함"; same text and notes |
| 1010i | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0001000954 | title "두뇌 퍼즐 게임 : 1010i", 100원 |
| Bang Mandarin | Google Play | https://play.google.com/store/apps/details?id=com.dreamy.bangmandarin.google | updated 2026-07-28, "광고 포함"; drag left/right to dodge rain, leaderboard; notes: follow-finger control, ad continue, shield/slow/2x items |
| Bang Mandarin | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0001000460 | title "꽈당, 잘 넘어지는 귤 왕자 : 피하기 게임", 100원 |
| Beep!2048 | Google Play | https://play.google.com/store/apps/details?id=com.ricecookey.ricecookey_2048 | updated 2026-07-28, "광고 포함"; merge same chicks; notes: 5x5/6x6, per-mode ranking with nickname, start screen board choice, fewer interstitials, per-mode best |
| Beep!2048 | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0000761443 | title "삐약 2048" and short intro only |
| Today Dungeon Commute | Web beta | https://ricecookeytodayis.vercel.app/ | played 2026-10-20 in headless Chromium 390x844: title "엔딩 68종 · BETA", 4 races with stat modifiers, auto department, 3-choice scenes with stat previews, race ability standby toggle, 도전장, 사표 낸다, ending collection hints |
| Rabbit 2048 (excluded) | ONE Store | https://m.onestore.co.kr/v2/ko-kr/app/0001000448 | one-line description, 490원, 4x4/game-over/options screenshots only — not enough for a guide |

| File | Source / index | SHA-256 |
| --- | --- | --- |
| assets/games/ductmong/home.jpg | App Store KR iPhone · lookup id=6816418338 country=kr screenshotUrls[0] | 5fcf0b21b51249e192540d299f354772f73035567db108c6c6700292e547213e |
| assets/games/ductmong/hood-airflow.jpg | App Store KR iPhone · lookup id=6816418338 country=kr screenshotUrls[1] | 0aa2a6e10543d461a1ba9684cb602549eeed3a91d11254726a35f528467b32c0 |
| assets/games/ductmong/fan-recommendation.jpg | App Store KR iPhone · lookup id=6816418338 country=kr screenshotUrls[2] | f8ddb60dec09d10064ca3d0ec4ee1766d19879cb8e571b3b77f2f9b0f82ecf2c |
| assets/games/ductmong/line-split.jpg | App Store KR iPhone · lookup id=6816418338 country=kr screenshotUrls[3] | bc8120f0b115db0c241470857794f5e333b88ed3ee6a245ed8d1097536e6d63f |
| assets/games/plants-keeper/home-diagnosis.jpg | App Store KR iPhone · lookup id=6793824278 country=kr screenshotUrls[1] | 9673c712a47ce713d4178c354c05895a13483c5b8ab263aa6eb1367918be502b |
| assets/games/plants-keeper/diagnosis-result.jpg | App Store KR iPhone · lookup id=6793824278 country=kr screenshotUrls[2] | 4534f8fca573d8f27505b8e3c7919f6b431494e962ca8b4aa3f5e80f04c7cf30 |
| assets/games/plants-keeper/my-plants.jpg | App Store KR iPhone · lookup id=6793824278 country=kr screenshotUrls[4] | bb171a13d1e05aae8cc23379ebb87d8295fbe863b2b3e696419317426a4e8ecf |
| assets/games/plants-keeper/care-timeline.jpg | App Store KR iPhone · lookup id=6793824278 country=kr screenshotUrls[3] | f21ec099c146c5065c8bfa5e20e29817dec54f723f12abb6d9de45f9bc6bfbb2 |
| assets/games/brrrp/face-mission.jpg | App Store KR iPhone · lookup id=6793560139 country=kr screenshotUrls[1] | 396fb068aae7d75e1c96d51570b612f89782625e849d16b1d960354382c70d1f |
| assets/games/brrrp/challenges.jpg | App Store KR iPhone · lookup id=6793560139 country=kr screenshotUrls[3] | f242cc89eaaffbefaab8952b56c469cc08660896bff9cbb2d1d30fd3dd5ec0e2 |
| assets/games/brrrp/alarm-list.jpg | App Store KR iPhone · lookup id=6793560139 country=kr screenshotUrls[5] | 09e7d8a2dca06cbb892ffbb9c637f5817918e585a383ad6aa130c20d4d8e7a12 |
| assets/games/brrrp/dashboard.jpg | App Store KR iPhone · lookup id=6793560139 country=kr screenshotUrls[4] | f49d028f56e70ed4ae639d1240d07c6b71b5952948caba3b43745b3029104e3e |
| assets/games/today-safe-weather/main-screen.jpg | Google Play KR · details?id=com.ricecookey.todaysafeweather&hl=ko&gl=KR data-screenshot-index=6 | cec2fa38a788a3cc984127d760843102283598c561da8f803379354bc911bbe9 |
| assets/games/today-safe-weather/action-guide.jpg | Google Play KR · details?id=com.ricecookey.todaysafeweather&hl=ko&gl=KR data-screenshot-index=1 | c8ff1abbd498e4b6a3a44bd74191d2ea3a0b14bb3bd5827d867c71011b50ebbc |
| assets/games/today-safe-weather/location-permission.jpg | Google Play KR · details?id=com.ricecookey.todaysafeweather&hl=ko&gl=KR data-screenshot-index=3 | 02f74d4e896e9dc77c825581500dff0befdec0ebeca377c3022ebce8c8b7eef4 |
| assets/games/today-safe-weather/location-manage.jpg | Google Play KR · details?id=com.ricecookey.todaysafeweather&hl=ko&gl=KR data-screenshot-index=2 | d0c15c99bc9fd0f871c0e407fcdba354cb8eb5ad36f286c4ca3f90fef702c6ed |
| assets/games/focus-my-lady/teacher-watching.jpg | App Store KR iPhone · lookup id=6819981098 country=kr screenshotUrls[1] | bee2ddab225b86f13f64368e9e495c6909a236277e13c2eb9e908f1f16c8f85b |
| assets/games/focus-my-lady/scolding.jpg | App Store KR iPhone · lookup id=6819981098 country=kr screenshotUrls[2] | f36ca0224aa074e2765e3f0f892bd95cc9196ec4ddda46fcc9fb1827aced776a |
| assets/games/focus-my-lady/choose-teacher.jpg | App Store KR iPhone · lookup id=6819981098 country=kr screenshotUrls[3] | 7a57536af613b90eb725e9d21199c5736d75aeb832ed8b2b4cd12feeed03e6f1 |
| assets/games/focus-my-lady/report-card.jpg | App Store KR iPhone · lookup id=6819981098 country=kr screenshotUrls[4] | 91b4906727372c8a40c2116b301a0ce2e59d86e39515e3565bb60f138d6e0ab3 |
| assets/games/poppop/same-color.jpg | Google Play KR · details?id=com.ricecookey.poppop&hl=ko&gl=KR data-screenshot-index=0 | 3ca984154fee5001a5aeed59aa9809ab4ca9a198ac2aca55752cf55ea77d98ce |
| assets/games/poppop/golden-card.jpg | Google Play KR · details?id=com.ricecookey.poppop&hl=ko&gl=KR data-screenshot-index=1 | 20fdefb23d60a92b3d7e712ec91e2ed803b30719f8fd0fbfa168a482593d737c |
| assets/games/poppop/missions.jpg | Google Play KR · details?id=com.ricecookey.poppop&hl=ko&gl=KR data-screenshot-index=4 | 19b10dc01ba6a06dfe2b423aef72dd366db07e84e077b0f10ae13887969156c1 |
| assets/games/poppop/skins.jpg | Google Play KR · details?id=com.ricecookey.poppop&hl=ko&gl=KR data-screenshot-index=5 | 28ff91462ca9f8595d0303b4095c4bb710747c1f8bf1b440669af594f59acb6b |
| assets/games/beep-2048/start-board.jpg | Google Play KR · details?id=com.ricecookey.ricecookey_2048&hl=ko&gl=KR data-screenshot-index=1 | 18a9087b0a1ef760a5a10f313f15762d3ca335389f0ea696c4759ffe592dcd5d |
| assets/games/beep-2048/chick-tiles.jpg | Google Play KR · details?id=com.ricecookey.ricecookey_2048&hl=ko&gl=KR data-screenshot-index=2 | 0bee8b1b0ee6efedc9d6b4cc2fe3ad324529b1392214199710b0a5240aa9b1f3 |
| assets/games/beep-2048/game-over.jpg | Google Play KR · details?id=com.ricecookey.ricecookey_2048&hl=ko&gl=KR data-screenshot-index=3 | 652b381b33863582becd0eeae3110e8fff192fda58fffd28244963db97b933a0 |
| assets/games/beep-2048/leaderboard.jpg | Google Play KR · details?id=com.ricecookey.ricecookey_2048&hl=ko&gl=KR data-screenshot-index=5 | 1373ecb01738f038625dbb942ced96149db7472bf38244c458d9d4921ac58673 |
| assets/games/bang-mandarin/dodge-rain.jpg | Google Play KR · details?id=com.dreamy.bangmandarin.google&hl=ko&gl=KR data-screenshot-index=3 | cc4d300df6e682cdf2aa4a5c5d1aadd5ed2a065c559ba0944a037da1b38218c0 |
| assets/games/bang-mandarin/menu.jpg | Google Play KR · details?id=com.dreamy.bangmandarin.google&hl=ko&gl=KR data-screenshot-index=4 | 5a4b912244c7cbb3bb6964390b3ee4ad1bf191d686b8035d71417edf57c0a366 |
| assets/games/bang-mandarin/ranking.jpg | Google Play KR · details?id=com.dreamy.bangmandarin.google&hl=ko&gl=KR data-screenshot-index=5 | b8c7ac1cb80f23a43ef130ca36d14d3ce53e2dd730f1a1388c0d43620ae11407 |
| assets/games/puzzle-1010i/title.jpg | App Store KR iPhone · lookup id=6795572711 country=kr screenshotUrls[0] | 703140e5ed25f3e857c7ad343b637f5c5afb855d18a28f0b1da2836ffd1188e9 |
| assets/games/puzzle-1010i/board.jpg | App Store KR iPhone · lookup id=6795572711 country=kr screenshotUrls[1] | a39a85f3b53d43cd5583671810ae64966c85d8955c6a2d541067d2d4d8b2e421 |
| assets/games/puzzle-1010i/pause.jpg | App Store KR iPhone · lookup id=6795572711 country=kr screenshotUrls[2] | 5f4b735c9caf4a0463ad5fb82c102176e43337dd0c773c468373638a41de1e98 |
| assets/games/today-dungeon/title.jpg | Public web beta (own capture, Chromium 390x844 DPR3, 2026-10-20) · title.png | 045dd8210f6f2370f97666a74b3540d5133f9d5103f3fe228203258765b947e3 |
| assets/games/today-dungeon/week-event.jpg | Public web beta (own capture, Chromium 390x844 DPR3, 2026-10-20) · week1-event.png | e83af8e519ca648ca5a220762ef7b17c86a8d75a3ad1986e7356c799565f42fc |
| assets/games/today-dungeon/ending-dex.jpg | Public web beta (own capture, Chromium 390x844 DPR3, 2026-10-20) · ending-dex.png | f0e15675bbbf341533688bcc2afee9a9cdd329de2acbc7138153317d5891526e |
