def analyze(text: str):
    t = text.lower()

    if "water" in t:
        return {"category": "Water", "priority": "High"}

    if "road" in t:
        return {"category": "Road", "priority": "Medium"}

    if "electric" in t:
        return {"category": "Electricity", "priority": "Medium"}

    if "police" in t:
        return {"category": "Police", "priority": "High"}

    return {"category": "Other", "priority": "Low"}