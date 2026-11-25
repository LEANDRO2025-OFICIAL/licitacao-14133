"""Testes do radar/documentos.py: geradores dos documentos do processo licitatório."""

from radar.documentos import (
    gerar_analise_recurso_contraposicoes,
    gerar_dfd,
    gerar_edital,
    gerar_etp,
    gerar_minuta_ata,
    gerar_minuta_contrato,
    gerar_resposta_impugnacao,
    gerar_sugestao_parecer,
    gerar_tr,
)
from radar.entidade import TipoEntidade
from radar.tc_analise import analise_critica

DADOS = {
    "orgao": "Município de Antônio João/MS",
    "objeto": "Suprimentos",
    "modalidade": "Pregão",
    "valor": "R$ 1.000.000,00",
    "prazo": "90 dias",
    "numero_processo": "000/2026",
    "data_edital": "10/12/2026",
}


def test_gerar_dfd_tem_diagrama():
    txt = gerar_dfd(DADOS)
    assert "Diagrama de Fluxo de Dados" in txt


def test_gerar_etp_tem_estudo():
    assert "Estudo Técnico Preliminar" in gerar_etp(DADOS)


def test_gerar_tr_tem_termo():
    assert "Termo de Referência" in gerar_tr(DADOS)


def test_gerar_edital_tem_edital():
    txt = gerar_edital(DADOS)
    assert "Edital" in txt


def test_gerar_minuta_contrato_tem_minuta():
    assert "Minuta de Contrato" in gerar_minuta_contrato(DADOS)


def test_gerar_minuta_ata_tem_minuta():
    assert "Minuta de Ata" in gerar_minuta_ata(DADOS)


def test_gerar_sugestao_parecer_tem_sugestao():
    assert "Sugestão de Parecer" in gerar_sugestao_parecer(DADOS)


def test_gerar_resposta_impugnacao_tem_resposta():
    assert "Resposta de Impugnação" in gerar_resposta_impugnacao(DADOS)


def test_gerar_analise_recurso_tem_analise():
    analise = analise_critica(TipoEntidade.MUNICIPAL, DADOS)
    txt = gerar_analise_recurso_contraposicoes(DADOS, analise)
    assert "Análise e Decisão de Recurso e Contraposições" in txt


def test_gerar_inclui_orgao_objeto_modalidade():
    txt = gerar_edital(DADOS)
    assert "Antônio João" in txt
    assert "Pregão" in txt
