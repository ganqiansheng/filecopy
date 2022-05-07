#!/usr/bin/env python
"""
##############################################################################
用法：./dirdiff.py dir1 dir2
比较两个目录，找出只在其中一个目录中出现的文件。
这个版本使用os.listdir并把差异汇入列表。请注意这个脚本只检查文件名而不涉及文件内容。关于后者
的比较请参考diffall.py，它通过比较.read()结果来实现这方面的拓展。
##############################################################################
"""

import os
import sys


def reportdiffs(unique1, unique2, dir1, dir2):
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


def diff(seq1, seq2):
    """
    仅返回seq1的独有文件；
    也可以使用set(seq1) - set(seq2)，不过集合内的顺序是随机的，
    所以会导致丢失具有平台依赖性的目录顺序。
    """
    return [item for item in seq1 if item not in seq2]


def comparedirs(dir1, dir2, files1=None, files2=None):
    """
    比较目录内容而非文件实际内容，可能需要listdir的bytes参数来处理
    某些系统平台上不可解码的文件名。
    """
    print('''正在比较目录
            {}
        和
            {}
            下的文件列表'''.format(dir1, dir2))
    files1 = os.listdir(dir1) if files1 is None else files1
    files2 = os.listdir(dir2) if files2 is None else files2
    unique1 = diff(files1, files2)
    unique2 = diff(files2, files1)
    reportdiffs(unique1, unique2, dir1, dir2)
    return unique1, unique2


def getargs():
    if len(sys.argv) != 3:
        print('用法：./dirdiff.py dir1 dir2')
        sys.exit()
    else:
        return sys.argv[1:]


def command():
    dir1, dir2 = getargs()
    comparedirs(dir1, dir2)


if __name__ == '__main__':
    command()
