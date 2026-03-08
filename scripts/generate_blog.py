#!/usr/bin/env python3
"""
PhysioVisit Automatische Blog Generator
========================================
Genereert en publiceert automatisch blogartikelen voor physiovisit.be

Gebruik: BLOG_TYPE=kinesitherapie python scripts/generate_blog.py
         BLOG_TYPE=kinetec python scripts/generate_blog.py
"""

import os
import sys
import json
import re
import datetime
import requests
from pathlib import Path
import anthropic

# ─── Padconfiguratie ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SITE_ROOT = SCRIPT_DIR.parent / "physiovisit_new_site"
BLOG_DIR = SITE_ROOT / "blog"
IMG_DIR = SITE_ROOT / "assets" / "img"
TOPICS_FILE = SCRIPT_DIR / "published_topics.json"

# ─── API-configuratie ─────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

# ─── Instellingen ─────────────────────────────────────────────────────────────
BLOG_TYPE = os.environ.get("BLOG_TYPE", "kinesitherapie")
BASE_URL = "https://www.physiovisit.be"

# Nederlandse maandnamen
DUTCH_MONTHS = {
    "January": "januari", "February": "februari", "March": "maart",
    "April": "april", "May": "mei", "June": "juni",
    "July": "juli", "August": "augustus", "September": "september",
    "October": "oktober", "November": "november", "December": "december",
}


# ─── Topic-tracking ──────────────────────────────────────────────────────────

def load_published_topics() -> dict:
    """Laad lijst van reeds gepubliceerde onderwerpen."""
    if TOPICS_FILE.exists():
        with open(TOPICS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"kinesitherapie": [], "kinetec": []}


def save_published_topics(topics: dict) -> None:
    """Sla bijgewerkte onderwerpenlijst op."""
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)


def get_existing_blog_titles() -> list:
    """Haal titels van bestaande blogartikelen op om herhaling te voorkomen."""
    titles = []
    for html_file in sorted(BLOG_DIR.glob("*.html")):
        if html_file.name == "index.html":
            continue
        content = html_file.read_text(encoding="utf-8")
        match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        if match:
            title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            if title:
                titles.append(title)
    return titles


# ─── Content generatie ───────────────────────────────────────────────────────

def generate_blog_content(blog_type: str, existing_titles: list) -> dict:
    """Genereer bloginhoud via Claude API."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    today = datetime.date.today()

    if blog_type == "kinesitherapie":
        topic_context = """
        Dienst: Kinesitherapie aan huis
        Praktijk: PhysioVisit, Grimbergen en omgeving (Strombeek-Bever, Humbeek, Beigem, Koningslo)
        Kinesitherapeuten: Timothy Assi en Charlotte
        Specialisaties: orthopedie, neurologie, gangrevalidatie, post-operatief herstel

        Mogelijke invalshoeken (kies een originele die NIET al behandeld is):
        - Specifieke aandoeningen thuis behandelen (CVA, Parkinson, MS, COPD, artritis)
        - Specifieke patiëntgroepen (ouderen, post-chirurgie, chronische pijn, zwangere vrouwen)
        - Specifieke behandelingen thuis (manuele therapie, oefentherapie, electrotherapie, ademhalingsoefeningen)
        - Praktische aspecten (terugbetaling ziekenfonds, doorverwijzing huisarts, eerste afspraak)
        - Seizoensgebonden onderwerpen (wintervallen ouderen, zomeractiviteiten met beperkingen)
        - Preventieve kinesitherapie aan huis
        - Balans- en valpreventie bij senioren
        - Revalidatie na beroerte aan huis
        - Kinesitherapie bij chronische rugpijn thuis
        - Ademhalingsrevalidatie thuis (COPD, post-COVID)
        - Kinesitherapie na heupfractuur
        - Thuisrevalidatie bij gewrichtsproblemen (artrose, reumatoïde artritis)
        - Oedeembehandeling en lymfedrainage aan huis
        - Neurologische revalidatie thuis
        - Kinesitherapie voor kinderen thuis
        """
        badge_category = "Kinesitherapie aan Huis"
        badge_color = "#D4A373"
        image_search_hint = "physiotherapy home visit patient treatment Belgium"
    else:
        topic_context = """
        Dienst: Kinetec CPM machine verhuur en gebruik
        Bedrijf: PhysioVisit verhuurt Kinetec CPM-machines in heel België
        Product: Kinetec Continuous Passive Motion (CPM) machines voor knie en heup

        Mogelijke invalshoeken (kies een originele die NIET al behandeld is):
        - Kinetec na specifieke ingrepen (kruisband, meniscus, knieprothese, heupprothese)
        - Hoe werkt een Kinetec machine precies? (technische uitleg)
        - CPM-therapie protocollen en behandelduur
        - Kinetec instellen en gebruiken stap voor stap
        - Kinetec vs traditionele oefeningen: wanneer welke?
        - Kinetec bij zwelling en stijfheid na knieoperatie
        - Kinetec huren vs kopen: kosten en voordelen
        - Terugbetaling Kinetec via ziekenfonds in België
        - Kinetec bij artroscopie knieherstel
        - Nachtelijk gebruik van Kinetec: tips en richtlijnen
        - Kinetec bij complicaties na knieoperatie
        - Combinatie van Kinetec en kinesitherapie
        - Kinetec voor heupoperatie (heupprothese, heupfractuur)
        - Kinetec bij pediatrische patiënten (kinderen na knieoperatie)
        - Veiligheid en contra-indicaties van CPM-therapie
        - Kinetec en zwelling: hoe omgaan met oedeem?
        - Kinetec levering en installatie thuis
        """
        badge_category = "Kinetec & CPM Therapie"
        badge_color = "#6D8299"
        image_search_hint = "CPM machine knee rehabilitation home physiotherapy equipment"

    existing_str = (
        "\n".join(f"- {t}" for t in existing_titles)
        if existing_titles
        else "Geen bestaande artikelen"
    )

    prompt = f"""Je bent een SEO-expert en ervaren kinesitherapeut die blogartikelen schrijft voor PhysioVisit, een kinesitherapiepraktijk in Grimbergen, België.

CONTEXT OVER DE PRAKTIJK:
{topic_context}

REEDS GEPUBLICEERDE BLOGARTIKELEN (vermijd deze onderwerpen volledig):
{existing_str}

DATUM VANDAAG: {today.strftime('%d %B %Y')}

SCHRIJFINSTRUCTIES:
1. Schrijf een NIEUW en UNIEK blogartikel in vloeiend Nederlands (Belgisch-Nederlands)
2. Het onderwerp moet VOLLEDIG ANDERS zijn dan de bestaande artikelen
3. Optimaliseer voor Belgische SEO (gebruik Belgische zoektermen, "kinesitherapeut" i.p.v. "fysiotherapeut")
4. Schrijf professioneel maar toegankelijk voor patiënten en hun familie (doelgroep 35-75 jaar)
5. Doellengte: 900-1200 woorden voor de hoofdinhoud
6. Gebruik een duidelijke H2/H3 structuur met minimaal 4 secties
7. Voeg 3 FAQ-vragen toe die patiënten echt stellen
8. Eindig met een sterke conclusie en call-to-action naar PhysioVisit
9. Verwerk concrete tips en praktische informatie
10. Gebruik Bootstrap HTML-elementen (alert, card, blockquote, lists) voor visuele variatie

SEO-EISEN:
- Primair zoekwoord: verwerk in H1, eerste paragraaf en 2-3 subkoppen
- Secundaire zoekwoorden: gebruik naturally in de tekst
- Interne links: verwijs naar physiovisit.be pagina's waar relevant
- Lokaal SEO: vermeld Grimbergen, Strombeek-Bever of regio Brussels Hoofdstedelijk Gewest waar passend

Genereer een JSON response in EXACT dit formaat (ALLEEN JSON, geen andere tekst):
{{
  "title": "Volledige SEO-vriendelijke artikel titel (max 60 tekens)",
  "seo_title": "Volledige titel | PhysioVisit Blog",
  "slug": "url-vriendelijke-slug-met-koppeltekens-zonder-accenten",
  "meta_description": "SEO meta beschrijving van exact 150-160 tekens met primair zoekwoord",
  "keywords": "zoekwoord1, zoekwoord2, zoekwoord3, zoekwoord4, zoekwoord5, zoekwoord6",
  "h1_title": "H1 paginatitel (mag iets uitgebreider zijn dan SEO titel)",
  "hero_subtitle": "Ondertitel voor hero sectie: 1 pakkende zin die bezoeker aantrekt",
  "read_time": 7,
  "badge_category": "{badge_category}",
  "badge_color": "{badge_color}",
  "excerpt": "Korte samenvatting voor blog-overzichtspagina (2-3 zinnen, max 150 tekens)",
  "intro": "Boeiende introductie (2-3 zinnen) die de lezer direct aanspreekt en het probleem erkent",
  "sections": [
    {{
      "h2": "Eerste hoofdsectie titel",
      "content_html": "<p>Volledige HTML content met <strong>vetgedrukte</strong> termen, <ul><li>lijstitems</li></ul>, etc.</p>",
      "subsections": [
        {{
          "h3": "Subsectie titel (optioneel)",
          "content_html": "<p>HTML content voor subsectie</p>"
        }}
      ]
    }},
    {{
      "h2": "Tweede hoofdsectie titel",
      "content_html": "<p>Content...</p><div class=\\"alert alert-info\\"><h5><i class=\\"bi bi-info-circle me-2\\"></i>Tip</h5><p class=\\"mb-0\\">Praktische tip...</p></div>",
      "subsections": []
    }},
    {{
      "h2": "Derde hoofdsectie titel",
      "content_html": "<div class=\\"row\\"><div class=\\"col-md-6\\"><h4>Voordeel A</h4><ul><li>Punt 1</li></ul></div><div class=\\"col-md-6\\"><h4>Voordeel B</h4><ul><li>Punt 1</li></ul></div></div>",
      "subsections": []
    }},
    {{
      "h2": "Vierde sectie titel",
      "content_html": "<p>Content...</p>",
      "subsections": []
    }}
  ],
  "faq": [
    {{
      "question": "Eerste veelgestelde vraag van patiënten?",
      "answer": "Uitgebreid en behulpzaam antwoord (3-5 zinnen) met concrete informatie."
    }},
    {{
      "question": "Tweede veelgestelde vraag?",
      "answer": "Uitgebreid antwoord."
    }},
    {{
      "question": "Derde veelgestelde vraag?",
      "answer": "Uitgebreid antwoord met vermelding van PhysioVisit indien relevant."
    }}
  ],
  "conclusion": "<p>Conclusie die de belangrijkste punten samenvat en afsluit met een motiverende call-to-action. Verwijs naar PhysioVisit voor persoonlijk advies en afspraken.</p>",
  "image_search_query": "{image_search_hint} professional",
  "image_alt": "Beschrijvende alt tekst voor de afbeelding in het Nederlands"
}}"""

    print("Verbinding maken met Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Verwijder mogelijke markdown code blocks
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    return json.loads(raw)


# ─── Afbeelding ophalen ───────────────────────────────────────────────────────

def search_and_download_image(query: str, slug: str, blog_type: str) -> str:
    """
    Zoek een afbeelding via Google Custom Search API en download deze.
    Valt terug op bestaande websiteafbeeldingen als API niet beschikbaar is.
    """
    fallback = {
        "kinesitherapie": "Kineaanhuis.jpeg",
        "kinetec": "Kinetec.jpeg",
    }

    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Google API-sleutels niet geconfigureerd → gebruik standaardafbeelding")
        return fallback.get(blog_type, "Kineaanhuis.jpeg")

    try:
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "searchType": "image",
            "q": query,
            "num": 5,
            "imgType": "photo",
            "imgSize": "xlarge",
            "safe": "active",
        }
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params,
            timeout=15,
        )
        data = resp.json()

        if "items" not in data or not data["items"]:
            print(f"Geen afbeeldingen gevonden voor: {query}")
            return fallback.get(blog_type, "Kineaanhuis.jpeg")

        # Probeer de eerste bruikbare afbeelding te downloaden
        for item in data["items"]:
            image_url = item.get("link", "")
            if not image_url:
                continue

            ext = ".jpg"
            if ".png" in image_url.lower():
                ext = ".png"
            elif ".webp" in image_url.lower():
                ext = ".webp"

            safe_slug = re.sub(r'[^a-z0-9-]', '', slug[:30])
            filename = f"blog-auto-{safe_slug}{ext}"
            filepath = IMG_DIR / filename

            try:
                headers = {"User-Agent": "Mozilla/5.0 (PhysioVisit Blog Bot/1.0)"}
                img_resp = requests.get(image_url, headers=headers, timeout=20, stream=True)
                img_resp.raise_for_status()

                # Controleer of het echt een afbeelding is (minimaal 10 KB)
                content_length = int(img_resp.headers.get("content-length", 0))
                if content_length and content_length < 10_000:
                    continue

                with open(filepath, "wb") as f:
                    downloaded = 0
                    for chunk in img_resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                    if downloaded < 10_000:
                        filepath.unlink(missing_ok=True)
                        continue

                print(f"Afbeelding gedownload: {filename} ({downloaded // 1024} KB)")
                return filename

            except Exception as e:
                print(f"Download mislukt voor {image_url}: {e}")
                continue

        print("Alle afbeeldingsdownloads mislukt → gebruik standaardafbeelding")
        return fallback.get(blog_type, "Kineaanhuis.jpeg")

    except Exception as e:
        print(f"Afbeeldingszoekfout: {e} → gebruik standaardafbeelding")
        return fallback.get(blog_type, "Kineaanhuis.jpeg")


# ─── HTML generatie ──────────────────────────────────────────────────────────

def format_date_dutch(date: datetime.date) -> str:
    """Formatteer datum in Nederlands."""
    date_str = date.strftime("%-d %B %Y")
    for eng, nl in DUTCH_MONTHS.items():
        date_str = date_str.replace(eng, nl)
    return date_str


def generate_sections_html(sections: list) -> str:
    """Genereer HTML voor alle secties."""
    html = ""
    for section in sections:
        html += f'\n                    <h2>{section["h2"]}</h2>\n'
        html += f'\n                    {section.get("content_html", "")}\n'
        for sub in section.get("subsections", []):
            html += f'\n                    <h3>{sub["h3"]}</h3>\n'
            html += f'\n                    {sub.get("content_html", "")}\n'
    return html


def generate_faq_html(faq_items: list) -> str:
    """Genereer HTML voor FAQ accordion."""
    html = ""
    for i, faq in enumerate(faq_items):
        show_class = "show" if i == 0 else ""
        collapsed_class = "" if i == 0 else " collapsed"
        html += f"""                            <div class="accordion-item">
                                <h3 class="accordion-header" id="faq{i + 1}">
                                    <button class="accordion-button{collapsed_class}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{i + 1}">
                                        {faq['question']}
                                    </button>
                                </h3>
                                <div id="collapse{i + 1}" class="accordion-collapse collapse {show_class}" data-bs-parent="#faqAccordion">
                                    <div class="accordion-body">
                                        {faq['answer']}
                                    </div>
                                </div>
                            </div>\n"""
    return html


def generate_faq_jsonld(faq_items: list) -> str:
    """Genereer FAQ JSON-LD structured data."""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
            }
            for faq in faq_items
        ],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def generate_blog_html(content: dict, image_filename: str, blog_type: str) -> str:
    """Genereer volledige HTML voor het blogartikel."""
    today = datetime.date.today()
    date_iso = today.strftime("%Y-%m-%d")
    date_display = format_date_dutch(today)

    img_path = f"../assets/img/{image_filename}"
    img_url = f"{BASE_URL}/assets/img/{image_filename}"
    article_url = f"{BASE_URL}/blog/{content['slug']}.html"

    sections_html = generate_sections_html(content.get("sections", []))
    faq_items = content.get("faq", [])
    faq_html = generate_faq_html(faq_items)
    faq_jsonld = generate_faq_jsonld(faq_items)

    # CTA op basis van blogtype
    if blog_type == "kinesitherapie":
        cta_title = "Kinesitherapie aan Huis Aanvragen?"
        cta_body = (
            "Onze ervaren kinesitherapeuten Timothy en Charlotte komen bij u thuis "
            "in Grimbergen en omgeving. Persoonlijke, professionele begeleiding."
        )
        cta_link = "../contact.html"
        cta_btn = "Maak een Afspraak"
        cta_icon = "bi-calendar-plus"
    else:
        cta_title = "Kinetec Machine Huren?"
        cta_body = (
            "PhysioVisit levert en installeert uw Kinetec CPM-machine thuis in heel België. "
            "Inclusief uitleg en begeleiding van onze kinesitherapeuten."
        )
        cta_link = "../kinetec-huren.html"
        cta_btn = "Kinetec Huren"
        cta_icon = "bi-box-seam"

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-620935990"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'AW-620935990');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <title>{content['seo_title']}</title>
    <meta name="description" content="{content['meta_description']}">
    <link rel="canonical" href="{article_url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{content['seo_title']}">
    <meta property="og:description" content="{content['meta_description']}">
    <meta property="og:url" content="{article_url}">
    <meta property="og:image" content="{img_url}">
    <meta property="og:locale" content="nl_BE">
    <meta property="og:site_name" content="PhysioVisit">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{content['seo_title']}">
    <meta name="twitter:description" content="{content['meta_description']}">
    <meta name="twitter:image" content="{img_url}">
    <meta name="keywords" content="{content['keywords']}">
    <meta name="author" content="PhysioVisit">

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="../styles.min.css?v=3">

    <!-- Structured Data: BlogPosting -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{content['h1_title']}",
      "description": "{content['meta_description']}",
      "image": "{img_url}",
      "author": {{
        "@type": "Organization",
        "name": "PhysioVisit"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "PhysioVisit",
        "logo": {{
          "@type": "ImageObject",
          "url": "{BASE_URL}/assets/img/physiovisit logo.png"
        }}
      }},
      "datePublished": "{date_iso}",
      "dateModified": "{date_iso}",
      "mainEntityOfPage": "{article_url}"
    }}
    </script>

    <!-- Structured Data: Breadcrumb -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "@id": "{article_url}#breadcrumb",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{BASE_URL}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "{BASE_URL}/blog/"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{content['title']}",
          "item": "{article_url}"
        }}
      ]
    }}
    </script>

    <!-- Structured Data: FAQ -->
    <script type="application/ld+json">
{faq_jsonld}
    </script>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-custom sticky-top">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="../index.html">
                <img src="../assets/img/physiovisit logo.png" alt="PhysioVisit Logo" width="45" height="45" class="me-2">
                <span>PhysioVisit</span>
            </a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="../index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../kinesitherapie.html">Kinesitherapie aan Huis</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="hurenDropdown" role="button" data-bs-toggle="dropdown">
                            Huren
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="../kinetec-huren.html">Kinetec Huren</a></li>
                            <li><a class="dropdown-item" href="../hometrainer-huren.html">Hometrainer Huren</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../ons-team.html">Ons Team</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../blog/">Blog</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../contact.html">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section py-5" style="background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.65)), url('{img_path}') center/cover no-repeat, linear-gradient(135deg, #6D8299, #D4A373); color: white;">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8">
                    <nav aria-label="breadcrumb" class="mb-3">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="../index.html" class="text-white">Home</a></li>
                            <li class="breadcrumb-item"><a href="../blog/" class="text-white">Blog</a></li>
                            <li class="breadcrumb-item active text-white">{content['title']}</li>
                        </ol>
                    </nav>
                    <h1 class="display-4 mb-3" style="color: #fff !important;">{content['h1_title']}</h1>
                    <p class="lead" style="color: rgba(255,255,255,0.95) !important;">{content['hero_subtitle']}</p>
                    <div class="d-flex align-items-center mt-4">
                        <i class="bi bi-calendar me-2"></i>
                        <span>{date_display}</span>
                        <span class="mx-3">|</span>
                        <i class="bi bi-clock me-2"></i>
                        <span>{content['read_time']} min leestijd</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Hoofdinhoud -->
    <article class="container py-5">
        <div class="row">
            <div class="col-lg-8">
                <div class="blog-content">
                    <p class="lead">{content['intro']}</p>
{sections_html}
                    <!-- FAQ Sectie -->
                    <div class="mt-5">
                        <h2>Veelgestelde Vragen</h2>

                        <div class="accordion" id="faqAccordion">
{faq_html}
                        </div>
                    </div>

                    <!-- CTA Sectie -->
                    <div class="text-white p-4 rounded my-5" style="background-color: #6D8299;">
                        <div class="row align-items-center">
                            <div class="col-lg-8">
                                <h3>{cta_title}</h3>
                                <p class="mb-0">{cta_body}</p>
                            </div>
                            <div class="col-lg-4 text-lg-end">
                                <a href="{cta_link}" class="btn btn-light btn-lg">
                                    <i class="bi {cta_icon} me-2"></i>{cta_btn}
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- Conclusie -->
                    <h2>Conclusie</h2>
                    {content['conclusion']}

                    <!-- Gerelateerde artikelen -->
                    <div class="mt-5">
                        <h3>Gerelateerde Artikelen</h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Kinesitherapie aan Huis</h5>
                                        <p class="card-text">Professionele thuisbehandeling in Grimbergen en omgeving</p>
                                        <a href="../kinesitherapie.html" class="btn btn-outline-primary btn-sm">Meer info</a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Kinetec CPM Machine Huren</h5>
                                        <p class="card-text">Kinetec revalidatiemachines aan huis in heel België</p>
                                        <a href="../kinetec-huren.html" class="btn btn-outline-primary btn-sm">Meer info</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Zijbalk -->
            <div class="col-lg-4">
                <div class="blog-sidebar">
                    <!-- Contact Widget -->
                    <div class="widget bg-light p-4 rounded mb-4">
                        <h5>Direct Contact</h5>
                        <div class="d-flex align-items-center mb-3">
                            <i class="bi bi-telephone text-primary me-3"></i>
                            <div>
                                <strong>0474 87 80 21</strong><br>
                                <small>Ma-Vr 9:00-17:00</small>
                            </div>
                        </div>
                        <div class="d-flex align-items-center mb-3">
                            <i class="bi bi-envelope text-primary me-3"></i>
                            <div>
                                <strong>info@physiovisit.be</strong><br>
                                <small>Binnen 24u reactie</small>
                            </div>
                        </div>
                        <a href="../contact.html" class="btn btn-primary w-100">
                            <i class="bi bi-calendar-plus me-2"></i>Online Afspraak
                        </a>
                    </div>

                    <!-- Diensten Widget -->
                    <div class="widget bg-light p-4 rounded mb-4">
                        <h5>Onze Diensten</h5>
                        <ul class="list-unstyled">
                            <li class="mb-2">
                                <a href="../kinesitherapie/orthopedie.html" class="text-decoration-none">
                                    <i class="bi bi-arrow-right text-primary me-2"></i>Orthopedische Revalidatie
                                </a>
                            </li>
                            <li class="mb-2">
                                <a href="../kinesitherapie/neurologie.html" class="text-decoration-none">
                                    <i class="bi bi-arrow-right text-primary me-2"></i>Neurologie Kinesitherapie
                                </a>
                            </li>
                            <li class="mb-2">
                                <a href="../kinesitherapie/gangrevalidatie.html" class="text-decoration-none">
                                    <i class="bi bi-arrow-right text-primary me-2"></i>Gangrevalidatie
                                </a>
                            </li>
                            <li class="mb-2">
                                <a href="../kinetec-huren.html" class="text-decoration-none">
                                    <i class="bi bi-arrow-right text-primary me-2"></i>Kinetec Huren
                                </a>
                            </li>
                            <li class="mb-2">
                                <a href="../hometrainer-huren.html" class="text-decoration-none">
                                    <i class="bi bi-arrow-right text-primary me-2"></i>Hometrainer Verhuur
                                </a>
                            </li>
                        </ul>
                    </div>

                    <!-- Reviews Widget -->
                    <div class="widget text-white p-4 rounded" style="background-color: #6D8299;">
                        <h5>Patiënt Ervaringen</h5>
                        <div class="text-center mb-3">
                            <span class="fs-2">⭐⭐⭐⭐⭐</span>
                            <div><strong>5.0/5</strong> op Google Reviews</div>
                        </div>
                        <p class="small">"Timothy en Charlotte zijn echte professionals. Warme begeleiding en uitstekende resultaten."</p>
                        <a href="https://g.page/physiovisit" target="_blank" class="btn btn-light btn-sm">
                            <i class="bi bi-google"></i> Alle Reviews
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="footer-custom">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <h5>PhysioVisit</h5>
                    <p>Professionele kinesitherapie aan huis en verhuur van revalidatieapparatuur in de regio Grimbergen.</p>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h5>Onze Diensten</h5>
                    <ul class="list-unstyled">
                        <li><a href="../kinesitherapie.html">Orthopedie</a></li>
                        <li><a href="../kinesitherapie.html">Neurologie</a></li>
                        <li><a href="../kinesitherapie.html">Gangrevalidatie</a></li>
                        <li><a href="../kinetec-huren.html">Kinetec Verhuur</a></li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h5>Service Gebieden</h5>
                    <ul class="list-unstyled">
                        <li>Grimbergen</li>
                        <li>Strombeek-Bever</li>
                        <li>Humbeek, Beigem, Koningslo</li>
                        <li><strong>Verhuur:</strong> Heel België</li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6">
                    <h5>Contact</h5>
                    <ul class="list-unstyled">
                        <li><i class="bi bi-telephone me-2"></i>0474 87 80 21</li>
                        <li><i class="bi bi-envelope me-2"></i>info@physiovisit.be</li>
                        <li><i class="bi bi-clock me-2"></i>Ma-Vr: 9:00 - 17:00</li>
                    </ul>
                </div>
            </div>

            <hr class="my-4 border-secondary">
            <div class="text-center">
                <p class="mb-0">&copy; 2025 PhysioVisit. Alle rechten voorbehouden.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/assets/js/gads-tracking.js" defer></script>
</body>
</html>"""
    return html


# ─── Blog index bijwerken ────────────────────────────────────────────────────

def update_blog_index(content: dict, image_filename: str) -> None:
    """Voeg nieuwe artikelkaart toe aan blog/index.html."""
    index_path = BLOG_DIR / "index.html"
    index_html = index_path.read_text(encoding="utf-8")

    badge_color = content.get("badge_color", "#6D8299")
    badge_category = content.get("badge_category", "Kinesitherapie")

    new_card = f"""
                        <!-- Auto-gepubliceerd: {datetime.date.today().isoformat()} -->
                        <div class="col-lg-6">
                            <div class="card h-100 border-0 shadow">
                                <img src="../assets/img/{image_filename}" alt="{content['image_alt']}" class="card-img-top" style="height: 200px; object-fit: cover;">
                                <div class="card-body">
                                    <span class="badge mb-2" style="background-color: {badge_color};">{badge_category}</span>
                                    <h5 class="card-title">{content['title']}</h5>
                                    <p class="card-text">{content['excerpt']}</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <small class="text-muted">{content['read_time']} min leestijd</small>
                                        <a href="{content['slug']}.html" class="btn btn-outline-primary btn-sm">Lees meer</a>
                                    </div>
                                </div>
                            </div>
                        </div>"""

    # Gebruik invoegmarkering als die bestaat
    insert_marker = "<!-- BLOG_INSERT_POINT -->"
    if insert_marker in index_html:
        index_html = index_html.replace(
            insert_marker,
            new_card + "\n                        " + insert_marker,
        )
    else:
        # Voeg markering en nieuw artikel in vóór Newsletter sectie
        newsletter_marker = "\n    <!-- Newsletter Signup -->"
        if newsletter_marker in index_html:
            # Vind het einde van de artikelgrid (vóór de afsluitende divs van de sectie)
            # en voeg daar het nieuwe artikel én de markering in
            replacement = new_card + "\n                        " + insert_marker + newsletter_marker
            index_html = index_html.replace(newsletter_marker, replacement, 1)
        else:
            print("WAARSCHUWING: Invoeglocation niet gevonden in blog/index.html")
            return

    index_path.write_text(index_html, encoding="utf-8")
    print(f"Blog-index bijgewerkt met: {content['title']}")


# ─── Hoofdfunctie ─────────────────────────────────────────────────────────────

def main() -> None:
    blog_type = BLOG_TYPE.strip().lower()
    if blog_type not in ("kinesitherapie", "kinetec"):
        print(f"Ongeldig BLOG_TYPE: {blog_type}. Gebruik 'kinesitherapie' of 'kinetec'.")
        sys.exit(1)

    if not ANTHROPIC_API_KEY:
        print("FOUT: ANTHROPIC_API_KEY is niet ingesteld.")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  PhysioVisit Blog Generator")
    print(f"  Type: {blog_type}")
    print(f"  Datum: {datetime.date.today().isoformat()}")
    print(f"{'=' * 60}\n")

    # Bestaande titels ophalen
    existing_titles = get_existing_blog_titles()
    print(f"Bestaande blogartikelen gevonden: {len(existing_titles)}")

    # Inhoud genereren
    print("\n[1/4] Inhoud genereren via Claude API...")
    content = generate_blog_content(blog_type, existing_titles)
    print(f"      Titel: {content['title']}")
    print(f"      Slug:  {content['slug']}")

    # Controleer op dubbele slug
    output_path = BLOG_DIR / f"{content['slug']}.html"
    if output_path.exists():
        date_suffix = datetime.date.today().strftime("%Y%m%d")
        content["slug"] = f"{content['slug']}-{date_suffix}"
        output_path = BLOG_DIR / f"{content['slug']}.html"
        print(f"      Slug aangepast (bestond al): {content['slug']}")

    # Afbeelding ophalen
    print("\n[2/4] Afbeelding zoeken en downloaden...")
    image_filename = search_and_download_image(
        content.get("image_search_query", "physiotherapy home visit"),
        content["slug"],
        blog_type,
    )
    print(f"      Afbeelding: {image_filename}")

    # HTML genereren
    print("\n[3/4] HTML genereren...")
    html = generate_blog_html(content, image_filename, blog_type)

    # Opslaan
    output_path.write_text(html, encoding="utf-8")
    print(f"      Opgeslagen: {output_path.relative_to(SCRIPT_DIR.parent)}")

    # Blog-index bijwerken
    print("\n[4/4] Blog-index bijwerken...")
    update_blog_index(content, image_filename)

    # Publicatiegeschiedenis bijwerken
    topics = load_published_topics()
    topics.setdefault(blog_type, []).append(
        {
            "title": content["title"],
            "slug": content["slug"],
            "date": datetime.date.today().isoformat(),
        }
    )
    save_published_topics(topics)

    print(f"\n{'=' * 60}")
    print(f"  GEPUBLICEERD: {content['title']}")
    print(f"  URL: /blog/{content['slug']}.html")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
