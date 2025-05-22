import json
from datetime import datetime

import dns.resolver
import whois
from future.standard_library import imp


class DomainAnalyzer:
    def __init__(self, domain):
        self.domain = domain
        self.api_url = "http://api:8000/analyze/"
        self.report = {
            "metadata": {
                "date": datetime.now().isoformat(),
                "domain": domain,
                "tool": "ReconBot Pro v3.1",
            },
            "dns": {},
            "whois": {},
            "dorks": {},
            "security_analysis": {},
        }

    def run_dns_scan(self):
        records = ["A", "MX", "NS", "SOA", "TXT"]
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5

        for record in records:
            try:
                answers = resolver.resolve(self.domain, record)
                self.report["dns"][record] = [str(r) for r in answers]
            except dns.resolver.NoAnswer:
                self.report["dns"][record] = "No records found"
            except dns.resolver.NXDOMAIN:
                self.report["dns"][record] = "Domain does not exist"
                break
            except Exception as e:
                self.report["dns"][record] = f"Error: {str(e)}"

        # Análisis de seguridad DNS mejorado
        txt_records = self.report["dns"].get("TXT", [])
        ns_records = self.report["dns"].get("NS", [])

        self.report["security_analysis"]["dns"] = {
            "has_dmarc": any(
                "v=DMARC1" in r for r in txt_records if isinstance(r, str)
            ),
            "has_spf": any(
                "v=spf1" in r.lower() for r in txt_records if isinstance(r, str)
            ),
            "has_secure_ns": any(
                any(
                    provider in ns.lower()
                    for provider in ["cloudflare", "awsdns", "akam", "fastly"]
                )
                for ns in ns_records
                if isinstance(ns, str)
            ),
            "has_dkim": any("DKIM1" in r for r in txt_records if isinstance(r, str)),
            "is_cdn_protected": any(
                ns.lower().endswith((".cdn.", ".cdncloud.", ".akamaized."))
                for ns in ns_records
                if isinstance(ns, str)
            ),
        }

    def run_whois_lookup(self):
        try:
            # Manejo especial para dominios .cl
            if self.domain.endswith(".cl"):
                w = whois.whois(self.domain, flags={"server": "whois.nic.cl"})
            else:
                w = whois.whois(self.domain)

            # Procesamiento seguro de fechas (pueden venir como lista)
            def process_date(date):
                if not date:
                    return None
                if isinstance(date, list):
                    return date[0] if date else None
                return date

            creation_date = process_date(w.creation_date)
            expiration_date = process_date(w.expiration_date)

            # Procesamiento de emails (pueden venir como str, list o None)
            emails = []
            if w.emails:
                if isinstance(w.emails, str):
                    emails = [w.emails]
                elif isinstance(w.emails, list):
                    emails = [e for e in w.emails if isinstance(e, str)]

            self.report["whois"] = {
                "registrar": w.registrar,
                "creation_date": str(creation_date) if creation_date else None,
                "expiration_date": str(expiration_date) if expiration_date else None,
                "name_servers": (
                    list(set(ns.lower() for ns in w.name_servers))
                    if w.name_servers
                    else []
                ),
                "status": w.status,
                "emails": emails,
            }

            # Análisis de seguridad WHOIS
            domain_age = (datetime.now() - creation_date).days if creation_date else 0
            is_expired = expiration_date < datetime.now() if expiration_date else False

            self.report["security_analysis"]["whois"] = {
                "domain_age_days": domain_age,
                "is_expired": is_expired,
                "privacy_protection": any(
                    "privacy" in str(s).lower() or "proxy" in str(s).lower()
                    for s in (
                        [w.status] if isinstance(w.status, str) else w.status or []
                    )
                ),
                "is_recent": domain_age < 365 if domain_age else False,
                "registrar_reputation": "unknown",  # Podrías añadir una lista de registradores de confianza
            }

        except Exception as e:
            self.report["whois"] = {"error": str(e)}
            self.report["security_analysis"]["whois"] = {
                "error": "No se pudo obtener información WHOIS",
                "details": str(e),
            }

    def save_report(self, filename=None):
        filename = filename or f"{self.domain}_report.json"
        with open(filename, "w") as f:
            json.dump(self.report, f, indent=4)
        print(f"Reporte guardado como {filename}")
        return filename


# Ejemplo de uso
if __name__ == "__main__":
    analyzer = DomainAnalyzer(
        "educativaipchile.cl"
    )  # Cambia por el dominio que quieras analizar
    print(f"Analizando dominio: {analyzer.domain}")
    analyzer.run_dns_scan()
    analyzer.run_whois_lookup()
    report_file = analyzer.save_report()

    print("\nResumen del análisis:")
    print(
        f"- DNS Records: {len(analyzer.report['dns'])} tipos de registros encontrados"
    )
    print(
        f"- Edad del dominio: {analyzer.report['security_analysis']['whois'].get('domain_age_days', 'N/A')} días"
    )
    print(
        f"- Protección SPF: {'Sí' if analyzer.report['security_analysis']['dns']['has_spf'] else 'No'}"
    )
    print(
        f"- Protección DMARC: {'Sí' if analyzer.report['security_analysis']['dns']['has_dmarc'] else 'No'}"
    )
