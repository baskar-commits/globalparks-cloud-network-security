# GlobalParks Cloud Network Security and Management Architecture

Detailed Design Document (DDD) for the GlobalParks platform - a multi-regional, cloud-native national park management system built on Microsoft Azure.

## What is in this repository

| File | Description |
|---|---|
| [`DESIGN.md`](DESIGN.md) | The full Detailed Design Document - scenarios, requirements, architecture walkthrough, decision records, and traceability matrix |
| [`azure-networking-flowchart.html`](azure-networking-flowchart.html) | Interactive architecture visualization - open in a browser |

## How to read the design document

Open [`DESIGN.md`](DESIGN.md) directly in GitHub. The document renders with full Mermaid diagram support - the Security Operations diagram in Section 4.3 and the N-Tier diagram in Appendix A display automatically.

The document is structured for two reading modes:

- **Top-down narrative** - Read Sections 1 through 5 in order to understand the architecture from first principles
- **Scenario-driven** - Jump to [Section 6 - Scenario Traces](DESIGN.md#6-scenario-traces) and follow a specific user journey (e.g. SCN-009: Sydney visitor booking Great Barrier Reef), then follow the `STEP-###` links back into Section 5 for detail on each hop

## Interactive visualization

Download the repository and open `azure-networking-flowchart.html` in any browser (Chrome, Edge, Firefox). No server or installation required - it is a single self-contained HTML file.

The interactive view supports:

- **Filter by Tier** - highlight all components in a tier (T0 through T8)
- **Filter by Scenario** - highlight the full path a specific user journey takes (SCN-001 through SCN-010)
- **Filter by Requirement** - highlight which components satisfy a given requirement (REQ-1.1 through REQ-4.3)
- **Filter by Step** - highlight components for a specific architecture step (STEP-010 through STEP-090)
- **Filter by OSI Layer** - highlight components operating at L1 through L7
- **Walkthrough mode** - step through SCN-009 (Sydney to Great Barrier Reef) and SCN-010 (Sydney to Yosemite) node by node with descriptions

## Architecture summary

The platform follows a Zero Trust, defence-in-depth model across eight tiers:

| Tier | Step | Description |
|---|---|---|
| Tier 0 | STEP-010 | External users - B2C Visitors, Park Administrators, Park Rangers |
| Tier 1 | STEP-030 | Internet edge - Azure Front Door, WAF, DDoS Protection (B2C path only) |
| Tier 2 | STEP-020 | Identity - Entra External ID (B2C), Entra ID + Conditional Access (Admin/Ranger) |
| Tier 3 | STEP-040/041 | Private connectivity - ExpressRoute, Azure Virtual WAN, VPN Gateway |
| Tier 4 | STEP-050 | Hub VNet - Azure Firewall Premium (24 instances across 12 regions) |
| Tier 5A/5B | STEP-060A/060B | Spoke VNets - 12 B2C public spokes + 12 Admin/Ranger private spokes |
| Tier 6 | STEP-070 | Data tier - Azure SQL + Cosmos DB via Private Endpoints |
| Tier 7 | STEP-080 | Security operations - Sentinel, Defender for Cloud, Azure Monitor, Azure Policy |
| Tier 8 | STEP-090 | On-premises and hybrid - Legacy systems, IoT, Government agency integration |

**Scale:** 12 Azure regions (4 Americas, 4 Europe, 4 Asia), 12 Hub VNets, 24 Spoke VNets, 24 Azure Firewall Premium instances, 12 Azure Virtual WAN instances.

**Compliance:** PCI-DSS, GDPR, ISO 27001, NIST.
