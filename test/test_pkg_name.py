import combat_tb_model


def test_package_name():
    name = combat_tb_model.name
    assert name == 'combat_tb_model'
