from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import time
import random
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignora los warnings de Selenium


def verify(driver,id, type=0):
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'}) #INTENTAR EVITAR CAPTCHA
    url = "https://yopmail.com/es"
    time.sleep(4)
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_id("login").send_keys(id)
    time.sleep(3)
    driver.find_element_by_id("refreshbut").click()
    time.sleep(3)
    driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@id='ifmail']"))
    time.sleep(2)
    link = driver.find_element_by_xpath("/html/body/main/div/div/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/a").get_attribute("href")
    return link
    

def register(id=str(random.randint(56789098,66789098)),password="0123456789Ab_123"):
    mail = id + "@yopmail.com"
    driver = webdriver.Chrome(executable_path='./chromedriver')
    url = "https://sharkclean.co.uk/register"
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_id("RegisterUserFullEmail_Login").send_keys(mail)
    driver.find_element_by_id("RegisterUserFullEmail_EmailConfirmation").send_keys(mail)
    driver.find_element_by_id("RegisterUserFullEmail_Password").send_keys(password)
    driver.find_element_by_id("RegisterUserFullEmail_PasswordConfirmation").send_keys(password)
    driver.find_element_by_id("AddressForm_FirstName").send_keys("matteo")
    driver.find_element_by_id("AddressForm_LastName").send_keys("panama")
    driver.find_element_by_id("AddressForm_Address1").send_keys("mile")
    driver.find_element_by_id("AddressForm_City").send_keys("London")
    driver.find_element_by_id("AddressForm_PostalCode").send_keys("E17AX")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/form/div[3]/div/div/div[3]/div/button").click()
    print("Registrado\n Correo: "+mail+"\n Contraseña: "+password)
    time.sleep(3)
    try:
        verificado = verify(driver,id)
        driver.get(verificado)
        time.sleep(2)
        print("Correo verificado")
    except:
        print("Ocurrió un problema en la verificación")
        pass

    return id,mail,password

def login(mail,password):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    software = [SoftwareName.CHROME.value]
    os = [OperatingSystem.WINDOWS.value, OperatingSystem.MAC.value]
    rotUA = UserAgent(software_names=software, operating_systems=os, limit=10)
    UA = rotUA.get_random_user_agent()
    options.add_argument('user-agent='+UA)
    time.sleep(2)
    driver = webdriver.Chrome(executable_path='./chromedriver',chrome_options=options)
    url = "https://sharkclean.co.uk/login"
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_id("ShopLoginForm_Login").send_keys(mail)
    time.sleep(1)
    driver.find_element_by_id("ShopLoginForm_Password").send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/form/div[3]/div/button").click()
    print("Sesión Iniciada: \n Correo: "+mail+"\n Contraseña: "+password)
    return driver

def recovery(id,password="123456789_Abc"):
    mail = id + "@yopmail.com"
    driver = webdriver.Chrome(executable_path='./chromedriver')
    url = "https://sharkclean.co.uk/INTERSHOP/web/WFS/SharkNinja-GB-Site/en_GB/-/GBP/ViewForgotLoginData-ForgotPassword"
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_id("ForgotPasswordStep1Email_Login").send_keys(mail)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/form/div/div[2]/div/button").click()
    time.sleep(3)
    try:
        validador = verify(driver,id)
        time.sleep(2)
        driver.get(validador)
        time.sleep(2)
        driver.find_element_by_id("NewPassword_Password").send_keys(password)
        driver.find_element_by_id("NewPassword_ConfirmPassword").send_keys(password)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/form/div/div[3]/div/button").click()
        time.sleep(2)
        print("Contraseña restablecida: \n Correo: "+mail+"\n Contraseña: "+password)
        time.sleep(2)
    except:
        print("Ocurrió un problema al restablecer la contraseña")
        pass
    return password

def changePw(id,old,newPw):
    mail = id + "@yopmail.com"
    driver = login(mail,old)
    url = "https://sharkclean.co.uk/INTERSHOP/web/WFS/SharkNinja-GB-Site/en_GB/-/GBP/ViewProfileSettings-ViewPassword"
    time.sleep(5)
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_id("UpdatePasswordForm_Password").send_keys(old)
    driver.find_element_by_id("UpdatePasswordForm_NewPassword").send_keys(newPw)
    driver.find_element_by_id("UpdatePasswordForm_NewPasswordConfirmation").send_keys(newPw)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/form/div[4]/div/button").click()
    print("Se ha cambiado la contraseña de "+mail+ " a "+newPw)
    time.sleep(3)
    return newPw


if __name__ == "__main__":
    id,mail,password = register()
    login(mail,password)
    newPassword = recovery(id)
    changePw(id,newPassword,"123456789_Demo")
    login(mail,"123456789_Demo")