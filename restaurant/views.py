from django.shortcuts import render
import random
import time

def main(request):
    return render(request, 'restaurant/main.html')

# ----- Simple Korean menu: (id, label, price) -----
MENU = [
    ("bibimbap",       "Bibimbap",            12.00),
    ("bulgogi_bowl",   "Bulgogi Beef Bowl",   14.00),
    ("kimchi_jjigae",  "Kimchi Jjigae",       11.00),
    ("tteokbokki",     "Tteokbokki",           8.00),
]

# ----- Simple specials: (id, name, price, short desc) -----
SPECIALS = [
    ("galbi",              "Galbi Short Ribs",          18.00, "soy-garlic glaze"),
    ("yangnyeom_chicken",  "Yangnyeom Fried Chicken",   15.00, "sweet & spicy glaze"),
]

def order(request):
    # choose one special for this page render
    daily = random.choice(SPECIALS)  # tuple: (id, name, price, desc)
    return render(request, "restaurant/order.html", {
        "menu": MENU,
        "daily": {
            "id": daily[0], "name": daily[1], "price": daily[2], "desc": daily[3]
        }
    })

def confirmation(request):
    template = 'restaurant/confirmation.html'

    # If the form wasn't posted, just show a friendly empty state
    if not request.POST:
        context = {
            "empty_order": True,
            "customer": {"name": "", "phone": "", "email": "", "instructions": ""},
        }
        return render(request, template, context)

    # --- Read form data like in the class example ---
    selected = request.POST.getlist("items")            # e.g., ["bibimbap", "daily"]
    daily_id = request.POST.get("daily_id", "")

    customer = {
        "name": request.POST.get("customer_name", "").strip(),
        "phone": request.POST.get("customer_phone", "").strip(),
        "email": request.POST.get("customer_email", "").strip(),
        "instructions": request.POST.get("instructions", "").strip(),
    }

    # Price lookups (match our simple MENU/SPECIALS from earlier)
    menu_map = {i: (label, price) for (i, label, price) in MENU}
    specials_map = {i: (name, price) for (i, name, price, _desc) in SPECIALS}

    # Build items + total
    items_out = []
    total = 0.0

    # Regular items
    for item_id in selected:
        if item_id == "daily":
            continue
        if item_id in menu_map:
            label, price = menu_map[item_id]
            items_out.append({"label": label, "price": price})
            total += price

    # Daily special (if chosen)
    if "daily" in selected and daily_id in specials_map:
        name, price = specials_map[daily_id]
        items_out.append({"label": f"Today’s Special: {name}", "price": price})
        total += price

    # If nothing was selected, still render confirmation (simple like the sample)
    if not items_out:
        context = {"empty_order": True, "customer": customer}
        return render(request, template, context)

    # Ready time: 30–60 min from now using time module
    minutes = random.randint(30, 60)
    ready_ts = time.time() + minutes * 60
    ready_str = time.strftime("%a %b %d, %I:%M %p", time.localtime(ready_ts)).lstrip("0")

    context = {
        "items": items_out,
        "total": round(total, 2),
        "ready_at": ready_str,
        "customer": customer,
    }
    return render(request, template, context)
