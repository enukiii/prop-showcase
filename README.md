# SS Property Showcase

A small Flask/Jinja property showcase with seven navigation tabs:

- Home
- All Listings
- New Launches
- Services
- Resources
- About Us
- Contact

## Run the website

Double-click `run.bat`. It installs the dependency, opens the website, and starts the local server.
Website address: `http://127.0.0.1:5000`

Keep the black terminal window open while using the website. Press `Ctrl+C` in that window to stop it.

## Property listing data

The app reads property listings from `data/listings.json`. The original district CSV files are retained, but are no longer loaded by the app.

Each JSON listing has a stable `id` for its detail-page URL. Edit its facts in the JSON record. Add optional marketing copy, highlights, nearby schools, and transport under `editorial`; keep `verified` set to `false` until those details have been checked. The app only displays editorial fields after `verified` is set to `true`.

Property photos remain under `static/img/HousesIMG`. Each listing's `images` object in `data/listings.json` names its folder and relative landing, floor-plan, interior, and gallery files. Shared property folders can be referenced by multiple listings. Missing media is represented by `null` or an empty list until the image is added.