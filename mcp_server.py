"""
MCP Server for Ocular Tear Film Breakup Dynamics & Digital Asthenopia Prevention.
Exposes JSON-RPC endpoints for Ocular Protection Index (OPI) calculation and ergonomic scheduling.
"""

import json
import sys
from client import OcularTearFilmClient

client = OcularTearFilmClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_ocular_protection_index",
                        "description": "Calculates Ocular Protection Index (OPI = NIBUT / IBI), effective corneal protection factoring incomplete blinks, and digital asthenopia risk score.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nibut_seconds": {"type": "number", "description": "Non-invasive tear breakup time in seconds (standard: > 10s)"},
                                "blink_rate_per_min": {"type": "number", "description": "Spontaneous blinks per minute (standard screen viewing: 5-8 bpm)"},
                                "incomplete_blink_fraction": {"type": "number", "default": 0.15, "description": "Fraction of blinks that are incomplete (0.0 to 1.0)"},
                                "continuous_screen_time_hours": {"type": "number", "default": 2.0, "description": "Hours of continuous visual display terminal exposure"},
                                "ambient_humidity_pct": {"type": "number", "default": 40.0, "description": "Ambient relative humidity percentage"}
                            },
                            "required": ["nibut_seconds", "blink_rate_per_min"]
                        }
                    },
                    {
                        "name": "generate_20_20_20_break_schedule",
                        "description": "Generates dynamic 20-20-20 visual rest reminders and guided micro-blink recovery drills.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "daily_screen_target_hours": {"type": "number", "default": 8.0, "description": "Target daily screen work hours"},
                                "current_session_minutes": {"type": "number", "default": 45.0, "description": "Current active screen session in minutes"}
                            }
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_ocular_protection_index":
            res = client.evaluate_ocular_protection_index(
                nibut_seconds=args.get("nibut_seconds", 8.0),
                blink_rate_per_min=args.get("blink_rate_per_min", 6.0),
                incomplete_blink_fraction=args.get("incomplete_blink_fraction", 0.15),
                continuous_screen_time_hours=args.get("continuous_screen_time_hours", 2.0),
                ambient_humidity_pct=args.get("ambient_humidity_pct", 40.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "generate_20_20_20_break_schedule":
            res = client.generate_20_20_20_break_schedule(
                daily_screen_target_hours=args.get("daily_screen_target_hours", 8.0),
                current_session_minutes=args.get("current_session_minutes", 45.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
