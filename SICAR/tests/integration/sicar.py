from pathlib import Path
import unittest
import requests
from SICAR import Sicar, OutputFormat
from SICAR.exceptions import EmailNotValidException, StateCodeNotValidException


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_get_base_url(self):
        assert self._car.get_base_url() == self._car._Sicar__base_url

    def test_invalid_email(self):
        with self.assertRaises(EmailNotValidException):
            self._car._validate_email("test@test")

    def test_valid_email(self):
        email = "name@email.com"
        self.assertEqual(self._car._validate_email(email), email)

    def test_class_str(self):
        assert str(self._car) == f"SICAR - {self._car._Sicar__email}"

    def test_create_default_session(self):
        self._car._create_session()
        session = self._car._Sicar__session
        self.assertIsInstance(
            session,
            requests.Session,
        )
        self.assertEqual(
            session.headers["User-Agent"],
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
        )
        self.assertEqual(session.headers["Accept-Encoding"], "gzip, deflate, br")
        self.assertEqual(
            session.headers["Accept"],
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        )

    def test_create_custom_session(self):
        self._car._create_session(
            {"User-Agent": "python-requests/2.28.2", "Accept": "*/*"}
        )
        session = self._car._Sicar__session
        self.assertIsInstance(session, requests.Session)
        self.assertEqual(session.headers["User-Agent"], "python-requests/2.28.2")
        self.assertEqual(session.headers["Accept"], "*/*")

    def test_get_cities_codes_invalid_state(self):
        with self.assertRaises(StateCodeNotValidException):
            self._car.get_cities_codes("BR")

    def test_get_cities_codes_valid_state(self):
        cities_codes = self._car.get_cities_codes("RR")
        self.assertIsInstance(
            cities_codes,
            dict,
        )
        self.assertEqual(len(cities_codes), 15)  # 15 cities in Roraima
        self.assertEqual(cities_codes["Alto Alegre"], "1400050")  # Verify city code

    def test_download_city_by_code_shapefile(self):
        self.assertIsInstance(
            self._car.download_city_code("3120870"),
            Path,
        )

    def test_download_city_by_code_csv(self):
        self.assertIsInstance(
            self._car.download_city_code("3120870", output_format=OutputFormat.CSV),
            Path,
        )


if __name__ == "__main__":
    unittest.main()
