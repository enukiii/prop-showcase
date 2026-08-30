import json
from pathlib import Path

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

LISTINGS = [
    {
        "name": "7 Coronation Road",
        "location": "D10 Tanglin / Holland / Bukit Timah",
        "type": "Semi-Detached House",
        "tenure": "Freehold",
        "price": "S$13,200,000",
        "details": "4 en-suite bedrooms · 4 storey · Land 2,539 sq ft",
        "description": "A 4-storey semi-detached home with a private lift serving all floors, a swimming pool and a functional layout, just 6 minutes' walk to Tan Kah Kee MRT and within 1km of Raffles Girls' and Nanyang Primary.",
        "land_size": "2,539 sq ft",
        "built_up": "7,000 sq ft",
        "top": "Q3 2026",
        "features": "Private lift serving all floors (wheelchair accessible), 4 en-suite bedrooms, 1 en-suite helper's room, 2 family living areas, garden terrace sitting area, double volume high ceiling living area, functional layout",
        "parking": "Park 3 cars",
        "schools": "Nanyang Primary and Raffles Girls' Primary within 1km; nearby Hwa Chong, Singapore Chinese Girls' School, ACS, SJI and Nanyang Kindergarten",
        "schools_list": "Nanyang Primary|Raffles Girls' Primary|Hwa Chong|Singapore Chinese Girls' School|ACS|SJI|Nanyang Kindergarten",
        "mrt": "1 min walk to Coronation Shopping Plaza; 6 mins walk to Tan Kah Kee MRT; 5 mins drive to Orchard Road",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty. Some photos or locations are withheld to respect the owner's privacy.",
        "image": "/static/img/HousesIMG/Coronation%20B7000/Coronation%20B7000%20Landing.PNG",
        "gallery": ["/static/img/HousesIMG/Coronation%20B7000/Coronation%20B7000%20Landing.PNG"],
        "floor_plan_images": [
            "/static/img/HousesIMG/Coronation%20B7000/floor%20plan%201.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/floor%20plan%202.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/floor%20plan%203.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/floor%20plan%204.jpg",
        ],
        "interior_images": [
            "/static/img/HousesIMG/Coronation%20B7000/interial%201.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%202.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%203.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%204.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%205.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%206.jpg",
            "/static/img/HousesIMG/Coronation%20B7000/interial%207.jpg",
        ],
        "video_url": "https://www.instagram.com/p/Da4FCIAvkNY/embed/",
        "is_launch": True,
    },
    {
        "name": "Fir Ave 1",
        "location": "D10 Tanglin / Holland / Bukit Timah",
        "type": "Semi-Detached House",
        "tenure": "Available on request",
        "price": "S$9,500,000",
        "details": "6 bedrooms · 7 bathrooms · Land 3,175 sq ft",
        "description": "Modern luxury meets family comfort in this stunning 5,000 sq ft semi-detached home, where space, style and convenience come together.",
        "land_size": "3,175 sq ft",
        "built_up": "Approx. 5,000 sq ft",
        "top": "Available on request",
        "features": "Basement entertainment room or private gym, Grand living and dining area, Kitchen and powder room, Helper's room with bathroom, 4 bedrooms on Level 2 (2 en-suite and 2 sharing a bathroom), 2 en-suite bedrooms on Level 3, Bright and well-proportioned spaces for modern family living",
        "parking": "Wide frontage with parking for 2 cars",
        "schools": "Within 1km of Methodist Girls' School (Primary); close to Nanyang Primary, Henry Park Primary and Raffles Girls' Primary",
        "schools_list": "Methodist Girls' School (Primary)|Nanyang Primary|Henry Park Primary|Raffles Girls' Primary",
        "mrt": "650m from Sixth Avenue MRT",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty. Some photos or locations are withheld to respect the owner's privacy.",
        "image": "/static/img/HousesIMG/Fir%20Ave%201%20B5000/Fir%20Ave%201%20B5000%20landing.jpeg",
        "gallery": ["/static/img/HousesIMG/Fir%20Ave%201%20B5000/Fir%20Ave%201%20B5000%20landing.jpeg"],
    },
    {
        "name": "20 Dafne Street",
        "location": "D16 Bedok / Upper East Coast",
        "type": "Inter-Terrace House",
        "tenure": "Freehold",
        "price": "S$5,913,000",
        "details": "5+1 bedrooms · 6 bathrooms · Land 1,319 sq ft",
        "description": "Opera Estate: a brand-new 2.5-storey inter-terrace home with a mezzanine, attic and private home lift, designed for modern family living.",
        "land_size": "1,319 sq ft",
        "built_up": "4,263 sq ft",
        "top": "Q4 2026",
        "features": "5 bedrooms (2 en-suite), Bedroom 1 with dual-access bathroom, Helper's room with attached bathroom, Powder room, Double-volume living room ceiling, Household shelter, Mezzanine and attic, Private home lift, 1st Storey: living area, dining area, dry kitchen, wet kitchen, household shelter, powder room and helper's room, 2nd Storey: get-together corner, Bedroom 1 with dual-access bathroom and balcony, 3rd Storey: master bedroom, junior master bedroom, tea room and spacious family area, Attic: Bedrooms 4 and 5 with balconies and a common bathroom",
        "parking": "Car porch for 2 cars",
        "schools": "Within 1km of Opera Estate Primary School and St. Stephen's School; within 2km of Bedok Green Primary, Fengshan Primary, Ngee Ann Primary, Red Swastika School, Telok Kurau Primary and Yu Neng Primary",
        "schools_list": "Opera Estate Primary School|St. Stephen's School|Bedok Green Primary School|Fengshan Primary School|Ngee Ann Primary School|Red Swastika School|Telok Kurau Primary School|Yu Neng Primary School",
        "mrt": "9 mins walk to Bedok MRT; 1 min walk to Before Tosca St bus stop; close to Bedok Mall, Siglap Shopping Centre, East Coast Park and nearby parks",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "/static/img/HousesIMG/Dafne%20Street%2020/Defne%20Street%20Landing.png",
        "gallery": ["/static/img/HousesIMG/Dafne%20Street%2020/Defne%20Street%20Landing.png"],
        "is_launch": True,
    },
    {
        "name": "Upper East Coast Road",
        "location": "D16 Bedok / Upper East Coast",
        "type": "Corner Terrace",
        "tenure": "Available on request",
        "price": "S$5,500,000",
        "details": "3 storey · 9m frontage · Land 3,100 sq ft",
        "description": "A generously sized three-storey corner terrace on Upper East Coast Road, offering a 9m frontage, approximately 4,000 sq ft of floor space and easy access to East Coast lifestyle amenities.",
        "land_size": "3,100 sq ft",
        "built_up": "Est. 4,000 sq ft",
        "top": "Available on request",
        "features": "3 storey home with 9m frontage, East Coast Park nearby for cycling, jogging and outdoor dining, East Coast Lagoon Food Village nearby, Siglap South Community Centre and Bedok Community Centre nearby, Future Bedok South integrated community hub planned with sports and community facilities",
        "schools": "Temasek Primary and Temasek Secondary nearby; close to Chai Chee Secondary, Opera Estate Primary, Rosemount International School, GIIS Singapore and St. Andrew's Autism School",
        "schools_list": "Temasek Primary School|Temasek Secondary School|Chai Chee Secondary School|Opera Estate Primary School|Rosemount International School|GIIS Singapore|St. Andrew's Autism School",
        "mrt": "Near Siglap MRT, Tanah Merah MRT, Bayshore MRT and Bedok South MRT (opening in 2026); close to Siglap Centre, Siglap V, Bedok Point, Bedok Mall and Kaki Bukit Mall",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "/static/img/HousesIMG/Upper%20East%20Coast%20Road%20B4000/Upper%20East%20Coast%20Landing.JPG",
        "gallery": ["/static/img/HousesIMG/Upper%20East%20Coast%20Road%20B4000/Upper%20East%20Coast%20Landing.JPG"],
    },
    {
        "name": "28 Jalan Zamrud",
        "location": "D23 Hillview / Dairy Farm / Bukit Batok",
        "type": "Inter-Terrace House",
        "tenure": "Freehold",
        "price": "S$6,580,000",
        "details": "5+1 bedrooms · 6 bathrooms · Land 1,868 sq ft",
        "description": "Hillview Green Estate: a brand-new three-level inter-terrace home with an attic, generous family spaces and unblocked greenery views.",
        "land_size": "1,868 sq ft",
        "built_up": "3,875 sq ft",
        "top": "2026",
        "features": "5 bedrooms, Helper's room with attached bathroom, Open-concept dry kitchen, Enclosed wet kitchen, Double-volume dining ceiling, Family area or entertainment room, Household shelter, Greenery unblocked views, Solar panels, Isolator provision for EV charger",
        "parking": "Car porch for 2 cars",
        "mrt": "12 mins walk to Hillview MRT; 7 mins walk to Hillbrooks bus stop; 8 mins walk to Hillington Green Condo bus stop; 9 mins walk to Opp Hillbrooks bus stop",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "/static/img/HousesIMG/Jalan%20Zamrud%2028/Jalan%20Zamrud%2028%20Landing.png",
        "gallery": ["/static/img/HousesIMG/Jalan%20Zamrud%2028/Jalan%20Zamrud%2028%20Landing.png"],
        "is_launch": True,
    },
    {
        "name": "34A Mackerrow Road",
        "location": "D19 Serangoon / Kovan",
        "type": "Semi-Detached House",
        "tenure": "Available on request",
        "price": "S$9,480,000",
        "details": "7 en-suite bedrooms · 4 levels · Land 3,106 sq ft",
        "description": "The Duo in the heart of Braddell Heights Estate: a brand-new luxury semi-detached home designed as a modern multi-generational residence with exceptional space, privacy and contemporary architecture.",
        "land_size": "Approx. 3,106 sq ft",
        "built_up": "Approx. 7,200 sq ft",
        "top": "Estimated Q2 2027",
        "features": "Brand-new luxury semi-detached home, Prestigious Braddell Heights Estate, 4 expansive levels of living, 7 en-suite bedrooms, Designed for multi-generational living, Architectural design by LAB Architects, Designed by award-winning architect Brenda Ang",
        "parking": "Parking for up to 5 cars",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "/static/img/HousesIMG/Mackerrow%20Road%2034A/Mackerrow%20Road%2034A%20Landing.png",
        "gallery": ["/static/img/HousesIMG/Mackerrow%20Road%2034A/Mackerrow%20Road%2034A%20Landing.png"],
        "is_launch": True,
    },
    {
        "name": "34 Mackerrow Road",
        "location": "D19 Serangoon / Kovan",
        "type": "Semi-Detached House",
        "tenure": "Available on request",
        "price": "S$9,680,000",
        "details": "7 en-suite bedrooms · 4 levels · Land 3,209 sq ft",
        "description": "The Duo in the heart of Braddell Heights Estate: a brand-new luxury semi-detached home designed as a modern multi-generational residence with exceptional space, privacy and contemporary architecture.",
        "land_size": "Approx. 3,209 sq ft",
        "built_up": "Approx. 7,200 sq ft",
        "top": "Estimated Q2 2027",
        "features": "Brand-new luxury semi-detached home, Prestigious Braddell Heights Estate, 4 expansive levels of living, 7 en-suite bedrooms, Designed for multi-generational living, Architectural design by LAB Architects, Designed by award-winning architect Brenda Ang",
        "parking": "Parking for up to 5 cars",
        "note": "Information and measurements are approximate and subject to final survey; they do not form part of any offer, contract, or warranty.",
        "image": "/static/img/HousesIMG/Mackerrow%20Road%2034A/Mackerrow%20Road%2034A%20Landing.png",
        "gallery": ["/static/img/HousesIMG/Mackerrow%20Road%2034A/Mackerrow%20Road%2034A%20Landing.png"],
        "is_launch": True,
    },
]



def page_context(active_page, **extra):
    return {"active_page": active_page, "nav_items": NAV_ITEMS, **extra}

@app.context_processor
def shared_property_context():
    return {"featured_listings": LISTINGS}


@app.route("/")
def home():
    launch_listings = [listing for listing in LISTINGS if listing.get("is_launch")]
    just_listed = [listing for listing in reversed(LISTINGS) if not listing.get("is_launch")][:4]
    return render_template(
        "home.html",
        **page_context("home", launch_listings=launch_listings, just_listed_listings=just_listed),
    )


@app.route("/all-listings")
def listings():
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_district = request.args.get("district", "")
    selected_type = request.args.get("type", "")
    query = request.args.get("q", "").strip()
    selected_school = request.args.get("school", "").strip()
    filtered_listings = [listing for listing in LISTINGS if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold()) and (not selected_school or selected_school.casefold() in [school.casefold() for school in listing.get("schools_list", "").split("|")])]
    return render_template("listings.html", **page_context("listings", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type, query=query, selected_school=selected_school))


@app.route("/new-launches")
def launches():
    launch_listings = [listing for listing in LISTINGS if listing.get("is_launch")]
    districts = SINGAPORE_DISTRICTS
    property_types = PROPERTY_TYPES
    selected_district = request.args.get("district", "")
    selected_type = request.args.get("type", "")
    launch_category = request.args.get("category", "").strip().casefold()
    query = request.args.get("q", "").strip()
    landed_types = {"Terraced House", "Inter-Terrace House", "Corner Terrace", "Semi-Detached House", "Detached House", "Detached Bungalow", "Good Class Bungalow", "Cluster House", "Strata Landed"}
    condo_types = {"Condominium", "Executive Condominium", "Luxury Apartment", "Penthouse", "Service Residence"}
    category_types = landed_types if launch_category == "landed" else condo_types if launch_category == "condo" else None
    filtered_listings = [listing for listing in launch_listings if (not selected_district or listing["location"] == selected_district) and (not selected_type or listing["type"] == selected_type) and (not category_types or listing["type"] in category_types) and (not query or query.casefold() in " ".join(str(value) for value in listing.values()).casefold())]
    return render_template("listings.html", **page_context("launches", listings=filtered_listings, districts=districts, property_types=property_types, selected_district=selected_district, selected_type=selected_type, query=query, launch_category=launch_category))


@app.route("/for-rent")
def for_rent():
    return render_template("listings.html", **page_context("rent", listings=[], districts=SINGAPORE_DISTRICTS, property_types=PROPERTY_TYPES, selected_district="", selected_type="", query=""))


@app.route("/search-by-school")
def search_by_school():
    query = request.args.get("q", "").strip()
    schools = [school for school in SCHOOLS if not query or query.casefold() in school.casefold()]
    return render_template("school_search.html", **page_context("school-search", schools=schools, query=query))


@app.route("/property/<path:property_name>")
def property_detail(property_name):
    listing = next((item for item in LISTINGS if item["name"] == property_name), None)
    if listing is None:
        return "Property not found", 404
    gallery = listing.get("gallery", [listing["image"]])
    return render_template("property_detail.html", **page_context("listings", listing=listing, gallery=gallery))


@app.route("/services")
def services():
    return render_template("text_page.html", **page_context("services", eyebrow="Our services", heading="A better way to <em>move.</em>", intro="From the first conversation to the final signature, our advice is clear, considered, and entirely yours.", items=[
        {"title": "Buying, thoughtfully", "text": "A calm, informed search shaped around how you want to live, with access to homes you will not find everywhere.", "link_endpoint": "buy_with_us"},
        {"title": "Selling, beautifully", "text": "We tell the story of your home with precision, introduce it to the right people, and handle every detail."},
        {"title": "Letting, simply", "text": "Long-term partnerships for landlords who care about their property and the people who live in it."},
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
