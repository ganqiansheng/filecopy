import os
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
        self.setHeaderLabels(['key', 'value'])
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def bind_event(self):
        self.clicked.connect(self.onTreeClicked)

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
        file_load_widget = QWidget()
        file_load_widget.setAttribute(Qt.WA_DeleteOnClose)
        ui = Ui_Form()
        ui.setupUi(file_load_widget)
        file_load_widget.show()

        self.clear()
        names = locals()
        record = []
        current_node = 0
        current_nodes = []
        parent_node = -1
        for i in range(30):
            record.append(0)
        lastlevel = -1
        level = -1
        for root, dirs, files in os.walk(self.startPath):
            # 设置遍历层级
            current_nodes.append(current_node)
            level = root.replace(self.startPath, '').count(os.sep)

            if lastlevel == level:  # 横向读取
                parent_node = record[level - 1]
                current_node = record[level] + 1
                record[level] = current_node
                names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                names['node' + str(current_node)].setText(0, os.path.basename(root))
                names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                # names['node' + str(current_node)].setCkeckState(0, Qt.Checked)
                names['node' + str(current_node)].setText(1, self.get_item_dir(names['node' + str(current_node)]))
                print(self.get_item_dir(names['node' + str(current_node)].parent()), '正在加载中......')
                liststr = '正在加载中......' + self.get_item_dir(names['node' + str(current_node)])
                ui.listWidget_load_file.addItem(liststr)
                # parent_node = parent_node
            elif lastlevel > level:  # 逆向读取
                if str(current_node)[:-1] == '':
                    parent_node = 0
                else:
                    parent_node = record[level - 1]
                current_node = record[level] + 1
                record[level] = current_node
                names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                names['node' + str(current_node)].setText(0, os.path.basename(root))
                names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                # names['node' + str(current_node)].setCheckState(0, Qt.Checked)
                names['node' + str(current_node)].setText(1, self.get_item_dir(names['node' + str(current_node)]))
                print(self.get_item_dir(names['node' + str(current_node)].parent()), '正在加载中......')
                liststr = '正在加载中......' + self.get_item_dir(names['node' + str(current_node)])
                ui.listWidget_load_file.addItem(liststr)
            else:  # 正向读取
                parent_node = current_node
                if level != 0:
                    current_node = int(str(record[level - 1]) + '1')
                    record[level] = current_node
                    names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                    names['node' + str(current_node)].setText(0, os.path.basename(root))
                    names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                    # names['node' + str(current_node)].setCkeckState(0,Qt.Checked)
                    names['node' + str(current_node)].setText(1, self.get_item_dir(names['node' + str(current_node)]))
                    print(self.get_item_dir(names['node' + str(current_node)].parent()), '正在加载中......')
                    liststr = '正在加载中......' + self.get_item_dir(names['node' + str(current_node)])
                    ui.listWidget_load_file.addItem(liststr)

                else:

                    names['node' + str(current_node)] = QTreeWidgetItem(self)
                    names['node' + str(current_node)] = names['node' + str(current_node)]
                    names['node' + str(current_node)].setText(0, os.path.basename(root))
                    names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                    # names['node' + str(current_node)].setCkeckState(0,Qt.Checked)
                    names['node' + str(current_node)].setText(1, self.get_item_dir((names['node' + str(current_node)])))
                    print(self.get_item_dir(names['node' + str(current_node)].parent() or self.topLevelItem(0)),
                          '正在加载中......')
                    liststr = '正在加载中......' + self.get_item_dir(names['node' + str(current_node)])
                    ui.listWidget_load_file.addItem(liststr)

                    # current_node = record[level] + 1
            lastlevel = level

        ############添加文件###############
        record = []
        current_node = 0
        current_nodes = []
        parent_node = -1
        for i in range(30):
            record.append(0)
        lastlevel = -1
        level = -1
        file_no = 1
        for root, dirs, files in os.walk(self.startPath):
            # 设置遍历层级
            current_nodes.append(current_node)
            level = root.replace(self.startPath, '').count(os.sep)

            if lastlevel == level:  # 横向读取
                parent_node = record[level - 1]
                current_node = record[level] + 1
                record[level] = current_node
                # names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                # names['node' + str(current_node)].setText(0, os.path.basename(root))
                # names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                startNo = current_node + 1
                for f in sorted(files):
                    # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    str_file_to_item_no = 'node'  + str(startNo)
                    while str_file_to_item_no in locals().keys():
                        startNo += 1
                        str_file_to_item_no = 'node' + str(startNo)
                        # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    names[str_file_to_item_no] = QTreeWidgetItem(names['node' + str(current_node)])
                    names[str_file_to_item_no].setText(0, f)
                    names[str_file_to_item_no].setIcon(0, QIcon('./icon/file.ico'))
                    # names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                    # names['node' + str(startNo)].setText(0, f)
                    # names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                    print(str(file_no).rjust(10), '：', str(f).ljust(50), '正在加载中......')
                    file_no += 1
                    ui.listWidget_load_file.addItem('正在加载中......' + f)

                    # startNo += 1
                # parent_node = parent_node
            elif lastlevel > level:  # 逆向读取
                if str(current_node)[:-1] == '':
                    parent_node = 0
                else:
                    parent_node = record[level - 1]
                current_node = record[level] + 1
                record[level] = current_node

                # names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                # names['node' + str(current_node)].setText(0, os.path.basename(root))
                # names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))

                startNo = current_node + 1
                for f in sorted(files):
                    # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    str_file_to_item_no = 'node' + str(startNo)
                    while str_file_to_item_no in locals().keys():
                        startNo += 1
                        str_file_to_item_no = 'node' + str(startNo)
                        # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    names[str_file_to_item_no] = QTreeWidgetItem(names['node' + str(current_node)])
                    names[str_file_to_item_no].setText(0, f)
                    names[str_file_to_item_no].setIcon(0, QIcon('./icon/file.ico'))
                    # names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                    # names['node' + str(startNo)].setText(0, f)
                    # names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                    print(str(file_no).rjust(10), '：', str(f).ljust(50), '正在加载中......')
                    file_no += 1
                    ui.listWidget_load_file.addItem('正在加载中......' + f)
                    # startNo += 1
            else:  # 正向读取
                parent_node = current_node
                if level != 0:
                    current_node = int(str(record[level - 1]) + '1')
                    record[level] = current_node
                #     names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                #     names['node' + str(current_node)].setText(0, os.path.basename(root))
                #     names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                #
                # else :
                #     names['node' + str(current_node)] = QTreeWidgetItem(tree)
                #     names['node' + str(current_node)].setText(0, os.path.basename(root))
                #     names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
                # current_node = record[level] + 1

                startNo = current_node + 1
                for f in sorted(files):
                    # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    str_file_to_item_no = 'node' + str(startNo)
                    while str_file_to_item_no in locals().keys():
                        startNo += 1
                        str_file_to_item_no = 'node' + str(startNo)
                        # str_file_to_item_no = 'node_' + f + '_' + str(startNo)
                    names[str_file_to_item_no] = QTreeWidgetItem(names['node' + str(current_node)])
                    names[str_file_to_item_no].setText(0, f)
                    names[str_file_to_item_no].setIcon(0, QIcon('./icon/file.ico'))
                    # names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                    # names['node' + str(startNo)].setText(0, f)
                    # names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                    try:
                        mtime = os.path.getmtime(os.path.abspath(f))
                        strmtime = datetime.fromtimestamp(mtime).strftime('%y-%m-%d      %H:%M:%S')
                        names[str_file_to_item_no].setText(1, strmtime)
                        names['node' + str(startNo)].setText(1, strmtime)

                    # ctime = time.ctime(os.path.getctime(f))
                    # print('mtime:',type(mtime))
                    except:
                        # af = os.path.abspath(f)
                        # print(af.split('/'))
                        # print('出错的文件有：',f)
                        with open('fileerrot.text', 'w') as file_error:
                            file_error.write('记录时间:' + datetime.now().strftime('%y-%m-%d      %H:%M:%S')+ '\n')
                            dir_str = self.get_item_dir(names[str_file_to_item_no].parent())
                            file_error.write(' ' * 10 + '出错目录：' + dir_str+ '\n')
                            file_error.write(' ' * 10 + '出错文件：' + str(f)+ '\n')

                        pass

                    print(str(file_no).rjust(10), '：', str(f).ljust(50), '正在加载中......')
                    file_no += 1

                    ui.listWidget_load_file.addItem('正在加载中......' + f)
                    # startNo += 1

            liststr = '以上文件所在目录为：' + self.get_item_dir(names[str_file_to_item_no].parent())
            ui.listWidget_load_file.addItem(liststr)
            ui.listWidget_load_file.addItem('-' * 200)
            # ui.listWidget_load_file.setCurrentRow(ui.listWidget_load_file.count() - 1)
            # ui.listWidget_load_file.currentItem().setIcon(QIcon('./icon/edit_add.ico'))
            # brush = QBrush(Qt.SolidPattern)
            # brush.setColor(Qt.lightGray)
            # ui.listWidget_load_file.currentItem().setBackground(brush)
            startNo += 1
            lastlevel = level

if __name__ == '__main__':
    app = QApplication(sys.argv)
    filePath = '/Users/francesco/Library/CloudStorage/OneDrive-个人/Pycharm_program/weather_forcast'
    main = FileManager()
    main.getPath(filePath)
    main.show()

    sys.exit(app.exec_())
