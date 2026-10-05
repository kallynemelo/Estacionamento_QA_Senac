"""
Sistema de Estacionamento - regras de negócio que serão testadas.

Requisitos:
  RF01 - Cálculo da tarifa (tolerância, valor por hora, teto diário)
  RF02 - Registro de entrada (placa válida, sem duplicidade, controle de lotação)
  RF03 - Desconto por tipo de cliente
  RF04 - Registro de saída com cobrança e liberação da vaga
"""
import math
import re

# ---------------------------------------------------------------------------
# BUG PROPOSITAL
# Mude para True (ou execute `python main.py --bug`) para introduzir o defeito:
# a função calcular_tarifa deixa de aplicar o teto da diária (R$ 30,00).
# ---------------------------------------------------------------------------
BUG_PROPOSITAL = False

TOLERANCIA_MIN = 15
VALOR_HORA = 5.00
DIARIA_MAXIMA = 30.00
DESCONTOS = {"comum": 0.0, "conveniado": 0.20, "mensalista": 1.0}
PADRAO_PLACA = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")  # antiga e Mercosul


class PlacaInvalidaError(ValueError):
    pass


class VeiculoJaEstacionadoError(Exception):
    pass


class EstacionamentoLotadoError(Exception):
    pass


class VeiculoNaoEncontradoError(Exception):
    pass


class TipoClienteInvalidoError(ValueError):
    pass


def calcular_tarifa(minutos):
    """RF01: até 15 min é grátis; depois cobra R$ 5,00 por hora iniciada, limitado a R$ 30,00."""
    if minutos < 0:
        raise ValueError("Tempo de permanência não pode ser negativo")
    if minutos <= TOLERANCIA_MIN:
        return 0.0
    valor = math.ceil(minutos / 60) * VALOR_HORA
    if BUG_PROPOSITAL:
        return valor  # DEFEITO: esqueceu de aplicar o teto da diária
    return min(valor, DIARIA_MAXIMA)


def aplicar_desconto(valor, tipo_cliente):
    """RF03: comum 0%, conveniado 20%, mensalista 100%."""
    if tipo_cliente not in DESCONTOS:
        raise TipoClienteInvalidoError(f"Tipo de cliente inválido: {tipo_cliente}")
    return round(valor * (1 - DESCONTOS[tipo_cliente]), 2)


class Estacionamento:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.veiculos = set()

    @property
    def vagas_livres(self):
        return self.capacidade - len(self.veiculos)

    def registrar_entrada(self, placa):
        """RF02: placa válida, veículo ainda não estacionado e pátio com vaga."""
        placa = placa.strip().upper()
        if not PADRAO_PLACA.match(placa):
            raise PlacaInvalidaError(f"Placa inválida: {placa}")
        if placa in self.veiculos:
            raise VeiculoJaEstacionadoError(f"Veículo já está no pátio: {placa}")
        if len(self.veiculos) >= self.capacidade:
            raise EstacionamentoLotadoError("Não há vagas disponíveis")
        self.veiculos.add(placa)
        return True

    def registrar_saida(self, placa, minutos, tipo_cliente="comum"):
        """RF04: cobra a tarifa (com desconto) e libera a vaga."""
        placa = placa.strip().upper()
        if placa not in self.veiculos:
            raise VeiculoNaoEncontradoError(f"Veículo não encontrado: {placa}")
        valor = aplicar_desconto(calcular_tarifa(minutos), tipo_cliente)
        self.veiculos.remove(placa)
        return valor
