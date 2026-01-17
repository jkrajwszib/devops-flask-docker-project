# Azure IaC (minimal)

Ten katalog zawiera minimalną infrastrukturę jako kod (Bicep) wymaganą w projekcie:
- Resource Group (tworzona osobno komendą `az group create`)
- Azure Container Registry (ACR) – tworzony przez `main.bicep`

## Wymagania
- Azure CLI (az)
- Zalogowane konto: `az login`

## Kroki

1. Utwórz Resource Group

```bash
az group create --name <RG_NAME> --location <LOCATION>