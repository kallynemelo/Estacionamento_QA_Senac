"""
Casos de teste do sistema de estacionamento.

Cada caso possui: ID, requisito, descrição, resultado esperado, severidade
e uma função `executar` que devolve o resultado OBTIDO.
Quando o sistema lança uma exceção, o resultado obtido é o NOME da exceção.
"""
from sistema.estacionamento import Estacionamento, calcular_tarifa, aplicar_desconto

REQUISITOS = {
    "RF01": "Cálculo da tarifa: 15 min de tolerância, R$ 5,00 por hora iniciada e teto de R$ 30,00 por dia.",
    "RF02": "Entrada de veículos: placa válida, sem duplicidade e respeitando a capacidade do pátio.",
    "RF03": "Desconto por tipo de cliente: comum 0%, conveniado 20%, mensalista 100%.",
    "RF04": "Saída de veículos: cobra a tarifa com desconto e libera a vaga.",
}


# ---------------- RF01 ----------------
def ct01():
    return calcular_tarifa(90)  # 2 horas iniciadas

def ct02():
    return calcular_tarifa(10)  # dentro da tolerância

def ct03():
    return calcular_tarifa(600)  # 10h = R$ 50 -> teto R$ 30

def ct04():
    return calcular_tarifa(-5)

def ct05():
    return calcular_tarifa(1440)  # 24h = R$ 120 -> teto R$ 30


# ---------------- RF02 ----------------
def ct06():
    return Estacionamento(2).registrar_entrada("ABC1D23")

def ct07():
    e = Estacionamento(2)
    e.registrar_entrada("ABC1D23")
    return e.registrar_entrada("ABC1D23")

def ct08():
    e = Estacionamento(1)
    e.registrar_entrada("ABC1D23")
    return e.registrar_entrada("XYZ9K88")

def ct09():
    return Estacionamento(2).registrar_entrada("12-ABC")


# ---------------- RF03 ----------------
def ct10():
    return aplicar_desconto(10.0, "conveniado")

def ct11():
    return aplicar_desconto(10.0, "vip")


# ---------------- RF04 ----------------
def ct12():
    e = Estacionamento(2)
    e.registrar_entrada("ABC1D23")
    return e.registrar_saida("ABC1D23", 120)

def ct13():
    return Estacionamento(2).registrar_saida("ABC1D23", 60)

def ct14():
    e = Estacionamento(1)
    e.registrar_entrada("ABC1D23")
    e.registrar_saida("ABC1D23", 60)
    return e.vagas_livres


def _caso(id_, req, descricao, esperado, severidade, executar):
    return {"ID": id_, "Requisito": req, "Teste": descricao,
            "Esperado": esperado, "Severidade": severidade, "executar": executar}


CASOS = [
    _caso("CT01", "RF01", "Calcular tarifa de 90 min (2 horas iniciadas)", 10.0, "Média", ct01),
    _caso("CT02", "RF01", "Não cobrar dentro da tolerância de 15 min", 0.0, "Média", ct02),
    _caso("CT03", "RF01", "Aplicar teto diário em 10 horas de permanência", 30.0, "Crítica", ct03),
    _caso("CT04", "RF01", "Rejeitar tempo de permanência negativo", "ValueError", "Alta", ct04),
    _caso("CT05", "RF01", "Aplicar teto diário em 24 horas de permanência", 30.0, "Alta", ct05),
    _caso("CT06", "RF02", "Registrar entrada de veículo com placa válida", True, "Alta", ct06),
    _caso("CT07", "RF02", "Impedir entrada duplicada do mesmo veículo", "VeiculoJaEstacionadoError", "Crítica", ct07),
    _caso("CT08", "RF02", "Impedir entrada com o pátio lotado", "EstacionamentoLotadoError", "Crítica", ct08),
    _caso("CT09", "RF02", "Rejeitar placa com formato inválido", "PlacaInvalidaError", "Média", ct09),
    _caso("CT10", "RF03", "Aplicar 20% de desconto a cliente conveniado", 8.0, "Média", ct10),
    _caso("CT11", "RF03", "Rejeitar tipo de cliente inexistente", "TipoClienteInvalidoError", "Média", ct11),
    _caso("CT12", "RF04", "Cobrar corretamente na saída (120 min)", 10.0, "Alta", ct12),
    _caso("CT13", "RF04", "Rejeitar saída de veículo que não está no pátio", "VeiculoNaoEncontradoError", "Alta", ct13),
    _caso("CT14", "RF04", "Liberar a vaga após a saída do veículo", 1, "Média", ct14),
]
