# BuyerMoment Azure footprint

This directory provisions a fresh, isolated development footprint. It does not reference the existing NeonPing or IntentPilot resource groups.

Resources are tagged `product=BuyerMoment`, `environment=dev`, `costOwner=BuyerMoment`, and `creditGuardrail=startup-credit` so spend can be filtered in the Azure portal.

The first deployment deliberately has no always-on PostgreSQL server and no model deployment. The app remains runnable locally, while Blob Storage, Key Vault, Container Registry, Log Analytics, Container Apps Environment, and an AIServices/Foundry account establish the provider seams. Add a model deployment only after verifying the model is Direct from Azure / startup-credit eligible and after a 100-record validation run.

```bash
az group create --name rg-buyermoment-dev --location eastus2 --tags product=BuyerMoment environment=dev costOwner=BuyerMoment managedBy=buyerMoment-iac
az deployment group create --resource-group rg-buyermoment-dev --template-file infra/main.bicep --parameters @infra/parameters.dev.json
```

No resource in this template is a reference to an existing resource. The only shared platform dependency is the Azure subscription itself.

