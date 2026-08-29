# Cisco AI Internship Final Project Summary
**Project Title:** NetSage AI - Advanced Diagnostic Engine  
**Domain:** Artificial Intelligence in Networking  

### Student Details (Solo Project)
- **Student Name:** [Enter Your Name Here]
- **College Name:** [Enter Your College Name Here]
- **AICTE ID:** [Enter Your AICTE ID Here]
- **Stream/Branch:** [Enter Your Branch, e.g., B.Tech Computer Science]

---

## 1. Project Overview
NetSage AI is an AI-assisted network troubleshooting application designed to bridge the gap between complex network telemetry and rapid incident resolution. The primary goal of this project was to build an intelligent assistant capable of analyzing raw CLI outputs (e.g., `show run`, `show ip route`) from simulated Packet Tracer environments, diagnosing the root cause, and suggesting deterministic fix steps—while keeping a human engineer firmly in the loop.

This project goes beyond simple scripts by delivering a **Full-Stack Web Application** that demonstrates how AI can be securely and professionally integrated into enterprise networking workflows.

---

## 2. Core Architecture
The application uses a decoupled, full-stack architecture to ensure scalability and safety:

### A. The Frontend (Holographic Dashboard)
- **Technology:** HTML5, Vanilla JavaScript, CSS3, Chart.js
- **Features:** A professional, glassmorphism-themed UI featuring an Analytics Dashboard, an interactive Diagnostic Terminal, and an integrated Responsible AI Matrix Log.
- **Functionality:** Engineers paste telemetry into the terminal, and the UI asynchronously communicates with the backend API to retrieve analysis without page reloads.

### B. The Backend (Python Flask API)
- **Technology:** Python, Flask (`app.py`)
- **Features:** Acts as the secure middleware between the user interface and the AI engine. It parses incoming telemetry and manages the diagnostic pipeline.

### C. The AI Engine & Prompt Engineering
- **Technology:** Advanced Few-Shot Prompting (`diagnose_prompt.md`)
- **Features:** The system uses a highly structured prompt library that forces the LLM to output strictly formatted JSON containing `root_cause`, `confidence`, `evidence`, `next_command`, and `fix_steps`. 

### D. Deterministic Rule Checker (Safety Guardrails)
- **Technology:** Python (`rule_checker.py`)
- **Features:** Because LLMs can hallucinate, a deterministic Python script runs in parallel to the AI. It uses hard-coded logic to check for critical misconfigurations (e.g., wildcard mask mismatches, missing VLANs). If the AI makes a dangerous suggestion, the Rule Checker overrides it and warns the engineer.

---

## 3. Key Deliverables & Requirements Fulfilled

### ✔️ 1. Dataset Generation (`cases.csv`)
A Python script (`generate_cases.py`) was developed to synthesize a realistic dataset of 34 distinct network failure scenarios. The dataset covers Layer 1 to Layer 7 issues, including VLAN misconfigurations, DHCP exhaustion, OSPF adjacency failures, and DNS typos.

### ✔️ 2. AI Troubleshooting Helper
The core engine successfully parses raw text symptoms and CLI outputs, mapping them to known networking failure states and generating actionable remediation steps.

### ✔️ 3. Responsible AI & Human-in-the-Loop
An AI is only as good as its guardrails. The project features a strict Human-in-the-Loop workflow requiring engineers to "Authorize", "Modify", or "Deny" the AI's suggestions. Instances where the AI failed (e.g., suggesting a command that would wipe a VLAN trunk) were documented and integrated directly into the dashboard's **Responsible AI Matrix Log** for continuous model retraining.

### ✔️ 4. Interactive Demonstration
The final deliverable is not just code—it is a fully deployable, highly interactive demonstration that proves the viability of the AI assistant in a realistic Operations Center environment.

---

## 4. How to Deploy and Test
To run this project locally:
1. Open a terminal in the project directory.
2. Install dependencies: `pip install flask`
3. Start the backend server: `python app.py`
4. Open a web browser and navigate to: `http://localhost:5000`
5. Authenticate with any Engineer ID to access the dashboard and initiate diagnostic scans.

---
*Report generated for Cisco AI Internship Evaluation.*
