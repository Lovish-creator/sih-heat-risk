"""
SIH26083 Public Health & Occupational Advisory Engine.

Generates persona-tailored, evidence-based mitigation actions grounded in:
1. National Centre for Disease Control (NCDC, 2024) National Action Plan for Heat-Related Illnesses (NAP-HRI)
2. NIOSH / CDC (2016) Occupational Criteria for Heat Exposure
3. World Health Organization (WHO) Heat-Health Guidelines
"""

from typing import Dict, Any, List


class AdvisoryEngine:
    """
    Translates biometeorological risk scores and alert levels into actionable
    operational guidance for Citizens, Outdoor Laborers, and Municipal Authorities.
    """

    def generate_advisories(
        self,
        alert_level: str,
        risk_score: float,
        wbgt_info: Dict[str, Any],
        utci_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate complete multi-persona advisory bundle for a given risk level.
        
        Args:
            alert_level: GREEN, YELLOW, ORANGE, or RED.
            risk_score: Composite risk score (0 - 100).
            wbgt_info: WBGT classification dictionary.
            utci_info: UTCI classification dictionary.
            
        Returns:
            Dictionary containing tailored advisories for general_public, outdoor_workers, and authorities.
        """
        lvl = str(alert_level).upper()

        if lvl == "RED":
            citizen_advisories = [
                "URGENT: Avoid all non-essential outdoor exposure between 11:00 and 16:00 IST.",
                "Drink oral rehydration solutions (ORS), lemon water, or buttermilk frequently even without feeling thirsty.",
                "Conduct mandatory wellness checks on elderly family members and neighbors living alone.",
                "Recognize Red Flag Heat Stroke symptoms: High body temperature (>40°C), confusion, loss of consciousness, cessation of sweating. Call 108 / Emergency Medical Services immediately."
            ]
            worker_advisories = [
                f"OCCUPATIONAL DIRECTIVE: {wbgt_info.get('work_rest_regimen', 'Cease strenuous outdoor labor')}.",
                "Mandatory 45-minute rest breaks in designated shaded, ventilated cooling zones for every 15 minutes of work.",
                "Maintain minimum fluid intake of 1.0 Liter/hour with electrolyte supplementation.",
                "Implement strict 'Buddy System' monitoring among workers for early signs of heat exhaustion/slurred speech."
            ]
            authority_advisories = [
                "Activate Level-3 Red Emergency Heat Action Plan protocols across all municipal zones.",
                "Deploy emergency mobile water tankers to informal settlements, construction clusters, and transit hubs.",
                "Operate 24/7 dedicated air-cooled cooling centers in community halls and religious institutions.",
                "Ensure municipal hospitals and primary health centres (PHCs) have reserved heat stroke stabilization beds with ice packs, intravenous fluids, and trained triage staff."
            ]

        elif lvl == "ORANGE":
            citizen_advisories = [
                "Limit direct sun exposure between 12:00 and 15:00 IST; wear lightweight, light-colored, loose cotton clothing.",
                "Keep living spaces cool using window curtains, fans, and wet evaporative curtains.",
                "Carry a water bottle and umbrella/hat during all outdoor transit.",
                "Never leave infants, elderly persons, or pets in parked vehicles even for brief periods."
            ]
            worker_advisories = [
                f"OCCUPATIONAL DIRECTIVE: {wbgt_info.get('work_rest_regimen', '50% Work / 50% Rest each hour')}.",
                "Shift strenuous physical tasks (concrete pouring, asphalt paving, manual digging) to early morning (06:00-10:00) or evening.",
                "Ensure employers provide accessible shaded rest shelters and clean, cool drinking water.",
                "Consume at least 750ml to 1.0L of water per hour of physical exertion."
            ]
            authority_advisories = [
                "Issue public broadcast alerts via SMS, radio, and digital traffic display boards.",
                "Inspect construction sites and industrial yards for mandatory shaded resting areas and hydration points.",
                "Keep public parks and air-conditioned libraries open for extended hours as public cooling respites.",
                "Review daily emergency medical service (EMS) call volumes for heat exhaustion spikes."
            ]

        elif lvl == "YELLOW":
            citizen_advisories = [
                "Stay informed through official weather and biometeorological risk forecasts.",
                "Maintain regular water intake; avoid dehydrating beverages with high sugar, caffeine, or alcohol content.",
                "Ensure children and vulnerable individuals take frequent hydration breaks during outdoor play."
            ]
            worker_advisories = [
                f"OCCUPATIONAL GUIDELINE: {wbgt_info.get('work_rest_regimen', '75% Work / 25% Rest each hour')}.",
                "Take 15-minute shaded rest breaks every hour during peak afternoon hours.",
                "Ensure clean drinking water is readily available on site; consume at least 500-750ml per hour."
            ]
            authority_advisories = [
                "Issue advisories to schools, construction contractors, and transit operators.",
                "Ensure all municipal public water kiosks (Piyavs) are functional and stocked.",
                "Alert hospital emergency departments to maintain adequate stocks of ORS and IV fluids."
            ]

        else: # GREEN
            citizen_advisories = [
                "Routine summer conditions. Normal daily outdoor activities are permissible.",
                "Maintain healthy hydration habits and standard sun protection (hat/sunglasses)."
            ]
            worker_advisories = [
                "Continuous work permissible with standard scheduled meal and hydration intervals.",
                "Maintain regular water intake of at least 500ml per hour during heavy physical exertion."
            ]
            authority_advisories = [
                "Routine surveillance. Maintain standard operational readiness and monitor 5-day forecast horizons."
            ]

        return {
            "alert_level": lvl,
            "risk_score": risk_score,
            "personas": {
                "general_public": {
                    "persona_title": "Citizens & Vulnerable Individuals",
                    "icon": "user",
                    "actions": citizen_advisories
                },
                "outdoor_workers": {
                    "persona_title": "Outdoor Workers & Employers (NIOSH Standard)",
                    "icon": "hard-hat",
                    "niosh_work_rest_cycle": wbgt_info.get("work_rest_regimen", "Standard"),
                    "actions": worker_advisories
                },
                "authorities": {
                    "persona_title": "Municipal Authorities & Disaster Management",
                    "icon": "shield-alt",
                    "actions": authority_advisories
                }
            },
            "provenance": {
                "clinical_reference": "NCDC National Action Plan for Heat-Related Illnesses (NAP-HRI 2024)",
                "occupational_reference": "NIOSH Criteria for a Recommended Standard: Heat Stress (2016)",
                "international_guidance": "WHO Heat-Health Action Plans (2021)"
            }
        }
