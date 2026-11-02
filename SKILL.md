---
name: genpark-personal-agent-ocular-tear-film-breakup-ergonomics-skill
description: Deterministic assessment of Ocular Protection Index (OPI), Non-Invasive Tear Breakup Time (NIBUT), blink completeness, and digital visual fatigue prevention.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Ocular Tear Film Breakup Dynamics & Digital Asthenopia Prevention Skill

## Overview
The `genpark-personal-agent-ocular-tear-film-breakup-ergonomics-skill` provides personal sovereign agents with computational ophthalmic modeling of tear film stability. Continuous viewing of computer and mobile screens suppresses spontaneous blink rates by up to 65% and induces incomplete blinks, leaving corneal epithelial cells exposed to evaporative dryout. This skill models the Ocular Protection Index (OPI), monitors digital eye strain (asthenopia), and schedules targeted 20-20-20 micro-rest interventions.

## Physiological Model & Mathematics
1. **Inter-Blink Interval ($IBI$)**:
   $$IBI = \frac{60}{\text{Blink Rate (bpm)}} \text{ seconds}$$
2. **Ocular Protection Index ($OPI$)**:
   $$OPI = \frac{NIBUT}{IBI}$$
   - $OPI \ge 1.0$: Intact tear film throughout the inter-blink cycle; cornea remains shielded.
   - $OPI < 1.0$: Tear film rupture occurs before the next blink, leading to dry spots, epithelial microtrauma, and tear hyperosmolarity.
3. **Effective OPI with Incomplete Blink Factor**:
   $$OPI_{\text{eff}} = OPI \times (1 - \text{Fraction}_{\text{incomplete}})$$
4. **Digital Asthenopia Risk Score ($DARS$)**:
   Synthesizes effective OPI deficit, cumulative screen hours, and low humidity penalties on a scale from 0 to 100.

## Tools & Endpoints
- `evaluate_ocular_protection_index`: Evaluates raw/effective OPI, corneal dry spot risk, and asthenopia score.
- `generate_20_20_20_break_schedule`: Generates clinical 20-20-20 rest intervals and guided complete-blink exercise routines.
