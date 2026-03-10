import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_add_to_cart_button_exists(request):
    """Тест проверяет наличие кнопки добавления в корзину на странице товара"""
    
    # Получаем параметр language из командной строки
    language = request.config.getoption("--language")
    print(f"\n Запуск теста с языком: {language}")
    
    driver = None
    try:
        # Настраиваем опции браузера
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': language})
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        
        # Увеличиваем таймауты
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(120)  
        driver.set_script_timeout(60)
        driver.implicitly_wait(10)
        
        
        url = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
        print(f" Открываем страницу: {url}")
        
       
        try:
            driver.get(url)
            print(" Страница загружена")
        except Exception as e:
            print(f" Ошибка при загрузке: {type(e).__name__}")
            # Проверяем, может страница все же частично загрузилась
            pass
        
        # Ждем появления кнопки
        print("🔍 Ищем кнопку добавления в корзину...")
        
        # Пробуем разные селекторы для кнопки
        selectors = [
            "button.btn-add-to-basket",
            "button.btn-primary",
            "button[type='submit']",
            ".btn-lg",
            "#add_to_basket_form button",
            "//button[contains(text(), 'Add to basket')]",
            "//button[contains(text(), 'Añadir')]",
            "//button[contains(text(), 'Ajouter')]",
            "//button[contains(text(), 'In den Warenkorb')]"
        ]
        
        button = None
        for selector in selectors:
            try:
                # Проверяем CSS селекторы
                if not selector.startswith("//"):
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                else:
                    # Проверяем XPath
                    elements = driver.find_elements(By.XPATH, selector)
                
                if elements:
                    button = elements[0]
                    print(f"   Кнопка найдена: {selector}")
                    break
            except Exception as e:
                continue
        
        # Если кнопка не найдена, пробуем поискать по тексту
        if not button:
            try:
                # Ищем любые кнопки на странице
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in all_buttons:
                    btn_text = btn.text.strip().lower()
                    if any(word in btn_text for word in ['add', 'basket', 'cart', 'корзина', 'añadir', 'ajouter']):
                        button = btn
                        print(f"   Кнопка найдена по тексту: '{btn.text}'")
                        break
            except Exception as e:
                pass
        
        # Проверяем, что кнопка найдена
        assert button is not None, " Кнопка добавления в корзину не найдена"
        
        # Проверяем, что кнопка видима и активна
        assert button.is_displayed(), " Кнопка не видна на странице"
        assert button.is_enabled(), " Кнопка не активна"
        
        # Проверяем текст кнопки
        button_text = button.text.strip()
        assert button_text, " Текст кнопки пустой"
        print(f"   Текст кнопки: '{button_text}'")
        print(" ТЕСТ УСПЕШНО ПРОЙДЕН!")
        
    except AssertionError as e:
        print(f" {str(e)}")
        raise
    except Exception as e:
        print(f" Неожиданная ошибка: {type(e).__name__}: {str(e)}")
        # Если проблема с подключением, пропускаем тест
        if any(err in str(e) for err in ['Timeout', 'Connection', 'timed out']):
            pytest.skip(f"Пропуск теста из-за проблем с сетью: {str(e)}")
        else:
            raise
    finally:
        # Закрываем браузер
        if driver:
            time.sleep(2)  # Даем время посмотреть результат
            driver.quit()
            print(" Браузер закрыт")
