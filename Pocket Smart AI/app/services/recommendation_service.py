from app.services.catalog_service import (
    catalog_for,
    product_link
)

from app.services.gemini_service import (
    generate_recommendation
)


def safe_number(
    value,
    default=0
):

    try:

        return float(value)

    except Exception:

        return default


def home_fallback(
    payload
):

    budget = float(
        payload["budget"]
    )

    catalog = catalog_for(
        "home"
    )

    requested_items = (
        payload["items"]
    )

    selected = []

    remaining = budget

    for requested in requested_items:

        wanted = (
            requested["name"]
            .lower()
        )

        quantity = requested[
            "quantity"
        ]

        matches = [

            item

            for item in catalog

            if any(

                word in
                item["name"].lower()

                for word in
                wanted.split()

                if len(word) > 3
            )
        ]

        if matches:

            item = matches[0]

        else:

            item = catalog[
                len(selected)
                %
                len(catalog)
            ]

        affordable_quantity = min(

            quantity,

            max(
                1,
                int(
                    remaining
                    //
                    item["price"]
                )
            )
        )

        if affordable_quantity:

            subtotal = (
                item["price"]
                *
                affordable_quantity
            )

            selected.append({

                "name":
                item["name"],

                "category":
                item["category"],

                "estimated_price":
                item["price"],

                "quantity":
                affordable_quantity,

                "platform":
                item["platform"],

                "reason":
                (
                    f"Fits the requested "
                    f"{requested['name']} "
                    f"category and style."
                ),

                "link":
                product_link(
                    item["platform"],
                    item["name"]
                ),

                "subtotal":
                subtotal
            })

            remaining -= subtotal

    return {

        "summary":
        (
            f"A {payload['style']} "
            f"{payload['room_type']} "
            f"plan was created "
            f"within a budget of "
            f"₹{budget:,.0f}."
        ),

        "allocation": {

            "products":
            round(
                budget - remaining,
                2
            ),

            "remaining":
            round(
                remaining,
                2
            )
        },

        "recommendations":
        selected
    }


def party_fallback(
    payload
):

    budget = float(
        payload["budget"]
    )

    guests = int(
        payload["guests"]
    )

    food_total = min(
        budget * 0.45,
        guests * 350
    )

    decoration = min(
        budget * 0.20,
        5000
    )

    venue = min(
        budget * 0.25,
        15000
    )

    entertainment = max(
        0,
        budget
        -
        food_total
        -
        decoration
        -
        venue
    )

    items = [

        {
            "name":
            "Catering Package",

            "category":
            "food",

            "estimated_price":
            round(
                food_total / guests,
                2
            ),

            "quantity":
            guests,

            "platform":
            "Zomato",

            "reason":
            (
                f"Food allowance "
                f"for {guests} guests."
            ),

            "link":
            product_link(
                "Zomato",
                payload["event_type"]
            ),

            "subtotal":
            round(
                food_total,
                2
            )
        },

        {
            "name":
            "Party Decoration Package",

            "category":
            "decoration",

            "estimated_price":
            round(
                decoration,
                2
            ),

            "quantity":
            1,

            "platform":
            "Amazon",

            "reason":
            "Decoration allowance based on the total budget.",

            "link":
            product_link(
                "Amazon",
                "party decoration"
            ),

            "subtotal":
            round(
                decoration,
                2
            )
        },

        {
            "name":
            "Event Venue Search",

            "category":
            "venue",

            "estimated_price":
            round(
                venue,
                2
            ),

            "quantity":
            1,

            "platform":
            "OYO",

            "reason":
            "Venue/accommodation search allowance.",

            "link":
            product_link(
                "OYO",
                payload["city"]
            ),

            "subtotal":
            round(
                venue,
                2
            )
        }
    ]

    return {

        "summary":
        (
            f"A {payload['event_type']} "
            f"budget plan for "
            f"{guests} guests was created. "
            f"Vendor prices are estimates, "
            f"not live quotes."
        ),

        "allocation": {

            "food":
            round(food_total, 2),

            "decoration":
            round(decoration, 2),

            "venue":
            round(venue, 2),

            "entertainment_or_buffer":
            round(entertainment, 2)
        },

        "recommendations":
        items
    }


def jewelry_fallback(
    payload
):

    budget = float(
        payload["budget"]
    )

    catalog = catalog_for(
        "jewelry"
    )

    selected = []

    remaining = budget

    for item in catalog:

        if (
            item["price"]
            <= remaining
            and
            len(selected) < 3
        ):

            selected.append({

                **item,

                "quantity":
                1,

                "estimated_price":
                item["price"],

                "reason":
                (
                    f"Selected as a "
                    f"{payload['style']} "
                    f"option for a "
                    f"{payload['occasion']} "
                    f"occasion."
                ),

                "link":
                product_link(
                    item["platform"],
                    item["name"]
                ),

                "subtotal":
                item["price"]
            })

            remaining -= item["price"]

    return {

        "summary":
        (
            f"Jewelry suggestions "
            f"for a "
            f"{payload['occasion']} "
            f"occasion, using "
            f"{payload['style']} "
            f"styling and a "
            f"₹{budget:,.0f} budget."
        ),

        "allocation": {

            "jewelry":
            round(
                budget - remaining,
                2
            ),

            "remaining":
            round(
                remaining,
                2
            )
        },

        "recommendations":
        selected
    }


def create_recommendation(
    planner_type,
    payload,
    image_path=None
):

    fallback_functions = {

        "home":
        home_fallback,

        "party":
        party_fallback,

        "jewelry":
        jewelry_fallback
    }

    fallback_function = (
        fallback_functions[
            planner_type
        ]
    )

    catalog = catalog_for(
        planner_type
    )

    ai_result = (
        generate_recommendation(
            planner_type,
            payload,
            catalog,
            image_path=image_path
        )
    )

    if (
        isinstance(ai_result, dict)
        and
        isinstance(
            ai_result.get(
                "recommendations"
            ),
            list
        )
    ):

        result = ai_result

        source = "gemini"

    else:

        result = fallback_function(
            payload
        )

        source = "fallback"

    for item in result.get(
        "recommendations",
        []
    ):

        platform = item.get(
            "platform",
            "Amazon"
        )

        name = item.get(
            "name",
            "product"
        )

        item["link"] = (
            item.get("link")
            or
            product_link(
                platform,
                name
            )
        )

        if "subtotal" not in item:

            price = safe_number(
                item.get(
                    "estimated_price"
                )
            )

            quantity = max(
                1,
                int(
                    item.get(
                        "quantity",
                        1
                    )
                )
            )

            item["subtotal"] = round(
                price * quantity,
                2
            )

    result["source"] = source

    return result