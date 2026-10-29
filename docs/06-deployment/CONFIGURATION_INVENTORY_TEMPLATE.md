# Environment Configuration Inventory Template

| Document ID | DEP-CONFIG-TPL-001 |
|---|---|
| Status | TEMPLATE — EXACT VARIABLES GENERATED IN P01/P12 |

| Key | Owner component | Environments | Type/validation | Secret? | Required/default | Rotation/change effect | Restart/reload | Evidence exposure | Owner |
|---|---|---|---|---|---|---|---|---|---|
| `EXAMPLE_ONLY` | — | — | — | — | — | — | — | — | — |

Rules: production-critical values fail closed; secrets have no committed value/default; URLs/hosts/schemes and numeric bounds validate; environment authority is least privilege; changes are versioned/audited; secret values are redacted from logs/CI/evidence; removed keys preserve migration/deprecation notes. The implemented inventory replaces the example row and is reconciled with `ENVIRONMENT_VARIABLES.md`.
