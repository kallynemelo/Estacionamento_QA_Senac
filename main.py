"""
Projeto de QA - Sistema de Estacionamento

Uso:
    python main.py          # executa os testes na versão original
    python main.py --bug    # executa os testes com o BUG PROPOSITAL ativado
"""
import argparse
import json
import sys
from pathlib import Path

from sistema import estacionamento
from qa.casos_de_teste import CASOS, REQUISITOS
from qa.executor import executar_casos
from qa.metricas import calcular_metricas, decidir
from qa import relatorio, comparativo

PASTA_SAIDA = Path(__file__).parent / "saida"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Automação de QA - Estacionamento")
    parser.add_argument("--bug", action="store_true", help="ativa o bug proposital no sistema")
    args = parser.parse_args()

    modo = "com_bug" if args.bug else "normal"
    if args.bug:
        estacionamento.BUG_PROPOSITAL = True

    print("=" * 62)
    print(f"QA - ESTACIONAMENTO | modo: {'COM BUG PROPOSITAL' if args.bug else 'versão original'}")
    print("=" * 62)

    # Requisito -> Teste -> Execução -> Resultado
    resultados = executar_casos(CASOS)

    # Dados -> Métricas -> Decisão
    metricas = calcular_metricas(resultados)
    decisao = decidir(metricas)

    # Relatório
    pasta = PASTA_SAIDA / modo
    pasta.mkdir(parents=True, exist_ok=True)
    defeitos = relatorio.salvar_csvs(pasta, resultados)
    relatorio.gerar_html(pasta, resultados, metricas, decisao, REQUISITOS, modo)
    with open(pasta / "resumo.json", "w", encoding="utf-8") as f:
        json.dump({"metricas": metricas, "decisao": decisao, "resultados": resultados},
                  f, ensure_ascii=False, indent=2)

    print("\n" + "-" * 62)
    print("INDICADORES DE QUALIDADE")
    print("-" * 62)
    print(f"Total de testes executados : {metricas['total']}")
    print(f"Aprovados (PASS)           : {metricas['aprovados']}")
    print(f"Falhas (FAIL)              : {metricas['falhas']}")
    print(f"Taxa de aprovação          : {metricas['taxa_aprovacao']}%")
    print(f"Falhas críticas            : {metricas['falhas_criticas']}")
    print(f"\nDECISÃO DE QA: {decisao}")
    if defeitos:
        print("\nDEFEITOS ENCONTRADOS:")
        for d in defeitos:
            print(f"  {d['ID']} [{d['Severidade']}] {d['Teste']}")
    print(f"\nRelatório gerado em: {pasta / 'relatorio_final_qa.html'}")

    # Comparativo, se as duas execuções existirem
    arq_a, arq_b = PASTA_SAIDA / "normal" / "resumo.json", PASTA_SAIDA / "com_bug" / "resumo.json"
    if arq_a.exists() and arq_b.exists():
        antes = json.loads(arq_a.read_text(encoding="utf-8"))
        depois = json.loads(arq_b.read_text(encoding="utf-8"))
        comparativo.imprimir(antes, depois)
        comparativo.gerar_html(PASTA_SAIDA, antes, depois)
        print(f"\nComparativo gerado em: {PASTA_SAIDA / 'comparativo_antes_depois.html'}")


if __name__ == "__main__":
    main()
