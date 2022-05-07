import os
import shutil
import sys
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import *
from form import *


# from treeevent import *

# global node_startNo
# node_startNo = 1
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.blocksize = 1024 * 1024
        # self.node_startNo = 1
        # 为比较文件而设的变量
        self.diffs = []
        self.verbose = False

        self.ui.treeWidget_source.setColumnCount(2)
        self.ui.treeWidget_source.setHeaderLabels(['文件名', '修改时间'])
        self.ui.treeWidget_destination.setColumnCount(2)
        self.ui.treeWidget_destination.setHeaderLabels(['文件名', '修改时间'])


        #把源文件和目标文件操作历史记录到置入到对应的comboBox列表中去
        self.ui.comboBox_source_folder.addItems(self.get_dir_from_file('s'))
        self.ui.comboBox_source_folder.setCurrentIndex(0)
        self.ui.comboBox_destination_folder.addItems(self.get_dir_from_file('d'))
        self.ui.comboBox_destination_folder.setCurrentIndex(0)

        # item = self.ui.treeWidget_source.topLevelItem(0)
        # item.setBackground()

        self.bind_event()

    def bind_event(self):
        self.ui.pushButton_source.clicked.connect(self.on_action_set_source_dir_triggered)
        self.ui.pushButton_destination.clicked.connect(self.on_action_set_destination_dir_triggered)
        self.ui.pushButton_compare.clicked.connect(lambda: self.compareTree(self.ui.treeWidget_source.topLevelItem(0),self.ui.treeWidget_destination.topLevelItem(0)))

        # self.ui.treeWidget_source.itemClicked.connect(self.isitemClicked)
        # self.ui.treeWidget_source.itemSelectionChanged.connect(self.selectitem)
        # self.ui.treeWidget_source.itemClicked['QTreeWidgetItem*', 'int'].connect(self.selectItem_column)

        self.ui.comboBox_source_folder.currentTextChanged.connect(self.on_comboBox_source_folder_currentIndexChanged)
        self.ui.comboBox_destination_folder.currentTextChanged.connect(self.on_comboBox_destination_folder_currentIndexChanged)

        # self.ui.label_source_tree_refresh.clicked.connect(self.on_label_source_tree_refresh_clicked)
        # self.ui.label_destination_tree_refresh.clicked.connect(self.on_label_destination_tree_refresh_clicked)

    def selectItem_column(self, item, column):
        print('selectItem_column', column)
        print('selectItem_column', item.checkState(0), item.text(0))
        for i in range(item.childCount()):
            print('*****', item.child(i).text(0))

    def selectitem(self):
        for item in self.ui.treeWidget_source.selectedItems():
            print(item.text(0))
            print(item.parent().text(0))

    def isitemClicked(self, item):

        print('-----', item.checkState(0), item.text(0))
        item.setCheckState(1,Qt.Checked)

    def reportdiffs(self, unique1, unique2, dir1, dir2):
        """
        为目录生成差异报告：comparedirs函数输出的一部分
        """
        if not (unique1 or unique2):
            print('{}和{}文件列表完全相同'.format(dir1, dir2))
        else:
            if unique1:
                print('{}的独有文件：'.format(dir1))
                for unique in unique1:
                    print('...', unique)
            if unique2:
                print('{}的独有文件：'.format(dir2))
                for unique in unique2:
                    print('...', unique)

    def diff(self, seq1, seq2):
        return [item for item in seq1 if item not in seq2]

    def get_item_dir(self, sign, item):
        if sign == 'source':
            root = self.ui.treeWidget_source.topLevelItem(0)
            if item == root:
                return self.source_dir_path
        else:
            root = self.ui.treeWidget_destination.topLevelItem(0)
            if item == root:
                return self.destination_dir_path
        dir = ''
        while item != root:
            dir = item.text(0) + os.sep + dir
            item = item.parent()
        if sign == 'source':
            dir = self.source_dir_path + os.sep + dir
            # dir = self.source_dir_path[0:self.source_dir_path.rfind(os.sep)] + os.sep + dir
        else:
            dir = self.destination_dir_path + os.sep + dir
            # dir = self.destination_dir_path[0:self.destination_dir_path.rfind(os.sep)] + os.sep + dir
        return dir

    def from_text_get_item(self, item_source, name):  # 这里有一个问题，如果一个目录下面有同名的目录和文件，则只能取到第一个
        item = None
        for item in item_source:
            if item.text(0) == name:
                break
        return item

    def comparedirs(self, item_source, item_destination, file1=None, file2=None):
        dir_source = self.get_item_dir('source', item_source)
        dir_destination = self.get_item_dir('destination', item_destination)
        file1 = dir_source if file1 is None else file1
        file2 = dir_destination if file2 is None else file2
        unique1 = self.diff(file1, file2)
        item_child_source, names = self.get_child_item_list(item_source)
        for uniqu1_member in unique1:
            processing_item = self.from_text_get_item(item_child_source, uniqu1_member)
            # processing_item.setBackground(0, QColor(50, 50, 50))
            processing_item.setForeground(0, QColor(255, 0, 0))
            processing_item.parent().setExpanded(True)
        unique2 = self.diff(file2, file1)
        item_child_destination, names = self.get_child_item_list(item_destination)
        for uniqu2_member in unique2:
            processing_item = self.from_text_get_item(item_child_destination, uniqu2_member)
            # processing_item.setBackground(0, QColor(50, 50, 50))
            processing_item.setForeground(0, QColor(255, 0, 255))
            processing_item.parent().setExpanded(True)

        self.reportdiffs(unique1, unique2, dir_source, dir_destination)
        return unique1, unique2

    def intersect(self, seq1, seq2):
        return [item for item in seq1 if item in seq2]

    def get_child_item_list(self, item):
        item_child = []
        names = []
        for i in range(item.childCount()):
            item_child.append(item.child(i))
            names.append(item.child(i).text(0))
        return item_child, names

    def compareTree(self, item_source, item_destination):
        if not item_source:
            QMessageBox.information(self,'提示','没有选择源目录，请重新选择')
            return
        if not item_destination:
            QMessageBox.information(self,'提示','没有选择目标目录，请重新选择')
            return
        item_child_source, source_names = self.get_child_item_list(item_source)
        item_child_destination, destination_names = self.get_child_item_list(item_destination)

        dir_source = self.get_item_dir('source', item_source)
        dir_destination = self.get_item_dir('destination', item_destination)

        self.comparedirs(item_source, item_destination, source_names, destination_names)

        common = self.intersect(source_names, destination_names)
        missed = common[:]

        # 在源文件夹和目标文件夹中有相同名称的文件的比对，确认同名文件是否为相同文件
        for name in common:
            path1 = os.path.join(dir_source, name)
            path2 = os.path.join(dir_destination, name)
            if os.path.isfile(path1) and os.path.isfile(path2):
                missed.remove(name)

                '''
                compare_way =  0   通过相同文件名的最后修改日期来判断
                compare_way =  1   通过二进制读取文件来判断
                '''
                compare_way = 0
                #通过相同文件名的最后修改日期来判断是不是同一个文件，如果修改日期相同则视为相同文件
                if compare_way == 0:
                    file_info1 = os.stat(path1)
                    file_info2 = os.stat(path2)
                    if file_info1.st_mtime == file_info2.st_mtime:
                        if self.verbose:
                            print(name, 'matchs')
                    else:
                        self.diffs.append('files differ at %s --- %s ' % (path1, path2))
                        processing_item = self.from_text_get_item(item_child_source, name)
                        # processing_item.setBackground(0,QColor(50,50,50))
                        processing_item.setForeground(0, QColor(255, 0, 0))
                        processing_item.parent().setExpanded(True)
                        processing_item = self.from_text_get_item(item_child_destination, name)
                        # processing_item.setBackground(0,QColor(50,50,50))
                        processing_item.setForeground(0, QColor(255, 0, 255))
                        processing_item.parent().setExpanded(True)

                        print(name, 'DIFFERS')
                # 通过用二进制的方式按设定大小读取文件并逐一进行比较，如果到文件读取结束还没有不同，则确认两个文件的内容相同，否则则不同，这种方法的准确性非常高，没有错误率
                else:
                    file1 = open(path1, 'rb')
                    file2 = open(path2, 'rb')
                    while True:
                        bytes1 = file1.read(self.blocksize)
                        bytes2 = file2.read(self.blocksize)
                        if (not bytes1) and (not bytes2):
                            if self.verbose:
                                print(name, 'matchs')
                            break
                        if bytes1 != bytes2:
                            self.diffs.append('files differ at %s --- %s ' % (path1, path2))
                            processing_item = self.from_text_get_item(item_child_source, name)
                            # processing_item.setBackground(0,QColor(50,50,50))
                            processing_item.setForeground(0, QColor(255, 0, 0))
                            processing_item.parent().setExpanded(True)
                            processing_item = self.from_text_get_item(item_child_destination, name)
                            # processing_item.setBackground(0,QColor(50,50,50))
                            processing_item.setForeground(0, QColor(255, 0, 255))
                            processing_item.parent().setExpanded(True)

                            print(name, 'DIFFERS')
                            break
                    file1.close()
                    file2.close()

            # 在源文件夹和目标文件夹中有相同名称的目录的比对，根据目录名确认树节点，然后递归比较
        #文件处理
        for name in common:
            path_source = os.path.join(dir_source, name)
            path_destination = os.path.join(dir_destination, name)
            if os.path.isdir(path_source) and os.path.isdir(path_destination):
                missed.remove(name)
                for item1 in item_child_source:
                    if item1.text(0) == name:
                        break
                for item2 in item_child_destination:
                    if item2.text(0) == name:
                        break
                self.compareTree(item1, item2)

        # 同名但一个是文件，一个是目录
        for name in missed:
            self.diffs.append('files missed at %s ---%s:%s' % (dir_source, dir_destination, name))
            print(name, 'DIFFERS')

    def dealwith_this_node(self, item):

        if item.childCount() != 0:
            print('这个节点的名字：', item.text(0))
            print('这个节点的子节点有：')
            for i in range(item.childCount()):
                childitem = item.child(i)
                print(childitem.text(0))
                self.dealwith_this_node(childitem)
        else:
            if item.text(1) != '':
                pass
                # print('这是一个文件')
            else:
                pass
                # print(item.text(0),'没有子节点')

    def copy_file(self, item_source, item_destination):
        #当前处理的源节点  item_source
        #当前处理的目标节点  item_destination
        #源节点对应的绝对路径 absolute_path
        # 源节点对应的相对路径 relative_path
        #目标节点对应的绝对路径 destination_path
        absolute_path = self.get_item_dir('source', item_source) + os.sep
        relative_path = ''
        destination_path = self.destination_dir_path  + os.sep
        if item_source != self.ui.treeWidget_source.topLevelItem(0):
            absolute_path = self.get_item_dir('source', item_source)
            relative_path = absolute_path.replace(self.ui.comboBox_source_folder.currentText(), '')
            destination_path = destination_path + relative_path

        print(absolute_path)
        print(relative_path)


        # 本层中需要处理的目录
        dir_list = []
        for n in range(item_source.childCount()):
            item_child = item_source.child(n)
            if item_child.childCount() == 0:
                continue
            if (item_child.childCount() != 0) and (
                    (item_child.checkState(0) == Qt.PartiallyChecked) or (item_child.checkState(0) == Qt.Checked)):
                dir_list.append(item_child.text(0))

        # dir 当前节点下子节点在选中状态或者半选中状态的目录列表（孙节点数不为0）
        for dir in dir_list:
            source_dir = absolute_path + dir
            destination_dir = destination_path + dir
            # 当前处理的源节点  item_source
            # 当前处理的目标节点  item_destination
            # 源节点对应的绝对路径 absolute_path
            # 源节点对应的相对路径 relative_path
            # 目标节点对应的绝对路径 destination_path
            # 取得源文件夹中的对应的节点

            # item_child_source_list 源节点下面的子节点列表
            # names 源节点下面的子节点名称列表
            item_child_source_list, names = self.get_child_item_list(item_source)
            # item_child_source 子目录名称相对应的树节点
            item_child_source = self.from_text_get_item(item_child_source_list, dir)
            if item_child_source.checkState(0) == Qt.Unchecked:
                pass
            # 需要同步的文件被全选中或者半选中
            else:
                # 目标文件中存在此名称的文件或者目录
                if os.path.exists(destination_dir) and item_source.checkState(0) == Qt.Checked:  # 目标文件中存在此名称的文件或者目录
                    item_child_destination_list, names = self.get_child_item_list(item_destination)
                    item_child_destination = self.from_text_get_item(item_child_destination_list, dir)
                    if item_child_destination.childCount() > 0:  # 目标文件中存在同名称的是目录
                        # 递归处理
                        self.copy_file(item_child_source, item_child_destination)
                else:
                    if (not os.path.exists(destination_dir)) and item_source.checkState(0) == Qt.PartiallyChecked:
                        # 创建此目录
                        print('需要创建的目录名为:', item_child_source.text(0))
                        os.makedirs(destination_dir)
                        # 把这个目录作为节点加入到目标目录树中
                        item_new_child = QTreeWidgetItem(item_destination)
                        item_new_child.setText(0, item_child_source.text(0))
                        item_new_child.setIcon(0,QIcon('./icon/folder1.ico'))
                        # 递归处理
                        self.copy_file(item_child_source, item_new_child)
                        # 目标文件中存在此名称目录同时本目录为半选中状态
                    elif os.path.exists(destination_dir) and item_source.checkState(0) == Qt.PartiallyChecked:
                        item_child_destination_list, names = self.get_child_item_list(item_destination)
                        item_child_destination = self.from_text_get_item(item_child_destination_list, dir)
                        # 递归处理
                        self.copy_file(item_child_source, item_child_destination)
                    else:
                        shutil.copytree(source_dir, destination_dir)


        # 本层中需要处理的文件
        file_list = []
        for n in range(item_source.childCount()):
            item_child = item_source.child(n)
            if (item_child.childCount() == 0) and (item_child.checkState(0) == Qt.Checked):
                file_list.append(item_child.text(0))
        for name in file_list:
            source_file = absolute_path + name
            destination_file = destination_path + name
            if os.path.exists(destination_path + name):
                mtime_source = os.path.getmtime(os.path.abspath(source_file))
                strmtime_source = datetime.fromtimestamp(mtime_source).strftime('%y-%m-%d      %H:%M:%S')
                mtime_destiation = os.path.getmtime(os.path.abspath(destination_file))
                strmtime_destiation = datetime.fromtimestamp(mtime_destiation).strftime('%y-%m-%d      %H:%M:%S')
                if QMessageBox.question(self, '提示:',
                                        '目标文件夹存在同名文件%s，是否覆盖？' % name + '\n源文件修改时间为：' + strmtime_source + '\n目标文件修改时间为：' + strmtime_destiation,
                                        QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes) == QMessageBox.Yes:
                    shutil.copyfile(source_file, destination_file)
                else:
                    continue
            else:
                shutil.copyfile(source_file, destination_file)

        # for i in range(self.node_startNo,1000):
        #     str1 = 'node' + str(self.node_startNo)
        #     while str1 in locals().keys():
        #         print(str1,'被占用')
        #         self.node_startNo += 1
        #         str1 = 'node' + str(self.node_startNo)



    @pyqtSlot()
    def on_label_source_tree_refresh_clicked(self):
        self.ui.treeWidget_source.getPath(self.source_dir_path)

    @pyqtSlot()
    def on_label_destination_tree_refresh_clicked(self):
        self.ui.treeWidget_destination.getPath(self.destination_dir_path)

    @pyqtSlot()
    def on_pushButton_copy_clicked(self):
        item_source = self.ui.treeWidget_source.topLevelItem(0)
        item_destination = self.ui.treeWidget_destination.topLevelItem(0)
        if item_source.checkState(0) == Qt.Unchecked:
            QMessageBox.information(self, '提示信息', '没有选中需要同步的目录或文件，请选择后重试！')
            return
        print(item_source.text(0))
        self.copy_file(item_source, item_destination)
        # self.ui.treeWidget_source.getPath(self.source_dir_path)
        # self.ui.treeWidget_destination.getPath(self.destination_dir_path)

    @pyqtSlot()
    def on_action_exit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_comboBox_source_folder_currentIndexChanged(self):
        self.source_dir_path = self.ui.comboBox_source_folder.currentText()
        self.ex_source = self.source_dir_path[0:self.source_dir_path.rfind(os.sep)] + os.sep
        if self.source_dir_path == '':
            return
        if not os.path.exists(self.source_dir_path):
            QMessageBox.information(self, '提示', '源文件夹输入的不是一个有效目录！')
            return
        self.ui.treeWidget_source.getPath(self.source_dir_path)
        self.ui.label_source_tree_refresh.setEnabled(True)

    @pyqtSlot()
    def on_comboBox_destination_folder_currentIndexChanged(self):
        self.destination_dir_path = self.ui.comboBox_destination_folder.currentText()
        self.ex_destination = self.destination_dir_path[0:self.destination_dir_path.rfind(os.sep)] + os.sep
        if self.destination_dir_path == '':
            return
        if not os.path.exists(self.destination_dir_path):
            QMessageBox.information(self,'提示','目标文件夹输入的不是一个有效目录！')
            return
        self.ui.treeWidget_destination.getPath(self.destination_dir_path)
        self.ui.label_destination_tree_refresh.setEnabled(True)
    @pyqtSlot()
    def on_action_set_source_dir_triggered(self):
        mytitle = '请选择需要复制的源文件夹：'
        mydir = '.'
        myfilter = '*.*'
        self.source_dir_path = QFileDialog.getExistingDirectory(None, mytitle, os.getcwd())
        self.ex_source = self.source_dir_path[0:self.source_dir_path.rfind(os.sep)] + os.sep
        if self.source_dir_path == '':
            return
        if self.source_dir_path == self.ui.comboBox_source_folder.currentText():
            return
        allitems = []
        for i in range(self.ui.comboBox_source_folder.count()):
            allitems.append(self.ui.comboBox_source_folder.itemText(i))
        if self.source_dir_path not in allitems:
            self.ui.comboBox_source_folder.addItem(self.source_dir_path)
            self.ui.comboBox_source_folder.setCurrentIndex(0)
            self.load_dir_to_file('s',self.source_dir_path)

        self.ui.treeWidget_source.getPath(self.source_dir_path)
        self.ui.label_source_tree_refresh.setEnabled(True)
        # self.ui.treeWidget_source.expandAll()

    @pyqtSlot()
    def on_action_set_destination_dir_triggered(self):
        mytitle = '请选择将要被复制到的目标文件夹：'
        mydir = '.'
        myfilter = '*.*'
        self.destination_dir_path = QFileDialog.getExistingDirectory(None, mytitle, os.getcwd())
        if self.destination_dir_path == self.ui.comboBox_destination_folder.currentText():
            return
        if self.destination_dir_path == '':
            return
        self.ex_destination = self.destination_dir_path[0:self.destination_dir_path.rfind(os.sep)] + os.sep
        allitems = []
        for i in range(self.ui.comboBox_destination_folder.count()):
            allitems.append(self.ui.comboBox_destination_folder.itemText(i))
        if self.destination_dir_path not in allitems:
            self.ui.comboBox_destination_folder.addItem(self.destination_dir_path)
            self.ui.comboBox_destination_folder.setCurrentIndex(0)
            self.load_dir_to_file('d',self.destination_dir_path)
        self.ui.treeWidget_destination.getPath(self.destination_dir_path)
        self.ui.label_destination_tree_refresh.setEnabled(True)
        # self.ui.treeWidget_destination.expandAll()

    def load_dir_to_file(self,sign,item):
        if sign == 's':
            filename = 'sourcedir'
        elif sign == 'd':
            filename = 'destdir'
        else:
            pass
        with open(filename,'a') as f:
            f.write(item +'\n')

    def get_dir_from_file(self,sign):
        if sign == 's':
            filename = 'sourcedir'
        elif sign == 'd':
            filename = 'destdir'
        else:
            pass
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                comment = f.read().strip()
                return comment.split('\n')
        else:
            return []

    def comboBox_item_down(self,combo):
        for i in range(combo.count(),-1,-1):
            combo.setItemText(i+1,combo.itemText(i))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_form)
    main_form.show()

    sys.exit(app.exec())
