from flask import Flask, request, jsonify, send_from_directory
import os
import re
import json
import urllib.request
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
    api_key = data.get('api_key', '').strip()

    # 1. Run Python Rule Checker (Deterministic Validation)
    network_state = parse_telemetry_for_rule_checker(telemetry)
    checker = RuleChecker()
    rule_issues = checker.run_checks(network_state)

    # 2. Call AI LLM
    ai_response = None
    if api_key:
        print("Using Live OpenAI API Mode...")
        ai_response = call_live_openai(symptom, telemetry, api_key)
        
    if not ai_response:
        print("Using Simulation Mode...")
        ai_response = simulate_llm_response(symptom, telemetry)

    return jsonify({
        "ai_diagnosis": ai_response,
        "rule_checker_issues": rule_issues
    })

def call_live_openai(symptom, telemetry, api_key):
    try:
        # Read the prompt system message we engineered
        with open('diagnose_prompt.md', 'r') as f:
            system_prompt = f.read()

        user_content = f"Symptom/Context:\n{symptom}\n\nTelemetry:\n{telemetry}\n\nDiagnose this."
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1
        }
        
        req = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply_text = result['choices'][0]['message']['content']
            
            # Extract JSON from markdown block if present
            json_str = reply_text
            if '```json' in reply_text:
                json_str = reply_text.split('```json')[1].split('```')[0].strip()
            elif '```' in reply_text:
                json_str = reply_text.split('```')[1].split('```')[0].strip()
                
            return json.loads(json_str)
            
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return None

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
