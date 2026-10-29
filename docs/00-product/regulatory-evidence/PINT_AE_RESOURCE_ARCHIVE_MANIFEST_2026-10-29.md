# PINT AE and UAE E-Invoicing Resource Evidence — 29 October 2026

| Property | Value |
|---|---|
| Document ID | REG-EV-EINV-20261029-001 |
| Status | VERIFIED RETRIEVAL EVIDENCE — NOT A COMPLIANCE CERTIFICATE |
| Evidence cut-off | 29 October 2026 |

## 1. OpenPeppol Resource Archives

| Publication | Source URL | Bytes | Entries | SHA-256 |
|---|---|---:|---:|---|
| Historical `2025-Q2` PINT AE Billing | `https://docs.peppol.eu/poac/ae/2025-Q2/pint-ae/resources.zip` | 939,553 | 69 | `f7f7dab580e6bc7d78b0492ed79e3bb1ad8061ff1694d90f4f7236bc81939562` |
| Historical `2025-Q2` PINT AE Self-Billing | `https://docs.peppol.eu/poac/ae/2025-Q2/pint-ae-sb/resources.zip` | 726,148 | 53 | `ffbedf890086681ff0768c86a6807147a76150611b9b0dac3aa50f190a97acd3` |
| Current PINT AE Billing `1.0.4` | `https://docs.peppol.eu/poac/ae/pint-ae/resources.zip` | 1,019,347 | 78 | `1e8b0bd595c672ac9d6fc886ddd0eb8027cb39a1d26bebdcb1ada37b7eee491f` |
| Current PINT AE Self-Billing `1.0.4` | `https://docs.peppol.eu/poac/ae/pint-ae-sb/resources.zip` | 784,521 | 50 | `7e6e58f120132dd2d2a6acf21b4a9318f0d07f2685c30ff282fae0e2a6613d15` |
| Current UAE TDD `1.0.4` | `https://docs.peppol.eu/poac/ae/ae-tdd/resources.zip` | 346,951 | 17 | `56cb018a5ac0500f5e6e9841788c8b62d894942ff820ab5449d90fdeb9981649` |

The archives were downloaded over HTTPS, hashed, opened with `.NET System.IO.Compression`, and entry-counted. The current URLs are mutable publication pointers. A build must use an internally preserved immutable copy matching the approved digest, subject to licensing and binary-storage policy; this register does not vendor the binaries into Git.

## 2. Current Release Resolution

The OpenPeppol UAE index retrieved on the evidence date identifies Billing `1.0.4`, Self-Billing `1.0.4`, TDD `1.0.4`, and PDK `1.4.4` released 29 July 2026. Billing release notes identify PINT AE `1.0.4`, PINT General `1.1.3`, release date 2 June 2026 and status `Final`. The notes state that this release corrects validation logic and stability without changing the semantic data model.

Therefore `2025-Q2` / `1.0.0` is historical evidence, while `1.0.4` is the current technical implementation candidate. Production activation still requires the selected UAE Accredited Service Provider (ASP), qualified UAE reviewer and Product Owner to confirm the contracted release and effective date. Billing, Self-Billing and TDD remain separate profiles and approval scopes.

## 3. Current Ministry Files

| Publication | Source URL | Bytes | SHA-256 | Observed content version |
|---|---|---:|---|---|
| UAE Electronic Invoicing Guidelines | `https://mof.gov.ae/wp-content/uploads/2026/10/UAE-Electronic-Invoicing-Guidelines_En.pdf` | 1,471,735 | `c85a45a440fe0b822f393cb052794749296365b8d3029d26d6fe80ad6726b9cb` | V2.0, 26 October 2026 |
| UAE Electronic Invoice Mandatory Field Requirements | `https://mof.gov.ae/wp-content/uploads/2026/10/UAE-Electronic-Invoice-Mandatory-Field-Requirements.pdf` | 418,512 | `cc7090af816eb35e7d205328de0fc245df0d682f5e9b90f1c682526b52394c88` | Current portal file retrieved 29 October 2026 |

The earlier June URL currently resolves to content marked V2.0. Implementers must verify document content and digest rather than infer version from a URL or filename.

## 4. Archive Content Verification

The Billing archives contain separate Invoice and Credit Note examples, generic PINT Schematron, AE-aligned Schematron and compiled XSLT. The current Billing archive adds identifier, allowance/charge and volume-discount examples. Self-Billing contains separate self-billed Invoice/Credit Note resources. TDD contains examples plus its own Schematron/XSLT.

The ZIPs do not contain the full browsable semantic-model and syntax-binding tables. The release set therefore comprises both the checksummed resources and a captured/reviewed semantic-to-UBL mapping from the same published version. Mixing releases is prohibited.

## 5. Reproduction Commands

```powershell
Invoke-WebRequest -Uri <source-url> -OutFile <local-file>
Get-FileHash -Algorithm SHA256 <local-file>
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead((Resolve-Path <local-file>))
$zip.Entries.Count
$zip.Dispose()
```

Record retrieval timestamp, source, bytes, digest, inventory and operator in release evidence. A changed digest at an unversioned URL opens a regulatory-change issue and blocks the affected deployment until reviewed.

## 6. E-Way-Bill Finding

No general UAE e-way-bill requirement was identified in the current MoF portal, V2.0 Guidelines, mandatory-field publication or PINT AE/TDD index at this cut-off. The Guidelines define an `Airway Bill` for an airline context; that is not a general road-goods e-way bill. Do not import another jurisdiction's e-way-bill workflow by analogy. Delivery/despatch, airway-bill, customs or transport references may be supported only under their own verified business or UAE regulatory requirements.

## 7. Limitations

Checksums prove file identity, not correctness, legal applicability, provider acceptance or regulatory compliance. Production still requires exact-source archiving, qualified UAE tax/legal review, ASP contract/conformance evidence, security review, tests and explicit approval.
