from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import random
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignora los warnings de Selenium


def verificarCorreo(username, type=0, password="123456"):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    options = webdriver.ChromeOptions() # PARA TRATAR DE EVADIR CAPTCHA
    options.add_argument("--window-size=800,800")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.get("https://yopmail.com/es")
    time.sleep(2)
    driver.find_element_by_id("login").send_keys(username)
    time.sleep(3)
    driver.find_element_by_id("refreshbut").click()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@id='ifmail']"))
    mail = driver.find_element_by_xpath("//pre").text
    driver.switch_to.default_content()
    counter = 0 #Esto se realiza para tener una "ubicación" de donde está el codigo de verificacion dentro del correo
    for letras in mail:
        if letras == "/":
            #print(counter) #Se busca el primer "/", se resta 6 para tener la posición 0 y se mantienen los siguientes 92 caracteres
            break
        counter += 1
    if type == 0: #ACTIVACION CORREO
        url = mail[counter-6:counter-6+92]
        time.sleep(4)
        #print(url)
        driver.get(str(url))
        time.sleep(2)
        driver.quit()
        print("Correo verificado")
        return 1
    else: #RECUPERACION DE CONTRASEÑA
        url = mail[counter-6:counter-6+91]
        #print(url)
        time.sleep(4)
        driver.get(str(url))
        time.sleep(2)
        driver.find_element_by_id("value").send_keys(password)
        driver.find_element_by_id("verification").send_keys(password)
        driver.find_element_by_css_selector("input[type='submit']").click()
        time.sleep(2)
        print("Se ha restablecido la contraseña de la cuenta "+str(username)+"@yopmail.com a: "+str(password)) 
        driver.quit()
        return 1
    

def crearCuenta(user=random.randint(45678616,46678616), password=str(random.randint(45678616,46678616))):
    username = str(user)+"@yopmail.com"
    nombre = "jdhfjshfsj"
    numero = "54545454"
    direccion = "jhdskhfkjsh"
    ciudad = "dhsfkjdshf"

    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https:/clientes.nic.cl/registrar/agregarUsuario.do")
    time.sleep(1)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("passwordVerification").send_keys(password)
    time.sleep(1)
    driver.find_element_by_id("contacto.nombreORazonSocial").send_keys(nombre)
    driver.find_element_by_id("contacto.telefono.numero").send_keys(numero)
    time.sleep(1)
    Select(driver.find_element_by_id("contacto.direccion.regionEstadoProvincia")).select_by_value("13")
    driver.find_element_by_id("contacto.direccion.calleYNumero").send_keys(direccion)
    driver.find_element_by_id("contacto.direccion.ciudad").send_keys(ciudad)
    time.sleep(2)
    Select(driver.find_element_by_id("contacto.direccion.comuna.id")).select_by_value("130208")

    driver.find_element_by_id("leyTransparencia").click()
    driver.find_element_by_id("envioDTE").click()

    driver.find_element_by_id("submitButton").click()
    time.sleep(2)
    driver.switch_to.alert.accept()
    time.sleep(2)
    driver.find_element_by_id("chkAceptado").click()
    driver.find_element_by_id("reglamentacionDialogSubmit").click()
    print("Cuenta creada\n Usuario: "+username+"\n Contraseña: "+password)
    driver.quit()
    time.sleep(5)
    verificarCorreo(user)
    return username, password, user

def iniciarSesion(user,password,type=0):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://clientes.nic.cl/registrar/logon.do")
    driver.find_element_by_id("j_username").send_keys(user)
    driver.find_element_by_id("j_password").send_keys(password)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(2)
    print("Sesión iniciada\n Usuario: "+user+"\n Contraseña: "+password)
    if type == 0:
        driver.quit()
        return 1
    else:
        time.sleep(2)
        return driver

def recuperarContra(user,password="123456"):
    username = str(user)+"@yopmail.com"
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://clientes.nic.cl/registrar/recuperaPassword.do")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("submitButton").click()
    time.sleep(2)
    driver.quit()
    time.sleep(5)
    verificarCorreo(user,1,password)
    return 1

def cambiarContra(user,old,password):
    username = str(user)+"@yopmail.com"
    driver = iniciarSesion(username,old,1)
    #driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://clientes.nic.cl/registrar/editarUsuario.do")
    #Select(driver.find_element_by_css_selector("input[type='button']"))
    time.sleep(2)
    driver.find_element_by_id("buttonChangePassword").click()
    time.sleep(5)
    driver.implicitly_wait(10)
    driver.find_element_by_id("passwordOld").send_keys(old)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("passwordVerification").send_keys(password)
    driver.find_element_by_id("submitButton").click()
    time.sleep(3)
    driver.switch_to.alert.accept()
    time.sleep(2)
    driver.quit()
    print("Contraseña cambiada\n Usuario: "+username+"\n Contraseña: "+str(password))
    return 1

if __name__ == "__main__":
    cuenta = crearCuenta()
    iniciarSesion(cuenta[0],cuenta[1])
    recuperarContra(cuenta[2])
    cambiarContra(cuenta[2],"123456","demostracion")
    iniciarSesion(cuenta[0],"demostracion")