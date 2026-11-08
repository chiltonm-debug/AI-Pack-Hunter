# AI Pack Hunter

A mobile-friendly, $0-budget starter web app for tracking Pokémon and One Piece pack opportunities.

## Current features
- Free Pack Finder: add and filter free or promotional opportunities.
- Discover tab: curated official sources plus an automatically refreshed list of possible promotion/reward announcements.
- Opportunity Scanner: search and triage saved entries; it does not crawl the web automatically.
- Pack Tracker: record saved, reviewed, claimed, or expired status.
- Grail Watchlist: track target cards, sets, conditions, and target prices.

## Current safety rules
- Daily spending limit is $0.
- No purchases are made.
- No packs are opened or automated.
- Paid opportunities are blocked from review/approval actions.
- Users must verify offer terms, total cost, eligibility, and platform rules themselves.
- Opportunity and grail data is stored locally in the browser using localStorage.

## Discovery source notes
The Discover tab combines a curated source directory with a daily scheduled discovery workflow. The GitHub Actions workflow searches Google News RSS for Pokémon and One Piece TCG promotion/reward terms, then keeps only results whose publisher metadata matches an allowlisted official domain. It does not crawl publisher pages, log in, claim offers, open packs, or buy anything. Results are candidate leads only; every result is marked for manual verification and its cost remains unknown until checked. Google News indexing is incomplete, so this is a discovery aid rather than a guarantee that every promotion will be found. GitHub Actions scheduled runs may be delayed or disabled by repository inactivity; the workflow can also be run manually from the Actions tab.\n\nThe Discover tab also links to these official sources:
- Pokémon League rewards: https://play.pokemon.com/en-us/rewards/
- Pokémon TCG Live announcements: https://community.pokemon.com/en-us/categories/tcg-live-news-announcements
- One Piece Card Game official site and events: https://en.onepiece-cardgame.com/
- Bandai Namco Amusement America One Piece official shop news: https://shop.bandainamco-am.com/onepiececardgame/

The current Pokémon League Prize Pack lead is a physical promotional reward that may be earned by participating in a local League. Distribution varies and availability is limited. Confirm that the event has no entry fee and that rewards are available before treating it as a $0 offer. No current free One Piece pack offer has been confirmed in the source review.

## Run locally
Open `index.html` in a modern browser. No build tools, API keys, subscriptions, or server are required.

## Publish free with GitHub Pages
1. In this repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose branch `main` and folder `/(root)`, then save.
4. Wait for GitHub Pages to publish the site. The Pages URL appears in Settings → Pages.

GitHub Pages availability and terms depend on repository/account settings. This app is a static prototype, not a production pack-opening bot.

## Next development steps
- Evaluate permitted RSS feeds or official APIs before implementing automated refresh.
- Add source last-checked dates and stale-source warnings.
- Add card checklist and collection tracking.
- Add published pull-rate and card-price references only where their terms permit.
- Keep all future opening actions manual and platform-compliant.
