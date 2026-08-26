from flask import Flask, render_template, request

app = Flask(__name__)

NAV_ITEMS = [
    ("All Listings", "listings"),
    ("New Launches", "launches"),
    ("Services", "services"),
    ("Resources", "resources"),
    ("About Us", "about"),
    ("Contact", "contact"),
]

SINGAPORE_DISTRICTS = [
    "D01 Raffles Place / Marina Bay",
    "D02 Shenton Way / Tanjong Pagar",
    "D03 Alexandra / Commonwealth / Tiong Bahru",
    "D04 Harbourfront / Telok Blangah",
    "D05 Buona Vista / Pasir Panjang / Clementi",
    "D06 City Hall / Clarke Quay",
    "D07 Beach Road / Bugis / Rochor",
    "D08 Farrer Park / Little India",
    "D09 Orchard / River Valley",
    "D10 Tanglin / Holland / Bukit Timah",
    "D11 Newton / Novena / Watten Estate",
    "D12 Balestier / Toa Payoh / Serangoon",
    "D13 Macpherson / Potong Pasir",
    "D14 Eunos / Geylang / Paya Lebar",
    "D15 East Coast / Marine Parade",
    "D16 Bedok / Upper East Coast",
    "D17 Loyang / Changi",
    "D18 Pasir Ris / Simei / Tampines",
    "D19 Serangoon / Kovan",
    "D20 Ang Mo Kio / Bishan / Thomson",
    "D21 Upper Bukit Timah / Clementi Park",
    "D22 Boon Lay / Jurong / Tuas",
    "D23 Hillview / Dairy Farm / Bukit Batok",
    "D24 Lim Chu Kang / Tengah",
    "D25 Admiralty / Woodlands",
    "D26 Upper Thomson / Springleaf",
    "D27 Sembawang / Yishun",
    "D28 Seletar / Yio Chu Kang",
]

PROPERTY_TYPES = [
    "Luxury Apartment",
    "Light Industrial",
    "Townhouse",
    "HDB Flat",
    "HDB Apartment",
    "Terraced House",
    "Corner Terrace",
    "Semi-Detached House",
    "Detached House",
    "Detached Bungalow",
    "Good Class Bungalow",
    "Cluster House",
    "Strata Landed",
    "Apartment",
    "Condominium",
    "Penthouse",
    "Mixed Development",
    "Executive Condominium",
    "Service Residence",
]

LISTINGS = [
    {
        "name": "96 Farrer Road",
        "location": "D10 Tanglin / Holland / Bukit Timah",
        "type": "Detached House",
        "tenure": "Freehold",
        "price": "S$17,500,000",
        "details": "5 ensuite bedrooms  ·  5 baths  ·  Land 4,224 sq ft",
        "description": "A brand-new three-level detached residence in the Gallop Park Road collection, offering 4,224 sq ft of freehold land and approximately 7,250 sq ft of built-up space. Designed for generous family living, the home brings together five ensuite bedrooms, a private swimming pool, a home lift and practical indoor-outdoor entertaining areas in a highly sought-after D10 setting.",
        "land_size": "4,224 sq ft",
        "built_up": "7,250 sq ft",
        "top": "June 2026",
        "features": "5 ensuite bedrooms, home lift, swimming pool",
        "parking": "3 cars on site; outside street parking available",
        "schools": "Nanyang Primary within 1km; Raffles Girls' Primary and Singapore Chinese Girls within 1-2km",
        "schools_list": "Nanyang Primary|Raffles Girls' Primary|St Margaret's Secondary|Hwa Chong Institution|Nanyang Girls' High|Singapore Chinese Girls|St Joseph's Institution|Anglo-Chinese School (Primary)|Anglo-Chinese School (Barker Road)",
        "mrt": "550m to Botanic Gardens MRT",
        "floor_plan": "1F: Park 3 cars, lift, living, dining, dry kitchen, wet kitchen, bathroom, helper's room and bathroom, store room|2F: Lift, master bedroom and 2 ensuite bedrooms|3F: Lift and 2 ensuite bedrooms",
        "collection": "Gallop Park Road Collection: Plot 1 Semi-Detached, 2,957 sq ft land / approx. 5,607 sq ft built-up, S$13.5 million (sold); Plot 2 Semi-Detached, 2,583 sq ft land / approx. 5,231 sq ft built-up, S$12.5 million; Plot 3 Detached, 4,224 sq ft land / approx. 7,250 sq ft built-up, S$17.5 million.",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
        "tag": "Featured",
    },
]


def page_context(active_page, **extra):
    return {"active_page": active_page, "nav_items": NAV_ITEMS, **extra}

@app.context_processor
def shared_property_context():
    return {"featured_listings": LISTINGS}


@app.route("/")
def home():
    return render_template("home.html", **page_context("home", listings=LISTINGS))


@app.route("/all-listings")
def listings():
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_district = request.args.get("district", "")
    selected_type = request.args.get("type", "")
    query = request.args.get("q", "").strip()
    filtered_listings = [listing for listing in LISTINGS if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold())]
    return render_template("listings.html", **page_context("listings", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type, query=query))


@app.route("/new-launches")
def launches():
    launch_listings = LISTINGS[:4]
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_district = request.args.get("district", "")
    selected_type = request.args.get("type", "")
    query = request.args.get("q", "").strip()
    filtered_listings = [listing for listing in launch_listings if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold())]
    return render_template("listings.html", **page_context("launches", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type, query=query))


@app.route("/property/<path:property_name>")
def property_detail(property_name):
    listing = next((item for item in LISTINGS if item["name"] == property_name), None)
    if listing is None:
        return "Property not found", 404
    gallery = [item["image"] for item in LISTINGS[:4]]
    return render_template("property_detail.html", **page_context("listings", listing=listing, gallery=gallery))


@app.route("/services")
def services():
    return render_template("text_page.html", **page_context("services", eyebrow="Our services", heading="A better way to <em>move.</em>", intro="From the first conversation to the final signature, our advice is clear, considered, and entirely yours.", items=[
        {"title": "Buying, thoughtfully", "text": "A calm, informed search shaped around how you want to live, with access to homes you will not find everywhere."},
        {"title": "Selling, beautifully", "text": "We tell the story of your home with precision, introduce it to the right people, and handle every detail."},
        {"title": "Letting, simply", "text": "Long-term partnerships for landlords who care about their property and the people who live in it."},
    ]))


@app.route("/resources")
def resources():
    return render_template("resources.html", **page_context("resources"))


@app.route("/resources/postal-districts")
def postal_districts():
    return render_template("postal_districts.html", **page_context("resources", districts=SINGAPORE_DISTRICTS))


@app.route("/about-us")
def about():
    return render_template("about.html", **page_context("about"))


@app.route("/contact")
def contact():
    return render_template("contact.html", **page_context("contact"))


if __name__ == "__main__":
    app.run(debug=True)
