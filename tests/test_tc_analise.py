"""Testes do radar/tc_analise.py: análise crítica do TC aplicável ao órgão."""

from radar.entidade import TipoEntidade
from radar.tc_analise import AnaliseTC, analise_critica

DADOS = {
    "orgao": "Município de Antônio João/MS",
    "obra": "Centro de Saúde",
    "valor": "R$ 500.000,00",
}


def test_analise_estadual_nivel_tribunal_de_contas_do_estado():
    a = analise_critica(TipoEntidade.ESTADUAL, DADOS)
    assert isinstance(a, AnaliseTC)
    assert a.tribunal_de_contas == "Tribunal de Contas do Estado"


def test_analise_federal_nivel_tribunal_da_uniao():
    a = analise_critica(TipoEntidade.FEDERAL, DADOS)
    assert a.tribunal_de_contas == "Tribunal de Contas da União"


def test_analise_municipal_nivel_tribunal_municipal():
    a = analise_critica(TipoEntidade.MUNICIPAL, DADOS)
    assert a.tribunal_de_contas == "Tribunal de Contas Municipal"


def test_pontos_base_aparecem_para_todos_os_niveis():
    for entidade in TipoEntidade:
        a = analise_critica(entidade, DADOS)
        texto = "\n".join(p.descricao for p in a.pontos)
        assert len(a.pontos) >= 3
        assert (
            "prazo de pagamento" in texto.lower()
            or "justificativa técnica" in texto.lower()
        )


def test_pontos_todos_com_fundamento_e_ids_unicos():
    a = analise_critica(TipoEntidade.ESTADUAL, DADOS)
    ids = [p.id for p in a.pontos]
    assert len(ids) == len(set(ids))
    assert all(p.descricao and p.fundamento for p in a.pontos)


def test_analise_critica_aceita_none():
    a = analise_critica(TipoEntidade.MUNICIPAL, None)
    assert a.tribunal_de_contas == "Tribunal de Contas Municipal"
