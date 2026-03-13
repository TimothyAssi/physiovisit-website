# PhysioVisit Blog Aanmaken

Je maakt een nieuwe SEO-geoptimaliseerde blogpost voor de PhysioVisit website.

## Stappen

### 1. Onderwerp & Keywords
- Vraag de gebruiker naar het onderwerp als dat niet duidelijk is
- Bepaal de primaire en secundaire zoekwoorden
- Kies een URL-vriendelijke bestandsnaam

### 2. Blog HTML Aanmaken
- Gebruik dezelfde structuur als bestaande blogs in `blog/`
- Inclusief: BlogPosting + FAQPage + BreadcrumbList structured data schemas
- Interne links naar relevante pagina's (kinetec-huren.html, hometrainer-huren.html, kinesitherapie.html, contact.html)
- Sidebar met contact widget, diensten widget en review widget
- Responsive Bootstrap 5 layout
- Google Analytics tracking tag (AW-620935990)

### 3. Afbeelding Genereren
- Gebruik de Google Gemini API (model: `gemini-2.5-flash-image`) voor het genereren van een unieke blog header afbeelding
- API Key: `AIzaSyDu9l1zRQ2fykJD_Yxj0ev4Wu4Vw20mD_A`
- Gebruik ALTIJD de Kinetec referentiefoto (`assets/img/Kinetec.webp`) als referentie als het blog gerelateerd is aan kinetec/revalidatie
- Genereer in landscape 16:9 formaat (1408x736)
- Converteer naar WebP (quality 85) voor optimale laadsnelheid
- Sla op in `assets/img/`

### 4. BELANGRIJK: Goedkeuring Vragen
- **Toon de gegenereerde afbeelding ALTIJD eerst aan de gebruiker**
- **Vraag expliciet toestemming voordat je de blog online zet (commit + push)**
- Als de gebruiker aanpassingen wil, genereer een nieuwe afbeelding
- Pas pas commit + push toe na goedkeuring

### 5. Online Zetten (na goedkeuring)
- Voeg de blog toe aan `blog/index.html` (nieuwe article card)
- Voeg de blog toe aan `sitemap.xml`
- Update eventueel gerelateerde pagina's met interne links
- Git commit en push naar main (Netlify deployment)

## Terugbetaling Info
- Kinetec terugbetaling is via VERZEKERING (niet mutualiteit)
- PhysioVisit geeft een factuur, patient dient in bij verzekering
- Verzekering betaalt terug: soms alles, soms helft, soms beperkt
- Advies: altijd vooraf informeren bij eigen verzekering
