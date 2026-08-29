# Responsible AI Log: NetSage AI Corrected Cases

This log tracks instances where the AI generated an incorrect or incomplete diagnosis that required human correction before being accepted. This ensures accountability and helps improve the AI prompt and rule-checking logic over time.

## Case 1: VLAN Misconfiguration (Symptom: PC cannot reach server)
- **AI Diagnosis:** The AI correctly identified that the trunk link was missing VLAN 30, but suggested `switchport trunk allowed vlan 30` which replaces the allowed VLAN list.
- **Human Correction:** A human reviewer caught this and corrected the fix step to `switchport trunk allowed vlan add 30` to prevent taking down other VLANs on the trunk.
- **Action Taken:** Updated the AI prompt library with a specific example emphasizing the `add` keyword when modifying allowed VLAN lists.

## Case 2: DHCP Pool Exhaustion (Symptom: New devices cannot get IPs)
- **AI Diagnosis:** The AI claimed the DHCP server service was disabled, because it didn't see `service dhcp` in the provided snippet.
- **Human Correction:** The human reviewer noted that the `show ip dhcp pool` output indicated "Free addresses: 0". The AI missed this critical evidence. The human corrected the root cause to "DHCP Pool Exhaustion" and changed the fix to expanding the pool or reducing lease time.
- **Action Taken:** Instructed the AI to prioritize data from `show ip dhcp pool` when investigating missing IP addresses.

## Case 3: OSPF Neighbor Adjacency Failure (Symptom: Branch A cannot reach Branch B)
- **AI Diagnosis:** AI identified that OSPF neighbors were missing, and incorrectly guessed that the interface was passive based on general OSPF issues.
- **Human Correction:** Human reviewer noticed the network statements had mismatched wildcard masks. The AI failed to compute that the IP address `10.1.1.1/30` didn't match the network statement `10.1.1.0 0.0.0.255`. 
- **Action Taken:** Handled by running the Python Rule Checker beforehand to detect subnet mismatches more reliably than the LLM.

## Case 4: DNS Resolution Issue (Symptom: Users can ping 8.8.8.8 but no URLs work)
- **AI Diagnosis:** AI diagnosed an ACL blocking DNS traffic on port 53.
- **Human Correction:** There were no ACLs in the `show run` output. The actual issue was a typo in the DHCP pool where the DNS server was given as `8.8.9.8` instead of `8.8.8.8`. The AI hallucinated the ACL because it is a common reason for DNS failure.
- **Action Taken:** Prompt modified to enforce the rule: "Do not guess or assume configurations that are not present in the show outputs."

## Case 5: WLC Guest WLAN Mapping (Symptom: Guest Wi-Fi clients get internal IPs)
- **AI Diagnosis:** AI suggested checking the physical switchport for the wrong access VLAN.
- **Human Correction:** The topology explicitly stated a Lightweight AP with a WLC. In a CAPWAP tunnel, the switchport VLAN doesn't dictate the client VLAN. The WLAN to interface mapping on the WLC was wrong. 
- **Action Taken:** Added a Wireless-specific example to the prompt library so the AI understands WLC logical mappings versus physical switchport VLANs.
