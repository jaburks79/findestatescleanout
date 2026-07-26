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

    listing_cards = ""
    for l in city_listings:
        featured_badge = '<span class="featured-badge">Featured</span>' if l.get('featured') else ''
        listing_cards += f"""
        <div class="listing-card {'featured' if l.get('featured') else ''}">
            {featured_badge}
            <h3><a href="/listing/{l['slug']}/">{l['name']}</a></h3>
            <p class="listing-desc">{l['description']}</p>
            <div class="listing-meta">
                <span>{l['city']}, {l['state']}</span>
                <span><a href="tel:{l['phone']}">{l['phone']}</a></span>
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
        .sidebar-cta {{ background: #1a3c5e; color: white; border-radius: 8px; padding: 24px; margin-top: 30px; text-align: center; }}
        .sidebar-cta h3 {{ margin-bottom: 10px; }}
        .sidebar-cta p {{ font-size: 0.9em; opacity: 0.9; margin-bottom: 16px; }}
        .sidebar-cta a {{ background: #e8a020; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; }}
        footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
    <header>
        <h1>Estate Cleanout Services in {city_name}, {state_name}</h1>
        <p>Trusted local professionals helping families clear homes with care</p>
    </header>
    <nav><a href="/">Back to All Cities</a></nav>
    <div class="container">
        {listing_cards}
        <div class="sidebar-cta">
            <h3>Own an Estate Cleanout Business in {city_name}?</h3>
            <p>Get listed for free and reach families who need your services.</p>
            <a href="/submit/">Add Your Business Free</a>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
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
        .featured-badge {{ background: #e8a020; color: white; font-size: 0.85em; padding: 4px 12px; border-radius: 4px; display: inline-block; margin-bottom: 16px; }}
        footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; }}
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
                <p><a href="tel:{l['phone']}">{l['phone']}</a></p>
                {f'<p><a href="{l["website"]}" target="_blank">{l["website"]}</a></p>' if l.get('website') else ''}
            </div>
            <a href="tel:{l['phone']}" class="cta-button">Call Now</a>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 FindEstatesCleanout.com</p>
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
            <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
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
    </footer>
</body>
</html>"""

os.makedirs('output/submit')
with open('output/submit/index.html', 'w') as f:
    f.write(submit_page)

print("Submit page generated")
print("Site generation complete! Check the output/ folder.")