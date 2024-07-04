import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains


# SE CREO LA PAGINA RETRIVE PHONE CODE PARA EL METODO DE OBTENER EL CODIGO DEL CELULAR
# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
    # Configurar la dirección
        self.from_field = (By.ID, 'from')
        self.to_field = (By.ID, 'to')
    # Seleccionar la tarifa Comfort.
        self.call_button = (By.CLASS_NAME, 'button.round')
        self.comfort_button = (By.XPATH, "(//div[text()='Comfort'])[1]")
        self.comfort_button_container = (By.XPATH, "//div[@class='tcard active']")
    # Rellenar el número de teléfono
        self.phone_button = (By.XPATH, '//div[@class="np-button"]')
        self.phone_field = (By.ID, "phone")
        self.phone_next_button = (By.XPATH, "(//button[@type='submit'])[1]")
        self.code_field = (By.ID, "code")
        self.code_confirm_button = (By.XPATH, "(//button[@type='submit'])[2]")
    # Agregar una tarjeta de crédito.
        self.payment_method_field = (By.CSS_SELECTOR, '.pp-button.filled >.pp-text')
        self.add_card_button = (By.XPATH, "//div[@class='pp-plus-container']//img[1]")
        self.card_number_field = (By.ID, "number")
        self.card_code_field = (By.XPATH, "(//input[@id='code'])[2]")
        self.add_card_confirm_button = (By.XPATH, "//button[text()='Agregar']")
        self.exit_button_in_payment = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
        self.payment_method_selected = (By.CLASS_NAME, 'pp-value-text')
    # Escribir un mensaje para el conductor
        self.message_to_driver_field = (By.ID, "comment")
        self.comment_field = (By.CSS_SELECTOR, '.tariff-picker.shown>.form>:nth-child(3)>div')
        self.error_message_comment = (By.XPATH, '//div[contains(text(), "Longitud máxima 24")]')
    # Pedir una manta y pañuelos.
        blankets_and_tissues_button = (By.XPATH, "(//span[@class='slider round'])[1]")
        blankets_and_tissues_checkbox = (By.CSS_SELECTOR, ".switch input.switch-input")
    # Pedir 2 helados
        add_ice_cream_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
        ice_cream_counter = (By.XPATH, "(//div[@class='counter']//div)[2]")
    # Aparece el modal para buscar un taxi.
        order_taxi_button = (By.XPATH, "(//button[@type='button']//span)[1]")
    # Esperar a que aparezca la información del conductor
        waiting_popup_header = (By.CLASS_NAME, "order-header-title")
        order_countdown_timer = (By.CLASS_NAME, "order-header-time")




# Configurar la dirección
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

# Seleccionar la tarifa Comfort.
    def click_request_taxi_button(self):
        self.driver.find_element(*self.call_button).click()

    def click_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()
        time.sleep(3)

# Rellenar el número de teléfono
    def click_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)
        time.sleep(3)


    def click_phone_next_button(self):
        self.driver.find_element(*self.phone_next_button).click()
        time.sleep(3)

    def set_code_phone(self):
        self.driver.find_element(*self.code_field).send_keys(retrive_phone_code.retrieve_phone_code(self.driver))

    def click_confirm_button_in_verification(self):
        self.driver.find_element(*self.code_confirm_button).click()
        time.sleep (5)

    def click_exit_button_in_payment_popup(self):
        self.driver.find_element(*self.exit_button_in_payment).click()

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep (5)

# Agregar una tarjeta de crédito.
    def scroll_and_click(self, payment_method_field):
        element = WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(payment_method_field))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(payment_method_field)).click()
    def click_payment_method_field(self):
        wait = WebDriverWait(self.driver, 10)
        payment_method_field = wait.until(expected_conditions.element_to_be_clickable(self.payment_method_field))
        # actions = ActionChains(self.driver)
        # actions.move_to_element(payment_method_field).perform()
        payment_method_field.click()
    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()
    def set_card_number(self):
        self.driver.find_element(*self.card_number_field).send_keys(data.CARD_NUMBER)
    def set_card_code(self):
        self.driver.find_element(*self.card_code_field).send_keys(data.CARD_CODE)
    def click_add_card_confirm_button(self):
       self.driver.find_element(*self.add_card_confirm_button).click()
    def click_exit_button_in_payment(self):
        self.driver.find_element(*self.exit_button_in_payment).click()
# Escribir un mensaje para el conductor
    def click_comment_field(self):
        self.driver.find_element(*self.comment_field).click()

    def write_comment(self, message):
        self.driver.find_element(*self.message_to_driver_field).send_keys(message)

    def set_comment_driver(self, message):
        self.click_comment_field()
        self.write_comment(message)
