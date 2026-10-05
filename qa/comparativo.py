"""Comparação ANTES (sem bug) x DEPOIS (com bug)."""
import html
from datetime import datetime

LINHAS = [
    ("Total de testes", "total"),
    ("Aprovados (PASS)", "aprovados"),
    ("Falhas (FAIL)", "falhas"),
    ("Taxa de aprovação (%)", "taxa_aprovacao"),
    ("Falhas críticas", "falhas_criticas"),
]


def _testes_que_mudaram(antes, depois):
    status_antes = {r["ID"]: r["Status"] for r in antes["resultados"]}
    mudou = []
    for r in depois["resultados"]:
        if status_antes.get(r["ID"]) == "PASS" and r["Status"] == "FAIL":
            mudou.append(r)
    return mudou


def imprimir(antes, depois):
    print("\n" + "=" * 62)
    print("COMPARATIVO: ANTES x DEPOIS DO BUG")
    print("=" * 62)
    print(f"{'Indicador':<26}{'Sem bug':>16}{'Com bug':>16}")
    for nome, chave in LINHAS:
        print(f"{nome:<26}{antes['metricas'][chave]:>16}{depois['metricas'][chave]:>16}")
    print(f"{'Decisão de QA':<26}{antes['decisao']:>16}{depois['decisao']:>16}")
    for r in _testes_que_mudaram(antes, depois):
        print(f"  -> {r['ID']} passou a FALHAR: {r['Teste']} (obtido: {r['Obtido']})")


def gerar_html(pasta, antes, depois):
    e = html.escape
    linhas = "".join(
        f"<tr><td>{n}</td><td>{antes['metricas'][c]}</td><td>{depois['metricas'][c]}</td></tr>"
        for n, c in LINHAS)
    linhas += f"<tr><td><b>Decisão de QA</b></td><td><b>{antes['decisao']}</b></td><td><b>{depois['decisao']}</b></td></tr>"
    mudaram = "".join(
        f"<li><b>{r['ID']}</b> - {e(r['Teste'])} (esperado {e(str(r['Esperado']))}, obtido {e(str(r['Obtido']))}, "
        f"severidade {r['Severidade']})</li>" for r in _testes_que_mudaram(antes, depois))
    pagina = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Comparativo antes x depois</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;max-width:800px;margin:30px auto;padding:0 16px}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:8px}}th{{background:#263238;color:#fff}}</style></head><body>
<h1>Comparativo: antes x depois do bug proposital</h1>
<p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
<table><tr><th>Indicador</th><th>Sem bug</th><th>Com bug</th></tr>{linhas}</table>
<h2>Testes que passaram a falhar</h2><ul>{mudaram or '<li>Nenhum</li>'}</ul>
</body></html>"""
    with open(pasta / "comparativo_antes_depois.html", "w", encoding="utf-8") as f:
        f.write(pagina)
