"""One-off: add nav-* anchors and normalize fragment links in SASE-DESIGN.md."""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "SASE-DESIGN.md"
text = path.read_text(encoding="utf-8")

for old, new in [
    ("#5-architecture-walkthrough", "#nav-section-5"),
    ("#6-scenario-traces", "#nav-section-6"),
    ("#4-security-architecture-overview", "#nav-section-4"),
    ("#3-user-personas", "#nav-section-3"),
    ("#7-requirements-traceability-matrix", "#nav-section-7"),
    ("#11-glossary-and-acronyms", "#nav-section-1-1"),
    ("#2-platform-context-and-constraints", "#nav-section-2"),
    ("#1-executive-summary", "#nav-section-1"),
    ("#platform-delivery-and-operations-beyond-section-1", "#nav-section-2-delivery"),
    ("#8-architectural-decisions", "#nav-section-8"),
    ("#9-open-questions", "#nav-section-9"),
    ("#10-revision-history", "#nav-section-10"),
    ("#using-this-document-with-the-flowchart", "#nav-using-flowchart"),
]:
    text = text.replace(old, new)

step = {
    "#step-010---users-and-personas": "#nav-step-010",
    "#step-020---identity-and-access": "#nav-step-020",
    "#step-040---connectivity---park-administrators-sd-wan-to-sase-pop": "#nav-step-040",
    "#step-041---connectivity---park-rangers-ztna-via-entra-private-access": "#nav-step-041",
    "#step-030---internet-edge-and-global-routing": "#nav-step-030",
    "#step-050---sase-pop-and-private-access-connector-replaces-hub-vnet": "#nav-step-050",
    "#step-060a---b2c-app-vnet---public-web-tier": "#nav-step-060a",
    "#step-060b---adminranger-app-vnet---internal-app-tier": "#nav-step-060b",
    "#step-070---regional-data-tier": "#nav-step-070",
    "#step-080---security-operations-and-governance": "#nav-step-080",
    "#step-090---on-premises-and-hybrid-systems": "#nav-step-090",
}
for o, n in step.items():
    text = text.replace(o, n)

scn = {
    "#scn-001---public-visitor-accesses-the-globalparks-platform": "#nav-scn-001",
    "#scn-002---park-administrator-accesses-via-sd-wan-and-sase": "#nav-scn-002",
    "#scn-002b---park-ranger-accesses-via-ztna": "#nav-scn-002b",
    "#scn-003---attacker-attempts-ddos-and-sqli-against-public-endpoints": "#nav-scn-003",
    "#scn-004---cross-region-traffic": "#nav-scn-004",
    "#scn-005---soc-investigates-a-multi-stage-attack": "#nav-scn-005",
    "#scn-006---iot-sensor-sends-telemetry-to-azure-iot-hub": "#nav-scn-006",
    "#scn-007---legacy-park-system-syncs-to-azure-sql": "#nav-scn-007",
    "#scn-008---government-agency-accesses-park-data": "#nav-scn-008",
    "#scn-009---sydney-visitor-books-a-campsite-at-great-barrier-reef-gold-coast-australia": "#nav-scn-009",
    "#scn-010---sydney-visitor-books-a-campsite-at-yosemite-national-park-california-usa": "#nav-scn-010",
}
for o, n in scn.items():
    text = text.replace(o, n)

# Section heading anchors (insert once each)
blocks = [
    ("## 1. Executive Summary\n", '<a id="nav-section-1"></a>\n\n## 1. Executive Summary\n'),
    ("## 2. Platform Context and Constraints\n", '<a id="nav-section-2"></a>\n\n## 2. Platform Context and Constraints\n'),
    ("## 3. User Personas\n", '<a id="nav-section-3"></a>\n\n## 3. User Personas\n'),
    ("## 4. Security Architecture Overview\n", '<a id="nav-section-4"></a>\n\n## 4. Security Architecture Overview\n'),
    ("## 5. Architecture Walkthrough\n", '<a id="nav-section-5"></a>\n\n## 5. Architecture Walkthrough\n'),
    ("## 6. Scenario Traces\n", '<a id="nav-section-6"></a>\n\n## 6. Scenario Traces\n'),
    ("## 7. Requirements Traceability Matrix\n", '<a id="nav-section-7"></a>\n\n## 7. Requirements Traceability Matrix\n'),
    ("## 8. Architectural Decisions\n", '<a id="nav-section-8"></a>\n\n## 8. Architectural Decisions\n'),
    ("## 9. Open Questions\n", '<a id="nav-section-9"></a>\n\n## 9. Open Questions\n'),
    ("## 10. Revision History\n", '<a id="nav-section-10"></a>\n\n## 10. Revision History\n'),
]
for old, new in blocks:
    if old not in text:
        raise SystemExit(f"Missing block for insert: {old!r}")
    text = text.replace(old, new, 1)

text = text.replace(
    "### Using this document with the flowchart\n",
    '<a id="nav-using-flowchart"></a>\n\n### Using this document with the flowchart\n',
    1,
)

text = text.replace(
    "### 1.1 Glossary and Acronyms\n",
    '<a id="nav-section-1-1"></a>\n\n### 1.1 Glossary and Acronyms\n',
    1,
)

text = text.replace(
    '<a id="platform-delivery-and-operations-beyond-section-1"></a>\n\n### Platform delivery',
    '<a id="platform-delivery-and-operations-beyond-section-1"></a>\n<a id="nav-section-2-delivery"></a>\n\n### Platform delivery',
    1,
)

# STEP nav targets in Appendix F
step_headers = [
    ("### STEP-010 - Users and Personas\n", '<a id="nav-step-010"></a>\n\n### STEP-010 - Users and Personas\n'),
    ("### STEP-020 - Identity and Access\n", '<a id="nav-step-020"></a>\n\n### STEP-020 - Identity and Access\n'),
    ("### STEP-040 - Connectivity - Park Administrators (SD-WAN to SASE PoP)\n", '<a id="nav-step-040"></a>\n\n### STEP-040 - Connectivity - Park Administrators (SD-WAN to SASE PoP)\n'),
    ("### STEP-041 - Connectivity - Park Rangers (ZTNA via Entra Private Access)\n", '<a id="nav-step-041"></a>\n\n### STEP-041 - Connectivity - Park Rangers (ZTNA via Entra Private Access)\n'),
    ("### STEP-030 - Internet Edge and Global Routing\n", '<a id="nav-step-030"></a>\n\n### STEP-030 - Internet Edge and Global Routing\n'),
    ("### STEP-050 - SASE PoP and Private Access Connector (replaces Hub VNet)\n", '<a id="nav-step-050"></a>\n\n### STEP-050 - SASE PoP and Private Access Connector (replaces Hub VNet)\n'),
    ("### STEP-060A - B2C App VNet - Public Web Tier\n", '<a id="nav-step-060a"></a>\n\n### STEP-060A - B2C App VNet - Public Web Tier\n'),
    ("### STEP-060B - Admin/Ranger App VNet - Internal App Tier\n", '<a id="nav-step-060b"></a>\n\n### STEP-060B - Admin/Ranger App VNet - Internal App Tier\n'),
    ("### STEP-070 - Regional Data Tier\n", '<a id="nav-step-070"></a>\n\n### STEP-070 - Regional Data Tier\n'),
    ("### STEP-080 - Security Operations and Governance\n", '<a id="nav-step-080"></a>\n\n### STEP-080 - Security Operations and Governance\n'),
    ("### STEP-090 - On-premises and Hybrid Systems\n", '<a id="nav-step-090"></a>\n\n### STEP-090 - On-premises and Hybrid Systems\n'),
]
for old, new in step_headers:
    if old not in text:
        raise SystemExit(f"Missing STEP header: {old!r}")
    text = text.replace(old, new, 1)

# SCN nav: insert after existing long-form anchor line
scn_lines = [
    ('<a id="scn-001---public-visitor-accesses-the-globalparks-platform"></a>\n', '<a id="nav-scn-001"></a>\n'),
    ('<a id="scn-002---park-administrator-accesses-via-sd-wan-and-sase"></a>\n', '<a id="nav-scn-002"></a>\n'),
    ('<a id="scn-002b---park-ranger-accesses-via-ztna"></a>\n', '<a id="nav-scn-002b"></a>\n'),
    ('<a id="scn-003---attacker-attempts-ddos-and-sqli-against-public-endpoints"></a>\n', '<a id="nav-scn-003"></a>\n'),
    ('<a id="scn-004---cross-region-traffic"></a>\n', '<a id="nav-scn-004"></a>\n'),
    ('<a id="scn-005---soc-investigates-a-multi-stage-attack"></a>\n', '<a id="nav-scn-005"></a>\n'),
    ('<a id="scn-006---iot-sensor-sends-telemetry-to-azure-iot-hub"></a>\n', '<a id="nav-scn-006"></a>\n'),
    ('<a id="scn-007---legacy-park-system-syncs-to-azure-sql"></a>\n', '<a id="nav-scn-007"></a>\n'),
    ('<a id="scn-008---government-agency-accesses-park-data"></a>\n', '<a id="nav-scn-008"></a>\n'),
    ('<a id="scn-009---sydney-visitor-books-a-campsite-at-great-barrier-reef-gold-coast-australia"></a>\n', '<a id="nav-scn-009"></a>\n'),
    ('<a id="scn-010---sydney-visitor-books-a-campsite-at-yosemite-national-park-california-usa"></a>\n', '<a id="nav-scn-010"></a>\n'),
]
for old, ins in scn_lines:
    if old not in text:
        raise SystemExit(f"Missing SCN anchor: {old!r}")
    text = text.replace(old, old + ins, 1)

# Appendix E: back to Section 4 under §4.x headings (after ### line)
text = text.replace(
    "### 4.1 N-Tier Architecture Diagram\n\nThe SASE architecture retains",
    "### 4.1 N-Tier Architecture Diagram\n\n← [Back to Section 4 - Security Architecture Overview](#nav-section-4)\n\nThe SASE architecture retains",
    1,
)
text = text.replace(
    "### 4.2 OSI Layer Control Mapping\n\nThe OSI mapping",
    "### 4.2 OSI Layer Control Mapping\n\n← [Back to Section 4 - Security Architecture Overview](#nav-section-4)\n\nThe OSI mapping",
    1,
)
text = text.replace(
    "### 4.3 Security Detection and Prevention by Tier\n\nThe SASE architecture adds",
    "### 4.3 Security Detection and Prevention by Tier\n\n← [Back to Section 4 - Security Architecture Overview](#nav-section-4)\n\nThe SASE architecture adds",
    1,
)

path.write_text(text, encoding="utf-8")
print("Updated", path)
