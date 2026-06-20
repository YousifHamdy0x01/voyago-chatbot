TRAINING_EXAMPLES = [
    # Hotels
    {"query": "أسعار فندق أوبرج الفيوم", "intent": "fayoum_hotels"},
    {"query": "Room in فندق أوبرج الفيوم kindly", "intent": "fayoum_hotels"},
    {"query": "أوضة في فندق كوم الدكة", "intent": "fayoum_hotels"},
    {"query": "Fayoum hotels kindly", "intent": "fayoum_hotels"},
    {"query": "فندق في الفيوم", "intent": "fayoum_hotels"},
    {"query": "I need a hotel in Fayoum", "intent": "fayoum_hotels"},
    {"query": "عايز اعلى فندق تقييم", "intent": "fayoum_hotels"},
    {"query": "ارخص فندق في الفيوم", "intent": "fayoum_hotels"},
    {"query": "احسن فندق", "intent": "fayoum_hotels"},
    {"query": "عايز احجز فندق", "intent": "fayoum_hotels"},

    # Attractions
    {"query": "أماكن سياحية في الفيوم", "intent": "fayoum_attractions"},
    {"query": "tourist places fayoum", "intent": "fayoum_attractions"},
    {"query": "وين أروح في الفيوم", "intent": "fayoum_attractions"},
    {"query": "what to visit in fayoum", "intent": "fayoum_attractions"},
    {"query": "أشهر مناطق الفيوم", "intent": "fayoum_attractions"},
    {"query": "اماكن جميلة في الفيوم", "intent": "fayoum_attractions"},
    {"query": "best places fayoum", "intent": "fayoum_attractions"},

    # Restaurants
    {"query": "مطاعم في الفيوم", "intent": "fayoum_restaurants"},
    {"query": "restaurants in fayoum", "intent": "fayoum_restaurants"},
    {"query": "أكل في الفيوم", "intent": "fayoum_restaurants"},
    {"query": "where to eat fayoum", "intent": "fayoum_restaurants"},
    {"query": "أحسن مطعم في الفيوم", "intent": "fayoum_restaurants"},
    {"query": "عايز اكل", "intent": "fayoum_restaurants"},
    {"query": "ارخص مطعم", "intent": "fayoum_restaurants"},

    # Tour Guides
    {"query": "مرشد سياحي في الفيوم", "intent": "fayoum_tourguides"},
    {"query": "tour guide fayoum", "intent": "fayoum_tourguides"},
    {"query": "محتاج دليل سياحي", "intent": "fayoum_tourguides"},
    {"query": "I need a guide in fayoum", "intent": "fayoum_tourguides"},
    {"query": "guide touristique fayoum", "intent": "fayoum_tourguides"},
    {"query": "محتاج حد يرشدني", "intent": "fayoum_tourguides"},

    # Emergency
    {"query": "شرطة الفيوم", "intent": "fayoum_emergency"},
    {"query": "Security Fayoum", "intent": "fayoum_emergency"},
    {"query": "حادث الفيوم مساعدة", "intent": "fayoum_emergency"},
    {"query": "ambulance fayoum", "intent": "fayoum_emergency"},
    {"query": "اسعاف الفيوم", "intent": "fayoum_emergency"},
    {"query": "emergency fayoum", "intent": "fayoum_emergency"},
    {"query": "محتاج نجدة", "intent": "fayoum_emergency"},
    {"query": "فيه حادثة", "intent": "fayoum_emergency"},
]

INTENT_CONFIG = {
    "fayoum_hotels": {
        "action": "open_fayoum_hotels",
        "navigate_to": "/hotels",
        "endpoint": "http://voyagoo.runasp.net/hotels",
    },
    "fayoum_attractions": {
        "action": "open_fayoum_attractions",
        "navigate_to": "/Attractions",
        "endpoint": "http://voyagoo.runasp.net/Attractions",
    },
    "fayoum_restaurants": {
        "action": "open_fayoum_restaurants",
        "navigate_to": "/Restaurants",
        "endpoint": "http://voyagoo.runasp.net/Restaurants",
    },
    "fayoum_tourguides": {
        "action": "open_fayoum_tourguides",
        "navigate_to": "/tour-guide",
        "endpoint": "http://voyagoo.runasp.net/TourGuides",
    },
    "fayoum_emergency": {
        "action": "display_fayoum_emergency",
        "navigate_to": None,
        "endpoint": None,
    }
}