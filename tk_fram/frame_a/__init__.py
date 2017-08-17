# -*- coding: utf-8 -*-

from tkinter import Tk, Menu
from .frame_a import init_a_frame, init_menu
# from .frame_api import menu_file
from .frame_a_view import FRAME_WIDTH, FRAME_HEIGHT


def create_a_frame():
    """"""
    #  =======================添加主视图===================
    root = Tk()
    # ============================文件批量配置=============
    # 标题
    menu_bar = init_menu(root)
    # =======================配置主视图尺寸=================
    root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}+0+0")
    root.title('杭州分拣中心仿真程序')
    #  =======================config主界面================
    root.config(
        menu=menu_bar,
        background='#A2B5CD',
    )
    #  =======================初始化r路侧界面===============
    init_a_frame(root=root)
    #  =======================启动主界面====================
    root.mainloop()