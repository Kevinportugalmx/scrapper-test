import unittest
from services import jumbo_service


class TestJumboService(unittest.TestCase):

    def setUp(self):
        self.urls = [
            "https://www.tiendasjumbo.co/supermercado/despensa/enlatados-y-conservas",
            "https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar",
            "https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo",
            "https://www.tiendasjumbo.co/supermercado/despensa/aceite",
        ]
        self.test_count = 20

    def test_scrape_products(self):
        for i in range(self.test_count):
            url = self.urls[i % len(self.urls)]
            with self.subTest(i=i, url=url):
                products = jumbo_service(url)
                self.assertIsInstance(products, list)
                self.assertEqual(
                    len(products),
                    15,
                    msg=f"Expected 15 products, but got {len(products)}",
                )
                for product in products:
                    self.assertIn("name", product)
                    self.assertIn("price", product)
                    self.assertIn("promo_price", product)


if __name__ == "__main__":
    unittest.main()
