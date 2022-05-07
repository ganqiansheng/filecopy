import os


def formatTime(atime):
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(atime))


fileinfo = os.stat("filemanager.py")
print("最后一次访问时间:", formatTime(fileinfo.st_atime))
print("最后一次修改时间:", formatTime(fileinfo.st_mtime))
print("最后一次状态变化的时间：", formatTime(fileinfo.st_ctime))
print("索引号：", fileinfo.st_ino)
print("被连接数目：", fileinfo.st_dev)
print("文件大小:", fileinfo.st_size, "字节")
print("最后一次访问时间:", fileinfo.st_atime)
print("最后一次修改时间:", fileinfo.st_mtime)
print("最后一次状态变化的时间：", formatTime(fileinfo.st_ctime))