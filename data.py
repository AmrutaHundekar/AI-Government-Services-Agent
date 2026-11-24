SCHEMES = [
    {
        "id": "post-matric-demo",
        "name": "Post-Matric Scholarship (Demo Record)",
        "category": "Scholarship",
        "level": "State / Central",
        "description": "Illustrative scholarship record for students pursuing education after Class 10.",
        "benefits": "Financial assistance toward eligible education expenses; amount varies by category and rules.",
        "min_age": 15, "max_age": 30, "max_income": 250000,
        "student_required": True, "states": ["Karnataka", "All India"],
        "documents": ["Recent photograph", "Previous examination marks card", "Bonafide/student certificate",
                      "Income certificate (if required)", "Category certificate (if applicable)", "Bank account proof"],
        "official_url": "https://scholarships.gov.in/"
    },
    {
        "id": "national-means-demo",
        "name": "National Means-cum-Merit Scholarship (Demo Record)",
        "category": "School Scholarship",
        "level": "Central",
        "description": "Illustrative record representing a merit-and-means school scholarship.",
        "benefits": "Scholarship support subject to official examination, income and continuation rules.",
        "min_age": 10, "max_age": 18, "max_income": 350000,
        "student_required": True, "states": ["All India"],
        "documents": ["School bonafide certificate", "Previous class marks card", "Income certificate",
                      "Bank account proof", "Photograph"],
        "official_url": "https://scholarships.gov.in/"
    },
    {
        "id": "pm-kisan-demo",
        "name": "PM-KISAN (Demo Record)",
        "category": "Farmer Support",
        "level": "Central",
        "description": "Illustrative record for a farmer-support service; actual exclusions and land rules apply.",
        "benefits": "Income support subject to official eligibility and verification.",
        "min_age": 18, "max_age": 100, "max_income": None,
        "student_required": False, "states": ["All India"],
        "documents": ["Landholding records", "Identity proof", "Bank account details", "Mobile number"],
        "official_url": "https://pmkisan.gov.in/"
    },
    {
        "id": "skill-demo",
        "name": "Skill Development Training (Demo Record)",
        "category": "Training",
        "level": "Central / State",
        "description": "Illustrative record for discovering skill-development training opportunities.",
        "benefits": "Training and certification may be available through approved centres.",
        "min_age": 18, "max_age": 35, "max_income": None,
        "student_required": False, "states": ["Karnataka", "All India"],
        "documents": ["Identity proof", "Address proof", "Education certificate", "Photograph"],
        "official_url": "https://www.skillindiadigital.gov.in/"
    }
]
