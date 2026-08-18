# SEO next steps — kaennakornkarnchang.com

Operational checklist. Everything in "Already done" is deployed and verified live;
the numbered tasks are the ones that need a human with account access.

**Site:** https://kaennakornkarnchang.com (Vercel, deploys from `main`)
**Search Console property:** kaennakornkarnchang.com
**Updated:** 2026-08-18

---

## Already done (no action needed)

- Canonical, Open Graph, Twitter tags and JSON-LD on all 9 pages now point at
  `kaennakornkarnchang.com`. They previously pointed at the old GitHub Pages URL,
  which told Google to index that host instead of this one.
- `sitemap.xml` — 9 URLs, all on the real domain.
- `robots.txt` — points at `https://kaennakornkarnchang.com/sitemap.xml`.
- `google15f34d1c7bfb3e62.html` at the site root for Search Console
  HTML-file verification.
- `LocalBusiness` / `Service` structured data with phone, hours, logo, Facebook,
  LINE and area-served for all 8 provinces.

---

## 1. Resubmit the sitemap

It could not work before: the sitemap listed `ai-deelabs.github.io` URLs, and
Search Console rejects URLs that are outside the property.

1. Open https://search.google.com/search-console
2. Top-left property picker → **kaennakornkarnchang.com**
3. Left menu → **Indexing** → **Sitemaps**
4. If an old sitemap row is listed with an error, click it →  ⋮  → **Remove sitemap**
   (this only removes the submission record, not the file)
5. Under **Add a new sitemap**, type: `sitemap.xml`
6. Click **SUBMIT**

Expected: status **Success**, "9 discovered pages". Status can sit on
"Couldn't fetch" for a few hours before flipping — that is normal, don't resubmit
repeatedly.

---

## 2. Request indexing for the 8 province pages

This is the fastest way to get them re-crawled now that the canonical is correct.

For each URL below:

1. Paste it into the **"Inspect any URL in 'kaennakornkarnchang.com'"** bar at the
   very top of Search Console, press Enter
2. Wait for "Retrieving data from Google index" to finish
3. Click **REQUEST INDEXING** (takes ~30–60 seconds per URL)

```
https://kaennakornkarnchang.com/
https://kaennakornkarnchang.com/chanthaburi/
https://kaennakornkarnchang.com/lopburi/
https://kaennakornkarnchang.com/nonthaburi/
https://kaennakornkarnchang.com/phetchaburi/
https://kaennakornkarnchang.com/pathumthani/
https://kaennakornkarnchang.com/ayutthaya/
https://kaennakornkarnchang.com/kanchanaburi/
https://kaennakornkarnchang.com/samutprakan/
```

The daily quota is roughly 10–12 URLs per property, so all 9 fit in one sitting.

**While you are in there, check one thing.** Expand **Coverage** in the inspection
result and look at the two canonical rows:

- *User-declared canonical* → should be the URL you inspected
- *Google-selected canonical* → should be the same URL

If Google-selected still shows an `ai-deelabs.github.io` URL, Google has not
re-crawled yet. Give it a few days and re-check — the fix is deployed, it just
needs a crawl.

---

## 3. Google Business Profile  ← highest impact

For searches like "ช่างซ่อมหลังคาใกล้ฉัน", the map pack outranks any website.
This will bring in more calls than the whole site will for months. It cannot be
done from the codebase — it needs business verification.

1. Go to https://business.google.com/create
2. **Business name:** แก่นนคร การช่าง
3. **Primary category:** `ผู้รับเหมาก่อสร้าง` (General contractor)
   Then add secondary categories — these matter for which searches you appear in:
   - `ช่างมุงหลังคา` (Roofing contractor)
   - `ช่างประปา` (Plumber)
   - `ผู้รับเหมาปูกระเบื้อง` (Tile contractor)
4. **"Do you want to add a location customers can visit?"** → **No**
   Important: you work at customers' homes, so this is a *service-area business*.
   Adding a shopfront address you don't have gets profiles suspended.
5. **Service areas:** add the provinces you actually cover. Limit is 20 areas.
   Start with the 8 the website has pages for: จันทบุรี, ลพบุรี, นนทบุรี,
   เพชรบุรี, ปทุมธานี, พระนครศรีอยุธยา, กาญจนบุรี, สมุทรปราการ
6. **Phone:** 099-017-7463
7. **Website:** https://kaennakornkarnchang.com
8. **Hours:** จันทร์–เสาร์ 08:00–18:00
9. **Verification:** usually video these days. You record one unbroken clip
   showing your tools/van, then the work in progress, then yourself. Approval
   takes a few days to two weeks.

Once it is live, in priority order:

- **Ask past customers for reviews.** Review count and rating are the single
  biggest local-ranking factor. Ten genuine reviews will move you more than
  anything on the website.
- **Upload photos.** There are already 86 real job photos in `assets/img/` —
  use them. Profiles with photos get materially more calls.
- **Post updates** every week or two (a finished job, a promotion).

---

## 4. Old GitHub Pages copy — tidy-up, not urgent

The same site is still served at
`https://ai-deelabs.github.io/kaennakhon-karnchang-9dc0/`.

This *was* going to be a duplicate-content problem, but it is now largely
defused: that host serves the same fixed files, so it self-canonicalises —

```
github.io/…/lopburi/  →  <link rel="canonical" href="https://kaennakornkarnchang.com/lopburi/">
```

It is telling Google the real version lives on the custom domain. So this is
housekeeping, not a fire. Still worth closing off so there is one live copy:

1. https://github.com/ai-deelabs/kaennakhon-karnchang-9dc0/settings/pages
2. Under **Build and deployment** → **Source**, select **None**
   (newer UI: an **Unpublish site** button next to the live URL)
3. Confirm

The URL then 404s and Google drops it over a few weeks.

---

## What to expect, honestly

- **Brand name** — already working. The site ranks #2 for "แก่นนคร การช่าง",
  behind the Facebook page.
- **Service + province keywords** ("ซ่อมหลังคารั่วลพบุรี") — these are
  competitive commercial terms. The domain is weeks old with no backlinks.
  Realistic window is **2–6 months**, and only with the work below.
- **"…ใกล้ฉัน" searches** — these are won by Google Business Profile, not by
  the website. See task 3.

### What would actually accelerate it

1. Google Business Profile live, with reviews coming in steadily.
2. **Photos tagged by province.** The 8 province pages currently share one photo
   pool because the 86 photos are not labelled by location. Even 5–10 real photos
   per province would make those pages genuinely distinct instead of merely
   adequate — this is the biggest content weakness right now.
3. Real reviews on the province pages (the three on the home page are still
   placeholder text from the original template).
4. Any inbound links — supplier pages, local directories, the Facebook page.

### Do not do this

Do not create a page per ตำบล. `keyword.md` holds ~1,100 location keywords, and
759 near-identical pages is a textbook doorway-page pattern under Google's spam
policy. The 8 province pages carry those keywords as served-area content instead,
which is the safe way to target them.
