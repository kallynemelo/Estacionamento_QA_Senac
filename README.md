# Projeto de QA - Sistema de Estacionamento

Automação de testes em Python (somente biblioteca padrão, sem instalar nada).

Fluxo: **Requisito -> Teste -> Execução -> Resultado -> Dados -> Defeitos -> Decisão de QA -> Relatório**

## Como executar (VS Code)
1. Abra a pasta `projeto_qa_estacionamento` no VS Code (File > Open Folder).
2. Abra o terminal (Ctrl + ') e rode:

```
python main.py          # versão original
python main.py --bug    # com o bug proposital
```
(no Windows, se `python` não funcionar, use `py main.py`)

## Estrutura
```
main.py                    # orquestra tudo
sistema/estacionamento.py  # regras de negócio (e o BUG_PROPOSITAL)
qa/casos_de_teste.py       # 14 casos de teste + descrição dos requisitos
qa/executor.py             # executa os testes e registra PASS/FAIL
qa/metricas.py             # métricas e decisão de QA
qa/relatorio.py            # CSVs e relatório HTML
qa/comparativo.py          # comparação antes x depois do bug
saida/                     # arquivos gerados automaticamente
```

## Requisitos (regras de negócio)
- RF01 - Tarifa: 15 min grátis, R$ 5,00 por hora iniciada, teto de R$ 30,00
- RF02 - Entrada: placa válida, sem duplicidade, respeitando a lotação
- RF03 - Desconto: comum 0%, conveniado 20%, mensalista 100%
- RF04 - Saída: cobra a tarifa com desconto e libera a vaga

## Decisão de QA
- Qualquer falha **Crítica** -> NÃO LIBERAR
- Falhas sem criticidade -> LIBERADO COM RESSALVAS
- Nenhuma falha -> LIBERADO

## Bug proposital
Em `sistema/estacionamento.py`, a constante `BUG_PROPOSITAL = True` (ou `--bug`) faz
`calcular_tarifa` ignorar o teto diário. Os testes CT03 e CT05 passam a falhar.

| Indicador | Sem bug | Com bug |
|---|---|---|
| Aprovados | 14 | 12 |
| Taxa de aprovação | 100% | 85,7% |
| Falhas críticas | 0 | 1 |
| Decisão | LIBERADO | NÃO LIBERAR |

## Arquivos gerados em `saida/`
- `normal/` e `com_bug/`: `resultados_qa.csv`, `defeitos_qa.csv`, `relatorio_final_qa.html`, `resumo.json`
- `comparativo_antes_depois.html`
