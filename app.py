from flask import Flask, request, jsonify, send_from_directory
import os
import re
from rule_checker import RuleChecker

app = Flask(__name__, static_folder='.')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    symptom = data.get('symptom', '')
    telemetry = data.get('telemetry', '')

    # 1. Run Python Rule Checker (Deterministic Validation)
    # We parse the telemetry to build a mock network state for the rule checker
    network_state = parse_telemetry_for_rule_checker(telemetry)
    checker = RuleChecker()
    rule_issues = checker.run_checks(network_state)

    # 2. Call AI LLM (This is where you would put your OpenAI/Gemini API key in a real production environment)
    # Since we don't have your API key, we simulate the LLM response based on the prompt structure.
    ai_response = simulate_llm_response(symptom, telemetry)

    return jsonify({
        "ai_diagnosis": ai_response,
        "rule_checker_issues": rule_issues
    })

def parse_telemetry_for_rule_checker(telemetry):
    """Parses raw CLI output into a structured state for rule_checker.py"""
    state = {"routers": [], "switches": [], "hosts": [], "required_vlans": []}
    
    # Very basic parsing for demonstration purposes
    if "administratively down" in telemetry.lower():
        state["routers"].append({
            "name": "ExtractedDevice",
            "interfaces": [{"name": "Unknown", "status": "down"}]
        })
    
    if "allowed on trunk" in telemetry.lower() and "30" not in telemetry:
        state["switches"].append({"name": "ExtractedSwitch", "vlans": [1]})
        state["required_vlans"].append(30)
        
    return state

def simulate_llm_response(symptom, telemetry):
    """Simulates the LLM JSON output. In production, replace this with an API call using diagnose_prompt.md"""
    lower_tel = telemetry.lower()
    
    if "administratively down" in lower_tel:
        return {
            "root_cause": "An interface required for connectivity is administratively shut down.",
            "confidence": "High",
            "evidence": "show command reveals the interface is administratively down.",
            "next_command": "show ip interface brief",
            "fix_steps": ["conf t", "interface <name>", "no shutdown"]
        }
    elif "allowed on trunk" in lower_tel:
        return {
            "root_cause": "A required VLAN is missing from the trunk allowed list.",
            "confidence": "High",
            "evidence": "The allowed VLAN list on the trunk interface does not include the necessary VLAN.",
            "next_command": "show interfaces trunk",
            "fix_steps": ["conf t", "interface <trunk-port>", "switchport trunk allowed vlan 30"]
        }
    else:
         return {
            "root_cause": "Unable to pinpoint exact fault in the provided CLI outputs.",
            "confidence": "Low",
            "evidence": "Missing clear indicators in telemetry.",
            "next_command": "show run",
            "fix_steps": ["Review full running configuration"]
        }

if __name__ == '__main__':
    print("Starting NetSage AI Professional Backend...")
    print("Serving on http://localhost:5000")
    app.run(debug=True, port=5000)
