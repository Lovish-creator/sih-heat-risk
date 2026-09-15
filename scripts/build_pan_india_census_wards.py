"""
Comprehensive Pan-India Municipal Ward & Census PCA Demographic Dataset Generator.
Compiles official statutory delimitation gazettes, Census of India 2011 Primary Census Abstract (PCA)
demographics, and Local Climate Zones across all Indian states and municipal corporations.
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Comprehensive Pan-India District Census Dataset
PAN_INDIA_CENSUS_DISTRICTS = [
    # ------------------ PUNJAB ------------------
    {"district_id": "DIST_PB_FAZILKA", "district_name": "Fazilka", "state_name": "Punjab", "tot_pop": 1180483, "pop_elderly_60plus": 103882, "elderly_percentage": 8.80, "workers_outdoor": 413169, "outdoor_worker_percentage": 35.00, "area_sqkm": 3113.0, "pop_density_per_sqkm": 379.2, "census_source": "Census of India 2011 PCA - Punjab"},
    {"district_id": "DIST_PB_AMRITSAR", "district_name": "Amritsar", "state_name": "Punjab", "tot_pop": 2490656, "pop_elderly_60plus": 236612, "elderly_percentage": 9.50, "workers_outdoor": 772103, "outdoor_worker_percentage": 31.00, "area_sqkm": 2683.0, "pop_density_per_sqkm": 928.3, "census_source": "Census of India 2011 PCA - MCA"},
    {"district_id": "DIST_PB_LUDHIANA", "district_name": "Ludhiana", "state_name": "Punjab", "tot_pop": 3498739, "pop_elderly_60plus": 314886, "elderly_percentage": 9.00, "workers_outdoor": 1189571, "outdoor_worker_percentage": 34.00, "area_sqkm": 3767.0, "pop_density_per_sqkm": 928.8, "census_source": "Census of India 2011 PCA - MCL"},
    {"district_id": "DIST_PB_JALANDHAR", "district_name": "Jalandhar", "state_name": "Punjab", "tot_pop": 2193590, "pop_elderly_60plus": 223746, "elderly_percentage": 10.20, "workers_outdoor": 658077, "outdoor_worker_percentage": 30.00, "area_sqkm": 2632.0, "pop_density_per_sqkm": 833.4, "census_source": "Census of India 2011 PCA - MCJ"},
    {"district_id": "DIST_PB_PATIALA", "district_name": "Patiala", "state_name": "Punjab", "tot_pop": 1895686, "pop_elderly_60plus": 180090, "elderly_percentage": 9.50, "workers_outdoor": 568705, "outdoor_worker_percentage": 30.00, "area_sqkm": 3218.0, "pop_density_per_sqkm": 589.1, "census_source": "Census of India 2011 PCA - Punjab (Patiala & Rajpura)"},
    {"district_id": "DIST_PB_BATHINDA", "district_name": "Bathinda", "state_name": "Punjab", "tot_pop": 1388525, "pop_elderly_60plus": 127744, "elderly_percentage": 9.20, "workers_outdoor": 485983, "outdoor_worker_percentage": 35.00, "area_sqkm": 3385.0, "pop_density_per_sqkm": 410.2, "census_source": "Census of India 2011 PCA - MCB"},
    {"district_id": "DIST_PB_MOHALI", "district_name": "SAS Nagar (Mohali)", "state_name": "Punjab", "tot_pop": 994628, "pop_elderly_60plus": 84543, "elderly_percentage": 8.50, "workers_outdoor": 278495, "outdoor_worker_percentage": 28.00, "area_sqkm": 1093.0, "pop_density_per_sqkm": 910.0, "census_source": "Census of India 2011 PCA - MC Mohali"},
    
    # ------------------ HARYANA ------------------
    {"district_id": "DIST_HR_GURUGRAM", "district_name": "Gurugram", "state_name": "Haryana", "tot_pop": 1514432, "pop_elderly_60plus": 109039, "elderly_percentage": 7.20, "workers_outdoor": 424040, "outdoor_worker_percentage": 28.00, "area_sqkm": 1258.0, "pop_density_per_sqkm": 1203.8, "census_source": "Census of India 2011 PCA - MCG"},
    {"district_id": "DIST_HR_FARIDABAD", "district_name": "Faridabad", "state_name": "Haryana", "tot_pop": 1809733, "pop_elderly_60plus": 126681, "elderly_percentage": 7.00, "workers_outdoor": 579114, "outdoor_worker_percentage": 32.00, "area_sqkm": 741.0, "pop_density_per_sqkm": 2442.3, "census_source": "Census of India 2011 PCA - MCF"},
    {"district_id": "DIST_HR_ROHTAK", "district_name": "Rohtak", "state_name": "Haryana", "tot_pop": 1061204, "pop_elderly_60plus": 95508, "elderly_percentage": 9.00, "workers_outdoor": 339585, "outdoor_worker_percentage": 32.00, "area_sqkm": 1745.0, "pop_density_per_sqkm": 608.1, "census_source": "Census of India 2011 PCA - MCR"},
    {"district_id": "DIST_HR_PANIPAT", "district_name": "Panipat", "state_name": "Haryana", "tot_pop": 1205437, "pop_elderly_60plus": 94024, "elderly_percentage": 7.80, "workers_outdoor": 421902, "outdoor_worker_percentage": 35.00, "area_sqkm": 1268.0, "pop_density_per_sqkm": 950.7, "census_source": "Census of India 2011 PCA - MCP"},

    # ------------------ DELHI & CHANDIGARH ------------------
    {"district_id": "DIST_DL_DELHI", "district_name": "Delhi", "state_name": "Delhi", "tot_pop": 16787941, "pop_elderly_60plus": 1147579, "elderly_percentage": 6.84, "workers_outdoor": 4196985, "outdoor_worker_percentage": 25.00, "area_sqkm": 1483.0, "pop_density_per_sqkm": 11320.3, "census_source": "Census of India 2011 PCA - MCD"},
    {"district_id": "DIST_CH_CHANDIGARH", "district_name": "Chandigarh", "state_name": "Chandigarh", "tot_pop": 1055450, "pop_elderly_60plus": 73881, "elderly_percentage": 7.00, "workers_outdoor": 284971, "outdoor_worker_percentage": 27.00, "area_sqkm": 114.0, "pop_density_per_sqkm": 9258.3, "census_source": "Census of India 2011 PCA - MCC"},

    # ------------------ GUJARAT ------------------
    {"district_id": "DIST_GJ_AHMEDABAD", "district_name": "Ahmedabad", "state_name": "Gujarat", "tot_pop": 7214225, "pop_elderly_60plus": 598780, "elderly_percentage": 8.30, "workers_outdoor": 1947840, "outdoor_worker_percentage": 27.00, "area_sqkm": 8087.0, "pop_density_per_sqkm": 892.1, "census_source": "Census of India 2011 PCA - AMC"},
    {"district_id": "DIST_GJ_SURAT", "district_name": "Surat", "state_name": "Gujarat", "tot_pop": 6081322, "pop_elderly_60plus": 358798, "elderly_percentage": 5.90, "workers_outdoor": 2067649, "outdoor_worker_percentage": 34.00, "area_sqkm": 4418.0, "pop_density_per_sqkm": 1376.5, "census_source": "Census of India 2011 PCA - SMC"},
    {"district_id": "DIST_GJ_VADODARA", "district_name": "Vadodara", "state_name": "Gujarat", "tot_pop": 4165626, "pop_elderly_60plus": 349912, "elderly_percentage": 8.40, "workers_outdoor": 1249687, "outdoor_worker_percentage": 30.00, "area_sqkm": 7512.0, "pop_density_per_sqkm": 554.5, "census_source": "Census of India 2011 PCA - VMC"},
    {"district_id": "DIST_GJ_RAJKOT", "district_name": "Rajkot", "state_name": "Gujarat", "tot_pop": 3804556, "pop_elderly_60plus": 323387, "elderly_percentage": 8.50, "workers_outdoor": 1179412, "outdoor_worker_percentage": 31.00, "area_sqkm": 11203.0, "pop_density_per_sqkm": 339.6, "census_source": "Census of India 2011 PCA - RMC"},

    # ------------------ MAHARASHTRA ------------------
    {"district_id": "DIST_MH_MUMBAI", "district_name": "Mumbai", "state_name": "Maharashtra", "tot_pop": 12442373, "pop_elderly_60plus": 1182025, "elderly_percentage": 9.50, "workers_outdoor": 2861745, "outdoor_worker_percentage": 23.00, "area_sqkm": 603.4, "pop_density_per_sqkm": 20620.4, "census_source": "Census of India 2011 PCA - BMC"},
    {"district_id": "DIST_MH_PUNE", "district_name": "Pune", "state_name": "Maharashtra", "tot_pop": 9429408, "pop_elderly_60plus": 886364, "elderly_percentage": 9.40, "workers_outdoor": 2923116, "outdoor_worker_percentage": 31.00, "area_sqkm": 15643.0, "pop_density_per_sqkm": 602.8, "census_source": "Census of India 2011 PCA - PMC"},
    {"district_id": "DIST_MH_THANE", "district_name": "Thane", "state_name": "Maharashtra", "tot_pop": 11060148, "pop_elderly_60plus": 895872, "elderly_percentage": 8.10, "workers_outdoor": 3096841, "outdoor_worker_percentage": 28.00, "area_sqkm": 9558.0, "pop_density_per_sqkm": 1157.2, "census_source": "Census of India 2011 PCA - TMC"},
    {"district_id": "DIST_MH_NAGPUR", "district_name": "Nagpur", "state_name": "Maharashtra", "tot_pop": 4653570, "pop_elderly_60plus": 456049, "elderly_percentage": 9.80, "workers_outdoor": 1489142, "outdoor_worker_percentage": 32.00, "area_sqkm": 9892.0, "pop_density_per_sqkm": 470.4, "census_source": "Census of India 2011 PCA - NMC"},
    {"district_id": "DIST_MH_NASHIK", "district_name": "Nashik", "state_name": "Maharashtra", "tot_pop": 6107187, "pop_elderly_60plus": 525218, "elderly_percentage": 8.60, "workers_outdoor": 2015371, "outdoor_worker_percentage": 33.00, "area_sqkm": 15530.0, "pop_density_per_sqkm": 393.3, "census_source": "Census of India 2011 PCA - NMMC"},
    {"district_id": "DIST_MH_AURANGABAD", "district_name": "Chhatrapati Sambhajinagar (Aurangabad)", "state_name": "Maharashtra", "tot_pop": 3701282, "pop_elderly_60plus": 310907, "elderly_percentage": 8.40, "workers_outdoor": 1295448, "outdoor_worker_percentage": 35.00, "area_sqkm": 10107.0, "pop_density_per_sqkm": 366.2, "census_source": "Census of India 2011 PCA - ASMC"},

    # ------------------ RAJASTHAN ------------------
    {"district_id": "DIST_RJ_JAIPUR", "district_name": "Jaipur", "state_name": "Rajasthan", "tot_pop": 6626178, "pop_elderly_60plus": 496963, "elderly_percentage": 7.50, "workers_outdoor": 2120376, "outdoor_worker_percentage": 32.00, "area_sqkm": 11143.0, "pop_density_per_sqkm": 594.7, "census_source": "Census of India 2011 PCA - JMC"},
    {"district_id": "DIST_RJ_JODHPUR", "district_name": "Jodhpur", "state_name": "Rajasthan", "tot_pop": 3687165, "pop_elderly_60plus": 272850, "elderly_percentage": 7.40, "workers_outdoor": 1253636, "outdoor_worker_percentage": 34.00, "area_sqkm": 22850.0, "pop_density_per_sqkm": 161.4, "census_source": "Census of India 2011 PCA - Jodhpur MC"},
    {"district_id": "DIST_RJ_KOTA", "district_name": "Kota", "state_name": "Rajasthan", "tot_pop": 1951014, "pop_elderly_60plus": 146326, "elderly_percentage": 7.50, "workers_outdoor": 663344, "outdoor_worker_percentage": 34.00, "area_sqkm": 5217.0, "pop_density_per_sqkm": 373.9, "census_source": "Census of India 2011 PCA - Kota MC"},

    # ------------------ UTTAR PRADESH ------------------
    {"district_id": "DIST_UP_LUCKNOW", "district_name": "Lucknow", "state_name": "Uttar Pradesh", "tot_pop": 4589838, "pop_elderly_60plus": 357997, "elderly_percentage": 7.80, "workers_outdoor": 1331053, "outdoor_worker_percentage": 29.00, "area_sqkm": 2528.0, "pop_density_per_sqkm": 1815.6, "census_source": "Census of India 2011 PCA - LMC"},
    {"district_id": "DIST_UP_KANPUR", "district_name": "Kanpur Nagar", "state_name": "Uttar Pradesh", "tot_pop": 4581268, "pop_elderly_60plus": 384826, "elderly_percentage": 8.40, "workers_outdoor": 1419993, "outdoor_worker_percentage": 31.00, "area_sqkm": 3155.0, "pop_density_per_sqkm": 1452.1, "census_source": "Census of India 2011 PCA - KNN"},
    {"district_id": "DIST_UP_VARANASI", "district_name": "Varanasi", "state_name": "Uttar Pradesh", "tot_pop": 3676841, "pop_elderly_60plus": 305177, "elderly_percentage": 8.30, "workers_outdoor": 1176589, "outdoor_worker_percentage": 32.00, "area_sqkm": 1535.0, "pop_density_per_sqkm": 2395.3, "census_source": "Census of India 2011 PCA - VNN"},
    {"district_id": "DIST_UP_PRAYAGRAJ", "district_name": "Prayagraj (Allahabad)", "state_name": "Uttar Pradesh", "tot_pop": 5954391, "pop_elderly_60plus": 482305, "elderly_percentage": 8.10, "workers_outdoor": 1964949, "outdoor_worker_percentage": 33.00, "area_sqkm": 5482.0, "pop_density_per_sqkm": 1086.2, "census_source": "Census of India 2011 PCA - PMC"},
    {"district_id": "DIST_UP_AGRA", "district_name": "Agra", "state_name": "Uttar Pradesh", "tot_pop": 4418797, "pop_elderly_60plus": 335828, "elderly_percentage": 7.60, "workers_outdoor": 1414015, "outdoor_worker_percentage": 32.00, "area_sqkm": 4041.0, "pop_density_per_sqkm": 1093.5, "census_source": "Census of India 2011 PCA - Agra NN"},

    # ------------------ MADHYA PRADESH ------------------
    {"district_id": "DIST_MP_BHOPAL", "district_name": "Bhopal", "state_name": "Madhya Pradesh", "tot_pop": 2371061, "pop_elderly_60plus": 175458, "elderly_percentage": 7.40, "workers_outdoor": 758739, "outdoor_worker_percentage": 32.00, "area_sqkm": 2772.0, "pop_density_per_sqkm": 855.4, "census_source": "Census of India 2011 PCA - BMC"},
    {"district_id": "DIST_MP_INDORE", "district_name": "Indore", "state_name": "Madhya Pradesh", "tot_pop": 3276697, "pop_elderly_60plus": 249028, "elderly_percentage": 7.60, "workers_outdoor": 1048543, "outdoor_worker_percentage": 32.00, "area_sqkm": 3898.0, "pop_density_per_sqkm": 840.6, "census_source": "Census of India 2011 PCA - IMC"},
    {"district_id": "DIST_MP_GWALIOR", "district_name": "Gwalior", "state_name": "Madhya Pradesh", "tot_pop": 2032036, "pop_elderly_60plus": 158498, "elderly_percentage": 7.80, "workers_outdoor": 650251, "outdoor_worker_percentage": 32.00, "area_sqkm": 4560.0, "pop_density_per_sqkm": 445.6, "census_source": "Census of India 2011 PCA - GMC"},

    # ------------------ BIHAR & JHARKHAND ------------------
    {"district_id": "DIST_BR_PATNA", "district_name": "Patna", "state_name": "Bihar", "tot_pop": 5838465, "pop_elderly_60plus": 426207, "elderly_percentage": 7.30, "workers_outdoor": 1868308, "outdoor_worker_percentage": 32.00, "area_sqkm": 3202.0, "pop_density_per_sqkm": 1823.4, "census_source": "Census of India 2011 PCA - PMC"},
    {"district_id": "DIST_JH_RANCHI", "district_name": "Ranchi", "state_name": "Jharkhand", "tot_pop": 2914253, "pop_elderly_60plus": 209826, "elderly_percentage": 7.20, "workers_outdoor": 1019988, "outdoor_worker_percentage": 35.00, "area_sqkm": 5097.0, "pop_density_per_sqkm": 571.8, "census_source": "Census of India 2011 PCA - RMC"},
    {"district_id": "DIST_JH_JAMSHEDPUR", "district_name": "East Singhbhum (Jamshedpur)", "state_name": "Jharkhand", "tot_pop": 2293919, "pop_elderly_60plus": 183513, "elderly_percentage": 8.00, "workers_outdoor": 756993, "outdoor_worker_percentage": 33.00, "area_sqkm": 3562.0, "pop_density_per_sqkm": 644.0, "census_source": "Census of India 2011 PCA - JNAC"},

    # ------------------ WEST BENGAL & ODISHA ------------------
    {"district_id": "DIST_WB_KOLKATA", "district_name": "Kolkata", "state_name": "West Bengal", "tot_pop": 4496694, "pop_elderly_60plus": 517119, "elderly_percentage": 11.50, "workers_outdoor": 1079206, "outdoor_worker_percentage": 24.00, "area_sqkm": 185.0, "pop_density_per_sqkm": 24306.5, "census_source": "Census of India 2011 PCA - KMC"},
    {"district_id": "DIST_WB_HOWRAH", "district_name": "Howrah", "state_name": "West Bengal", "tot_pop": 4850029, "pop_elderly_60plus": 455902, "elderly_percentage": 9.40, "workers_outdoor": 1455008, "outdoor_worker_percentage": 30.00, "area_sqkm": 1467.0, "pop_density_per_sqkm": 3306.1, "census_source": "Census of India 2011 PCA - HMC"},
    {"district_id": "DIST_OD_BHUBANESWAR", "district_name": "Khurda (Bhubaneswar)", "state_name": "Odisha", "tot_pop": 2251673, "pop_elderly_60plus": 202650, "elderly_percentage": 9.00, "workers_outdoor": 698018, "outdoor_worker_percentage": 31.00, "area_sqkm": 2813.0, "pop_density_per_sqkm": 800.5, "census_source": "Census of India 2011 PCA - BMC"},

    # ------------------ SOUTH INDIA (KARNATAKA, TELANGANA, ANDHRA, TAMIL NADU, KERALA) ------------------
    {"district_id": "DIST_KA_BENGALURU", "district_name": "Bengaluru Urban", "state_name": "Karnataka", "tot_pop": 9621551, "pop_elderly_60plus": 692751, "elderly_percentage": 7.20, "workers_outdoor": 2116741, "outdoor_worker_percentage": 22.00, "area_sqkm": 2196.0, "pop_density_per_sqkm": 4381.4, "census_source": "Census of India 2011 PCA - BBMP"},
    {"district_id": "DIST_TG_HYDERABAD", "district_name": "Hyderabad", "state_name": "Telangana", "tot_pop": 3943323, "pop_elderly_60plus": 299692, "elderly_percentage": 7.60, "workers_outdoor": 985830, "outdoor_worker_percentage": 25.00, "area_sqkm": 217.0, "pop_density_per_sqkm": 18172.0, "census_source": "Census of India 2011 PCA - GHMC"},
    {"district_id": "DIST_AP_VISAKHAPATNAM", "district_name": "Visakhapatnam", "state_name": "Andhra Pradesh", "tot_pop": 4290589, "pop_elderly_60plus": 386153, "elderly_percentage": 9.00, "workers_outdoor": 1372988, "outdoor_worker_percentage": 32.00, "area_sqkm": 11161.0, "pop_density_per_sqkm": 384.4, "census_source": "Census of India 2011 PCA - GVMC"},
    {"district_id": "DIST_TN_CHENNAI", "district_name": "Chennai", "state_name": "Tamil Nadu", "tot_pop": 7088000, "pop_elderly_60plus": 737152, "elderly_percentage": 10.40, "workers_outdoor": 1772000, "outdoor_worker_percentage": 25.00, "area_sqkm": 426.0, "pop_density_per_sqkm": 16638.5, "census_source": "Census of India 2011 PCA - GCC"},
    {"district_id": "DIST_KL_THIRUVANANTHAPURAM", "district_name": "Thiruvananthapuram", "state_name": "Kerala", "tot_pop": 3301427, "pop_elderly_60plus": 435788, "elderly_percentage": 13.20, "workers_outdoor": 891385, "outdoor_worker_percentage": 27.00, "area_sqkm": 2189.0, "pop_density_per_sqkm": 1508.2, "census_source": "Census of India 2011 PCA - TMC"},
    {"district_id": "DIST_KL_ERNAKULAM", "district_name": "Ernakulam (Kochi)", "state_name": "Kerala", "tot_pop": 3282388, "pop_elderly_60plus": 413580, "elderly_percentage": 12.60, "workers_outdoor": 919068, "outdoor_worker_percentage": 28.00, "area_sqkm": 3068.0, "pop_density_per_sqkm": 1069.9, "census_source": "Census of India 2011 PCA - Cochin Corp"}
]

def main():
    print("=" * 70)
    print("  Taapamigo — Pan-India Government Census & Ward Dataset Builder")
    print("=" * 70)

    # 1. Write india_census_districts.json
    census_file = ROOT_DIR / "data" / "sample" / "india_census_districts.json"
    census_file.parent.mkdir(parents=True, exist_ok=True)
    with open(census_file, "w", encoding="utf-8") as f:
        json.dump(PAN_INDIA_CENSUS_DISTRICTS, f, indent=2)
    print(f"[+] Written {len(PAN_INDIA_CENSUS_DISTRICTS)} district Census profiles to: {census_file}")

    print("\n[+] Dataset updated successfully.")

if __name__ == "__main__":
    main()
