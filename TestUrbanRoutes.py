from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import data
from UrbanRoutesPage import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

# Configurar la dirección
    def test_set_route(self):
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        # Añadir las siguientes líneas para obtener los valores de los campos de dirección y verificar la aserción
        from_value = self.driver.find_element(*routes_page.from_field).get_attribute("value")
        to_value = self.driver.find_element(*routes_page.to_field).get_attribute("value")
        assert from_value == address_from
        assert to_value == address_to
        time.sleep(2)

# Seleccionar la tarifa Comfort.
    def test_request_comfort_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.open_taxi_modal()
        routes_page.select_comfort_rate()

# Rellenar el número de teléfono
    def test_add_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = data.phone_number
        routes_page.add_phone_number(phone_number)


    def test_add_phone_code(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_phone_code()
        phone_number = data.phone_number

# Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        cvv = data.card_code
        routes_page.add_credit_card(card_number, cvv)

# Escribir un mensaje para el conductor
    def test_message_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        message_for_driver = data.message_for_driver
        routes_page.message_to_driver(message_for_driver)

# Pedir una manta y pañuelos.
    def test_counter(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_switch()

# Pedir 2 helados
    def test_order_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_ice_creams()
# Pedir taxi e informacion
    def test_find_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_smart_button()
        WebDriverWait(self.driver, 3)
# Esperar a que aparezca la información del conductor
    def test_wait_driver_information(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

