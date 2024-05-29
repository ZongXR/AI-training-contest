# -*- coding: utf-8 -*-
from control import *


change_screen_command("page 7")
for i in range(71, 80):
    if i in (71, 72, 73):
        send_screen_information_command(f"t{i}.txt", 99)
    else:
        send_screen_information_command(f"t{i}.txt", 0)
for i in range(701, 713):
    if i == 707:
        send_screen_information_command(f"t{i}.txt", 99)
    else:
        send_screen_information_command(f"t{i}.txt", 0)
