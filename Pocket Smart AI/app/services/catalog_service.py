from urllib.parse import quote_plus


CATALOG = {

    "home": [

        {
            "name":
            "Modern LED Ceiling Light",

            "category":
            "lighting",

            "price":
            1499,

            "platform":
            "Amazon"
        },

        {
            "name":
            "Minimalist Ceiling Fan",

            "category":
            "fan",

            "price":
            2999,

            "platform":
            "Amazon"
        },

        {
            "name":
            "Compact 4-Seater Dining Table",

            "category":
            "dining",

            "price":
            8999,

            "platform":
            "IKEA"
        },

        {
            "name":
            "Wall Art Set",

            "category":
            "decor",

            "price":
            1299,

            "platform":
            "Flipkart"
        },

        {
            "name":
            "Storage Cabinet",

            "category":
            "storage",

            "price":
            4999,

            "platform":
            "IKEA"
        },

        {
            "name":
            "Accent Floor Lamp",

            "category":
            "lighting",

            "price":
            2199,

            "platform":
            "IKEA"
        }
    ],


    "party": [

        {
            "name":
            "Catering Package",

            "category":
            "food",

            "price":
            350,

            "unit":
            "guest",

            "platform":
            "Zomato"
        },

        {
            "name":
            "Party Decoration Package",

            "category":
            "decoration",

            "price":
            5000,

            "platform":
            "Amazon"
        },

        {
            "name":
            "Event Venue Search",

            "category":
            "venue",

            "price":
            15000,

            "platform":
            "OYO"
        },

        {
            "name":
            "Cake & Dessert Options",

            "category":
            "food",

            "price":
            2500,

            "platform":
            "Swiggy"
        },

        {
            "name":
            "Table Decoration Kit",

            "category":
            "decoration",

            "price":
            1799,

            "platform":
            "Amazon"
        }
    ],


    "jewelry": [

        {
            "name":
            "Gold-Tone Jhumka Earrings",

            "category":
            "earrings",

            "price":
            899,

            "platform":
            "Amazon"
        },

        {
            "name":
            "Pearl Drop Earrings",

            "category":
            "earrings",

            "price":
            1299,

            "platform":
            "Flipkart"
        },

        {
            "name":
            "Delicate Necklace Set",

            "category":
            "necklace",

            "price":
            1699,

            "platform":
            "Amazon"
        },

        {
            "name":
            "Minimal Bracelet",

            "category":
            "bracelet",

            "price":
            799,

            "platform":
            "Flipkart"
        },

        {
            "name":
            "Statement Necklace",

            "category":
            "necklace",

            "price":
            2499,

            "platform":
            "Amazon"
        }
    ]
}


PLATFORM_URLS = {

    "Amazon":
    "https://www.amazon.in/s?k={query}",

    "Flipkart":
    "https://www.flipkart.com/search?q={query}",

    "IKEA":
    "https://www.ikea.com/in/en/search/?q={query}",

    "Swiggy":
    "https://www.swiggy.com/search?query={query}",

    "Zomato":
    "https://www.zomato.com/search?q={query}",

    "OYO":
    "https://www.oyorooms.com/search?location={query}"
}


def product_link(
    platform: str,
    query: str
):

    template = PLATFORM_URLS.get(
        platform
    )

    if not template:

        return "#"

    return template.format(
        query=quote_plus(query)
    )


def catalog_for(
    planner_type: str
):

    return [
        dict(item)
        for item in
        CATALOG.get(
            planner_type,
            []
        )
    ]