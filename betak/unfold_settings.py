UNFOLD_CONFIG = {
    "SITE_TITLE": "لوحة تحكم الهضبة العقارية",
    "SITE_HEADER": "الهضبة العقارية",
    "SITE_SYMBOL": "apartment",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": False,
    "COLORS": {
        "primary": {
            "50": "#FFF7F2",
            "100": "#FFEAE0",
            "200": "#FFD1BD",
            "300": "#FFAF90",
            "400": "#FF815E",
            "500": "#E76F51", # Burnt Orange
            "600": "#D35A3E",
            "700": "#B0422B",
            "800": "#8E3320",
            "900": "#72291B",
            "950": "#3F130B",
        },
        "accent": {
            "50": "#F4FAF9",
            "100": "#D8EFEB",
            "200": "#B3DDD6",
            "300": "#83C4BA",
            "400": "#54A59A",
            "500": "#2A9D8F", # Teal Accent
            "600": "#228075",
            "700": "#1B675E",
            "800": "#16514B",
            "900": "#13433E",
            "950": "#0A2422",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "إدارة الموافقات والطلبات",
                "items": [
                    {
                        "title": "شاشة الموافقات (كروت)",
                        "icon": "gavel",
                        "link": lambda request: "/admin/approvals/",
                    }
                ]
            }
        ]
    }
}
