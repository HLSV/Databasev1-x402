import json
import urllib.request
from datetime import datetime, timezone

URL_FONTE = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def gerar_boletim_cyber():
    print("Coletando boletins oficiais de cibersegurança...")
    req = urllib.request.Request(
        URL_FONTE,
        headers={"User-Agent": "CyberThreatDatasetBuilder/1.0"}
    )
    
    with urllib.request.urlopen(req, timeout=20) as response:
        raw_data = json.loads(response.read().decode("utf-8"))

    vulnerabilidades = raw_data.get("vulnerabilities", [])
    # Pega os 150 boletins mais recentes e ordena do mais novo para o mais antigo
    recentes = sorted(
        vulnerabilidades,
        key=lambda x: x.get("dateAdded", ""),
        reverse=True
    )[:150]

    registros_limpos = []
    for idx, item in enumerate(recentes, start=1):
        registros_limpos.append({
            "report_id": f"SEC-{idx:04d}",
            "cve_id": item.get("cveID", "").strip(),
            "vendor": item.get("vendorProject", "").strip(),
            "product": item.get("product", "").strip(),
            "advisory_title": item.get("vulnerabilityName", "").strip(),
            "technical_summary": item.get("shortDescription", "").strip(),
            "remediation_action": item.get("requiredAction", "").strip(),
            "known_ransomware_use": item.get("knownRansomwareCampaignUse", "Unknown"),
            "published_date": item.get("dateAdded", ""),
            "remediation_due_date": item.get("dueDate", "")
        })

    dataset_final = {
        "metadata": {
            "dataset_name": "Global Cybersecurity Threat & Exploited Vulnerabilities Bulletin",
            "language": "en",
            "format": "structured_json",
            "source_authority": "CISA / Public Security Advisories",
            "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_records": len(registros_limpos)
        },
        "bulletins": registros_limpos
    }

    with open("dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset_final, f, indent=2, ensure_ascii=False)

    print(f"Sucesso! dataset.json gerado com {len(registros_limpos)} boletins técnicos.")

if __name__ == "__main__":
    gerar_boletim_cyber()

