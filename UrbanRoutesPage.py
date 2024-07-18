from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from helpers import retrieve_phone_code
import data
# quite la importacion time



# Localizadores
class UrbanRoutesPage:
# Configurar la dirección
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
# Seleccionar la tarifa Comfort.
    ask_for_taxi_button = (By.XPATH, '//button[@type="button" and @class="button round" and text()="Pedir un taxi"]')
    comfort_rate_button = (By.XPATH, '//div[@class="tcard-icon"]/img[@alt="Comfort"]')
# Rellenar el número de teléfono
    phone_number_area = (By.CSS_SELECTOR, "div.np-text")
    phone_number_label = (By.CSS_SELECTOR, "label[for='phone']")
    phone_number_input = (By.CSS_SELECTOR, "input#phone")
    next_button = (By.CSS_SELECTOR, "button.button.full")
    phone_number_display = (By.XPATH, "//div[@class='np-text' and text()='+1 123 123 12 12']")
# Codigo de telefono
    code_label = (By.CSS_SELECTOR, "label[for='code']")
    code_input = (By.CSS_SELECTOR, "input#code")
    submit_button = (By.XPATH, "//button[@type='submit' and contains(@class, 'button full') and text()='Confirmar']")
# Agregar una tarjeta de crédito.
    payment_method_button = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    add_credit_card_button = (By.XPATH, '//img[@class="pp-plus" and @alt="plus"]')
    credit_card_number_field = (By.ID, 'number')
    cvv_field = (By.CSS_SELECTOR, "div.card-code-input input.card-input")
    outside_click_area = (By.CSS_SELECTOR, "div.plc")
    add_card_button = (By.XPATH, '//button[@type="submit" and @class="button full" and text()="Agregar"]')
    close_button_payment_method = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    payment_method_card_label = (By.XPATH, '//div[@class="pp-value-text" and text()="Tarjeta"]')
# Mensaje para el conductor
    label_for_comment = (By.CSS_SELECTOR, 'label[for="comment"].label')
    message_to_driver_field = (By.ID, "comment")
# Pedir una manta y pañuelos.
    blanket_and_tissues_switch = (By.CSS_SELECTOR, "div.switch")
    blanket_and_tissues_checkbox = (By.CLASS_NAME, 'r-sw') #selector class name
# # Pedir 2 helados
    ice_cream_plus_button = (By.XPATH,
                             "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    ice_cream_counter = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[contains(@class, 'counter-value')]")
# Pedir taxi e informacion
    request_taxi_button = (By.XPATH, "//button[@type='button' and .//span[text()='Pedir un taxi']]")
    order_popup = (
    By.XPATH, "//div[@class='order-body']//div[@class='order-header-title' and text()='Buscar automóvil']")
    driver_info = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'El conductor llegará en')]")


    def __init__(self, driver):
        self.driver = driver
# Configurar la dirección
    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def open_taxi_modal(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.ask_for_taxi_button)).click()

# Seleccionar la tarifa Comfort.
    def select_comfort_rate(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.comfort_rate_button)).click()

# Rellenar el número de teléfono
    def add_phone_number(self, phone_number):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.phone_number_area)).click()
        wait.until(EC.element_to_be_clickable(self.phone_number_label)).click()
        self.driver.find_element(*self.phone_number_input).send_keys(phone_number)
        wait.until(EC.element_to_be_clickable(self.next_button)).click()


    def add_phone_code(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.code_label)).click()
        self.driver.find_element(*self.code_input).send_keys(retrieve_phone_code(self.driver))
        wait.until(EC.element_to_be_clickable(self.submit_button)).click()

# Agregar una tarjeta de crédito.
    def add_credit_card(self, card_number, cvv):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()
        wait.until(EC.element_to_be_clickable(self.add_credit_card_button)).click()

        credit_card_field = self.driver.find_element(*self.credit_card_number_field)
        credit_card_field.click()
        credit_card_field.send_keys(card_number)

        cvv_field = self.driver.find_element(*self.cvv_field)
        cvv_field.click()
        cvv_field.send_keys(cvv)
        # quite el time slepp

        self.driver.find_element(*self.outside_click_area).click()
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.close_button_payment_method).click()


    def verify_credit_card_added(self):
        wait = WebDriverWait(self.driver, 10)
        payment_method_card_element = wait.until(EC.visibility_of_element_located(self.payment_method_card_label))
        return payment_method_card_element.is_displayed()
# Escribir un mensaje para el conductor
    def message_to_driver(self, message):
        label_field = self.driver.find_element(*self.label_for_comment)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", label_field)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.label_for_comment))
        label_field.click()
        message_field = self.driver.find_element(*self.message_to_driver_field)
        message_field.send_keys(message)

# Pedir una manta y pañuelos.
    def click_blanket_switch(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.blanket_and_tissues_switch)).click()
        self.driver.find_element(*self.blanket_and_tissues_switch).click()


# Pedir 2 helados
    def order_ice_creams(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()
        wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()


# Pedir taxi e informacion
    def click_smart_button(self):
       self.driver.find_element(*self.request_taxi_button).click()
# Esperar a que aparezca la información del conductor
    def get_driver_information(self):
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.driver_info))

# quite el time slepp ya que en el mismo metodo llama a la espera de forma mejor
