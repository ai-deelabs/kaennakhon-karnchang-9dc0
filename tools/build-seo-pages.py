#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the per-province service-area pages, sitemap.xml and robots.txt.

Run from the repo root:   python3 tools/build-seo-pages.py

Reads data/areas.json. Everything the pages say comes from that file, so editing
the data (or base_url, after pointing a custom domain at the site) and re-running
is the whole update process.
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(io.open(os.path.join(ROOT, "data/areas.json"), encoding="utf-8"))
BASE = DATA["base_url"].rstrip("/")
BIZ = DATA["business"]
PROVINCES = DATA["provinces"]

# Concrete work items per service line, reused from the home page copy.
SERVICE_DETAIL = {
    "ช่างซ่อมประปา": {
        "h": "งานประปา",
        "desc": "รับงานประปาทุกชนิด ตั้งแต่หาจุดรั่วที่มองไม่เห็นไปจนถึงเดินระบบใหม่ทั้งหลัง",
        "items": [
            "ตรวจเช็คน้ำรั่วซึมที่ไม่ทราบสาเหตุ หาให้เจอแล้วแก้ให้จบ",
            "เดินท่อใหม่และเปลี่ยนท่อเก่า ทั้ง PVC, PPR และ PE",
            "ทะลวงท่อตันด้วยงูเหล็กทุกขนาด",
            "วางระบบท่อถังบำบัด (ถังแซ็ก) ให้ระบายได้จริง",
            "ติดตั้งสุขภัณฑ์ ชักโครก อ่างล้างหน้า ก๊อกน้ำ ฝักบัว",
        ],
    },
    "ซ่อมหลังคารั่ว": {
        "h": "งานหลังคาและกันรั่ว",
        "desc": "ซ่อมหลังคารั่วซึมให้จบในรอบเดียว ตรวจทุกจุดก่อนปิดงาน ไม่ใช่แค่อุดผิวหน้า",
        "items": [
            "ซ่อมหลังคารั่ว เปลี่ยนแผ่นหลังคาที่แตกหรือร่อน",
            "ทำโครงหลังคาใหม่ ซ่อมโครงเหล็กที่ผุหรือทรุดตัว",
            "แก้ปัญหาฝนสาด ลมตี น้ำย้อนเข้าฝ้า",
            "ติดตั้งและเปลี่ยนรางน้ำฝน แก้ปัญหาน้ำล้น",
            "ต่อกันสาดและโรงจอดรถ โครงเหล็กหลังคาเมทัลชีท",
        ],
    },
    "รับปูกระเบื้อง": {
        "h": "งานปูกระเบื้องและงานปูน",
        "desc": "ปูกระเบื้องพื้นและผนังทุกชนิด งานเรียบได้แนว ร่องยาแนวสวย ไม่ล่อนไม่โก่ง",
        "items": [
            "ปูกระเบื้องพื้นและผนัง ทั้งแผ่นเล็กและแกรนิตโต้แผ่นใหญ่",
            "เทพื้นคอนกรีต ปรับระดับพื้นให้เรียบ",
            "ฉาบผนัง ซ่อมปูนแตกร่อน",
            "ปูกระเบื้องห้องน้ำพร้อมงานกันซึม",
        ],
    },
}

# Services offered everywhere, listed so each page is not single-service.
ALSO = [
    "รับเหมาต่อเติมบ้าน ครัว ห้องน้ำ", "รับสร้างบ้านและรับเหมาก่อสร้าง",
    "งานเหล็ก กันสาด โรงจอดรถ", "งานฝ้า ระแนง ผนังเบา",
    "เดินไฟภายในบ้าน เพิ่มจุดปลั๊กและไฟส่องสว่าง", "งานทาสีภายใน-ภายนอก",
    "ซ่อมแซมงานบ้านทุกชนิด",
]

# Shared photo pool. These are the crew's own jobs but are NOT tagged by
# province, so pages must not claim they were shot in that province.
PHOTOS = [
    "line_oa_chat_260730_124306.jpg", "line_oa_chat_260730_124328.jpg",
    "line_oa_chat_260730_124516.jpg", "line_oa_chat_260730_124406.jpg",
    "line_oa_chat_260730_124446.jpg", "line_oa_chat_260730_124543.jpg",
]
PHOTO_ALT = [
    "งานมุงหลังคากระเบื้อง", "งานกันสาดโครงเหล็กและโรงจอดรถ",
    "งานปูกระเบื้องพื้นภายในบ้าน", "งานทาสีผนังภายนอกอาคาร",
    "งานวางท่อระบบถังบำบัด", "งานติดตั้งสุขภัณฑ์ในห้องน้ำ",
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_page(p, others):
    th, en, slug = p["th"], p["en"], p["slug"]
    services = p["services"]
    primary = SERVICE_DETAIL[services[0]]
    n_amphoe, n_tambon = len(p["amphoe"]), p["tambon_count"]
    url = f"{BASE}/{slug}/"
    svc_names = " · ".join(services)

    title = f"{services[0]}{th} — {BIZ['name']} โทร {BIZ['phone']}"
    desc = (f"{services[0]}{th} ครอบคลุมทั้ง {n_amphoe} อำเภอ {n_tambon} ตำบล "
            f"ทีมช่างมืออาชีพ ประเมินราคาหน้างานฟรี โทร {BIZ['phone']} ({BIZ['contact_person']})")
    og_img = f"{BASE}/assets/img/web/{p['hero']}"

    # ---- JSON-LD: breadcrumb + service ----
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "หน้าแรก", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": f"{services[0]}{th}", "item": url},
        ],
    }
    service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": f"{services[0]}{th}",
        "serviceType": services,
        "url": url,
        "areaServed": [{"@type": "AdministrativeArea", "name": th}] +
                      [{"@type": "AdministrativeArea", "name": "อำเภอ" + a["name"]}
                       for a in p["amphoe"]],
        "provider": {
            "@type": "HomeAndConstructionBusiness",
            "name": BIZ["name"], "telephone": BIZ["phone_e164"],
            "url": BASE + "/", "logo": BASE + "/assets/logo/logo.png", "image": og_img,
            "sameAs": [BIZ["facebook"], BIZ["line"]],
            "openingHours": BIZ["hours_schema"],
        },
    }

    o = []
    a = o.append
    a('<!DOCTYPE html>')
    a('<html lang="th">')
    a('<head>')
    a('<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    a(f'<title>{esc(title)}</title>')
    a(f'<meta name="description" content="{esc(desc)}">')
    a(f'<link rel="canonical" href="{url}">')
    a('<meta property="og:type" content="website">')
    a(f'<meta property="og:title" content="{esc(title)}">')
    a(f'<meta property="og:description" content="{esc(desc)}">')
    a(f'<meta property="og:url" content="{url}">')
    a(f'<meta property="og:image" content="{og_img}">')
    a('<meta property="og:locale" content="th_TH">')
    a(f'<meta property="og:site_name" content="{esc(BIZ["name"])}">')
    a('<meta name="twitter:card" content="summary_large_image">')
    a(f'<meta name="twitter:title" content="{esc(title)}">')
    a(f'<meta name="twitter:description" content="{esc(desc)}">')
    a(f'<meta name="twitter:image" content="{og_img}">')
    a('<link rel="icon" type="image/png" sizes="32x32" href="../assets/logo/favicon-32.png">')
    a('<link rel="icon" type="image/png" sizes="192x192" href="../assets/logo/favicon-192.png">')
    a('<link rel="icon" type="image/png" sizes="512x512" href="../assets/logo/favicon-512.png">')
    a('<link rel="apple-touch-icon" sizes="180x180" href="../assets/logo/apple-touch-icon.png">')
    a('<meta name="theme-color" content="#e84c1e">')
    a('<link rel="preconnect" href="https://fonts.googleapis.com">')
    a('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    a('<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@400;700;800;900&family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">')
    a('<link rel="stylesheet" href="../assets/css/area.css">')
    a(f'<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>')
    a(f'<script type="application/ld+json">{json.dumps(service_ld, ensure_ascii=False)}</script>')
    a('</head>')
    a('<body>')

    a('<header class="top"><div class="wrap top__inner">')
    a('  <a class="logo" href="../">'
      '<img class="logo__mark" src="../assets/logo/mark-96.png" width="96" height="96" alt="">'
      '<span class="logo__text">แก่นนคร<span>การช่าง</span></span></a>')
    a(f'  <a class="top__cta" href="tel:{BIZ["phone_e164"]}">โทร {BIZ["phone"]}</a>')
    a('</div></header>')

    a('<main class="wrap">')
    a(f'  <nav class="crumb" aria-label="breadcrumb"><a href="../">หน้าแรก</a> › {esc(services[0])}{th}</nav>')

    a('  <div class="hero">')
    a(f'    <img src="../assets/img/web/{p["hero"]}" width="1400" height="1050" fetchpriority="high" alt="ผลงานจริงของทีมช่างแก่นนคร การช่าง">')
    a('    <div class="hero__text">')
    a(f'      <span class="eyebrow">{esc(svc_names)}</span>')
    a(f'      <h1>{esc(services[0])}{th}</h1>')
    a('    </div>')
    a('  </div>')

    a(f'  <p class="lead">แก่นนคร การช่าง รับ{esc(primary["h"])}และงานช่างทุกชนิดใน{th} '
      f'ครอบคลุมทั้ง {n_amphoe} อำเภอ {n_tambon} ตำบล ประเมินราคาหน้างานฟรี '
      f'ไม่มีค่าใช้จ่ายแอบแฝง ติดต่อ {BIZ["contact_person"]} โทร '
      f'<a href="tel:{BIZ["phone_e164"]}">{BIZ["phone"]}</a></p>')

    # services
    a('  <section>')
    a(f'    <h2>บริการหลักใน{th}</h2>')
    a('    <div class="cards">')
    for s in services:
        d = SERVICE_DETAIL[s]
        a('      <div class="card">')
        a(f'        <h3>{esc(s)}{th}</h3>')
        a(f'        <p>{esc(d["desc"])}</p>')
        a('        <ul>')
        for it in d["items"]:
            a(f'          <li>{esc(it)}</li>')
        a('        </ul>')
        a('      </div>')
    a('      <div class="card">')
    a('        <h3>งานอื่นที่รับด้วย</h3>')
    a('        <ul>')
    for it in ALSO:
        a(f'          <li>{esc(it)}</li>')
    a('        </ul>')
    a('      </div>')
    a('    </div>')
    a('  </section>')

    # photos — deliberately not claimed as local
    a('  <section>')
    a('    <h2>ผลงานจริงของทีมเรา</h2>')
    a('    <p class="lead" style="margin-top:0">ภาพหน้างานจริงจากงานที่ทีมเราลงมือทำ '
      f'<a href="../#gallery">ดูผลงานทั้งหมด 86 ภาพ</a></p>')
    a('    <div class="strip">')
    for f, alt in zip(PHOTOS, PHOTO_ALT):
        a(f'      <img src="../assets/img/thumb/{f}" loading="lazy" alt="{esc(alt)}">')
    a('    </div>')
    a('  </section>')

    # served areas — the long-tail payload
    a('  <section>')
    a(f'    <h2>พื้นที่ให้บริการใน{th}</h2>')
    a(f'    <p class="lead" style="margin-top:0">เรารับงานครอบคลุมทั้ง {n_amphoe} อำเภอ '
      f'{n_tambon} ตำบลใน{th}</p>')
    for am in p["amphoe"]:
        a('    <div class="amphoe">')
        a(f'      <h3>อำเภอ{esc(am["name"])}</h3>')
        a('      <ul class="tambon">')
        for t in am["tambon"]:
            a(f'        <li>{esc(t)}</li>')
        a('      </ul>')
        a('    </div>')
    a('  </section>')

    # contact
    a('  <section>')
    a('    <div class="contact">')
    a(f'      <h2>แจ้งงานใน{th} วันนี้</h2>')
    a('      <p>ทักมาคุยงานได้ทุกวัน ประเมินราคาให้ฟรี ไม่มีข้อผูกมัด</p>')
    a(f'      <a class="phone" href="tel:{BIZ["phone_e164"]}">{BIZ["phone"]}</a>')
    a(f'      <div class="sub">{esc(BIZ["contact_person"])} · {esc(BIZ["hours"])}</div>')
    a('      <div class="btns">')
    a(f'        <a class="btn btn--solid" href="tel:{BIZ["phone_e164"]}">โทรติดต่อทีมช่าง</a>')
    a(f'        <a class="btn btn--ghost" href="{BIZ["line"]}" target="_blank" rel="noopener">ทักแชททาง LINE</a>')
    a('      </div>')
    a('    </div>')
    a('  </section>')

    # sibling links
    a('  <section>')
    a('    <h2>พื้นที่ให้บริการอื่น</h2>')
    a('    <ul class="links">')
    for q in others:
        a(f'      <li><a href="../{q["slug"]}/">{q["services"][0]}{q["th"]}</a></li>')
    a('    </ul>')
    a('  </section>')
    a('</main>')

    a('<footer><div class="wrap">')
    a('  <div class="foot-row">')
    a(f'    <a href="tel:{BIZ["phone_e164"]}">{BIZ["phone"]} ({BIZ["contact_person"]})</a>')
    a(f'    <a href="{BIZ["line"]}" target="_blank" rel="noopener">เพิ่มเพื่อนทาง LINE</a>')
    a(f'    <a href="{BIZ["facebook"]}" target="_blank" rel="noopener">Facebook: แก่นนครการช่าง</a>')
    a('    <a href="../">หน้าแรก</a>')
    a('  </div>')
    a('  <div class="foot-bottom">')
    a(f'    <span>© 2569 {esc(BIZ["name"])} · {esc(BIZ["hours"])} · รับงานทุกจังหวัดทั่วประเทศ</span>')
    a('    <a class="deelabs-badge" '
      'href="https://deelabs.co/?utm_source=badge&amp;utm_medium=referral&amp;utm_campaign=kaennakhon-karnchang" '
      'target="_blank" rel="noopener noreferrer">Powered by <b>DeeLabs</b></a>')
    a('  </div>')
    a('</div></footer>')
    a('</body>')
    a('</html>')
    return "\n".join(o) + "\n"


def main():
    written = []
    for p in PROVINCES:
        others = [q for q in PROVINCES if q["slug"] != p["slug"]]
        d = os.path.join(ROOT, p["slug"])
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
        io.open(path, "w", encoding="utf-8").write(build_page(p, others))
        written.append(f'{p["slug"]}/index.html')

    # sitemap
    urls = [BASE + "/"] + [f'{BASE}/{p["slug"]}/' for p in PROVINCES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for i, u in enumerate(urls):
        sm.append("  <url>")
        sm.append(f"    <loc>{u}</loc>")
        sm.append(f"    <priority>{'1.0' if i == 0 else '0.8'}</priority>")
        sm.append("  </url>")
    sm.append("</urlset>")
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

    io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

    print("pages:")
    for w in written:
        print("  " + w)
    print("sitemap.xml (%d urls), robots.txt" % len(urls))


if __name__ == "__main__":
    main()
