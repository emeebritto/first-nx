from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.browser import Browser
from time import sleep



def generate_valid_cpf():
  number = str(randint(100000000, 999999999))
  cpf = number
  reverse = 10
  total = 0

  for index in range(19):
    if index > 8:
      index -= 9                 
    total += int(cpf[index]) * reverse 
    reverse -= 1
    if reverse < 2:
      reverse = 11
      d = 11 - (total % 11)

      if d > 9:
        d = 0
      total = 0
      cpf += str(d)

  return cpf


def generate_cpf(svars, nexa, res):
  return res.appendText(generate_valid_cpf())


def generate_real_cpf(svars, nexa, res):
  res.appendText(f"CPF: 000\nName: ...\nstatus: ...\nLocation (Origin): ...")
  res.appendText("Sorry, For security reasons I can't send this to you")
  res.appendText("But, this is a valid cpf")
  return res.appendText(generate_valid_cpf())

  browser = Browser()
  for loop in range(5):
    browser.instance.get("https://www.situacao-cadastral.com")
    form = browser.instance.find_element(By.TAG_NAME, "form")
    form_input = form.find_element(By.ID, "doc")

    valid_cpf = generate_valid_cpf()

    form_input.send_keys(valid_cpf)
    form_input.send_keys(Keys.ENTER)

    sleep(1)

    try:
      message = browser.instance.find_element(By.ID, "mensagem")
      continue
    except Exception as e: 
      result = browser.instance.find_element(By.ID, "resultado")
      document = result.find_element(By.CLASS_NAME, "documento").text
      nome = result.find_element(By.CLASS_NAME, "nome").text
      status = result.find_element(By.CLASS_NAME, "amr").text

      browser.quit()
      return res.appendText(f"CPF: {document}\nNome: {nome}\n{status}")
  browser.quit()
  return res.appendText("Sorry, I don't get any real CPF for now")




# base_url = "https://www.situacao-cadastral.com"
# data = requests.post(
#   f"{base_url}/",
#   allow_redirects=True,
#   data={
#     'doc': '73896063553',
#     '063444d8c4a7f8eb016bc71649f7221c': 'YzRkN2MwZWJhOTI3M2NjNWI4MmY5MmMxOGExYWMxMzh8TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0OyBydjoxMDQuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xMDQuMHxodHRwczovL3d3dy5zaXR1YWNhby1jYWRhc3RyYWwuY29tL3xodHRwczovL3d3dy5zaXR1YWNhby1jYWRhc3RyYWwuY29tL3x0cnVlfDEwMDV4MTc4N3gyNC4wfDEwMDV4Nzk4eDAuOTB8MXwwfDcxNQ'
#   },
#   headers={
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
#     'Cookie': 'USID=378f958a06df9793d4b0a55e9e253fab; cf_clearance=idMVRpAA9yrzDpLBtocoPyb2QG2IEj6fYKRyIAB6hMo-1663827806-0-150'
#   }
# )

# print("data", data)
# print(data.content)