import pyautogui
import time
import keyboard
import traceback

search = 'search.png'
go = 'go.png'
hands = 'hands.png'
camp = 'camp.png'
zmb = 'zmb.png'
attack = 'attack.png'
force = 'force.png'
forces = 'forces.png'
use_50 = 'use_50.png'
use_500 = 'use_500.png'
use_100 = 'use_100.png'
close = 'close.png'
close2 = 'close2.png'
close_adv = 'close_adv.png'
no_found = 'no_found.png'
lvl_down = 'lvl_down.png'
x = 'x.png'

lvl_down_counter = 0
max_lvl_down_attempts = 5
lvl_up = 'lvl_up.png'

paused = False

free_camp = False
select_zmb = False
click_search = False
click_zmb = False
click_attack = False
select_force = False
click_go = False
click_use = False
click_x = False

desc = ""

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Программа на паузе. Нажмите 'P' для продолжения.")
    else:
        print("Программа возобновлена. Нажмите 'P' для паузы.")

keyboard.add_hotkey('p', toggle_pause)

print("Запуск программы. Нажмите 'P' для паузы/возобновления.")

def locate_and_click(image_path, confidence=0.99, delay=0.5, move_offset=None, desc="Description"):
    print(f"Выполняется поиск изображения {image_path}")
    try:
        x, y = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=False)
        if move_offset:
            x += move_offset[0]
            y += move_offset[1]
        print(f"Изображение {image_path} найдено. Координаты: {x, y}")
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        print(f"Выполнен клик по {desc}")
        time.sleep(delay)
        return True
    except pyautogui.ImageNotFoundException:
        print(f"Изображение {image_path} не найдено")
    except Exception:
        print("Произошла другая ошибка:")
        traceback.print_exc()
        time.sleep(2)
    return False

while True:
    if paused:
        time.sleep(1)
        continue
    
    locate_and_click(hands, desc="ручкам")

    # if not free_camp:
    if locate_and_click(camp, move_offset=(-1200, 230), desc="поиску"):
        free_camp = True

    # if not select_zmb and free_camp:
    if locate_and_click(zmb, desc="типу зомби"):
        select_zmb = True

    # # if not click_search and select_zmb:
    # if locate_and_click(search, delay=2, desc="кнопке Поиск"):
    #     click_search = True


    if locate_and_click(search, delay=2, desc="кнопке Поиск"):
        try:
            if pyautogui.locateCenterOnScreen(no_found, confidence=0.9):
                print("Ничего не найдено. Пытаемся сменить уровень зомби...")

                if lvl_down_counter < max_lvl_down_attempts:
                    if locate_and_click(camp, move_offset=(-1200, 230), desc="поиску"):
                        if locate_and_click(zmb, desc="типу зомби"):
                            time.sleep(1)
                            if locate_and_click(lvl_down, desc="понижению уровня зомби"):
                                lvl_down_counter += 1
                                time.sleep(1)
                                locate_and_click(search, delay=1, desc="повторной кнопке Поиск")
                            else:
                                print("lvl_down не найден — пропуск.")
                        else:
                            print("zmb не найден — пропуск.")
                    else:
                        print("лупа не найдена")
                else:
                    print(f"Достигнут лимит понижений ({lvl_down_counter}). Повышаем уровень на столько же.")
                    if locate_and_click(camp, move_offset=(-1200, 230), desc="поиску"):
                        if locate_and_click(zmb, desc="типу зомби"):
                            time.sleep(1)

                            success_count = 0
                            for _ in range(lvl_down_counter):
                                if locate_and_click(lvl_up, desc=f"повышению уровня зомби ({success_count+1}/{lvl_down_counter})"):
                                    success_count += 1
                                    time.sleep(0.5)
                                else:
                                    print("lvl_up не найден — попытка пропущена.")
                                    break

                            if success_count == lvl_down_counter:
                                print("Уровень зомби успешно повышен.")
                            else:
                                print(f"Уровень повышен только {success_count} раз(а).")

                            lvl_down_counter = 0
            else:
                click_search = True
        except pyautogui.ImageNotFoundException:
            print(f"Изображение {no_found} не найдено")
            click_search = True
        except Exception:
            print("Произошла другая ошибка:")
            traceback.print_exc()
            time.sleep(2)


    # if not click_zmb and click_search:
    if click_search:        
        if locate_and_click(camp, move_offset=(-590, 150), desc="зомби"):
            click_zmb = True

    # if not click_attack and click_zmb:
    if locate_and_click(attack, desc="кнопке Атаковать"):
        click_attack = True

    # if not select_force and click_attack:
    if locate_and_click(forces, confidence=0.9, desc="иконке отряда в лагере"):
        select_force = True

    # if select_force:
    if locate_and_click(go, desc="кнопке Марш"): 
        free_camp = False
        select_zmb = False
        click_search = False
        click_zmb = False
        click_attack = False
        select_force = False
        click_go = True

    # if click_go:
    if locate_and_click(use_100, confidence=0.999, delay=1, desc="использовать банку"):
        click_use = True

    if click_use:
        if locate_and_click(x, confidence=0.999, delay=1, desc="использовать все банки"):
            click_x = True

    if click_x:
        if locate_and_click(close, desc="кнопке закрыть"):
            click_use = False
            click_x = False
            select_force = True

    locate_and_click(close2, desc="закрыть задания")
    locate_and_click(close_adv, desc="закрыть рекламу")

    # click_go = False

    print("Цикл завершен, ждём 3 секунды")
    time.sleep(3)