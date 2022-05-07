from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os,sys

from filemanager  import *


class Solution:
    def isSameTree(self, p, q):
        if p == None and q == None:
            return True
        # 前提条件是两个节点不同时为空 一个为空，一个非空，显然不同
        if p == None or q == None:
            return False
        # 中间发现值不相等，也不为空
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

def btnsource_clicked():
    pathdir = QFileDialog.getExistingDirectory(main,'请选择路径','')
    t1.getPath(pathdir)

def btndest_clicked():
    pathdir = QFileDialog.getExistingDirectory(main,'请选择路径','')
    t2.getPath(pathdir)

def btncompare_clicked(main,t1,t2):
    if t1.currentItem() == '':
        return
    item1 = t1.currentItem()
    print(Solution.isSameTree(main,item1,t2))

    if t2.currentItem() == '':
        return
    item2 = t2.currentItem()
    print(Solution.isSameTree(main,item1,item2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main =QWidget()
    main.resize(1000,600)
    t1 = FileManager()
    t1.setColumnCount(2)
    t1.setHeaderLabels(['文件名','修改日期'])
    t1.setColumnWidth(0,200)
    # path1 = ''
    # t1.getPath(path1)
    t2 = FileManager()
    t2.setColumnCount(2)
    t2.setHeaderLabels(['文件名','修改日期'])
    t2.setColumnWidth(0,200)
    # path2 = ''
    # t2.getPath(path2)
    layouttree = QHBoxLayout()
    layouttree.addWidget(t1)
    layouttree.addWidget(t2)

    btnsource  = QPushButton('源')
    btnsource.clicked.connect(btnsource_clicked)
    btndest = QPushButton('目标')
    btndest.clicked.connect(btndest_clicked)
    btncompare = QPushButton('比较')
    btncompare.clicked.connect(lambda :btncompare_clicked(main,t1,t2))

    layoutbtn =QHBoxLayout()
    layoutbtn.setStretch(0,1)
    layoutbtn.addWidget(btnsource)
    layoutbtn.addWidget(btndest)
    layoutbtn.addWidget(btncompare)
    layoutbtn.setStretch(2,0)

    layout = QVBoxLayout()
    layout.addLayout(layouttree)
    layout.addLayout(layoutbtn)

    main.setLayout(layout)

    # solution = Solution()


    main.show()
    sys.exit(app.exec())
