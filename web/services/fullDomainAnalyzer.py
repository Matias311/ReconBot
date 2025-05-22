import json
from datetime import datetime

from .deepseek import consultar_deepseek
from .domain_analyzer import DomainAnalyzer
from .google_dorks import busqueda_start


class FullDomainAnalyzer:
    def __init__(self, domain):
        self.domain = domain
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
            "ai_analysis": {},
        }

    def run_full_analysis(self):
        # Ejecutar análisis DNS
        domain_analyzer = DomainAnalyzer(self.domain)
        domain_analyzer.run_dns_scan()
        domain_analyzer.run_whois_lookup()

        # Ejecutar Google Dorks
        dorks_results = busqueda_start(self.domain)

        # Actualizar reporte
        self.report.update(
            {
                "dns": domain_analyzer.report["dns"],
                "whois": domain_analyzer.report["whois"],
                "dorks": dorks_results,
                "security_analysis": domain_analyzer.report["security_analysis"],
            }
        )

        # Preparar prompt para DeepSeek
        analysis_prompt = self._prepare_ai_prompt()
        self.report["ai_analysis"] = consultar_deepseek(analysis_prompt)

        return self.report

    def _prepare_ai_prompt(self):
        prompt = f"""Analiza el siguiente reporte de seguridad del dominio {self.domain} y proporciona un resumen ejecutivo con recomendaciones:

1. Información WHOIS:
{json.dumps(self.report['whois'], indent=2)}

2. Registros DNS:
{json.dumps(self.report['dns'], indent=2)}

3. Resultados de Google Dorks:
{json.dumps(self.report['dorks'], indent=2)}

4. Análisis de Seguridad:
{json.dumps(self.report['security_analysis'], indent=2)}

Proporciona:
- Resumen ejecutivo
- Puntos fuertes de seguridad
- Vulnerabilidades potenciales
- Recomendaciones de mejora
- Calificación de seguridad (1-10)
"""
        return prompt

    def generate_report_file(self):
        filename = f"{self.domain}_full_report.json"
        with open(filename, "w") as f:
            json.dump(self.report, f, indent=4)
        return filename
