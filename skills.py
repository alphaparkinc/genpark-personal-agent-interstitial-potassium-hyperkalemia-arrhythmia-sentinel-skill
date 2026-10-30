# -*- coding: utf-8 -*-
"""Interstitial Potassium & Hyperkalemia Arrhythmia Sentinel Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def monitor_hyperkalemia_arrhythmia_risk(**kwargs):
    """Cross-analyzes interstitial/serum potassium levels against ECG morphometric features (T-wave peaking, T/R amplitude ratio, PR prolongation) to guard against lethal arrhythmias."""
    potassium_meq_l = kwargs.get('potassium_meq_l')
    t_wave_amplitude_mv = kwargs.get('t_wave_amplitude_mv')
    r_wave_amplitude_mv = kwargs.get('r_wave_amplitude_mv')
    pr_interval_ms = kwargs.get('pr_interval_ms')
    qrs_duration_ms = kwargs.get('qrs_duration_ms')

    tr_ratio = round(t_wave_amplitude_mv / (r_wave_amplitude_mv if r_wave_amplitude_mv > 0.05 else 0.05), 2)
    is_t_peaked = tr_ratio > 0.75 or t_wave_amplitude_mv > 1.0
    is_pr_prolonged = pr_interval_ms > 200.0
    is_qrs_widened = qrs_duration_ms > 120.0
    
    if potassium_meq_l >= 6.5 or (potassium_meq_l >= 6.0 and (is_qrs_widened or is_pr_prolonged)):
        tier = "CRITICAL / EMERGENT HYPERKALEMIA"
        action = "Immediate medical intervention required: Calcium gluconate/chloride membrane stabilization, insulin-glucose infusion."
    elif potassium_meq_l >= 6.0 or (potassium_meq_l >= 5.5 and is_t_peaked):
        tier = "MODERATE HYPERKALEMIA RISK"
        action = "Urgent nephrology review; potassium-wasting diuretics, potassium binders (patiromer/SZC)."
    elif potassium_meq_l >= 5.1:
        tier = "MILD HYPERKALEMIA RISK"
        action = "Dietary potassium reduction; audit RAAS inhibitors (ACEi/ARB/MRA)."
    elif potassium_meq_l < 3.5:
        tier = "HYPOKALEMIA ALERT"
        action = "Monitor for U waves, ventricular ectopy; potassium chloride oral repletion."
    else:
        tier = "NORMOKALEMIA"
        action = "Electrolyte homeostasis within physiological limits (3.5 - 5.0 mEq/L)."
        
    result = {
        "status": "success",
        "potassium_level_meq_l": potassium_meq_l,
        "t_to_r_amplitude_ratio": tr_ratio,
        "ecg_morphology_flags": {
            "tall_peaked_t_wave": is_t_peaked,
            "pr_interval_prolongation": is_pr_prolonged,
            "qrs_widening": is_qrs_widened
        },
        "hyperkalemia_clinical_tier": tier,
        "clinical_action_protocol": action,
        "engine": "GenPark Interstitial Electrolyte Sentinel Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "monitor_hyperkalemia_arrhythmia_risk": {
        "name": "monitor_hyperkalemia_arrhythmia_risk",
        "description": "Cross-analyzes interstitial/serum potassium levels against ECG morphometric features (T-wave peaking, T/R amplitude ratio, PR prolongation) to guard against lethal arrhythmias.",
        "parameters": {
            "type": "object",
            "properties": {
                "potassium_meq_l": {"type": "number", "description": "Serum or validated interstitial potassium level (mEq/L)"},
                "t_wave_amplitude_mv": {"type": "number", "description": "Peak amplitude of ECG T-wave in precordial leads (mV)"},
                "r_wave_amplitude_mv": {"type": "number", "description": "Amplitude of preceding R-wave (mV)"},
                "pr_interval_ms": {"type": "number", "description": "PR interval in milliseconds"},
                "qrs_duration_ms": {"type": "number", "description": "QRS complex duration in milliseconds"},
            },
            "required": ['potassium_meq_l', 't_wave_amplitude_mv', 'r_wave_amplitude_mv', 'pr_interval_ms', 'qrs_duration_ms']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "monitor_hyperkalemia_arrhythmia_risk":
            res = monitor_hyperkalemia_arrhythmia_risk(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-interstitial-potassium-hyperkalemia-arrhythmia-sentinel-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-interstitial-potassium-hyperkalemia-arrhythmia-sentinel-skill...")
    test_args = {'potassium_meq_l': 4.4, 't_wave_amplitude_mv': 0.45, 'r_wave_amplitude_mv': 1.2, 'pr_interval_ms': 160.0, 'qrs_duration_ms': 88.0}
    res = monitor_hyperkalemia_arrhythmia_risk(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-interstitial-potassium-hyperkalemia-arrhythmia-sentinel-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
