from flask import Flask, render_template, request
import pandas as pd
from pathlib import Path
import re

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

def _format_area(value):
    """Format a CSV area value for display without showing NaN."""
    if pd.isna(value) or str(value).strip() == "":
        return "Available on request"
    return f"{int(float(value)):,} sq ft"


def _format_price(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Price on request"
    price = str(value).strip()
    return price.replace("$", "S$")


def normalise_listing(row, district):
    property_type = str(row["Type"]).strip()
    property_type = {
        "Semi D": "Semi-Detached House",
        "Detached": "Detached House",
    }.get(property_type, property_type)
    house_number = str(row["House No"]).strip()
    address = str(row["Address"]).strip()
    bedrooms = str(row["Bedroom"]).strip()
    bathrooms = str(row["Bathroom"]).strip()
    land_size = _format_area(row["Land Size"])
    built_up = _format_area(row["Build Up"])
    remarks = "" if pd.isna(row["Remarks"]) else str(row["Remarks"]).strip()
    condition = "" if pd.isna(row["Condition"]) else str(row["Condition"]).strip()

    return {
        "name": f"{house_number} {address}",
        "location": district,
        "address": address,
        "type": property_type,
        "condition": condition,
        "tenure": str(row["Tenure"]).strip(),
        "price": _format_price(row["Price"]),
        "details": f"{bedrooms} beds  ·  {bathrooms} baths  ·  Land {land_size}",
        "description": remarks or f"A {condition.lower()} {property_type.lower()} at {address}.",
        "land_size": land_size,
        "built_up": built_up,
        "top": "" if pd.isna(row["TOP"]) else str(row["TOP"]).strip(),
        "features": remarks,
        "facing": str(row["Facing"]).strip(),
        "developer": "" if pd.isna(row["Developer"]) else str(row["Developer"]).strip(),
        "lister": "" if pd.isna(row["Lister"]) else str(row["Lister"]).strip(),
        "privyr": "" if pd.isna(row["Privy"]) else str(row["Privy"]).strip(),
        "image": "",
        "tag": condition or "New",
    }


def load_listings():
    district_names = {
        district.split(" ", 1)[0]: district
        for district in SINGAPORE_DISTRICTS
    }
    listings = []

    for csv_path in sorted(Path("data").glob("SSP Listing - D*.csv")):
        match = re.fullmatch(r"SSP Listing - (D\d+)\.csv", csv_path.name)
        if not match:
            continue
        district_code = match.group(1).upper()
        district = district_names.get(district_code, district_code)
        dataframe = pd.read_csv(csv_path)
        dataframe.columns = dataframe.columns.str.strip()
        listings.extend(
            normalise_listing(row, district)
            for _, row in dataframe.iterrows()
        )

    return listings


LISTINGS = load_listings()

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
