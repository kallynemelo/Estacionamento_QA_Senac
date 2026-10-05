"""Executa os casos de teste e registra os resultados automaticamente."""
from datetime import datetime

VERDE, VERMELHO, RESET = "\033[92m", "\033[91m", "\033[0m"


def executar_casos(casos):
    resultados = []
    for caso in casos:
        try:
            obtido = caso["executar"]()
        except Exception as erro:  # a exceção lançada vira o "resultado obtido"
            obtido = type(erro).__name__

        status = "PASS" if obtido == caso["Esperado"] else "FAIL"
        resultados.append({
            "ID": caso["ID"],
            "Requisito": caso["Requisito"],
            "Teste": caso["Teste"],
            "Esperado": caso["Esperado"],
            "Obtido": obtido,
            "Status": status,
            "Severidade": caso["Severidade"],
            "DataHora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

        cor = VERDE if status == "PASS" else VERMELHO
        print(f"{cor}[{status}]{RESET} {caso['ID']} ({caso['Requisito']}) - {caso['Teste']}")
        if status == "FAIL":
            print(f"        esperado: {caso['Esperado']!r} | obtido: {obtido!r} | severidade: {caso['Severidade']}")
    return resultados
