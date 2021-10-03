from currency_converter import CurrencyConverter


class Converter:
    def __init__(self):
        self.obj = CurrencyConverter()

    def convert_cur(self, volume, from_cur, to_cur):
        """
        Конвертатор
        conv(10, 'USD', 'RUB')
        """
        return round(self.obj.convert(volume, from_cur, to_cur),3)

    def list_currencies(self):
        """
        Вывод всех валют
        """
        return list(self.obj.currencies)
