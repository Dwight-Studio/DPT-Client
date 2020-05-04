from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.progressbar import ProgressBar
from dpt.engine.gui.menu.slider import Slider
from dpt.engine.gui.menu.window import Window
from dpt.engine.gui.menu.text import Text
from dpt.engine.gui.menu.radioButton import RadioButton
from dpt.engine.gui.menu.timer import Timer


def delete_items():
    """Supprime toutes les éléments de menu"""
    for item in Timer.timer_list.copy():
        item.kill()
    for win in Window.window_list:
        win.sprites.empty()
    Window.window_list = []
    Button.buttonsGroup.empty()
    Button.text_sprite_buttonsGroup.empty()
    Checkbox.checkbox_group.empty()
    ProgressBar.progress_bar_group.empty()
    ProgressBar.bar_group.empty()
    Slider.slide_group.empty()
    for slide in Slider.slider_list:
        slide.kill()
    Slider.slider_list = []
    Text.text_list = []
    RadioButton.radio_button_group.empty()


def main_loop():
    """Execute toutes les boucles des éléments de menu"""
    Window.main_loop()
    Button.main_loop()
    Checkbox.main_loop()
    ProgressBar.main_loop()
    Slider.main_loop()
    Text.main_loop()
    RadioButton.main_loop()
