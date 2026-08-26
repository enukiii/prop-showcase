from flask import Flask, render_template, request
import pandas as pd

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

df = pd.read_csv("data/realDummyData.csv")
LISTINGS = df.to_dict(orient="records")

# LISTINGS = [
#     {
#         "name": "96 Farrer Road",
#         "location": "D10 Tanglin / Holland / Bukit Timah",
#         "type": "Detached House",
#         "tenure": "Freehold",
#         "price": "S$17,500,000",
#         "details": "5 ensuite bedrooms  ·  5 baths  ·  Land 4,224 sq ft",
#         "description": "A brand-new 2.5-storey detached home in Gallop Park Road with a private swimming pool, home lift and generous built-up space.",
#         "land_size": "4,224 sq ft",
#         "built_up": "7,250 sq ft",
#         "top": "June 2026",
#         "features": "5 ensuite bedrooms, home lift, swimming pool",
#         "parking": "3 cars on site; outside street parking available",
#         "schools": "Nanyang Primary within 1km; Raffles Girls' Primary and Singapore Chinese Girls within 1-2km",
#         "mrt": "550m to Botanic Gardens MRT",
#         "collection": "Gallop Park Road Collection: Plot 2 Semi-Detached House, Land 2,583 sq ft / Built-up approx. 5,231 sq ft, S$12.5 million.",
#         "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
#         "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Featured",
#     },
#     {
#         "name": "Aster Penthouse",
#         "location": "D03 Alexandra / Commonwealth / Tiong Bahru",
#         "type": "Penthouse",
#         "price": "S$2,100,000",
#         "details": "3 beds  ·  2 baths  ·  1,840 sq ft",
#         "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85",
#         "tag": "New",
#     },
#     {
#         "name": "Cedar Ridge",
#         "location": "D28 Seletar / Yio Chu Kang",
#         "type": "Detached Bungalow",
#         "price": "S$1,750,000",
#         "details": "5 beds  ·  4 baths  ·  3,110 sq ft",
#         "image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Private",
#     },
#     {
#         "name": "Maple Grove House",
#         "location": "D11 Newton / Novena / Watten Estate",
#         "type": "Detached House",
#         "tenure": "Freehold",
#         "price": "S$2,950,000",
#         "details": "4 beds  ·  3 baths  ·  2,680 sq ft",
#         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Just listed",
#     },
#     {
#         "name": "Willow Lane",
#         "location": "D15 East Coast / Marine Parade",
#         "type": "Semi-Detached House",
#         "tenure": "Freehold",
#         "price": "S$1,980,000",
#         "details": "4 beds  ·  2 baths  ·  2,110 sq ft",
#         "image": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Just listed",
#     },
#     {
#         "name": "The Orchard",
#         "location": "D19 Serangoon / Kovan",
#         "type": "Terraced House",
#         "tenure": "Freehold",
#         "price": "S$895,000",
#         "details": "3 beds  ·  2 baths  ·  1,540 sq ft",
#         "image": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85",
#         "tag": "New",
#     },
#     {
#         "name": "Ashwood Place",
#         "location": "D16 Bedok / Upper East Coast",
#         "type": "Detached Bungalow",
#         "tenure": "Freehold",
#         "price": "S$1,425,000",
#         "details": "5 beds  ·  3 baths  ·  2,940 sq ft",
#         "image": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Just listed",
#     },
#     {
#         "name": "Linden Mews",
#         "location": "D20 Ang Mo Kio / Bishan / Thomson",
#         "type": "Townhouse",
#         "tenure": "Freehold",
#         "price": "S$1,675,000",
#         "details": "3 beds  ·  2 baths  ·  1,720 sq ft",
#         "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Featured",
#     },
#     {
#         "name": "Rosewood Court",
#         "location": "D09 Orchard / River Valley",
#         "type": "Corner Terrace",
#         "tenure": "Freehold",
#         "price": "S$2,250,000",
#         "details": "4 beds  ·  3 baths  ·  2,280 sq ft",
#         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Featured",
#     },
#     {
#         "name": "Oakfield Manor",
#         "location": "D21 Upper Bukit Timah / Clementi Park",
#         "type": "Good Class Bungalow",
#         "tenure": "Freehold",
#         "price": "S$3,200,000",
#         "details": "6 beds  ·  4 baths  ·  3,680 sq ft",
#         "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85",
#         "tag": "New",
#     },
#     {
#         "name": "Elm Park House",
#         "location": "D14 Eunos / Geylang / Paya Lebar",
#         "type": "Terraced House",
#         "tenure": "Freehold",
#         "price": "S$1,350,000",
#         "details": "3 beds  ·  2 baths  ·  1,690 sq ft",
#         "image": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Featured",
#     },
#     {
#         "name": "Meadow View",
#         "location": "D23 Hillview / Dairy Farm / Bukit Batok",
#         "type": "Cluster House",
#         "tenure": "Freehold",
#         "price": "S$2,700,000",
#         "details": "5 beds  ·  4 baths  ·  3,250 sq ft",
#         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85",
#         "tag": "Featured",
#     },
#     {
#         "name": "Marina One Residence",
#         "location": "D01 Raffles Place / Marina Bay",
#         "type": "Luxury Apartment",
#         "tenure": "99-year Leasehold",
#         "price": "S$2,480,000",
#         "details": "2 beds  ·  2 baths  ·  1,120 sq ft",
#         "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
#         "tag": "New",
#     },
# ]


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
    filtered_listings = [listing for listing in LISTINGS if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type)]
    return render_template("listings.html", **page_context("listings", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type))


@app.route("/new-launches")
def launches():
    launch_listings = LISTINGS[:4]
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_district = request.args.get("district", "")
    selected_type = request.args.get("type", "")
    filtered_listings = [listing for listing in launch_listings if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type)]
    return render_template("listings.html", **page_context("launches", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type))


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
