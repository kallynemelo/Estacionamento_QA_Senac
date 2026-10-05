"""Cálculo das métricas de qualidade e da decisão final de QA."""


def calcular_metricas(resultados):
    total = len(resultados)
    aprovados = sum(1 for r in resultados if r["Status"] == "PASS")
    falhas = total - aprovados
    criticas = sum(1 for r in resultados if r["Status"] == "FAIL" and r["Severidade"] == "Crítica")
    taxa = (aprovados / total * 100) if total else 0.0

    por_requisito = {}
    for r in resultados:
        item = por_requisito.setdefault(r["Requisito"], {"total": 0, "pass": 0, "fail": 0})
        item["total"] += 1
        item["pass" if r["Status"] == "PASS" else "fail"] += 1

    return {
        "total": total,
        "aprovados": aprovados,
        "falhas": falhas,
        "taxa_aprovacao": round(taxa, 1),
        "taxa_falha": round(100 - taxa, 1) if total else 0.0,
        "falhas_criticas": criticas,
        "por_requisito": por_requisito,
    }


def decidir(metricas):
    """
    Política de liberação:
      - qualquer falha CRÍTICA        -> NÃO LIBERAR
      - falhas, mas nenhuma crítica   -> LIBERADO COM RESSALVAS
      - nenhuma falha                 -> LIBERADO
    """
    if metricas["falhas_criticas"] > 0:
        return "NÃO LIBERAR"
    if metricas["falhas"] > 0:
        return "LIBERADO COM RESSALVAS"
    return "LIBERADO"
