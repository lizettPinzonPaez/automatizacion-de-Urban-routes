import time

import data
# import pytest
from selenium import webdriver
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from UrbanRoutesPage import UrbanRoutesPage
from selenium.webdriver.support.ui import WebDriverWait



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.EDGE
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def setup_class(cls):
        cls.driver = webdriver.Edge()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.driver.implicitly_wait(10)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    # Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.ADDRESS_FROM
        address_to = data.ADDRESS_TO
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # Seleccionar la tarifa Comfort.
    def test_request_comfort_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_button()

    # Rellenar el número de teléfono
    def test_fill_phone_verification(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_button()
        routes_page.set_phone_number(data.PHONE_NUMBER)
        routes_page.click_phone_next_button()
        routes_page.click_confirm_button_in_verification()

    # Agregar una tarjeta de crédito.
    def test_add_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method_field()  # Presiona el campo de método de pago
        routes_page.click_add_card_button()  # Presiona el botón de agregar tarjeta
        routes_page.set_card_number()  # Ingresa el número de tarjeta
        routes_page.set_card_code()  # Ingresa el código de la tarjeta
        routes_page.click_add_card_confirm_button()  # Presiona el botón de confirmación
        routes_page.click_exit_button_in_payment()  # Presiona el botón de salida

    # Escribir un mensaje para el conductor
    def test_write_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        driver_message = data.MESSAGE_FOR_DRIVER
        routes_page.set_comment_driver(driver_message)
        WebDriverWait(self.driver, 3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


