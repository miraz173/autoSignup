import string
import secrets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def secure_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))
    
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://pre-live.decoraan.com/")

wait = WebDriverWait(driver, 20)

driver.implicitly_wait(15)
sign_in_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(normalize-space(),'Sign in')]")
))
sign_in_btn.click()

driver.implicitly_wait(10)
sign_up_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//span[contains(normalize-space(),'Sign up')]")
))
sign_up_btn.click()

#clicks ^above^ can be avoided by directly using "https://auth.decoraan.com/sign-up" URL
wait.until(EC.presence_of_element_located((By.ID, "username")))

#optional, as BD is selected by default
# driver.find_element(By.XPATH, "//div[contains(@class,'custom-select')]").click()
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(normalize-space(),'Bangladesh')]"))).click()

password = secure_password()
print("Generated Password:", password)

driver.find_element(By.ID, "username").send_keys("testid3@gmail.com")
driver.find_element(By.ID, "firstName").send_keys("Moshiur")
driver.find_element(By.ID, "lastName").send_keys("Rahman")
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "confirmpassword").send_keys(password)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

# --- OTP page ---
otp_boxes = wait.until(EC.visibility_of_all_elements_located(
    (By.CLASS_NAME, "otp-form-input")
))

otp = "123456"

for i, box in enumerate(otp_boxes):
    if i < len(otp):
        box.send_keys(otp[i])


otp_submit = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[@type='submit' and not(@disabled)]")
))
otp_submit.click()
