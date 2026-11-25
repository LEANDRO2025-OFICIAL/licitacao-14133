"""Testes do radar/entidade.py: classificação de órgão -> nível do Tribunal de Contas."""

from radar.entidade import TipoEntidade, classificar_entidade, nivel_tribunal_de_contas


def test_classifica_municipio_antionio_joao():
    assert (
        classificar_entidade("Município de Antônio João/MS") is TipoEntidade.MUNICIPAL
    )


def test_classifica_prefeitura():
    assert (
        classificar_entidade("Prefeitura do Município de Adamantina (SP)")
        is TipoEntidade.MUNICIPAL
    )


def test_classifica_estado():
    assert (
        classificar_entidade("Governo do Estado de Mato Grosso do Sul")
        is TipoEntidade.ESTADUAL
    )


def test_classifica_tribunal_de_contas_do_estado():
    assert classificar_entidade("Tribunal de Contas do Estado") is TipoEntidade.ESTADUAL


def test_classifica_federal():
    assert (
        classificar_entidade("Secretaria Nacional do Tesouro") is TipoEntidade.FEDERAL
    )


def test_classifica_valor_explicito():
    assert classificar_entidade(None, "federal") is TipoEntidade.FEDERAL
    assert classificar_entidade(None, "estadual") is TipoEntidade.ESTADUAL
    assert classificar_entidade(None, "municipal") is TipoEntidade.MUNICIPAL


def test_default_municipal():
    assert classificar_entidade(None) is TipoEntidade.MUNICIPAL


def test_nivel_tribunal_municipal():
    assert (
        nivel_tribunal_de_contas(TipoEntidade.MUNICIPAL)
        == "Tribunal de Contas Municipal"
    )


def test_nivel_tribunal_estadual():
    assert (
        nivel_tribunal_de_contas(TipoEntidade.ESTADUAL)
        == "Tribunal de Contas do Estado"
    )


def test_nivel_tribunal_federal():
    assert (
        nivel_tribunal_de_contas(TipoEntidade.FEDERAL) == "Tribunal de Contas da União"
    )
