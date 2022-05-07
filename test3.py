import sys
import time
import os
import subprocess as sp

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def list_files(startPath,tree):
    # 目录输出的文件
    filename = '/Users/francesco/Library/CloudStorage/OneDrive-个人/Pycharm_program/filecopy/list.txt'
    # with open(r'd:\list.txt', 'w') as fileSave:
    names = locals()
    record = []
    current_node = 0
    current_nodes = []
    parent_node =-1
    for i in range(30):
        record.append(0)
    lastlevel = -1
    level = -1

    # 遍历目录
    for root, dirs, files in os.walk(startPath):
        # 设置遍历层级
        current_nodes.append(current_node)
        level = root.replace(startPath, '').count(os.sep)

        if lastlevel == level:  # 横向读取
            parent_node = record[level - 1]
            current_node = record[level] + 1
            record[level] = current_node
            names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
            names['node' + str(current_node)].setText(0, os.path.basename(root))
            names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
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

        else:  # 正向读取
            parent_node = current_node
            if level != 0:
                current_node = int(str(record[level-1]) + '1')
                record[level] = current_node
                names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
                names['node' + str(current_node)].setText(0, os.path.basename(root))
                names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))

            else :
                names['node' + str(current_node)] = QTreeWidgetItem(tree)
                names['node' + str(current_node)].setText(0, os.path.basename(root))
                names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
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
    for root, dirs, files in os.walk(startPath):
        # 设置遍历层级
        current_nodes.append(current_node)
        level = root.replace(startPath, '').count(os.sep)

        if lastlevel == level:  # 横向读取
            parent_node = record[level - 1]
            current_node = record[level] + 1
            record[level] = current_node
            # names['node' + str(current_node)] = QTreeWidgetItem(names['node' + str(parent_node)])
            # names['node' + str(current_node)].setText(0, os.path.basename(root))
            # names['node' + str(current_node)].setIcon(0, QIcon('./icon/folder1.ico'))
            startNo = current_node + 1
            str1 = 'node' + str(startNo)
            while  str1 in locals().keys():
                startNo += 1
                str1 = 'node' + str(startNo)
            for f in files:
                names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                names['node' + str(startNo)].setText(0, f)
                names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                startNo += 1
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
            str1 = 'node' + str(startNo)
            while  str1 in locals().keys():
                startNo += 1
                str1 = 'node' + str(startNo)
            for f in files:
                names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                names['node' + str(startNo)].setText(0, f)
                names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                startNo += 1
        else:  # 正向读取
            parent_node = current_node
            if level != 0:
                current_node = int(str(record[level-1]) + '1')
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
            str1 = 'node' + str(startNo)
            while  str1 in locals().keys():
                startNo += 1
                str1 = 'node' + str(startNo)
            for f in files:
                names['node' + str(startNo)] = QTreeWidgetItem(names['node' + str(current_node)])
                names['node' + str(startNo)].setText(0, f)
                names['node' + str(startNo)].setIcon(0, QIcon('./icon/file.ico'))
                startNo += 1


        lastlevel = level


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QMainWindow()
    main.resize(600,600)
    tree = QTreeWidget(main)
    main.setCentralWidget(tree)
    path = r'/Users/francesco/Library/CloudStorage/OneDrive-个人/Pycharm_program/filecopy2'
    # dir = raw_input('please input the path:')

    main.show()
    list_files(path,tree)

    sys.exit(app.exec())