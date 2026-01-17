# Azure Infrastructure (IaC)

Ten katalog zawiera minimalny przykład Infrastructure as Code w Azure, przygotowany w Bicep.

Celem jest demonstracja:
- znajomości IaC,
- umiejętności definiowania zasobów Azure,
- integracji warstwy infrastruktury z projektem kontenerowym.

## Zawartość

- `main.bicep` – definicja Azure Container Registry (ACR)
- `parameters.json` – przykładowe parametry wdrożeniowe
- `README.md` – opis infrastruktury

## Opis infrastruktury

Szablon `main.bicep` tworzy:
- Azure Container Registry (ACR)

Zasób ten może być wykorzystany do:
- przechowywania obrazów Docker aplikacji,
- integracji z pipeline CI/CD,
- dalszej rozbudowy infrastruktury (np. AKS, App Service).

## Deployment (opcjonalny)

Wdrożenie wymaga aktywnej subskrypcji Azure.

Przykładowe polecenie:
```bash
az deployment group create \
  --resource-group <resource-group-name> \
  --template-file main.bicep \
  --parameters @parameters.json
