"""
Example usage for Ocular Tear Film Breakup Dynamics & Digital Asthenopia Prevention Skill.
Demonstrates assessing Ocular Protection Index (OPI) during continuous VDT display use.
"""

from client import OcularTearFilmClient


def main():
    client = OcularTearFilmClient()

    print("=== 1. Evaluating Ocular Protection Index (Screen Session) ===")
    opi_res = client.evaluate_ocular_protection_index(
        nibut_seconds=7.0,
        blink_rate_per_min=5.5,
        incomplete_blink_fraction=0.25,
        continuous_screen_time_hours=3.5,
        ambient_humidity_pct=35.0
    )
    print(f"NIBUT: {opi_res['nibut_seconds']} s | IBI: {opi_res['inter_blink_interval_sec']} s")
    print(f"Raw OPI: {opi_res['raw_opi']} | Effective OPI: {opi_res['effective_opi']}")
    print(f"Corneal Exposure Present: {opi_res['is_corneal_exposure_present']}")
    print(f"Digital Asthenopia Risk Score: {opi_res['digital_asthenopia_risk_score']} / 100")
    print(f"Risk Tier: {opi_res['risk_tier']}")
    print(f"Recommendation: {opi_res['ergonomic_recommendation']}")

    print("\n=== 2. Generating 20-20-20 Rule Micro-Break Schedule ===")
    break_res = client.generate_20_20_20_break_schedule(
        daily_screen_target_hours=8.0,
        current_session_minutes=42.0
    )
    print(f"Current Session: {break_res['current_session_minutes']} min")
    print(f"Minutes Until Next Break: {break_res['minutes_until_next_break']} min")
    print(f"Trigger Break Now: {break_res['should_trigger_break_now']}")
    print(f"Protocol Drill: {break_res['protocol_drill']}")


if __name__ == "__main__":
    main()
