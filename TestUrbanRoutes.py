from unittest import result
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from UrbanRoutesPage import UrbanRoutesPage
import data
from selenium.webdriver.support import expected_conditions as EC
# quite la importacion time



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
        self.driver.implicitly_wait(10)
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        # Añadir las siguientes líneas para obtener los valores de los campos de dirección y verificar la aserción
        from_value = self.driver.find_element(*routes_page.from_field).get_attribute("value")
        to_value = self.driver.find_element(*routes_page.to_field).get_attribute("value")
        assert from_value == address_from
        assert to_value == address_to

# Seleccionar la tarifa Comfort.
    def test_request_comfort_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.open_taxi_modal()
        routes_page.select_comfort_rate()
        wait = WebDriverWait(self.driver, 10)
        modal_open = wait.until(EC.visibility_of_element_located(routes_page.comfort_rate_button))
        assert modal_open, "El modal del taxi no se abrió correctamente."


    # Rellenar el número de teléfono
    def test_add_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = data.phone_number
        routes_page.add_phone_number(phone_number)
        # assert
        current_value = self.driver.find_element(*routes_page.phone_number_input).get_attribute("value") #assert
        assert current_value == phone_number


    def test_add_phone_code(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_phone_code()
        displayed_phone_number = self.driver.find_element(*routes_page.phone_number_display).text #assert
        assert displayed_phone_number == data.phone_number, f"Esperado: {data.phone_number}, Actual: {displayed_phone_number}"

# Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        cvv = data.card_code
        routes_page.add_credit_card(card_number, cvv)  #assert
        assert routes_page.verify_credit_card_added()

# Escribir un mensaje para el conductor
    def test_message_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        message_for_driver = data.message_for_driver
        routes_page.message_to_driver(message_for_driver)
        displayed_message = self.driver.find_element(*routes_page.message_to_driver_field).get_attribute("value")
        assert displayed_message == message_for_driver #assert

# Pedir una manta y pañuelos.
    def test_Toggle_Switch_Activation(self): #cambio de nombre de test
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_switch()
        checkbox_element = self.driver.find_element(*routes_page.blanket_and_tissues_checkbox)
        assert result, "El interruptor no se activó correctamente"

# Pedir 2 helados
    def test_order_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_ice_creams()
        ice_cream_counter_element = self.driver.find_element(*routes_page.ice_cream_counter)
        counter_value = ice_cream_counter_element.text #assert
        assert counter_value == "2"

# Pedir taxi e informacion
    def test_find_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_smart_button()
        WebDriverWait(self.driver, 3)
        assert self.driver.find_element(*routes_page.request_taxi_button).is_displayed(), "El botón 'Pedir un taxi' no está visible después de llenar el formulario."

# Esperar a que aparezca la información del conductor
    def test_wait_driver_information(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 3)
        routes_page.get_driver_information()
        assert self.driver.find_element(
        *routes_page.driver_info).is_displayed(), "La información del conductor no está visible después de solicitar el taxi."

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
