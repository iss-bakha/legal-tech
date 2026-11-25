from app.services.pii import mask_pii, unmask


def test_masks_iin_phone_email():
    text = "Мой ИИН 990101300123, тел. +7 (777) 123-45-67, почта ivan@mail.kz"
    result = mask_pii(text)
    assert "990101300123" not in result.text
    assert "777" not in result.text
    assert "ivan@mail.kz" not in result.text
    assert "[ИИН_1]" in result.text
    assert "[ТЕЛЕФОН_1]" in result.text
    assert "[EMAIL_1]" in result.text


def test_same_value_gets_same_tag_and_unmasks():
    text = "ИИН 990101300123 указан дважды: 990101300123"
    result = mask_pii(text)
    assert result.text.count("[ИИН_1]") == 2
    assert unmask(result.text, result.mapping) == text


def test_plain_numbers_untouched():
    result = mask_pii("Статья 113 ТК РК, зарплата 250000 тенге за 3 месяца")
    assert result.text == "Статья 113 ТК РК, зарплата 250000 тенге за 3 месяца"
