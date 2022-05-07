import os,time
import random
import sys
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from fileloadform import *


class FileManager(QTreeWidget):
    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.initUI()
        self.bind_event()

    def initUI(self):
        self.setWindowTitle('树控件单击响应演示案例')
        # self = QTreeWidget()
        self.setColumnCount(2)
        self.setColumnWidth(0,200)
        self.header().setStretchLastSection(True)
        self.setHeaderLabels(['文件名', '修改时间'])
        self.header().setSectionResizeMode(1, QHeaderView.Stretch)

    def bind_event(self):
        self.clicked.connect(self.onTreeClicked)
        # self.itemSelectionChanged.connect(self.selectitem)



    def selectitem(self):
        for item in self.selectedItems():
            # item = self.currentItem()
            #     for i in range(item.parent().childCount()):
            #         if item == item.parent().child(i):
            #             index = i

            # print('=====', item. row())
            # print('#####'',文件名：%s,修改时间:%s' % (item.text(0), item.text(1)))
            # item = QTreeWidgetItem()
            if item.checkState(0) == Qt.Checked:
                item.setCheckState(0, Qt.Unchecked)
                item.setBackground(0, Qt.transparent)
                item.setBackground(1, Qt.transparent)
            else:
                item.setCheckState(0, Qt.Checked)
                item.setBackground(0, Qt.lightGray)
                item.setBackground(1, Qt.lightGray)
            self.dealwith_item_up(item)
            self.dealwith_item_down(item)
    def onTreeClicked(self, index):
        item = self.currentItem()
        print('=====', index.row())
        print('#####'',文件名：%s,修改时间:%s' % (item.text(0), item.text(1)))
        # item = QTreeWidgetItem()
        if item.checkState(0) == Qt.Checked:
            item.setCheckState(0, Qt.Unchecked)
            item.setBackground(0, Qt.transparent)
            item.setBackground(1, Qt.transparent)
        else:
            item.setCheckState(0, Qt.Checked)
            item.setBackground(0, Qt.lightGray)
            item.setBackground(1, Qt.lightGray)
        self.dealwith_item_up(item)
        self.dealwith_item_down(item)

    def dealwith_item_down(self, item):
        for i in range(item.childCount()):
            itemchild = item.child(i)
            itemchild.setCheckState(0, item.checkState(0))
            if item.checkState(0) == Qt.Checked:
                itemchild.setBackground(0, Qt.lightGray)
                itemchild.setBackground(1, Qt.lightGray)
            if item.checkState(0) == Qt.Unchecked:
                itemchild.setBackground(0, Qt.transparent)
                itemchild.setBackground(1, Qt.transparent)
            if itemchild.childCount() > 0:
                self.dealwith_item_down(itemchild)

    def dealwith_item_up(self, item):
        if item == self.topLevelItem(0):
            return
        if self.item_parent_all_selected(item) == 2:  # 全部选中
            item.parent().setCheckState(0, Qt.Checked)
            item.parent().setBackground(0, Qt.lightGray)
            item.parent().setBackground(1, Qt.lightGray)
        elif self.item_parent_all_selected(item) == 1:
            item.parent().setCheckState(0, Qt.PartiallyChecked)
            item.parent().setBackground(0, QColor(230, 230, 230))
            item.parent().setBackground(1, QColor(230, 230, 230))
        else:
            item.parent().setCheckState(0, Qt.Unchecked)
            item.parent().setBackground(0, Qt.transparent)
            item.parent().setBackground(1, Qt.transparent)
        if item != self.topLevelItem(0):
            self.dealwith_item_up(item.parent())

    def item_parent_all_selected(self, item):
        Checked_number = 0
        PartiallyChecked_number = 0
        Unchecked_number = 0
        for i in range(item.parent().childCount()):
            if item.parent().child(i).checkState(0) == Qt.Checked:
                Checked_number += 1
            elif item.parent().child(i).checkState(0) == Qt.PartiallyChecked:
                PartiallyChecked_number += 1
            else:
                Unchecked_number += 1

        if Checked_number == item.parent().childCount():
            return 2
        elif Unchecked_number == item.parent().childCount():
            return 0
        else:
            return 1

    def item_child_all_selected(self, item):
        Checked_number = 0
        PartiallyChecked_number = 0
        Unchecked_number = 0
        for n in range(item.childCount()):
            item_child = item.child(n)
            if item_child.childCount() == 0:
                if item.checkState(0) == Qt.Checked:
                    Checked_number += 1
                elif item.checkState(0) == Qt.PartiallyChecked:
                    PartiallyChecked_number += 1
                else:
                    Unchecked_number += 1
            else:
                result = self.item_child_all_selected(item_child)
                if result == 2:
                    Checked_number += 1
                elif result == 1:
                    PartiallyChecked_number += 1
                else:
                    Unchecked_number += 1
        if Checked_number == item.childCount():
            return 2
        elif Unchecked_number == item.childCount():
            return 0
        else:
            return 1

    def getPath(self, startPath):
        self.startPath = startPath
        self.draw_tree(self.startPath)

    def get_item_dir(self, item):
        root = self.topLevelItem(0)
        if item == root:
            return self.startPath
        dir = ''
        while item != root:
            dir = item.text(0) + '/' + dir
            item = item.parent()
        dir = self.startPath + '/' + dir
        return dir


    def draw_tree(self, startPath):
        self.clear()
        self.startPath = startPath
        self.dir_SN = 1
        self.file_SN = 1
        self.names = locals()

        for root,dirs,files in os.walk(startPath):
            #确定父节点
            if root == self.startPath:
                relative_path = ''
                str_item_parent_name = 'item_root'
                self.names[str_item_parent_name] = QTreeWidgetItem(self)
                self.names[str_item_parent_name].setText(0,startPath.split(os.sep)[-1])
                self.names[str_item_parent_name].setIcon(0, QIcon('./icon/folder1.ico'))
            else:
                relative_path = root.replace(startPath,'')
                str_item_parent_name = 'item_dir_' + relative_path
            item_parent = self.names[str_item_parent_name]
            #创建目录类子节点
            self.create_directory_node(item_parent,relative_path,dirs)

            #创建文件类子节点
            self.create_file_node(item_parent,relative_path,files)

    # 创建目录类子节点
    def create_directory_node(self,item_parent,relative_path,dirs):
        for dir in dirs:
            str_item_dir_name = 'item_dir_' + relative_path + os.sep + dir
            self.names[str_item_dir_name] = QTreeWidgetItem(item_parent)
            self.names[str_item_dir_name].setText(0,dir)
            self.names[str_item_dir_name].setIcon(0, QIcon('./icon/folder1.ico'))
            print(str(self.dir_SN).rjust(10), '：', (relative_path + os.sep + dir).ljust(50), '正在加载中......')
            self.dir_SN += 1
    # 创建文件类子节点
    def create_file_node(self,item_parent,relative_path,files):
        for file in files:
            str_item_file_name = 'item_file_' + relative_path + os.sep + file
            self.names[str_item_file_name] = QTreeWidgetItem(item_parent)
            self.names[str_item_file_name].setText(0, file)
            self.names[str_item_file_name].setIcon(0, QIcon('./icon/file.ico'))
            try:
                fileinfo = os.stat(self.startPath + relative_path + os.sep + file)
                self.names[str_item_file_name].setText(1,self.formatTime(fileinfo.st_mtime))
                print(str(self.file_SN).rjust(10), '：', file.ljust(50), '正在加载中......')
                self.file_SN += 1
            except:
                self.deal_with_file_error(relative_path,file)
                pass
            # print('*' * 100)
            # print("最后一次访问时间:",self.formatTime(fileinfo.st_atime)) # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileinfo.st_atime)))  #
            # print("最后一次修改时间:", self.formatTime(fileinfo.st_mtime))
            # print("最后一次状态变化的时间：", self.formatTime(fileinfo.st_ctime))
            # print("索引号：", fileinfo.st_ino)
            # print("被连接数目：", fileinfo.st_dev)
            # print("文件大小:", fileinfo.st_size, "字节")
            # print("最后一次访问时间:", fileinfo.st_atime)
            # print("最后一次修改时间:", fileinfo.st_mtime)
            # print("最后一次状态变化的时间：", fileinfo.st_ctime)
    def deal_with_file_error(self,relative_path,file):
        with open('fileerrot.text', 'w') as file_error:
            file_error.write('记录时间:' + datetime.now().strftime('%y-%m-%d      %H:%M:%S') + '\n')
            dir_str = self.startPath + relative_path
            file_error.write(' ' * 10 + '出错目录：' + dir_str + '\n')
            file_error.write(' ' * 10 + '出错文件：' + str(file) + '\n')
    def formatTime(self,atime):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(atime))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    filePath = '/Users/francesco/Library/CloudStorage/OneDrive-个人/Pycharm_program/weather_forcast'
    main = FileManager()
    main.getPath(filePath)
    main.show()

    sys.exit(app.exec_())
