from combattbmodel.core import Gene


def test_gene():
    gene = Gene()
    assert gene.so_id == 'SO:0000704'
