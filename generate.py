import json
import os
import shutil
from collections import defaultdict

# Load listings
with open('data/listings.json', 'r') as f:
    data = json.load(f)

listings = data['listings']

# Clean and recreate output folder
if os.path.exists('output'):
    shutil.rmtree('output')
os.makedirs('output')
os.makedirs('output/city')
os.makedirs('output/listing')

# Group listings by city and state
cities = defaultdict(list)
states = defaultdict(list)

for listing in listings:
    cities[listing['city_slug']].append(listing)
    states[listing['state_slug']].append(listing)

# ---- HOMEPAGE ----
city_links = ""
for city_slug, city_listings in sorted(cities.items()):
    city_name = city_listings[0]['city']
    state_name = city_listings[0]['state']
    count = len(city_listings)
    city_links += f'<a href="/city/{city_slug}/" class="city-card"><span class="city-name">{city_name}, {state_name}</span><span class="city-count">{count} listing{"s" if count != 1 else ""}</span></a>\n'

homepage = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Find Estate Cleanout Services Near You | FindEstatesCleanout.com</title>
    <meta name="description" content="Find trusted estate cleanout companies in your area. Browse local professionals who help families clear homes after a loss or downsizing event.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; color: #1a1a1a; background: #f9f9f9; }}
        header {{ background: #1a3c5e; color: white; padding: 40px 20px; text-align: center; }}
        header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        header p {{ font-size: 1.1em; opacity: 0.9; }}
        .hero-cta {{ margin-top: 20px; }}
        .hero-cta a {{ background: #e8a020; color: white; padding: 14px 28px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1em; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 20px; }}
        h2 {{ font-size: 1.6em; margin-bottom: 20px; color: #1a3c5e; }}
        .city-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }}
        .city-card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; text-decoration: none; color: #1a1a1a; display: flex; justify-content: space-between; align-items: center; transition: box-shadow 0.2s; }}
        .city-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .city-name {{ font-weight: 600; }}
        .city-count {{ font-size: 0.85em; color: #888; }}
        .how-it-works {{ background: white; border-radius: 8px; padding: 40px; margin-top: 40px; }}
        .steps {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 24px; margin-top: 20px; }}
        .step {{ text-align: center; }}
        .step-num {{ background: #1a3c5e; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-weight: bold; }}
        .step p {{ font-size: 0.95em; color: #555; }}
        .submit-banner {{ background: #1a3c5e; color: white; text-align: center; padding: 40px 20px; margin-top: 40px; border-radius: 8px; }}
        .submit-banner h2 {{ color: white; margin-bottom: 10px; }}
        .submit-banner p {{ opacity: 0.9; margin-bottom: 20px; }}
        .submit-banner a {{ background: #e8a020; color: white; padding: 14px 28px; border-radius: 6px; text-decoration: none; font-weight: bold; }}
        footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; margin-top: 40px; }}
        footer a {{ color: #888; text-decoration: none; margin: 0 10px; }}
        footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <h1>Find Estate Cleanout Services Near You</h1>
        <p>Connecting families with trusted local estate cleanout professionals</p>
        <div class="hero-cta">
            <a href="/submit/">List Your Business Free</a>
        </div>
    </header>
    <div class="container">
        <h2>Browse by City</h2>
        <div class="city-grid">
            {city_links}
        </div>
        <div class="how-it-works">
            <h2>How It Works</h2>
            <div class="steps">
                <div class="step">
                    <div class="step-num">1</div>
                    <h3>Search Your City</h3>
                    <p>Browse estate cleanout companies in your area</p>
                </div>
                <div class="step">
                    <div class="step-num">2</div>
                    <h3>Compare Listings</h3>
                    <p>Read descriptions and find the right fit for your needs</p>
                </div>
                <div class="step">
                    <div class="step-num">3</div>
                    <h3>Make Contact</h3>
                    <p>Call or visit the company directly to get a quote</p>
                </div>
            </div>
        </div>
        <div class="submit-banner">
            <h2>Own an Estate Cleanout Business?</h2>
            <p>Get listed for free and reach families in your area who need your services.</p>
            <a href="/submit/">Add Your Business Free</a>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com &mdash; Connecting families with trusted estate cleanout professionals</p>
        <p style="margin-top: 10px;"><a href="/privacy/">Privacy Policy</a></p>
    </footer>
</body>
</html>"""

with open('output/index.html', 'w') as f:
    f.write(homepage)

print("Homepage generated")

# ---- CITY PAGES ----
for city_slug, city_listings in cities.items():
    city_name = city_listings[0]['city']
    state_name = city_listings[0]['state']

    city_blurb = city_listings[0].get('city_blurb', '')
    city_blurb_html = f'<div class="city-blurb"><p>{city_blurb}</p></div>' if city_blurb else ''

    listing_cards = ""
    for l in city_listings:
        featured_badge = '<span class="featured-badge">Featured</span>' if l.get('featured') else ''
        if l.get('phone') and l.get('claimed'):
            contact_html = f'<span><a href="tel:{l["phone"]}">{l["phone"]}</a></span>'
        else:
            contact_html = '<span><a href="/submit/" class="claim-link">Claim This Listing</a></span>'

        listing_cards += f"""
        <div class="listing-card {'featured' if l.get('featured') else ''}">
            {featured_badge}
            <h3><a href="/listing/{l['slug']}/">{l['name']}</a></h3>
            <p class="listing-desc">{l['description']}</p>
            <div class="listing-meta">
                <span>{l['city']}, {l['state']}</span>
                {contact_html}
            </div>
        </div>"""

    city_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estate Cleanout Services in {city_name}, {state_name} | FindEstatesCleanout.com</title>
    <meta name="description" content="Find trusted estate cleanout companies in {city_name}, {state_name}. Browse local professionals who help families clear homes after a loss or downsizing event.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; color: #1a1a1a; background: #f9f9f9; }}
        header {{ background: #1a3c5e; color: white; padding: 30px 20px; }}
        header h1 {{ font-size: 1.8em; margin-bottom: 6px; }}
        header p {{ opacity: 0.9; }}
        nav {{ background: #122b44; padding: 10px 20px; }}
        nav a {{ color: #e8a020; text-decoration: none; font-size: 0.9em; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        .listing-card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 24px; margin-bottom: 20px; position: relative; }}
        .listing-card.featured {{ border-color: #e8a020; border-width: 2px; }}
        .featured-badge {{ background: #e8a020; color: white; font-size: 0.8em; padding: 4px 10px; border-radius: 4px; position: absolute; top: 16px; right: 16px; font-weight: bold; }}
        .listing-card h3 {{ font-size: 1.2em; margin-bottom: 8px; }}
        .listing-card h3 a {{ color: #1a3c5e; text-decoration: none; }}
        .listing-card h3 a:hover {{ text-decoration: underline; }}
        .listing-desc {{ color: #555; margin-bottom: 12px; line-height: 1.6; }}
        .listing-meta {{ display: flex; gap: 20px; font-size: 0.9em; color: #444; }}
        .listing-meta a {{ color: #1a3c5e; }}
        .claim-link {{ background: #f0f4f8; border: 1px solid #1a3c5e; color: #1a3c5e; padding: 4px 12px; border-radius: 4px; text-decoration: none; font-weight: 600; font-size: 0.85em; }}
        .claim-link:hover {{ background: #1a3c5e; color: white; }}
        .sidebar-cta {{ background: #1a3c5e; color: white; border-radius: 8px; padding: 24px; margin-top: 30px; text-align: center; }}
        .sidebar-cta h3 {{ margin-bottom: 10px; }}
        .sidebar-cta p {{ font-size: 0.9em; opacity: 0.9; margin-bottom: 16px; }}
        .sidebar-cta a {{ background: #e8a020; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; }}
        .city-blurb {{ background: white; border-radius: 8px; padding: 24px; margin-bottom: 24px; border-left: 4px solid #e8a020; }}
        .city-blurb p {{ color: #555; line-height: 1.7; }}
        footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; }}
        footer a {{ color: #888; text-decoration: none; margin: 0 10px; }}
        footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <h1>Estate Cleanout Services in {city_name}, {state_name}</h1>
        <p>Trusted local professionals helping families clear homes with care</p>
    </header>
    <nav><a href="/">Back to All Cities</a></nav>
    <div class="container">
        {city_blurb_html}
        {listing_cards}
        <div class="sidebar-cta">
            <h3>Own an Estate Cleanout Business in {city_name}?</h3>
            <p>Get listed for free and reach families who need your services.</p>
            <a href="/submit/">Add Your Business Free</a>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
        <p style="margin-top: 10px;"><a href="/privacy/">Privacy Policy</a></p>
    </footer>
</body>
</html>"""

    city_dir = f'output/city/{city_slug}'
    os.makedirs(city_dir)
    with open(f'{city_dir}/index.html', 'w') as f:
        f.write(city_page)

print("City pages generated")

# ---- LISTING PAGES ----
for l in listings:
    if l.get('phone') and l.get('claimed'):
        contact_html = f'<p><a href="tel:{l["phone"]}">{l["phone"]}</a></p>'
        cta_html = f'<a href="tel:{l["phone"]}" class="cta-button">Call Now</a>'
    else:
        contact_html = ''
        cta_html = '<a href="/submit/" class="cta-button claim-cta">Claim This Listing</a>'

    listing_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{l['name']} | Estate Cleanout Services in {l['city']}, {l['state']}</title>
    <meta name="description" content="{l['description']}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; color: #1a1a1a; background: #f9f9f9; }}
        header {{ background: #1a3c5e; color: white; padding: 30px 20px; }}
        header h1 {{ font-size: 1.8em; margin-bottom: 6px; }}
        nav {{ background: #122b44; padding: 10px 20px; }}
        nav a {{ color: #e8a020; text-decoration: none; font-size: 0.9em; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .listing-detail {{ background: white; border-radius: 8px; padding: 32px; border: 1px solid #ddd; }}
        .listing-detail h2 {{ color: #1a3c5e; margin-bottom: 16px; }}
        .listing-detail p {{ color: #555; line-height: 1.7; margin-bottom: 20px; }}
        .contact-info {{ background: #f0f4f8; border-radius: 6px; padding: 20px; margin-top: 20px; }}
        .contact-info h3 {{ margin-bottom: 12px; color: #1a3c5e; }}
        .contact-info p {{ margin-bottom: 8px; }}
        .contact-info a {{ color: #1a3c5e; font-weight: bold; }}
        .cta-button {{ display: inline-block; background: #e8a020; color: white; padding: 14px 28px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 20px; }}
        .claim-cta {{ background: #1a3c5e; }}
        .unclaimed-notice {{ background: #fff8e6; border: 1px solid #e8a020; border-radius: 6px; padding: 16px; margin-top: 20px; font-size: 0.95em; color: #7a5c00; }}
        .featured-badge {{ background: #e8a020; color: white; font-size: 0.85em; padding: 4px 12px; border-radius: 4px; display: inline-block; margin-bottom: 16px; }}
        footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; }}
        footer a {{ color: #888; text-decoration: none; margin: 0 10px; }}
        footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <h1>{l['name']}</h1>
        <p>Estate Cleanout Services in {l['city']}, {l['state']}</p>
    </header>
    <nav><a href="/city/{l['city_slug']}/">Back to {l['city']} Listings</a></nav>
    <div class="container">
        <div class="listing-detail">
            {'<span class="featured-badge">Featured Listing</span>' if l.get('featured') else ''}
            <h2>About {l['name']}</h2>
            <p>{l['description']}</p>
            <div class="contact-info">
                <h3>Contact Information</h3>
                <p>{l['city']}, {l['state']}</p>
                {contact_html}
                {f'<p><a href="{l["website"]}" target="_blank">{l["website"]}</a></p>' if l.get('website') else ''}
            </div>
            {'' if l.get('claimed') else '<div class="unclaimed-notice">This listing has not yet been claimed by the business owner. If this is your business, click below to claim it and add your contact information for free.</div>'}
            {cta_html}
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
        <p style="margin-top: 10px;"><a href="/privacy/">Privacy Policy</a></p>
    </footer>
</body>
</html>"""

    listing_dir = f'output/listing/{l["slug"]}'
    os.makedirs(listing_dir)
    with open(f'{listing_dir}/index.html', 'w') as f:
        f.write(listing_page)

print("Listing pages generated")

# ---- SUBMIT PAGE ----
submit_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit Your Business | FindEstatesCleanout.com</title>
    <meta name="description" content="List your estate cleanout business for free on FindEstatesCleanout.com and reach families in your area.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; color: #1a1a1a; background: #f9f9f9; }
        header { background: #1a3c5e; color: white; padding: 30px 20px; text-align: center; }
        header h1 { font-size: 1.8em; margin-bottom: 6px; }
        nav { background: #122b44; padding: 10px 20px; }
        nav a { color: #e8a020; text-decoration: none; font-size: 0.9em; }
        .container { max-width: 700px; margin: 0 auto; padding: 40px 20px; }
        .form-card { background: white; border-radius: 8px; padding: 32px; border: 1px solid #ddd; }
        .form-card h2 { color: #1a3c5e; margin-bottom: 8px; }
        .form-card p { color: #555; margin-bottom: 24px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 6px; color: #333; }
        input, textarea, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; font-family: inherit; }
        textarea { height: 120px; resize: vertical; }
        .submit-btn { background: #e8a020; color: white; padding: 14px 28px; border: none; border-radius: 6px; font-size: 1em; font-weight: bold; cursor: pointer; width: 100%; }
        .submit-btn:hover { background: #d4911c; }
        footer { text-align: center; padding: 30px; color: #888; font-size: 0.9em; }
        footer a { color: #888; text-decoration: none; margin: 0 10px; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <h1>List Your Business Free</h1>
        <p>Reach families who need estate cleanout services in your area</p>
    </header>
    <nav><a href="/">Back to Home</a></nav>
    <div class="container">
        <div class="form-card">
            <h2>Submit Your Business</h2>
            <p>Fill out the form below and we'll add your listing within 24 hours. It's completely free.</p>
            <form action="https://formspree.io/f/mbdnqygl" method="POST">
                <div class="form-group">
                    <label>Business Name *</label>
                    <input type="text" name="business_name" required>
                </div>
                <div class="form-group">
                    <label>Your Name *</label>
                    <input type="text" name="contact_name" required>
                </div>
                <div class="form-group">
                    <label>Email Address *</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Phone Number *</label>
                    <input type="tel" name="phone" required>
                </div>
                <div class="form-group">
                    <label>City *</label>
                    <input type="text" name="city" required>
                </div>
                <div class="form-group">
                    <label>State *</label>
                    <input type="text" name="state" required>
                </div>
                <div class="form-group">
                    <label>Website (optional)</label>
                    <input type="url" name="website">
                </div>
                <div class="form-group">
                    <label>Business Description *</label>
                    <textarea name="description" required placeholder="Tell families about your services..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Submit My Business Free</button>
            </form>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
        <p style="margin-top: 10px;"><a href="/privacy/">Privacy Policy</a></p>
    </footer>
</body>
</html>"""

os.makedirs('output/submit')
with open('output/submit/index.html', 'w') as f:
    f.write(submit_page)

print("Submit page generated")

# ---- PRIVACY POLICY PAGE ----
privacy_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy | FindEstatesCleanout.com</title>
    <meta name="description" content="Privacy Policy for FindEstatesCleanout.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; color: #1a1a1a; background: #f9f9f9; }
        header { background: #1a3c5e; color: white; padding: 30px 20px; text-align: center; }
        header h1 { font-size: 1.8em; margin-bottom: 6px; }
        nav { background: #122b44; padding: 10px 20px; }
        nav a { color: #e8a020; text-decoration: none; font-size: 0.9em; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        .policy-card { background: white; border-radius: 8px; padding: 40px; border: 1px solid #ddd; }
        h2 { color: #1a3c5e; font-size: 1.4em; margin-top: 30px; margin-bottom: 12px; }
        h2:first-child { margin-top: 0; }
        p { color: #555; line-height: 1.8; margin-bottom: 16px; }
        ul { color: #555; line-height: 1.8; margin-bottom: 16px; padding-left: 24px; }
        ul li { margin-bottom: 8px; }
        .last-updated { color: #888; font-size: 0.9em; margin-bottom: 24px; }
        footer { text-align: center; padding: 30px; color: #888; font-size: 0.9em; }
        footer a { color: #888; text-decoration: none; margin: 0 10px; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <h1>Privacy Policy</h1>
        <p>FindEstatesCleanout.com</p>
    </header>
    <nav><a href="/">Back to Home</a></nav>
    <div class="container">
        <div class="policy-card">
            <p class="last-updated">Last updated: July 2026</p>

            <h2>Introduction</h2>
            <p>FindEstatesCleanout.com ("we", "us", or "our") operates as an online directory connecting families with estate cleanout service providers. This Privacy Policy explains how we collect, use, and protect information when you use our website.</p>

            <h2>Information We Collect</h2>
            <p>We collect information in the following ways:</p>
            <ul>
                <li><strong>Business Listing Submissions:</strong> When a business submits a listing, we collect the business name, contact name, email address, phone number, city, state, website, and business description.</li>
                <li><strong>Usage Data:</strong> We may collect anonymous data about how visitors use our site, including pages visited and time spent on the site.</li>
                <li><strong>Cookies:</strong> Our site may use cookies to improve user experience. You can disable cookies in your browser settings at any time.</li>
            </ul>

            <h2>How We Use Your Information</h2>
            <p>Information collected through business listing submissions is used to:</p>
            <ul>
                <li>Create and maintain your business listing on our directory</li>
                <li>Contact you regarding your listing</li>
                <li>Send occasional updates about the directory</li>
            </ul>

            <h2>We Do Not Sell Your Information</h2>
            <p>We do not sell, trade, or rent your personal information to third parties. Business listing information that you submit is displayed publicly on our website as part of the directory service.</p>

            <h2>Third Party Services</h2>
            <p>We use the following third party services to operate our website:</p>
            <ul>
                <li><strong>Formspree:</strong> Used to process business listing submission forms. Submissions are subject to Formspree's privacy policy.</li>
                <li><strong>Cloudflare:</strong> Used to host and deliver our website. Subject to Cloudflare's privacy policy.</li>
                <li><strong>Google Analytics:</strong> We may use Google Analytics to understand how visitors use our site. Google Analytics collects anonymous usage data.</li>
            </ul>

            <h2>Data Retention</h2>
            <p>Business listing information is retained for as long as the listing remains active on our directory. You may request removal of your listing and associated information at any time by contacting us.</p>

            <h2>Your Rights</h2>
            <p>You have the right to:</p>
            <ul>
                <li>Request access to information we hold about your business</li>
                <li>Request correction of inaccurate information</li>
                <li>Request removal of your business listing and associated data</li>
            </ul>

            <h2>Children's Privacy</h2>
            <p>Our website is not directed at children under the age of 13. We do not knowingly collect personal information from children.</p>

            <h2>Changes to This Policy</h2>
            <p>We may update this Privacy Policy from time to time. We will post any changes on this page with an updated date.</p>

            <h2>Contact Us</h2>
            <p>If you have any questions about this Privacy Policy or wish to request removal of your information, please contact us through our <a href="/submit/" style="color: #1a3c5e;">listing submission form</a>.</p>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
        <p style="margin-top: 10px;"><a href="/privacy/">Privacy Policy</a></p>
    </footer>
</body>
</html>"""

os.makedirs('output/privacy')
with open('output/privacy/index.html', 'w') as f:
    f.write(privacy_page)

print("Privacy policy generated")

# ---- SITEMAP ----
urls = []
urls.append('https://findestatescleanout.com/')
for city_slug in cities:
    urls.append(f'https://findestatescleanout.com/city/{city_slug}/')
for l in listings:
    urls.append(f'https://findestatescleanout.com/listing/{l["slug"]}/')
urls.append('https://findestatescleanout.com/submit/')
urls.append('https://findestatescleanout.com/privacy/')

sitemap_urls = ""
for url in urls:
    sitemap_urls += f"""    <url>
        <loc>{url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>\n"""

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}</urlset>"""

with open('output/sitemap.xml', 'w') as f:
    f.write(sitemap)

print("Sitemap generated")

# ---- ROBOTS.TXT ----
robots = """User-agent: *
Allow: /

Sitemap: https://findestatescleanout.com/sitemap.xml"""

with open('output/robots.txt', 'w') as f:
    f.write(robots)

print("Robots.txt generated")
print("Site generation complete! Check the output/ folder.")
