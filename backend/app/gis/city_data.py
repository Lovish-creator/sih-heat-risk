"""
SIH26083 Comprehensive Pan-India Municipal Ward Profiles Database.
Contains official municipal delimitation metadata, Census PCA demographics,
and authentic locality templates across all regions of India.
"""

from typing import Dict, Any

MUNICIPAL_WARD_PROFILES: Dict[str, Dict[str, Any]] = {
    # ------------------ NORTH INDIA ------------------
    "abohar": {
        "city_name": "Abohar",
        "state_name": "Punjab",
        "district_name": "Fazilka",
        "total_wards": 50,
        "center": {"lat": 30.14505, "lon": 74.19566},
        "radius_km": 3.8,
        "tot_population": 145300,
        "census_source": "Census of India 2011 PCA & Punjab Municipal Corporation Delimitation (50 Wards)",
        "locality_templates": [
            ("Nai Abadi North", "Dense Residential", "LCZ 3 Compact Low-Rise", 1.08, 1.15, 1.4),
            ("Gaushala Road", "Residential / Commercial", "LCZ 2 Compact Mid-Rise", 1.05, 0.95, 1.2),
            ("Gobind Nagari", "Residential", "LCZ 3 Compact Low-Rise", 1.00, 0.90, 1.1),
            ("Circular Road", "Commercial Corridor", "LCZ 2 Compact Mid-Rise", 1.06, 1.05, 1.3),
            ("Patel Nagar", "Residential Core", "LCZ 3 Compact Low-Rise", 1.02, 0.85, 1.0),
            ("Seed Farm Area", "Agricultural Outskirts", "LCZ D Low Plants/Agri", 0.96, 1.35, 0.6),
            ("Fazilka Road", "Transit & Warehouse", "LCZ 8 Large Low-Rise", 1.03, 1.30, 0.8),
            ("Old Grain Market", "Dense Wholesale Market", "LCZ 3 Compact Low-Rise", 1.10, 1.45, 1.6),
            ("Dharm Nagari", "High Density Core", "LCZ 3 Compact Low-Rise", 1.07, 1.10, 1.5),
            ("Sant Nagar", "Residential", "LCZ 3 Compact Low-Rise", 1.01, 0.90, 1.0),
            ("Defense Road", "Mixed Development", "LCZ 6 Open Low-Rise", 0.98, 1.00, 0.7),
            ("Hanumangarh Road", "Industrial & Labor Cluster", "LCZ 10 Heavy Industry", 1.09, 1.50, 1.2),
            ("Indira Nagari", "Informal Settlement", "LCZ 7 Lightweight Low-Rise", 1.08, 1.40, 1.7),
            ("New Grain Market", "Wholesale Market / Loading", "LCZ 8 Large Low-Rise", 1.11, 1.55, 1.4),
            ("Malout Road", "Transport Hub", "LCZ 8 Large Low-Rise", 1.04, 1.25, 0.9),
            ("Industrial Estate", "Industrial Heavy Metal / Processing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.1),
            ("Subhash Nagar", "High Density Residential", "LCZ 3 Compact Low-Rise", 1.06, 1.05, 1.3),
            ("Major Harjit Singh Ward", "Central Residential", "LCZ 3 Compact Low-Rise", 1.02, 0.95, 1.1)
        ]
    },
    "amritsar": {
        "city_name": "Amritsar",
        "state_name": "Punjab",
        "district_name": "Amritsar",
        "total_wards": 85,
        "center": {"lat": 31.6340, "lon": 74.8723},
        "radius_km": 7.5,
        "tot_population": 1132383,
        "census_source": "Census of India 2011 PCA - Municipal Corporation Amritsar (MCA)",
        "locality_templates": [
            ("Walled City (Golden Temple Zone)", "Heritage & Ultra-Dense Core", "LCZ 3 Compact Low-Rise", 1.08, 1.25, 2.4),
            ("Hall Bazaar / Katra Jaimal Singh", "Dense Commercial Wholesale", "LCZ 2 Compact Mid-Rise", 1.07, 1.20, 2.2),
            ("Civil Lines / Lawrence Road", "Planned Commercial / Institutional", "LCZ 5 Open Mid-Rise", 0.99, 0.75, 0.8),
            ("Ranjit Avenue", "Modern Planned Commercial", "LCZ 5 Open Mid-Rise", 1.01, 0.80, 0.9),
            ("Chheharta Industrial Area", "Textile & Heavy Manufacturing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.3),
            ("Putlighar", "Dense Mixed Commercial / Residential", "LCZ 3 Compact Low-Rise", 1.06, 1.15, 1.8),
            ("Verka Focal Point", "Industrial & Dairy Processing", "LCZ 8 Large Low-Rise", 1.09, 1.45, 1.1),
            ("Batala Road Suburbs", "Suburban Residential Growth", "LCZ 6 Open Low-Rise", 1.00, 0.90, 0.9)
        ]
    },
    "ludhiana": {
        "city_name": "Ludhiana",
        "state_name": "Punjab",
        "district_name": "Ludhiana",
        "total_wards": 95,
        "center": {"lat": 30.9010, "lon": 75.8573},
        "radius_km": 8.5,
        "tot_population": 1618879,
        "census_source": "Census of India 2011 PCA - Municipal Corporation Ludhiana (MCL)",
        "locality_templates": [
            ("Focal Point Industrial Phases", "Heavy Engineering / Hosiery Hub", "LCZ 10 Heavy Industry", 1.14, 1.65, 1.4),
            ("Chaura Bazaar / Old City", "Ultra-Dense Commercial Core", "LCZ 3 Compact Low-Rise", 1.09, 1.30, 2.5),
            ("Sarabha Nagar", "Affluent Low-Density Residential", "LCZ 6 Open Low-Rise", 0.98, 0.70, 0.7),
            ("Model Town", "Planned Residential / Commercial", "LCZ 5 Open Mid-Rise", 1.01, 0.80, 0.9),
            ("Gill Road / Industrial Area B", "Bicycle & Auto-Parts Industrial", "LCZ 10 Heavy Industry", 1.13, 1.60, 1.5),
            ("Shimlapuri / Daba", "High-Density Worker Settlements", "LCZ 7 Lightweight Low-Rise", 1.08, 1.45, 2.0),
            ("BRS Nagar", "Planned Residential West", "LCZ 6 Open Low-Rise", 0.99, 0.75, 0.8),
            ("Rahon Road Outskirts", "Semi-Industrial Peri-Urban", "LCZ 9 Sparsely Built", 1.02, 1.30, 0.7)
        ]
    },
    "delhi": {
        "city_name": "Delhi",
        "state_name": "Delhi",
        "district_name": "Delhi",
        "total_wards": 50,
        "center": {"lat": 28.6139, "lon": 77.2090},
        "radius_km": 14.0,
        "tot_population": 16787941,
        "census_source": "Census of India 2011 PCA - Municipal Corporation of Delhi (MCD)",
        "locality_templates": [
            ("Chandni Chowk", "Walled City Commercial Core", "LCZ 3 Compact Low-Rise", 1.10, 1.35, 2.5),
            ("Connaught Place", "Central Business District", "LCZ 2 Compact Mid-Rise", 1.05, 0.90, 1.2),
            ("Karol Bagh", "High Density Commercial", "LCZ 2 Compact Mid-Rise", 1.07, 1.15, 1.8),
            ("Okhla Industrial Area", "Industrial / Manufacturing Hub", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.4),
            ("Mayapuri", "Industrial Scrap & Auto Hub", "LCZ 10 Heavy Industry", 1.11, 1.55, 1.3),
            ("Anand Vihar", "Transit Hub & East Delhi Core", "LCZ 4 Open High-Rise", 1.06, 1.25, 1.6),
            ("Rohini Sector 1-15", "High-Density Planned Residential", "LCZ 4 Open High-Rise", 1.01, 0.85, 1.1),
            ("Narela Industrial", "Outer Industrial North", "LCZ 8 Large Low-Rise", 1.09, 1.50, 0.9),
            ("Lajpat Nagar", "South Delhi Dense Commercial", "LCZ 2 Compact Mid-Rise", 1.03, 0.85, 1.3),
            ("Civil Lines", "North Low Density / Greenery", "LCZ B Scattered Trees", 0.97, 0.70, 0.6),
            ("Shahdara North", "East Ultra-High Density Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.0),
            ("Dwarka Sector 1-22", "Planned Sub-city South West", "LCZ 4 Open High-Rise", 0.98, 0.80, 0.9)
        ]
    },
    "chandigarh": {
        "city_name": "Chandigarh",
        "state_name": "Chandigarh",
        "district_name": "Chandigarh",
        "total_wards": 35,
        "center": {"lat": 30.7333, "lon": 76.7794},
        "radius_km": 5.5,
        "tot_population": 1055450,
        "census_source": "Census of India 2011 PCA - Municipal Corporation Chandigarh (MCC)",
        "locality_templates": [
            ("Sector 17 (City Center)", "Central Commercial Plaza", "LCZ 5 Open Mid-Rise", 1.03, 0.85, 1.0),
            ("Sector 22 (Aroma / Market)", "Dense Commercial / Residential", "LCZ 5 Open Mid-Rise", 1.04, 0.95, 1.3),
            ("Industrial Area Phase I & II", "Manufacturing & Auto Cluster", "LCZ 8 Large Low-Rise", 1.10, 1.55, 1.1),
            ("Manimajra / NAC", "High Density Fringe Zone", "LCZ 3 Compact Low-Rise", 1.06, 1.20, 1.6),
            ("Sector 9 & 10 (High End)", "Low Density Green Residential", "LCZ 6 Open Low-Rise", 0.97, 0.65, 0.6),
            ("Dhanas / Rehab Colonies", "High Density Informal Settlement", "LCZ 7 Lightweight Low-Rise", 1.07, 1.40, 1.9),
            ("Sector 35 / 36 Commercial", "Commercial & Institutional Hub", "LCZ 5 Open Mid-Rise", 1.02, 0.85, 1.1)
        ]
    },
    "lucknow": {
        "city_name": "Lucknow",
        "state_name": "Uttar Pradesh",
        "district_name": "Lucknow",
        "total_wards": 110,
        "center": {"lat": 26.8467, "lon": 80.9462},
        "radius_km": 10.0,
        "tot_population": 2817105,
        "census_source": "Census of India 2011 PCA - Lucknow Municipal Corporation (LMC)",
        "locality_templates": [
            ("Hazratganj", "Central Business District", "LCZ 2 Compact Mid-Rise", 1.04, 0.85, 1.2),
            ("Chowk / Old City", "Heritage & Ultra-Dense Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.4),
            ("Aminabad", "Dense Wholesale Market Hub", "LCZ 3 Compact Low-Rise", 1.09, 1.35, 2.3),
            ("Gomti Nagar", "Planned High-Rise / Commercial", "LCZ 4 Open High-Rise", 0.99, 0.75, 0.8),
            ("Talkatora Industrial Area", "Heavy Engineering / Processing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.3),
            ("Alambagh", "Transit Hub & High Density Rail Zone", "LCZ 2 Compact Mid-Rise", 1.06, 1.25, 1.7),
            ("Indira Nagar", "Planned Residential Sector", "LCZ 6 Open Low-Rise", 1.00, 0.80, 0.9),
            ("Chinhat Peri-Urban", "Eastern Suburban Growth Fringe", "LCZ 9 Sparsely Built", 1.01, 1.20, 0.7)
        ]
    },
    "jaipur": {
        "city_name": "Jaipur",
        "state_name": "Rajasthan",
        "district_name": "Jaipur",
        "total_wards": 100,
        "center": {"lat": 26.9124, "lon": 75.7873},
        "radius_km": 11.0,
        "tot_population": 3046163,
        "census_source": "Census of India 2011 PCA - Jaipur Heritage & Greater Municipal Corporations",
        "locality_templates": [
            ("Walled City (Johari / Bapu Bazaar)", "Heritage Dense Commercial Core", "LCZ 3 Compact Low-Rise", 1.09, 1.30, 2.6),
            ("MI Road / C-Scheme", "Central Commercial & Institutional", "LCZ 5 Open Mid-Rise", 1.02, 0.80, 1.0),
            ("Sitapura Industrial Area", "Export Zone & Manufacturing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.2),
            ("Vishwakarma (VKIA) Industrial", "Heavy Metal & Marble Cutting", "LCZ 10 Heavy Industry", 1.13, 1.65, 1.3),
            ("Mansarovar", "Large Planned Residential Sector", "LCZ 6 Open Low-Rise", 1.00, 0.85, 1.0),
            ("Vaishali Nagar", "Western Planned Residential", "LCZ 6 Open Low-Rise", 0.99, 0.80, 0.9),
            ("Sanganer", "Textile Dyeing & Airport Cluster", "LCZ 8 Large Low-Rise", 1.07, 1.45, 1.5),
            ("Jagatpura", "South-East High Rise Expansion", "LCZ 4 Open High-Rise", 1.01, 0.90, 0.8)
        ]
    },

    # ------------------ WEST INDIA ------------------
    "ahmedabad": {
        "city_name": "Ahmedabad",
        "state_name": "Gujarat",
        "district_name": "Ahmedabad",
        "total_wards": 48,
        "center": {"lat": 23.0225, "lon": 72.5714},
        "radius_km": 11.5,
        "tot_population": 5577940,
        "census_source": "Census of India 2011 PCA - Ahmedabad Municipal Corporation (AMC)",
        "locality_templates": [
            ("Navrangpura", "Commercial/Institutional", "LCZ 5 Open Mid-Rise", 1.02, 0.75, 0.9),
            ("Paldi", "Residential", "LCZ 5 Open Mid-Rise", 1.01, 0.80, 0.95),
            ("Sabarmati", "Residential/Transit", "LCZ 6 Open Low-Rise", 1.00, 0.95, 1.0),
            ("Jamalpur", "Walled City Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.1),
            ("Khadia", "Dense Heritage Core", "LCZ 3 Compact Low-Rise", 1.07, 1.15, 2.0),
            ("Shahpur", "Central Dense", "LCZ 3 Compact Low-Rise", 1.06, 1.20, 1.8),
            ("Maninagar", "Residential South", "LCZ 5 Open Mid-Rise", 1.01, 0.90, 1.1),
            ("Vatva GIDC", "Heavy Chemical & Textile Industrial", "LCZ 10 Heavy Industry", 1.12, 1.65, 1.3),
            ("Danilimda", "Industrial Fringe", "LCZ 7 Lightweight Low-Rise", 1.08, 1.40, 1.5),
            ("Naroda GIDC", "Heavy Industrial East", "LCZ 10 Heavy Industry", 1.11, 1.60, 1.4),
            ("Bapunagar", "Textile/Dense Residential", "LCZ 3 Compact Low-Rise", 1.07, 1.35, 1.7),
            ("Gomtipur", "Labor & Industrial", "LCZ 7 Lightweight Low-Rise", 1.08, 1.40, 1.6),
            ("Odhav GIDC", "Industrial East", "LCZ 10 Heavy Industry", 1.10, 1.55, 1.2),
            ("Chandkheda", "North Suburban", "LCZ 6 Open Low-Rise", 0.97, 0.85, 0.8),
            ("Ghatlodia", "Residential North West", "LCZ 5 Open Mid-Rise", 0.99, 0.90, 1.0),
            ("Bodakdev", "Modern Commercial West", "LCZ 4 Open High-Rise", 1.00, 0.70, 0.8),
            ("Thaltej", "New West Residential", "LCZ 4 Open High-Rise", 0.98, 0.75, 0.75),
            ("Jodhpur", "New West Residential", "LCZ 4 Open High-Rise", 0.99, 0.80, 0.85),
            ("Sarkhej", "South West Fringe", "LCZ 8 Large Low-Rise", 1.04, 1.25, 1.1),
            ("Vejalpur", "South West Residential", "LCZ 5 Open Mid-Rise", 1.01, 0.95, 1.1)
        ]
    },
    "surat": {
        "city_name": "Surat",
        "state_name": "Gujarat",
        "district_name": "Surat",
        "total_wards": 30,
        "center": {"lat": 21.1702, "lon": 72.8311},
        "radius_km": 10.0,
        "tot_population": 4467797,
        "census_source": "Census of India 2011 PCA - Surat Municipal Corporation (SMC)",
        "locality_templates": [
            ("Varachha (Diamond Bourse Hub)", "Ultra-Dense Diamond Cutting & Polishing", "LCZ 2 Compact Mid-Rise", 1.08, 1.35, 2.5),
            ("Katargam", "Industrial Diamond & Dense Living", "LCZ 2 Compact Mid-Rise", 1.07, 1.30, 2.3),
            ("Pandesara GIDC", "Heavy Textile Dyeing & Chemicals", "LCZ 10 Heavy Industry", 1.13, 1.65, 1.4),
            ("Sachin GIDC", "Industrial SEZ / Heavy Manufacturing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.2),
            ("Athwa Lines", "Affluent Coastal / Riverfront", "LCZ 5 Open Mid-Rise", 0.98, 0.70, 0.7),
            ("Rander / Adajan", "Western Planned Residential", "LCZ 5 Open Mid-Rise", 1.00, 0.80, 0.9),
            ("Udhna Industrial", "Textile Weaving & Engineering", "LCZ 8 Large Low-Rise", 1.10, 1.55, 1.5),
            ("Bhestan / Dindoli", "Migrant Labor Settlement", "LCZ 7 Lightweight Low-Rise", 1.08, 1.45, 1.9)
        ]
    },
    "mumbai": {
        "city_name": "Mumbai",
        "state_name": "Maharashtra",
        "district_name": "Mumbai",
        "total_wards": 24,
        "center": {"lat": 19.0760, "lon": 72.8777},
        "radius_km": 13.0,
        "tot_population": 12442373,
        "census_source": "Census of India 2011 PCA - Brihanmumbai Municipal Corporation (BMC)",
        "locality_templates": [
            ("Ward A (Colaba / Fort)", "Commercial / Heritage", "LCZ 2 Compact Mid-Rise", 1.01, 0.85, 1.2),
            ("Ward B (Sandhurst Road)", "High Density Coastal", "LCZ 2 Compact Mid-Rise", 1.04, 1.20, 2.3),
            ("Ward C (Marine Lines)", "Dense Commercial / Residential", "LCZ 2 Compact Mid-Rise", 1.03, 1.10, 2.1),
            ("Ward D (Malabar Hill)", "Residential Coastal", "LCZ 5 Open Mid-Rise", 0.97, 0.70, 0.8),
            ("Ward E (Byculla)", "Central Mixed Industrial", "LCZ 3 Compact Low-Rise", 1.06, 1.30, 1.9),
            ("Ward F/South (Parel)", "Former Mill Area / Commercial", "LCZ 1 Compact High-Rise", 1.05, 1.10, 1.6),
            ("Ward F/North (Matunga)", "Residential Educational", "LCZ 5 Open Mid-Rise", 1.01, 0.85, 1.2),
            ("Ward G/South (Worli)", "Coastal Mixed / High Rise", "LCZ 4 Open High-Rise", 1.00, 0.90, 1.3),
            ("Ward G/North (Dharavi / Dadar)", "Ultra-Dense Informal / Industrial", "LCZ 7 Lightweight Low-Rise", 1.10, 1.55, 2.8),
            ("Ward H/East (Santacruz E)", "Suburban Dense Transit", "LCZ 3 Compact Low-Rise", 1.05, 1.25, 1.7),
            ("Ward H/West (Bandra W)", "Coastal Residential", "LCZ 5 Open Mid-Rise", 0.98, 0.75, 1.0),
            ("Ward K/East (Andheri E)", "Industrial / IT Hub / Airport", "LCZ 8 Large Low-Rise", 1.09, 1.45, 1.5),
            ("Ward K/West (Andheri W)", "Commercial / Residential", "LCZ 4 Open High-Rise", 1.02, 0.90, 1.3),
            ("Ward L (Kurla)", "Dense Central Transit Hub", "LCZ 3 Compact Low-Rise", 1.08, 1.40, 2.2),
            ("Ward M/East (Govandi / Chembur E)", "Refinery / High Vulnerability", "LCZ 10 Heavy Industry", 1.12, 1.60, 2.4),
            ("Ward M/West (Chembur W)", "Residential Suburban", "LCZ 5 Open Mid-Rise", 1.02, 0.95, 1.1),
            ("Ward N (Ghatkopar)", "Central Suburb Mixed", "LCZ 3 Compact Low-Rise", 1.04, 1.15, 1.5),
            ("Ward P/South (Goregaon S)", "Commercial / Industrial Hub", "LCZ 8 Large Low-Rise", 1.05, 1.20, 1.3),
            ("Ward P/North (Malad N)", "Dense Western Suburb", "LCZ 3 Compact Low-Rise", 1.04, 1.25, 1.6),
            ("Ward R/South (Kandivali)", "Residential / Industrial", "LCZ 4 Open High-Rise", 1.03, 1.15, 1.3),
            ("Ward R/Central (Borivali)", "Western Suburb Core", "LCZ 5 Open Mid-Rise", 1.00, 0.85, 1.1),
            ("Ward R/North (Dahisar)", "Northern Outskirts", "LCZ 6 Open Low-Rise", 0.99, 1.05, 0.9),
            ("Ward S (Bhandup)", "Industrial / Slum Clusters", "LCZ 7 Lightweight Low-Rise", 1.09, 1.50, 1.8),
            ("Ward T (Mulund)", "Planned Suburb East", "LCZ 5 Open Mid-Rise", 1.01, 0.85, 1.0)
        ]
    },
    "pune": {
        "city_name": "Pune",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "total_wards": 58,
        "center": {"lat": 18.5204, "lon": 73.8567},
        "radius_km": 11.0,
        "tot_population": 3124458,
        "census_source": "Census of India 2011 PCA - Pune Municipal Corporation (PMC)",
        "locality_templates": [
            ("Shivajinagar / FC Road", "Educational & Institutional Hub", "LCZ 5 Open Mid-Rise", 1.01, 0.75, 1.0),
            ("Kasba Peth / Old Core", "Dense Historical Peth Core", "LCZ 3 Compact Low-Rise", 1.07, 1.25, 2.3),
            ("Hadapsar / Magarpatta", "IT Park & Manufacturing Hub", "LCZ 4 Open High-Rise", 1.05, 1.15, 1.3),
            ("Bhosari / Pimpri Industrial", "Automobile & Heavy Engineering", "LCZ 10 Heavy Industry", 1.13, 1.65, 1.4),
            ("Kothrud", "High Density Residential West", "LCZ 5 Open Mid-Rise", 0.99, 0.80, 1.1),
            ("Viman Nagar / Kharadi", "IT Hub & Modern Residential", "LCZ 4 Open High-Rise", 1.01, 0.85, 1.0),
            ("Swargate / Dhankawadi", "South Transit & Dense Residential", "LCZ 3 Compact Low-Rise", 1.06, 1.30, 1.8),
            ("Katraj Peri-Urban", "Southern Valley Fringe", "LCZ 6 Open Low-Rise", 0.98, 0.95, 0.8)
        ]
    },
    "indore": {
        "city_name": "Indore",
        "state_name": "Madhya Pradesh",
        "district_name": "Indore",
        "total_wards": 85,
        "center": {"lat": 22.7196, "lon": 75.8577},
        "radius_km": 8.5,
        "tot_population": 1994397,
        "census_source": "Census of India 2011 PCA - Indore Municipal Corporation (IMC)",
        "locality_templates": [
            ("Rajwada / Sarafa", "Historical Commercial Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.4),
            ("Vijay Nagar", "Modern Commercial & IT Corridor", "LCZ 4 Open High-Rise", 1.01, 0.75, 0.9),
            ("Sanwer Road Industrial Area", "Heavy Industrial & Chemical", "LCZ 10 Heavy Industry", 1.13, 1.65, 1.3),
            ("Pithampur Industrial Corridor", "Auto Manufacturing & Pharma Hub", "LCZ 10 Heavy Industry", 1.14, 1.70, 1.2),
            ("Palasia / Old Palasia", "Commercial & Residential Core", "LCZ 5 Open Mid-Rise", 1.02, 0.80, 1.0),
            ("Rau / Silicon City", "South-Western Suburban Corridor", "LCZ 6 Open Low-Rise", 0.99, 0.85, 0.8),
            ("Bhawarkua", "Student & High Density Commercial", "LCZ 3 Compact Low-Rise", 1.05, 1.10, 1.7)
        ]
    },

    # ------------------ SOUTH INDIA ------------------
    "bengaluru": {
        "city_name": "Bengaluru",
        "state_name": "Karnataka",
        "district_name": "Bengaluru Urban",
        "total_wards": 60,
        "center": {"lat": 12.9716, "lon": 77.5946},
        "radius_km": 13.5,
        "tot_population": 8443675,
        "census_source": "Census of India 2011 PCA - Bruhat Bengaluru Mahanagara Palike (BBMP)",
        "locality_templates": [
            ("Chickpet / Majestic", "Ultra-Dense Commercial / Transit Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.6),
            ("MG Road / CBD", "Central Business District", "LCZ 1 Compact High-Rise", 1.03, 0.80, 1.1),
            ("Peenya Industrial Area", "Heavy Machinery & MSME Manufacturing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.3),
            ("Whitefield / ITPL", "Tech Corridor & High Density SEZ", "LCZ 4 Open High-Rise", 1.04, 1.10, 1.2),
            ("Electronic City", "IT Corridor & Manufacturing South", "LCZ 4 Open High-Rise", 1.04, 1.10, 1.1),
            ("Jayanagar / JP Nagar", "Planned Green Residential South", "LCZ 5 Open Mid-Rise", 0.98, 0.70, 0.8),
            ("Indiranagar / Koramangala", "Commercial & Upscale Residential", "LCZ 5 Open Mid-Rise", 1.01, 0.75, 0.9),
            ("Hebbal / Manyata Tech Park", "North Transit & Tech Hub", "LCZ 4 Open High-Rise", 1.02, 0.90, 1.0),
            ("Bommanahalli", "Dense Mixed Worker Settlement", "LCZ 3 Compact Low-Rise", 1.06, 1.35, 1.8),
            ("Yelahanka Peri-Urban", "North Suburban Growth Corridor", "LCZ 6 Open Low-Rise", 0.97, 0.85, 0.7)
        ]
    },
    "chennai": {
        "city_name": "Chennai",
        "state_name": "Tamil Nadu",
        "district_name": "Chennai",
        "total_wards": 60,
        "center": {"lat": 13.0827, "lon": 80.2707},
        "radius_km": 12.5,
        "tot_population": 4646732,
        "census_source": "Census of India 2011 PCA - Greater Chennai Corporation (GCC)",
        "locality_templates": [
            ("George Town / Parrys", "Ultra-Dense Port & Commercial Core", "LCZ 3 Compact Low-Rise", 1.07, 1.35, 2.5),
            ("T. Nagar", "High Density Retail Commercial Hub", "LCZ 2 Compact Mid-Rise", 1.06, 1.20, 2.0),
            ("Ambattur Industrial Estate", "Automobile & Engineering Hub", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.3),
            ("Guindy Industrial / IT", "Industrial & Tech Corridor", "LCZ 8 Large Low-Rise", 1.08, 1.40, 1.4),
            ("OMR / Thoraipakkam", "IT Expressway Corridor", "LCZ 4 Open High-Rise", 1.02, 0.95, 1.1),
            ("Mylapore / Triplicane", "Coastal Heritage & Residential", "LCZ 3 Compact Low-Rise", 1.01, 0.85, 1.4),
            ("Anna Nagar", "Planned High-Standard Residential", "LCZ 5 Open Mid-Rise", 0.99, 0.75, 0.8),
            ("Ennore / Manali", "Petrochemical & Thermal Power Hub", "LCZ 10 Heavy Industry", 1.14, 1.65, 1.2)
        ]
    },
    "hyderabad": {
        "city_name": "Hyderabad",
        "state_name": "Telangana",
        "district_name": "Hyderabad",
        "total_wards": 60,
        "center": {"lat": 17.3850, "lon": 78.4867},
        "radius_km": 13.0,
        "tot_population": 6809970,
        "census_source": "Census of India 2011 PCA - Greater Hyderabad Municipal Corporation (GHMC)",
        "locality_templates": [
            ("Charminar / Old City", "Heritage & Ultra-Dense Commercial Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.6),
            ("Hitec City / Madhapur", "IT Corridor & Modern High-Rise", "LCZ 4 Open High-Rise", 1.02, 0.80, 1.0),
            ("Jeedimetla Industrial Area", "Chemical & Pharma Manufacturing", "LCZ 10 Heavy Industry", 1.13, 1.65, 1.3),
            ("Balanagar / Sanathnagar", "Heavy Engineering Hub", "LCZ 10 Heavy Industry", 1.11, 1.55, 1.4),
            ("Banjara Hills / Jubilee Hills", "Affluent Low-Density Green Core", "LCZ 6 Open Low-Rise", 0.97, 0.65, 0.6),
            ("Secunderabad / Station", "Dense Transit & Commercial Hub", "LCZ 2 Compact Mid-Rise", 1.05, 1.25, 1.7),
            ("Kukatpally / KPHB", "High Density Residential Suburb", "LCZ 4 Open High-Rise", 1.02, 0.90, 1.3),
            ("LB Nagar / Nagole", "Eastern Transit Corridor", "LCZ 5 Open Mid-Rise", 1.01, 1.05, 1.1)
        ]
    },

    # ------------------ EAST & NORTH-EAST INDIA ------------------
    "kolkata": {
        "city_name": "Kolkata",
        "state_name": "West Bengal",
        "district_name": "Kolkata",
        "total_wards": 60,
        "center": {"lat": 22.5726, "lon": 88.3639},
        "radius_km": 11.0,
        "tot_population": 4496694,
        "census_source": "Census of India 2011 PCA - Kolkata Municipal Corporation (KMC)",
        "locality_templates": [
            ("Bara Bazar / Burrabazar", "Ultra-Dense Commercial Wholesale Core", "LCZ 2 Compact Mid-Rise", 1.08, 1.35, 2.7),
            ("BBD Bagh / Esplanade", "Colonial Administrative / CBD", "LCZ 2 Compact Mid-Rise", 1.03, 0.85, 1.2),
            ("Taratala / Hyde Road", "Heavy Engineering / Port Logistic Hub", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.3),
            ("Salt Lake (Bidhannagar)", "Planned Sector / IT Hub", "LCZ 5 Open Mid-Rise", 0.99, 0.75, 0.8),
            ("New Town / Rajarhat", "Modern Tech Hub & High-Rise", "LCZ 4 Open High-Rise", 1.01, 0.80, 0.8),
            ("Shyambazar / North Kolkata", "Dense Heritage Residential", "LCZ 3 Compact Low-Rise", 1.06, 1.15, 2.0),
            ("Gariahat / South Kolkata", "Commercial & High Density Living", "LCZ 2 Compact Mid-Rise", 1.03, 0.95, 1.4),
            ("Topsia / Tangra", "Former Tannery & Dense Settlements", "LCZ 7 Lightweight Low-Rise", 1.09, 1.45, 1.9)
        ]
    },
    "patna": {
        "city_name": "Patna",
        "state_name": "Bihar",
        "district_name": "Patna",
        "total_wards": 75,
        "center": {"lat": 25.5941, "lon": 85.1376},
        "radius_km": 8.5,
        "tot_population": 1684222,
        "census_source": "Census of India 2011 PCA - Patna Municipal Corporation (PMC)",
        "locality_templates": [
            ("Patna City / Chowk", "Historical Ultra-Dense Core", "LCZ 3 Compact Low-Rise", 1.08, 1.30, 2.5),
            ("Frazer Road / Dak Bungalow", "Central Commercial Corridor", "LCZ 2 Compact Mid-Rise", 1.04, 0.90, 1.3),
            ("Patliputra Industrial Estate", "Industrial MSME / Logistics", "LCZ 8 Large Low-Rise", 1.10, 1.55, 1.2),
            ("Kankarbagh", "Large Dense Residential Colony", "LCZ 5 Open Mid-Rise", 1.02, 0.95, 1.3),
            ("Boring Road", "High Density Commercial / Student Hub", "LCZ 2 Compact Mid-Rise", 1.04, 0.90, 1.5),
            ("Danapur Cantonment Area", "Western Fringe & Transit", "LCZ 6 Open Low-Rise", 0.98, 0.85, 0.8),
            ("Phulwari Sharif", "South-Western Dense Settlement", "LCZ 3 Compact Low-Rise", 1.06, 1.35, 1.7)
        ]
    },
    "guwahati": {
        "city_name": "Guwahati",
        "state_name": "Assam",
        "district_name": "Kamrup Metropolitan",
        "total_wards": 60,
        "center": {"lat": 26.1445, "lon": 91.7362},
        "radius_km": 7.5,
        "tot_population": 957352,
        "census_source": "Census of India 2011 PCA - Guwahati Municipal Corporation (GMC)",
        "locality_templates": [
            ("Fancy Bazaar / Pan Bazaar", "Commercial Wholesale Hub", "LCZ 2 Compact Mid-Rise", 1.07, 1.30, 2.4),
            ("Paltan Bazaar / Station", "Dense Transit & Commercial Corridor", "LCZ 2 Compact Mid-Rise", 1.06, 1.25, 1.8),
            ("Noonmati Refinery Area", "Petroleum Refinery & Heavy Processing", "LCZ 10 Heavy Industry", 1.12, 1.60, 1.2),
            ("Dispur / Capital Complex", "Administrative & Institutional", "LCZ 5 Open Mid-Rise", 1.00, 0.75, 0.9),
            ("Ganeshguri / GS Road", "Modern Commercial Corridor", "LCZ 4 Open High-Rise", 1.03, 0.85, 1.1),
            ("Maligaon / Railway HQ", "Railway & Residential Cluster", "LCZ 5 Open Mid-Rise", 1.01, 1.05, 1.2),
            ("Jalukbari / University Fringe", "Western Outskirts / Greenery", "LCZ B Scattered Trees", 0.96, 0.70, 0.6)
        ]
    }
}
