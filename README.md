[![make.fun · post-x-promote-make-your-own-bounty-01](https://make.fun/badge/post-x-promote-make-your-own-bounty-01.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01?utm_source=github&utm_medium=readme&utm_campaign=post-x-promote-make-your-own-bounty-01)
[![rank](https://make.fun/badge/post-x-promote-make-your-own-bounty-01/romdhoncom/post-x-promote-make-your-own-bounty-01/rank.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-x-promote-make-your-own-bounty-01)
[![reward](https://make.fun/badge/post-x-promote-make-your-own-bounty-01/romdhoncom/post-x-promote-make-your-own-bounty-01/reward.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01?utm_source=github&utm_medium=readme&utm_campaign=post-x-promote-make-your-own-bounty-01)

# post-x-promote-make-your-own-bounty-01

An entry for make.fun's bounty "Promote make.fun's make-your-own-bounty post on X": one post of my own on X that quotes make.fun's post (https://x.com/makefunai/status/2124915864336236646), with a photo of its own attached (photo.png) and make.fun, the @makefunai tag and my play code in its text. Places go by the post's score — replies + reposts + quotes — and the top 50 share $250.

## The post

The exact text is in POST_TEXT.md: 224 characters raw, 219 as X counts it (one link counts 23). It is posted from @pijantung51112 as a quote of make.fun's post, with photo.png attached. The photo is an original illustration drawn by make_photo.py (pure Python standard library, no PIL): a bounty board under a dusk sky, "Make your own bounty" in big letters, three pinned bounty cards and gold coins. No logo of any kind is drawn; the name make.fun appears only as plain text.

## The program

main.ts copies POST.json from the repository root to /output/POST.json — that is all it has to do. POST.json holds the post's address once it is posted; until then it holds the placeholder.

Run it locally:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
