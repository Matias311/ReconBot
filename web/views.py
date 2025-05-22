import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import View

from .models import DomainAnalysis
from .services.fullDomainAnalyzer import FullDomainAnalyzer


class FullAnalysisView(View):
    template_name = "full_analysis.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        domain = request.POST.get("domain", "").strip()
        if not domain:
            return render(
                request,
                self.template_name,
                {"error": "Debe ingresar un dominio válido"},
            )

        # Verificar si ya existe un análisis reciente (opcional)
        recent_analysis = DomainAnalysis.objects.filter(
            domain=domain, created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).first()

        if recent_analysis:
            report = recent_analysis.report
            latest_analysis = recent_analysis
        else:
            # Ejecutar nuevo análisis
            analyzer = FullDomainAnalyzer(domain)
            report = analyzer.run_full_analysis()

            # Guardar en base de datos
            latest_analysis = DomainAnalysis.objects.create(
                domain=domain, report=report
            )

        context = {
            "domain": domain,
            "report": report,
            "latest_analysis": latest_analysis,
            "dns_records": report["dns"],
            "whois_info": report["whois"],
            "dorks_results": report["dorks"],
            "security_analysis": report["security_analysis"],
            "ai_analysis": report["ai_analysis"],
            "report_generated": True,
        }
        return render(request, self.template_name, context)


def download_report(request, pk):
    analysis = get_object_or_404(DomainAnalysis, pk=pk)

    # Opcional: verificar sesión si quieres algo de seguridad
    if (
        request.session.session_key
        and analysis.session_key != request.session.session_key
    ):
        return HttpResponse("No tienes permiso para descargar este reporte", status=403)

    # Crear respuesta con el JSON
    response = HttpResponse(
        json.dumps(analysis.report, indent=4, ensure_ascii=False),
        content_type="application/json",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="{analysis.domain}_report.json"'
    )
    return response
