"""
Local development and evaluation server runner for ThermoShield India (SIH26083).
Initializes the database, checks environment, and starts Uvicorn ASGI server.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    print("=" * 70)
    print("  ThermoShield India — SIH 2026 PS26083 Local Server Runner")
    print("  Extreme Heatwave Early Warning & Thermal Stress Assessment")
    print("=" * 70)

    # 1. Check or initialize Database
    db_path = ROOT_DIR / "data" / "heat_risk.db"
    if not db_path.exists() or db_path.stat().st_size == 0:
        print("\n[*] Initializing SQLite database and seeding 18 cities & 1,145 wards...")
        try:
            from scripts.seed_db import seed_all
            seed_all()
            print("[+] Database seeded successfully.")
        except Exception as e:
            print(f"[!] Warning during database seed: {e}")
    else:
        print(f"\n[+] SQLite database verified at: {db_path} ({db_path.stat().st_size / 1024:.1f} KB)")

    # 2. Display Access URLs
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    
    print("\n" + "-" * 70)
    print(f"  WEB DASHBOARD (UI):       http://{host}:{port}/")
    print(f"  INTERACTIVE SWAGGER DOCS: http://{host}:{port}/docs")
    print(f"  REDOC API SPECIFICATION:  http://{host}:{port}/redoc")
    print(f"  SYSTEM HEALTH CHECK:      http://{host}:{port}/health")
    print(f"  DATA FRESHNESS STATUS:    http://{host}:{port}/api/v1/data-freshness")
    print(f"  SAMPLE WARDS (Abohar):    http://{host}:{port}/api/v1/wards?city=abohar")
    print(f"  SAMPLE RISK ASSESSMENT:   http://{host}:{port}/api/v1/risk/current?city=abohar")
    print("-" * 70)
    print("\n[*] Starting Uvicorn server (Press Ctrl+C to stop)...\n")

    try:
        import uvicorn
        uvicorn.run(
            "backend.app.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n[*] Server shutdown requested by user.")
    except Exception as e:
        print(f"[!] Failed to run server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
