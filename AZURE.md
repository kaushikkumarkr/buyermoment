# Azure operating notes

## Dedicated resource decision

The dedicated BuyerMoment deployment is intentionally separate from the existing NeonPing/IntentPilot resource groups. The deployment name is `rg-buyermoment-dev`; resource IDs and outputs should be written to `BUILD_STATUS.md` after provisioning.

## Credit guardrails

- Use only Microsoft/Azure-billed model deployments after billing eligibility is verified in the Azure portal / model catalog.
- Run 100 examples first, inspect outputs, then 500, then scale only when evaluation justifies it.
- Do not create AKS, GPUs, Databricks, or always-on VMs.
- The initial Bicep footprint uses Standard_LRS storage, ACR Basic, 30-day Log Analytics retention, an empty Container Apps Environment, and no managed PostgreSQL server.
- Before a model batch, record estimated input/output tokens, deployment SKU, batch size, and expected spend in the evaluation artifact.

## Model configuration

Logical roles are configured by environment variables rather than hard-coded deployments: `bulk_generator`, `extractor`, `judge`, `reasoner`, and `fallback`.

The Phase 2 model decision uses Azure-direct GPT deployments after checking the Microsoft Foundry sponsorship guidance. The deterministic provider remains the evaluation fallback; partner/community models are not enabled.

## Deployment shape

Use a Container Apps API and web container after images exist in the new registry. Key Vault should hold secrets, and Managed Identity should be used for storage, registry pull, and Key Vault access. The current local MVP does not include a live customer authentication surface; tenant/org IDs are represented in the data model boundary and must be wired before production use.
