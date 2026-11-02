"""
Ocular Tear Film Breakup Dynamics & Digital Asthenopia Prevention Engine.
Provides deterministic, zero-dependency calculation of Ocular Protection Index (OPI),
Non-Invasive Tear Breakup Time (NIBUT), blink dynamics, and 20-20-20 ergonomic scheduling.
"""

from typing import Dict, Any, List, Optional


class OcularTearFilmClient:
    """
    Deterministic client for modeling tear film stability and digital visual fatigue.
    Pure Python standard library implementation based on standard Ophthalmic OPI formulas.
    """

    def __init__(self):
        pass

    def evaluate_ocular_protection_index(
        self,
        nibut_seconds: float,
        blink_rate_per_min: float,
        incomplete_blink_fraction: float = 0.15,
        continuous_screen_time_hours: float = 2.0,
        ambient_humidity_pct: float = 40.0
    ) -> Dict[str, Any]:
        """
        Evaluates the Ocular Protection Index (OPI) and digital asthenopia risk.
        OPI = NIBUT / Inter-Blink Interval (IBI).
        When OPI < 1.0, the tear film breaks up prior to the subsequent blink, exposing dry corneal spots.
        """
        if nibut_seconds <= 0 or blink_rate_per_min <= 0:
            return {"error": "NIBUT and blink rate must be positive values"}

        ibi_seconds = round(60.0 / blink_rate_per_min, 2)
        raw_opi = round(nibut_seconds / max(0.1, ibi_seconds), 3)

        # Completeness factor: incomplete blinks do not renew the lipid layer on inferior cornea
        incompleteness = max(0.0, min(1.0, incomplete_blink_fraction))
        completeness_ratio = 1.0 - incompleteness
        effective_opi = round(raw_opi * completeness_ratio, 3)

        # Environmental & continuous screen exposure factor
        humidity_penalty = max(0.0, (50.0 - ambient_humidity_pct) * 0.5) if ambient_humidity_pct < 50.0 else 0.0
        screen_penalty = min(35.0, continuous_screen_time_hours * 10.0)

        # Digital Asthenopia Risk Score (DARS, 0 - 100)
        # Low effective OPI heavily drives asthenopia risk
        opi_deficit = max(0.0, 1.0 - min(1.0, effective_opi)) * 50.0
        dars_score = round(min(100.0, max(5.0, opi_deficit + screen_penalty + humidity_penalty)), 1)

        is_dry_eye_risk = effective_opi < 1.0

        if dars_score < 25.0 and effective_opi >= 1.0:
            tier = "OPTIMAL_CORNEAL_PROTECTION"
            advice = "Tear film is robustly protecting the corneal surface. Maintain standard visual ergonomic hygiene."
        elif effective_opi >= 0.80 and dars_score < 50.0:
            tier = "MILD_TEAR_FILM_ATTENUATION"
            advice = "Minor tear evaporation detected. Increase deliberate blink frequency and verify ambient humidity."
        elif effective_opi >= 0.50:
            tier = "SIGNIFICANT_ASTHENOPIA_RISK"
            advice = "Corneal dry spot exposure between blinks. Execute 20-20-20 protocol immediately: 20s gaze at 20 feet with 5 complete full blinks."
        else:
            tier = "SEVERE_TEAR_FILM_DESTABILIZATION"
            advice = "Critical tear film breakup. Enforce 10-minute non-screen break, apply lubricating eye drops if advised, and adjust monitor height below eye level."

        return {
            "nibut_seconds": nibut_seconds,
            "blink_rate_per_min": blink_rate_per_min,
            "inter_blink_interval_sec": ibi_seconds,
            "raw_opi": raw_opi,
            "incomplete_blink_fraction": incompleteness,
            "effective_opi": effective_opi,
            "is_corneal_exposure_present": is_dry_eye_risk,
            "digital_asthenopia_risk_score": dars_score,
            "risk_tier": tier,
            "ergonomic_recommendation": advice
        }

    def generate_20_20_20_break_schedule(
        self,
        daily_screen_target_hours: float = 8.0,
        current_session_minutes: float = 45.0
    ) -> Dict[str, Any]:
        """
        Generates micro-break cadence adhering to the clinical 20-20-20 rule
        (every 20 minutes look 20 feet away for at least 20 seconds).
        """
        breaks_per_hour = 3
        total_breaks_needed = int(daily_screen_target_hours * breaks_per_hour)
        minutes_until_next_break = max(0, 20 - int(current_session_minutes % 20))

        should_break_now = (current_session_minutes >= 20.0 and (current_session_minutes % 20.0) < 2.0) or (current_session_minutes >= 50.0)

        return {
            "daily_screen_target_hours": daily_screen_target_hours,
            "current_session_minutes": current_session_minutes,
            "minutes_until_next_break": minutes_until_next_break,
            "should_trigger_break_now": should_break_now,
            "total_daily_microbreaks_planned": total_breaks_needed,
            "protocol_drill": "Fix gaze at distant object (>= 6 meters / 20 feet) for 20 seconds. Perform 5 slow, complete eyelid closures with gentle pause."
        }
