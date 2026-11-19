import json
import pytest
from selenium.webdriver.common.by import By
from Utils.login_page import LoginPage

# Leemos los datos desde el archivo externo usuarios.json
def cargar_usuarios():
    with open("usuarios.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

@pytest.mark.parametrize("datos", cargar_usuarios())
def test_login_parametrizado(setup_driver, datos):
    """Prueba de login parametrizada con casos positivos y negativos desde JSON"""
    username = datos["username"]
    password = datos["password"]
    esperado = datos["esperado"]

    # Guardo en la memoria de la compu la página de login que estoy probando
    login_page = LoginPage(setup_driver)

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    if esperado == "exito":
        assert "inventory.html" in setup_driver.current_url
    elif esperado == "bloqueado":
        error_message = setup_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert "Epic sadface: Sorry, this user has been locked out." in error_message
    elif esperado == "invalido":
        error_message = setup_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert "Username and password do not match" in error_message