import pytest

from src.lawngrass import LawnGrass


def test_smartphone_product_init(lawngrass_1):
    assert lawngrass_1.name == "Газонная трава 1"
    assert lawngrass_1.description == "Элитная трава для газона"
    assert lawngrass_1.price == 500.0
    assert lawngrass_1.quantity == 20
    assert lawngrass_1.country == "Россия"
    assert lawngrass_1.germination_period == "7 дней"
    assert lawngrass_1.color == "Зеленый"


def test_smartphone_product_add(lawngrass_1, lawngrass_2):
    assert lawngrass_1 + lawngrass_2 == 16750.0


def test_smartphone_product_add_error(lawngrass_1):
    with pytest.raises(TypeError):
        lawngrass_1 + 1  # noqa


def test_lawn_grass_mixin_log(capsys):
    """Проверяем, что миксин автоматически определяет имя класса-наследника LawnGrass."""
    LawnGrass(
        "Газон",
        "Зеленый",
        1000.0,
        10,
        "Россия",
        "14 дней",
        "Зеленый",
    )

    captured = capsys.readouterr()
    assert captured.out.strip() == "LawnGrass(Газон, Зеленый, 1000.0, 10)"
