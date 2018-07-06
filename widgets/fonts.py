"""
Fonts for UI

Author: Eric Sluyter
Last edited: July 2018
"""

from PyQt5.QtGui import QFont

class UIFonts:
    title_font = QFont('SansSerif', 20)
    label_font = QFont('SansSerif', 10, 100)
    butt_font = QFont('SansSerif', 10)
    sm_label_font = QFont('SansSerif', 10, -1, True)
    cuelist_font = QFont('SansSerif', 15)
    cue_name_font = QFont('SansSerif', 40)
    notes_font = QFont('SansSerif', 15, 100)
    gobutton_font = QFont('SansSerif', 50)
    transport_rwff_font = QFont('SansSerif', 20)
    transport_play_font = QFont('SansSerif', 40)
    transport_pause_font = QFont('SansSerif', 35)
