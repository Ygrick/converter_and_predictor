from prediction import Predict
from converter import Converter


class TestProgram:
    def setup(self):
        self.test_predict_obj = Predict()
        self.test_converter_obj = Converter()

    def test_predict_cur_list(self):
        assert type(self.test_predict_obj.currencies()) == list

    def test_predict_rcode_str(self):
        assert self.test_predict_obj.get_rcode('Australian Dollar') == 'R01010'

    def test_predict_prediction_str(self):
        assert self.test_predict_obj.get_prediction('Australian Dollar') == 52.0

    def test_converter_list(self):
        assert type(self.test_converter_obj.list_currencies()) == list

    def test_converter_cur(self):
        assert self.test_converter_obj.convert_cur(1, 'USD', 'RUB') == 74.0


obj = TestProgram()
