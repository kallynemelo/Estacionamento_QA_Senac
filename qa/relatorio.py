"""Geração dos arquivos de saída: CSV de resultados, CSV de defeitos e relatório HTML."""
import csv
import html
from datetime import datetime

CAMPOS = ["ID", "Requisito", "Teste", "Esperado", "Obtido", "Status", "Severidade", "DataHora"]

CSS = """
body{font-family:Segoe UI,Arial,sans-serif;max-width:1000px;margin:30px auto;padding:0 16px;color:#222}
h1{margin-bottom:0} .sub{color:#666;margin-top:4px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}
.kpi{flex:1;min-width:130px;background:#f4f6f8;border-radius:8px;padding:12px;text-align:center}
.kpi b{display:block;font-size:26px}
.decisao{padding:18px;border-radius:8px;text-align:center;font-size:26px;font-weight:bold;color:#fff}
.LIBERADO{background:#2e7d32}.COMRESSALVAS{background:#ef8f00}.NAOLIBERAR{background:#c62828}
table{border-collapse:collapse;width:100%;margin:12px 0}
th,td{border:1px solid #ddd;padding:7px 9px;text-align:left;font-size:14px}
th{background:#263238;color:#fff}
tr.PASS td.st{background:#c8e6c9;font-weight:bold}tr.FAIL td.st{background:#ffcdd2;font-weight:bold}
tr.FAIL{background:#fff5f5}
.crit{color:#c62828;font-weight:bold}
"""


def _classe_decisao(decisao):
    return decisao.replace(" ", "").replace("Ã", "A")


def salvar_csvs(pasta, resultados):
    with open(pasta / "resultados_qa.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(resultados)

    defeitos = [r for r in resultados if r["Status"] == "FAIL"]
    with open(pasta / "defeitos_qa.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(defeitos)
    return defeitos


def gerar_html(pasta, resultados, metricas, decisao, requisitos, modo):
    e = html.escape
    versao = "COM BUG PROPOSITAL" if modo == "com_bug" else "versão original (sem bug)"

    linhas_req = ""
    for req, descricao in requisitos.items():
        m = metricas["por_requisito"].get(req, {"total": 0, "pass": 0, "fail": 0})
        situacao = "OK" if m["fail"] == 0 else f"{m['fail']} falha(s)"
        linhas_req += (f"<tr><td>{req}</td><td>{e(descricao)}</td><td>{m['total']}</td>"
                       f"<td>{m['pass']}</td><td>{m['fail']}</td><td>{situacao}</td></tr>")

    linhas_res = ""
    for r in resultados:
        linhas_res += (f"<tr class='{r['Status']}'><td>{r['ID']}</td><td>{r['Requisito']}</td>"
                       f"<td>{e(r['Teste'])}</td><td>{e(str(r['Esperado']))}</td>"
                       f"<td>{e(str(r['Obtido']))}</td><td class='st'>{r['Status']}</td>"
                       f"<td>{r['Severidade']}</td></tr>")

    defeitos = [r for r in resultados if r["Status"] == "FAIL"]
    if defeitos:
        linhas_def = ""
        for r in defeitos:
            classe = " class='crit'" if r["Severidade"] == "Crítica" else ""
            linhas_def += (f"<tr><td>{r['ID']}</td><td>{r['Requisito']}</td><td>{e(r['Teste'])}</td>"
                           f"<td>Esperado <b>{e(str(r['Esperado']))}</b>, mas o sistema retornou "
                           f"<b>{e(str(r['Obtido']))}</b></td><td{classe}>{r['Severidade']}</td></tr>")
        tabela_def = ("<table><tr><th>ID</th><th>Requisito</th><th>Teste</th><th>Descrição do defeito</th>"
                      f"<th>Severidade</th></tr>{linhas_def}</table>")
    else:
        tabela_def = "<p>Nenhum defeito encontrado nesta execução.</p>"

    if decisao == "NÃO LIBERAR":
        conclusao = "Há pelo menos uma falha crítica. A versão não deve ser liberada até a correção."
    elif decisao == "LIBERADO COM RESSALVAS":
        conclusao = "Existem falhas, mas nenhuma crítica. A versão pode ser liberada com as ressalvas listadas."
    else:
        conclusao = "Todos os testes passaram. A versão está apta para liberação."

    pagina = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Relatório de QA - Estacionamento</title><style>{CSS}</style></head><body>
<h1>Relatório Final de QA - Sistema de Estacionamento</h1>
<p class="sub">Execução em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {versao}</p>

<div class="decisao {_classe_decisao(decisao)}">DECISÃO DE QA: {decisao}</div>

<div class="kpis">
<div class="kpi"><b>{metricas['total']}</b>Testes</div>
<div class="kpi"><b>{metricas['aprovados']}</b>Aprovados</div>
<div class="kpi"><b>{metricas['falhas']}</b>Falhas</div>
<div class="kpi"><b>{metricas['taxa_aprovacao']}%</b>Taxa de aprovação</div>
<div class="kpi"><b>{metricas['falhas_criticas']}</b>Falhas críticas</div>
</div>

<h2>Funcionalidades testadas</h2>
<table><tr><th>Req.</th><th>Regra de negócio</th><th>Testes</th><th>PASS</th><th>FAIL</th><th>Situação</th></tr>
{linhas_req}</table>

<h2>Resultados dos testes</h2>
<table><tr><th>ID</th><th>Req.</th><th>Teste</th><th>Esperado</th><th>Obtido</th><th>Status</th><th>Severidade</th></tr>
{linhas_res}</table>

<h2>Defeitos encontrados</h2>
{tabela_def}

<h2>Conclusão</h2>
<p>{conclusao}</p>
<p><small>Política: falha crítica = NÃO LIBERAR; falhas não críticas = LIBERADO COM RESSALVAS; sem falhas = LIBERADO.</small></p>
</body></html>"""
    with open(pasta / "relatorio_final_qa.html", "w", encoding="utf-8") as f:
        f.write(pagina)
