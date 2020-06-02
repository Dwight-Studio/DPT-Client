#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.progressbar import ProgressBar
from dpt.engine.gui.menu.slider import Slider
from dpt.engine.gui.menu.window import Window
from dpt.engine.gui.menu.text import Text
from dpt.engine.gui.menu.radioButton import RadioButton
from dpt.engine.gui.menu.timer import Timer
from dpt.engine.gui.menu.levelOverview import LevelOverview


def delete_items():
    """Supprime toutes les éléments de menu"""
    Timer.kill()
    for win in Window.window_list:
        win.sprites.empty()
    for lo in LevelOverview.level_overview_list:
        lo.kill(False)
    LevelOverview.level_overview_list.clear()
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
    LevelOverview.main_loop()
