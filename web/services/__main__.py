import sys
from datetime import datetime


def main():
    print("=== Probador de FullDomainAnalyzer ===")

    # Verificar si se proporcionó un dominio como argumento
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Ingrese el dominio a analizar (ej: ejemplo.com): ").strip()

    if not domain:
        print("Error: Debe especificar un dominio")
        return

    print(f"\nIniciando análisis completo de: {domain}")
    print(f"Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        # 1. Crear el analizador
        print("\n[1/4] Configurando analizador...")
        analyzer = FullDomainAnalyzer(domain)

        # 2. Ejecutar análisis completo
        print("[2/4] Ejecutando análisis DNS/WHOIS...")
        print("[3/4] Realizando búsquedas con Google Dorks...")
        report = analyzer.run_full_analysis()

        # 3. Mostrar resultados clave
        print("\n[4/4] Resultados del análisis:")
        print("=" * 50)

        # Resumen de DeepSeek
        print("\n=== RESUMEN EJECUTIVO ===")
        print(report["ai_analysis"])

        # Información WHOIS
        print("\n=== INFORMACIÓN WHOIS ===")
        print(f"Registrador: {report['whois'].get('registrar', 'No disponible')}")
        print(
            f"Fecha creación: {report['whois'].get('creation_date', 'No disponible')}"
        )
        print(
            f"Fecha expiración: {report['whois'].get('expiration_date', 'No disponible')}"
        )

        # Análisis de seguridad
        print("\n=== ANÁLISIS DE SEGURIDAD ===")
        sec = report["security_analysis"]
        print(f"SPF: {'Sí' if sec['dns']['has_spf'] else 'No'}")
        print(f"DMARC: {'Sí' if sec['dns']['has_dmarc'] else 'No'}")
        print(f"Edad del dominio: {sec['whois'].get('domain_age_days', 'N/A')} días")

        # Google Dorks
        print("\n=== GOOGLE DORKS (primeros 3 resultados) ===")
        for i, dork in enumerate(report["dorks"][:3], 1):
            print(f"\nResultado {i}:")
            print(f"Título: {dork.get('titulo')}")
            print(f"Enlace: {dork.get('enlace')}")

        # 4. Generar archivo de reporte
        print("\nGenerando archivo de reporte...")
        filename = analyzer.generate_report_file()
        print(f"\nReporte completo guardado como: {filename}")

    except Exception as e:
        print(f"\nError durante el análisis: {str(e)}")
    finally:
        print("\nAnálisis completado")
        print(f"Hora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    from fullDomainAnalyzer import FullDomainAnalyzer

    main()
