"""
Generate a CSV that mirrors the Kaggle 'Sample - Superstore.csv' schema.
Run once:  python generate_data.py
Output  :  data/Sample - Superstore.csv
"""

import csv, random, os
from datetime import datetime, timedelta

random.seed(42)

# ---------- reference lists ----------
SHIP_MODES    = ["Standard Class", "Second Class", "First Class", "Same Day"]
SEGMENTS      = ["Consumer", "Corporate", "Home Office"]
REGIONS       = ["West", "East", "Central", "South"]

STATES_BY_REGION = {
    "West":    ["California", "Washington", "Oregon", "Colorado", "Arizona", "Nevada", "Utah"],
    "East":    ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Virginia", "Connecticut", "Maryland"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan", "Indiana", "Minnesota", "Wisconsin"],
    "South":   ["Florida", "Georgia", "North Carolina", "Tennessee", "Kentucky", "Alabama", "Louisiana"],
}

CITIES_BY_STATE = {
    "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
    "Washington": ["Seattle", "Tacoma", "Spokane"],
    "Oregon": ["Portland", "Salem", "Eugene"],
    "Colorado": ["Denver", "Colorado Springs"],
    "Arizona": ["Phoenix", "Tucson"],
    "Nevada": ["Las Vegas", "Reno"],
    "Utah": ["Salt Lake City", "Provo"],
    "New York": ["New York City", "Buffalo", "Rochester", "Albany"],
    "Pennsylvania": ["Philadelphia", "Pittsburgh", "Harrisburg"],
    "Massachusetts": ["Boston", "Cambridge", "Springfield"],
    "New Jersey": ["Newark", "Jersey City", "Trenton"],
    "Virginia": ["Richmond", "Virginia Beach", "Arlington"],
    "Connecticut": ["Hartford", "New Haven", "Stamford"],
    "Maryland": ["Baltimore", "Annapolis", "Rockville"],
    "Texas": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
    "Illinois": ["Chicago", "Springfield", "Naperville"],
    "Ohio": ["Columbus", "Cleveland", "Cincinnati"],
    "Michigan": ["Detroit", "Grand Rapids", "Ann Arbor"],
    "Indiana": ["Indianapolis", "Fort Wayne"],
    "Minnesota": ["Minneapolis", "Saint Paul"],
    "Wisconsin": ["Milwaukee", "Madison"],
    "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville"],
    "Georgia": ["Atlanta", "Savannah", "Augusta"],
    "North Carolina": ["Charlotte", "Raleigh", "Durham"],
    "Tennessee": ["Nashville", "Memphis", "Knoxville"],
    "Kentucky": ["Louisville", "Lexington", "Henderson"],
    "Alabama": ["Birmingham", "Montgomery"],
    "Louisiana": ["New Orleans", "Baton Rouge"],
}

CATEGORIES = {
    "Furniture": {
        "sub_categories": ["Bookcases", "Chairs", "Tables", "Furnishings"],
        "products": {
            "Bookcases":  ["Sauder Classic Bookcase", "O'Sullivan Bookcase", "Bush Westfield Bookcase", "Hon Bookcase"],
            "Chairs":     ["Hon Deluxe Chair", "Global Leather Chair", "Bretford Folding Chair", "Office Star Chair"],
            "Tables":     ["Bretford Round Table", "Chromcraft Table", "KI Adjustable Table", "Bevis Round Table"],
            "Furnishings":["Eldon Shelf", "Tenex Rug Pad", "Dana Mirror", "Howard Miller Clock"],
        },
        "price_range": (30, 1200),
        "profit_margin": (-0.25, 0.30),
    },
    "Office Supplies": {
        "sub_categories": ["Labels", "Storage", "Art", "Binders", "Paper", "Envelopes", "Fasteners", "Supplies", "Appliances"],
        "products": {
            "Labels":     ["Avery Labels", "Self-Adhesive Labels", "Avery Round Labels"],
            "Storage":    ["Fellowes Banker Box", "Safco Organizer", "Rubbermaid CleverStore"],
            "Art":        ["Newell Markers Set", "Prang Coloring Pencils", "Fiskars Scissors"],
            "Binders":    ["GBC Premium Binder", "Avery Binder", "Wilson Jones Binder"],
            "Paper":      ["Xerox Multipurpose Paper", "HP Copy Paper", "Hammermill Paper"],
            "Envelopes":  ["Staple Manila Envelope", "Poly String Envelope", "Tyvek Envelopes"],
            "Fasteners":  ["Advantus Clip Pack", "Staple Paper Clips", "OIC Binder Clips"],
            "Supplies":   ["Acme Stapler", "BIC Ballpoint Pens", "Sanford Highlighters"],
            "Appliances": ["Belkin Surge Protector", "Hamilton Beach Toaster", "Hoover Vacuum"],
        },
        "price_range": (2, 300),
        "profit_margin": (-0.10, 0.45),
    },
    "Technology": {
        "sub_categories": ["Phones", "Accessories", "Copiers", "Machines"],
        "products": {
            "Phones":      ["Cisco IP Phone", "AT&T Cordless Phone", "Motorola Smartphone", "Samsung Galaxy Phone"],
            "Accessories": ["Logitech Wireless Mouse", "Belkin USB Hub", "Kensington Laptop Lock", "Targus Laptop Bag"],
            "Copiers":     ["Canon ImageClass Copier", "HP LaserJet Copier", "Brother Copier"],
            "Machines":    ["Hewlett-Packard Laptop", "Lexmark Printer", "Brother Fax Machine", "Canon PC Printer"],
        },
        "price_range": (10, 2500),
        "profit_margin": (-0.15, 0.50),
    },
}

# ---------- generation ----------
NUM_ROWS = 9994  # matches the real dataset size
START = datetime(2019, 1, 1)
END   = datetime(2022, 12, 31)
DAYS  = (END - START).days

rows = []
order_counter = 0

for i in range(1, NUM_ROWS + 1):
    # Order timing
    if i == 1 or random.random() < 0.35:
        order_counter += 1
        order_date = START + timedelta(days=random.randint(0, DAYS))
    ship_delay = {"Standard Class": (3,7), "Second Class": (2,5), "First Class": (1,3), "Same Day": (0,0)}
    ship_mode = random.choice(SHIP_MODES)
    lo, hi = ship_delay[ship_mode]
    ship_date = order_date + timedelta(days=random.randint(lo, hi))

    order_id = f"US-{order_date.year}-{order_counter:06d}"
    customer_id = f"CG-{random.randint(10000,99999)}"

    # Location
    region = random.choice(REGIONS)
    state  = random.choice(STATES_BY_REGION[region])
    city   = random.choice(CITIES_BY_STATE[state])
    postal_code = random.randint(10000, 99999)

    # Product
    segment  = random.choice(SEGMENTS)
    category = random.choice(list(CATEGORIES.keys()))
    cat_info = CATEGORIES[category]
    sub_cat  = random.choice(cat_info["sub_categories"])
    product  = random.choice(cat_info["products"][sub_cat])
    product_id = f"{category[:3].upper()}-{sub_cat[:2].upper()}-{random.randint(1000,9999)}"

    # Financials
    lo_p, hi_p = cat_info["price_range"]
    sales    = round(random.uniform(lo_p, hi_p), 2)
    quantity = random.randint(1, 9)
    discount = random.choice([0.0, 0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40])
    margin   = random.uniform(*cat_info["profit_margin"])
    if discount >= 0.30:
        margin -= 0.15   # heavy discounts eat profit
    profit = round(sales * quantity * margin, 2)
    sales  = round(sales * quantity * (1 - discount), 2)

    # Customer names (simple)
    first_names = ["Aaron","Beth","Carlos","Diana","Ethan","Fiona","Greg","Hannah","Ivan","Julia",
                   "Ken","Laura","Mike","Nina","Oscar","Priya","Quinn","Rachel","Sean","Tina"]
    last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Moore",
                   "Anderson","Thomas","Jackson","White","Harris","Martin","Clark","Lewis","Hall","Allen"]
    cust_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    rows.append([
        i,  # Row ID
        order_id,
        order_date.strftime("%m/%d/%Y"),
        ship_date.strftime("%m/%d/%Y"),
        ship_mode,
        customer_id,
        cust_name,
        segment,
        "United States",
        city,
        state,
        postal_code,
        region,
        product_id,
        category,
        sub_cat,
        product,
        sales,
        quantity,
        discount,
        profit,
    ])

os.makedirs("data", exist_ok=True)
with open("data/Sample - Superstore.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        "Row ID","Order ID","Order Date","Ship Date","Ship Mode",
        "Customer ID","Customer Name","Segment","Country","City",
        "State","Postal Code","Region","Product ID","Category",
        "Sub-Category","Product Name","Sales","Quantity","Discount","Profit",
    ])
    w.writerows(rows)

print(f"✅ Created data/Sample - Superstore.csv  ({len(rows):,} rows)")
