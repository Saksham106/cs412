# File: restaurant/views.py
# Author: Saksham Goel (saksham@bu.edu), 09/15/2025
# Description: Views for the restaurant app. Renders the main page,
# shows the order form with a randomized daily special, and processes
# the order to display a confirmation page.

from django.shortcuts import render
import random
import time

# MENU: list of (id, label, price). Prices are in USD.
MENU = [
    ("bibimbap", "Bibimbap", 12.00),
    ("bulgogi_bowl", "Bulgogi Beef Bowl", 14.00),
    ("kimchi_jjigae", "Kimchi Jjigae", 11.00),
    ("tteokbokki", "Tteokbokki", 8.00),
]

# SPECIALS: list of (id, name, price, short_description).
SPECIALS = [
    ("galbi", "Galbi Short Ribs", 18.00, "soy-garlic glaze"),
    ("yangnyeom_chicken", "Yangnyeom Fried Chicken", 15.00, "sweet & spicy glaze"),
]


def main(request):
    """Render the main/landing page."""
    return render(request, "restaurant/main.html")


def order(request):
    """Render the order page with one randomly chosen daily special."""
    # Choose one special for this page render.
    special = random.choice(SPECIALS)
    context = {
        "menu": MENU,
        "daily": {"id": special[0], "name": special[1], "price": special[2], "desc": special[3]},
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    """
    Process the posted order and render the confirmation page.

    - Reads selected items from POST.
    - Extra option for Tteokbokki (spice level).
    - Adds up the prices and shows a ready time 30-60 minutes from now.
    """
    template = "restaurant/confirmation.html"

    # If the form wasn't posted, show a simple empty state.
    if not request.POST:
        context = {
            "empty_order": True,
            "customer": {"name": "", "phone": "", "email": "", "instructions": ""},
        }
        return render(request, template, context)

    # Read submitted form data.
    selected_ids = request.POST.getlist("items")     # e.g., ["bibimbap", "daily"]
    daily_id = request.POST.get("daily_id", "")
    tteok_spice = request.POST.get("tteokbokki_spice", "").strip()

    # Customer information fields.
    customer = {
        "name": request.POST.get("customer_name", "").strip(),
        "phone": request.POST.get("customer_phone", "").strip(),
        "email": request.POST.get("customer_email", "").strip(),
        "instructions": request.POST.get("instructions", "").strip(),
    }

    # Build quick lookup tables for prices.
    menu_map = {mid: (label, price) for (mid, label, price) in MENU}
    specials_map = {sid: (name, price) for (sid, name, price, _desc) in SPECIALS}

    # Process selected items + calculate total.
    items_out = []
    total = 0.0

    # Add selected regular menu items.
    for item_id in selected_ids:
        if item_id == "daily":
            continue

        if item_id in menu_map:
            label, price = menu_map[item_id]

            if item_id == "tteokbokki" and tteok_spice:
                label = f"{label} (Spice: {tteok_spice})"

            items_out.append({"label": label, "price": price})
            total += price

    # Add the daily special if it was selected.
    if "daily" in selected_ids and daily_id in specials_map:
        name, price = specials_map[daily_id]
        items_out.append({"label": f"Today’s Special: {name}", "price": price})
        total += price

    if not items_out:
        return render(request, template, {"empty_order": True, "customer": customer})

    # Time calculation
    minutes = random.randint(30, 60)
    ready_ts = time.time() + (minutes * 60)
    ready_str = time.strftime("%a %b %d, %I:%M %p", time.localtime(ready_ts)).lstrip("0")

    context = {
        "items": items_out,
        "total": round(total, 2),
        "ready_at": ready_str,
        "customer": customer,
    }
    return render(request, template, context)
