import json
from pathlib import Path

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
    "Inter-Terrace House",
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

SCHOOLS = json.loads((Path(app.root_path) / "static" / "schools.json").read_text(encoding="utf-8-sig"))
MRT_LINES = json.loads((Path(app.root_path) / "static" / "mrt_lines.json").read_text(encoding="utf-8-sig"))
PSF_BENCHMARKS = json.loads((Path(app.root_path) / "static" / "psf_benchmarks.json").read_text(encoding="utf-8-sig"))

LANDED_TYPES = {"Terraced House", "Inter-Terrace House", "Corner Terrace", "Semi-Detached House", "Detached House", "Detached Bungalow", "Good Class Bungalow", "Cluster House", "Strata Landed"}
CONDO_TYPES = {"Condominium", "Executive Condominium", "Luxury Apartment", "Penthouse", "Service Residence"}

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
    launch_listings = [listing for listing in LISTINGS if listing.get("is_launch")]
    just_listed = [listing for listing in reversed(LISTINGS) if not listing.get("is_launch")][:4]
    gcb_listings = [listing for listing in LISTINGS if listing["type"] == "Good Class Bungalow"]
    return render_template(
        "home.html",
        **page_context("home", launch_listings=launch_listings, just_listed_listings=just_listed, gcb_listings=gcb_listings),
    )


@app.route("/all-listings")
def listings():
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_districts = request.args.getlist("district")
    selected_types = request.args.getlist("type")
    selected_category = request.args.get("category", "").strip().casefold()
    sale_status = request.args.get("status", "").strip().casefold()
    query = request.args.get("q", "").strip()
    selected_school = request.args.get("school", "").strip()
    selected_mrt = request.args.get("mrt", "").strip()
    category_types = LANDED_TYPES if selected_category == "landed" else CONDO_TYPES if selected_category == "condo" else None
    filtered_listings = [listing for listing in LISTINGS if (not selected_districts or listing["location"] in selected_districts) and (not selected_types or listing["type"] in selected_types) and (not category_types or listing["type"] in category_types) and (sale_status != "resale" or not listing.get("is_launch")) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold()) and (not selected_school or selected_school.casefold() in [school.casefold() for school in listing.get("schools_list", "").split("|")]) and (not selected_mrt or selected_mrt.casefold() in listing.get("mrt", "").casefold())]
    return render_template("listings.html", **page_context("listings", listings=filtered_listings, districts=districts, property_types=property_types, selected_districts=selected_districts, selected_types=selected_types, query=query, selected_school=selected_school, selected_mrt=selected_mrt))


@app.route("/new-launches")
def launches():
    launch_listings = [listing for listing in LISTINGS if listing.get("is_launch")]
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_districts = request.args.getlist("district")
    selected_types = request.args.getlist("type")
    launch_category = request.args.get("category", "").strip().casefold()
    query = request.args.get("q", "").strip()
    category_types = LANDED_TYPES if launch_category == "landed" else CONDO_TYPES if launch_category == "condo" else None
    filtered_listings = [listing for listing in launch_listings if (not selected_districts or listing["location"] in selected_districts) and (not selected_types or listing["type"] in selected_types) and (not category_types or listing["type"] in category_types) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold())]
    return render_template("listings.html", **page_context("launches", listings=filtered_listings, districts=districts, property_types=property_types, selected_districts=selected_districts, selected_types=selected_types, query=query, launch_category=launch_category))


@app.route("/for-rent")
def for_rent():
    return render_template("listings.html", **page_context("rent", listings=[], districts=SINGAPORE_DISTRICTS, property_types=PROPERTY_TYPES, selected_districts=[], selected_types=[], query=""))


@app.route("/search-by-school")
def search_by_school():
    query = request.args.get("q", "").strip()
    schools = [school for school in SCHOOLS if not query or query.casefold() in school.casefold()]
    return render_template("school_search.html", **page_context("school-search", schools=schools, query=query))


@app.route("/search-by-mrt")
def search_by_mrt():
    query = request.args.get("q", "").strip()
    lines = []
    for line in MRT_LINES:
        stations = [station for station in line["stations"] if not query or query.casefold() in station.casefold()]
        if stations:
            lines.append({**line, "stations": stations})
    total_stations = sum(len(line["stations"]) for line in lines)
    return render_template("mrt_search.html", **page_context("mrt-search", lines=lines, query=query, total_stations=total_stations))


@app.route("/property/<path:property_name>")
def property_detail(property_name):
    listing = next((item for item in LISTINGS if item["name"] == property_name), None)
    if listing is None:
        return "Property not found", 404
    gallery = listing.get("gallery", [listing["image"]])
    return render_template("property_detail.html", **page_context("listings", listing=listing, gallery=gallery))


@app.route("/services")
def services():
    return render_template("services.html", **page_context("services", services=[
        {"number": "01", "eyebrow": "For buyers", "title": "Find a home that fits your life.", "text": "A focused search shaped around your priorities. Compare suitable homes, understand the market and make your next move with a clear plan.", "link_endpoint": "buy_with_us", "link_label": "Explore buying"},
        {"number": "02", "eyebrow": "For sellers", "title": "Bring your property to the right people.", "text": "Thoughtful pricing, considered presentation and purposeful marketing—supported by clear advice from the first conversation to completion.", "link_endpoint": "sell_with_us", "link_label": "Explore selling"},
        {"number": "03", "eyebrow": "For landlords", "title": "Make leasing feel simpler.", "text": "Practical support to help you prepare, market and lease your property, while finding tenants who are the right fit.", "link_endpoint": "contact", "link_label": "Talk to our team"},
    ]))


@app.route("/buy-with-us")
def buy_with_us():
    return render_template("buy_with_us.html", **page_context("services"))


@app.route("/sell-with-us")
def sell_with_us():
    return render_template("sell_with_us.html", **page_context("services"))


@app.route("/home-valuation")
def home_valuation():
    return render_template("home_valuation.html", **page_context("services", property_types=PROPERTY_TYPES))


@app.route("/resources")
def resources():
    return render_template("resources.html", **page_context("resources"))


@app.route("/resources/market-trends")
def market_trends():
    return render_template("resource_collection.html", **page_context("market-trends", eyebrow="SS Property / Resources", heading="Market <em>trends.</em>", intro="A practical view of the signals buyers and sellers watch when assessing Singapore property.", articles=[
        {"title": "Private residential property index", "text": "Official data on prices, rentals, vacancy and supply in Singapore's private residential market.", "source": "Urban Redevelopment Authority", "image_credit": "Image: Urban Redevelopment Authority", "image": "https://isomer-user-content.by.gov.sg/467/eb9d7819-ed32-43b2-897d-2a11a9d19158/IMG01.jpg", "url": "https://www.ura.gov.sg/property-data/private-residential-properties/"},
        {"title": "Prices and rentals", "text": "URA's latest quarterly chart for private residential prices and rentals.", "source": "Urban Redevelopment Authority", "image_credit": "Chart: Urban Redevelopment Authority", "image": "https://isomer-user-content.by.gov.sg/467/76d9451c-8062-43c7-aef1-1de9a6908575/IMG02.jpg", "url": "https://www.ura.gov.sg/news/media/pr26-57/"},
        {"title": "New launches and take-up", "text": "Official data on developer launches and sales of private residential homes.", "source": "Urban Redevelopment Authority", "image_credit": "Chart: Urban Redevelopment Authority", "image": "https://isomer-user-content.by.gov.sg/467/5b462fce-0162-446b-8da9-15553173ec18/IMG04.jpg", "url": "https://www.ura.gov.sg/news/media/pr26-57/"},
    ]))


@app.route("/resources/news-articles")
def news_articles():
    return render_template("resource_collection.html", **page_context("news-articles", eyebrow="SS Property / Resources", heading="News <em>articles.</em>", intro="Property news and explainers to help you follow developments that may affect your next move.", articles=[
        {"title": "Release of Q2 2026 real estate statistics", "text": "URA's official release covering prices, rentals, supply and private residential transactions.", "source": "Urban Redevelopment Authority", "image_credit": "Chart: Urban Redevelopment Authority", "image": "https://isomer-user-content.by.gov.sg/467/ffc0ec55-8891-48e3-b858-70f9404448b8/IMG05.jpg", "url": "https://www.ura.gov.sg/news/media/pr26-57/"},
        {"title": "URA media releases", "text": "Official planning, development and property-market announcements from URA.", "source": "Urban Redevelopment Authority", "image_credit": "Image: Urban Redevelopment Authority", "image": "https://isomer-user-content.by.gov.sg/467/eb9d7819-ed32-43b2-897d-2a11a9d19158/IMG01.jpg", "url": "https://www.ura.gov.sg/news/media/"},
        {"title": "Shorter waiting times for Toa Payoh and Sin Ming BTO flats", "text": "CNA reporting on planned BTO projects with waiting times under three years.", "source": "CNA", "image_credit": "Image: CNA", "image": "https://dam.mediacorp.sg/image/upload/s--LABtXPfr--/f_auto,q_auto/c_fill,g_center,h_598,w_747/v1/mediacorp/cna/image/2026/08/30/tp.png?itok=fKm7PqzE", "url": "https://www.channelnewsasia.com/singapore/1200-bto-flats-toay-payoh-sin-ming-shorter-waiting-times-6350066"},
    ]))


@app.route("/resources/postal-districts")
def postal_districts():
    return render_template("postal_districts.html", **page_context("resources", districts=SINGAPORE_DISTRICTS))


@app.route("/resources/loan-calculator")
def loan_calculator():
    return render_template("loan_calculator.html", **page_context("loan-calculator"))


def parse_price(price_text):
    digits = "".join(char for char in price_text if char.isdigit())
    return int(digits) if digits else None


def listing_category(property_type):
    if property_type in LANDED_TYPES:
        return "landed"
    if property_type in CONDO_TYPES:
        return "condo"
    return "hdb"


@app.route("/resources/property-value-calculator")
def property_value_calculator():
    priced_listings = [
        {**listing, "category": listing_category(listing["type"])}
        for listing in sorted(LISTINGS, key=lambda listing: parse_price(listing["price"]) or 0)
        if parse_price(listing["price"])
    ]
    return render_template("property_value_calculator.html", **page_context("resources", districts=SINGAPORE_DISTRICTS, psf_benchmarks=PSF_BENCHMARKS, listings=priced_listings, parse_price=parse_price))


@app.route("/resources/property-types")
def property_types_resource():
    property_groups = [
        {"title": "Landed properties", "description": "Private homes with their own land, offering more space and independence.", "types": [
            {"name": "Terraced House", "description": "A landed home joined to neighbouring houses on both sides."},
            {"name": "Inter-Terrace House", "description": "A terrace home positioned between two neighbouring houses."},
            {"name": "Corner Terrace", "description": "An end-unit terrace with more land and additional natural light."},
            {"name": "Semi-Detached House", "description": "A landed home joined to one neighbouring house only."},
            {"name": "Detached House", "description": "A standalone landed home with space on all sides."},
            {"name": "Detached Bungalow", "description": "A larger standalone home on its own plot of land."},
            {"name": "Good Class Bungalow", "description": "Singapore's most exclusive bungalow category, subject to planning rules."},
            {"name": "Cluster House", "description": "A landed-style home within a shared private development."},
            {"name": "Strata Landed", "description": "A landed-style property held under strata ownership."},
        ]},
        {"title": "Apartments & condominiums", "description": "Private residences in shared developments, often with facilities and security.", "types": [
            {"name": "Apartment", "description": "A private home in a low- or mid-rise residential building."},
            {"name": "Condominium", "description": "A private development that commonly includes shared facilities."},
            {"name": "Luxury Apartment", "description": "A premium apartment with higher-end finishes and location."},
            {"name": "Penthouse", "description": "A larger, often top-floor apartment with elevated views."},
            {"name": "Serviced Residence", "description": "A furnished residence with hotel-style services and conveniences."},
        ]},
        {"title": "HDB homes", "description": "Singapore's public-housing options for eligible buyers and households.", "types": [
            {"name": "HDB Flat", "description": "A public-housing home built by the Housing & Development Board."},
            {"name": "HDB Apartment", "description": "An HDB home with an apartment-style layout in a public estate."},
            {"name": "Executive Condominium", "description": "A hybrid housing option with private-condominium features."},
        ]},
    ]
    return render_template("property_types.html", **page_context("resources", property_groups=property_groups))


@app.route("/about-us")
def about():
    return render_template("about.html", **page_context("about"))


@app.route("/our-people")
def our_people():
    return render_template("about.html", **page_context("our-people"))


@app.route("/contact")
def contact():
    return render_template("contact.html", **page_context("contact"))


LEGAL_PAGES = {
    "disclaimer": {
        "eyebrow": "Legal information",
        "title": "Disclaimer",
        "intro": "Please read these terms before relying on information published on this website.",
        "sections": [
            {"title": "General information", "text": "The information on this website is provided for general reference only. It is not legal, financial, tax, property or investment advice, and should not be relied on as a substitute for independent professional advice."},
            {"title": "Property details", "text": "Property descriptions, measurements, prices, availability, images and other details are believed to be accurate when published, but may change without notice. They are subject to contract, final verification and the seller's approval."},
            {"title": "No offer or warranty", "text": "Nothing on this website constitutes an offer, representation or warranty. Prospective purchasers and tenants should carry out their own inspections, enquiries and due diligence before making any decision."},
            {"title": "External content", "text": "Links and embedded content from third-party websites are provided for convenience. We are not responsible for their availability, content, privacy practices or accuracy."},
        ],
    },
    "privacy_policy": {
        "eyebrow": "Legal information",
        "title": "Privacy Policy",
        "intro": "This policy explains how personal information provided through this website is handled.",
        "sections": [
            {"title": "Information we collect", "text": "We may collect your name, email address, telephone number, property preferences and the contents of enquiries you send through the website."},
            {"title": "How we use information", "text": "We use this information to respond to enquiries, provide requested property services, communicate relevant updates and improve our website and services."},
            {"title": "Sharing and retention", "text": "Information is shared only where reasonably necessary to provide our services, meet legal obligations or work with trusted service providers. We retain it only for as long as necessary for these purposes or as required by law."},
            {"title": "Cookies and external services", "text": "This website may use cookies and embedded third-party services. Those providers may collect information under their own privacy policies."},
        ],
    },
    "data_protection": {
        "eyebrow": "Legal information",
        "title": "Data Protection",
        "intro": "We take reasonable steps to protect personal data entrusted to us.",
        "sections": [
            {"title": "Safeguarding personal data", "text": "We use reasonable administrative, technical and physical safeguards to protect personal data from unauthorised access, collection, use, disclosure, copying, modification or disposal."},
            {"title": "Your choices", "text": "You may ask about the personal data we hold about you, request correction of inaccurate information or withdraw consent for certain uses, subject to applicable legal and contractual requirements."},
            {"title": "Marketing communications", "text": "You may opt out of marketing communications at any time by contacting us through the Contact page or using any unsubscribe option provided in the communication."},
            {"title": "Policy updates", "text": "We may update these notices from time to time. The version published on this website applies from its publication date."},
        ],
    },
}


def render_legal_page(page_name):
    return render_template("legal_page.html", **page_context("", **LEGAL_PAGES[page_name]))


@app.route("/disclaimer")
def disclaimer():
    return render_legal_page("disclaimer")


@app.route("/privacy-policy")
def privacy_policy():
    return render_legal_page("privacy_policy")


@app.route("/data-protection")
def data_protection():
    return render_legal_page("data_protection")


if __name__ == "__main__":
    app.run(debug=True)
