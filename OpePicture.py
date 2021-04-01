import os,shutil
from PIL import Image
import os
import os.path
from tqdm import tqdm
import shutil
from PIL import Image




class OpePicture():
    """判断两个文件夹有无相同文件：根据文件名判断"""
    def __init__(self,path=0,path1=1,path2=2,name=3):
        self.path=path
        self.path1=path1
        self.path2=path2
        self.name=name # 没啥用，不知道怎么用

    def fileList(self,path):
        filelist = {}
        n = 1
        for root, folders, files in os.walk(path):
            # 地址，里面的目录名，所有文件名
            for file in files:
                n += 1
                filelist[file] = os.path.join(root, file)
        # print('\n')
        return filelist

    def compare(self):
        dict1 = OpePicture.fileList(self,path=path1)
        dict2 = OpePicture.fileList(self,path=path2)
        f = open("same.txt", "w", encoding="utf-8")
        for key in dict1:
            if key in dict2:
                f.write(dict1[key])
                f.write("\n")
        f.close()
        print("Done.")

    '''
    批量重命名文件夹中的图片文件
    '''
    def rename(self):
        i = 1
        ls = ['.JPG', ".PNG", ".JPG", ".gif", ".webp", ".png", ".jpg", ".JPEG", ".jpeg"]

        for j in ls:
            g = 1
            print(path)
            for root, folders, files in os.walk(path):

                for file in files:

                        # 判断是否有指定的后缀
                    if file.endswith(j) and file in files:
                        src = os.path.join(os.path.abspath(root), file)
                        # 下面是新名字
                        dst = os.path.join(os.path.abspath(root), name + str(i) + j.lower())
                        # 原名,新名
                        os.rename(src, dst)
                        i = i + 1
                        g += 1
                    else:
                        continue
            print("{}类型的有张{}".format(j, g))
        print("一共有{}图片".format(i))

    '''
    记住转移之前要先重命名
    一般用来把不同子目录下的的文件全部放入一个文件里
    '''

    def fileList2(input_dir, save):
        filelist = {}
        i = 1
        for root, folders, files in os.walk(input_dir):
            # 地址，里面的目录名，所有文件名(不包括子目录)
            for file in files:
                print(i)
                shutil.move(os.path.join(root, file), save + "\\" + file)
                i += 1

    def move_file(self):

        save = path + "\集合"
        if not os.path.exists(save):
            os.makedirs(save)
        OpePicture.fileList2(path, save)

    ####====第四个功能====
    # 函数查找指定路径中所有文件的路径
    # 函数查找指定路径中所有文件的路径
    def get_file(self,path):
        list1 = []  # 用于存储递归查找到的所有文件,传递给函数
        fileList = os.listdir(path)  # 获取path目录下所有文件
        for filename in fileList:
            pathTmp = os.path.join(path, filename)  # 获取path与filename组合后的路径
            if os.path.isdir(pathTmp):  # 如果是目录
                a = OpePicture.get_file(self,pathTmp)  # 则递归查找(注意一定要有接受变量,不然就出错了)
                for i in a:
                    list1.append(i)
            else:
                list1.append(pathTmp)
        return list1

    # ---------------------修改处1,修改原始文件位置------------------------------------



    # 筛选后缀函数,传入包含所有后缀名的列表,以及需要筛选的后缀(默认筛选txt文件)
    def shai_xuan_hou_zhui(self, file_path_list):
        list2 = []  # 用于储存筛选好的文件的路径
        for filepath in file_path_list:
            ls = ['.JPG', ".PNG", ".JPG", ".gif", ".png", ".jpg", ".webp"]
            for i in ls:
                if os.path.splitext(filepath)[1] == i:
                    list2.append(filepath)

        return list2

    # ----------------------修改2，修改文件后缀，(可完善）------------------------------------
    def split(self):

        file_path_list = OpePicture.get_file(self,path=path)
        pig_list = OpePicture.shai_xuan_hou_zhui(self,file_path_list=file_path_list)  # 筛选jpg格式文件

        # -----------------------修改处3，修改图片存储路径-------------------------------
        folder1 = path + '\横屏'  # 存放横屏图片的地址
        folder2 = path + '\竖屏'  # 存放竖屏图片的地址

        if not os.path.exists(folder1):
            os.makedirs(folder1)
        if not os.path.exists(folder2):
            os.makedirs(folder2)

        for i in tqdm(range(len(pig_list))):
            lujing = pig_list[i]
            try:
                picture = Image.open(lujing)
                width = picture.width
                height = picture.height
                picture.close()
                if width < height:
                    shutil.move(lujing, folder2)
                else:
                    shutil.move(lujing, folder1)
            except:
                continue

        print('over,over,over!')

    """判断两个文件夹有无相同文件：根据文件名判断"""
    "文件比较多的时候，很容易出现相同大小但实际图片不同"
    """所以运行完，自己可以按大小排列，去看看有没有差别"""

    def compare_filesize(self,path1, file_same_size):
        file_dict = {}
        n = 0
        for root, folders, files in os.walk(path1):
            # 缺点是会不断的更新path
            # 根目录地址，里面的目录名，所有文件名

            for file in files:

                path2 = os.path.join(root, file)
                if os.path.getsize(os.path.join(root, file)) in list(file_dict.values()):
                    if os.path.exists(root + "\\" + list(file_dict.keys())[
                        list(file_dict.values()).index(os.path.getsize(path2))]):
                        shutil.move(root + "\\" + list(file_dict.keys())[
                            list(file_dict.values()).index(os.path.getsize(path2))], file_same_size)
                    shutil.move(os.path.join(root, file), file_same_size)
                    n += 1
                else:
                    file_dict[file] = os.path.getsize(path2)
        print("一共有{}张相同大小的文件".format(n))
        return file_dict

    def output(self,path):

        file_same_size = "相同的文件"
        path1 = path
        if not os.path.exists(file_same_size):
            os.makedirs(file_same_size)
        OpePicture.compare_filesize(self,path1=path1, file_same_size=file_same_size)
        print("Done.")

    """删除内存大小、分辨率相同的文件，虽然加了层保险，但还是要自己
    检查一下，比较保险"""
    def delete(self,path):

        file_dict = {}
        n = 0
        for root, folders, files in os.walk(path):
            # 缺点是会不断的更新path
            # 根目录地址，里面的目录名，所有文件名

            for file in files:

                path2 = os.path.join(root, file)
                if os.path.getsize(os.path.join(root, file)) in list(file_dict.values()):

                    try:
                        picture1 = Image.open(os.path.join(root, file))
                        width1 = picture1.width
                        height1 = picture1.height
                        picture1.close()

                        picture2 = Image.open(root + "\\" + list(file_dict.keys())[list(file_dict.values()).index(os.path.getsize(path2))])
                        width2 = picture2.width
                        height2 = picture2.height
                        picture2.close()
                        if width1==width2 and height1==height2:
                            os.remove(os.path.join(root, file))
                            n += 1
                    except:
                        continue

                else:
                    file_dict[file] = os.path.getsize(path2)
            print("一共有删除了{}张大小相同的文件".format(n))
        return file_dict


if __name__ == '__main__':
    dict = {"1": "compare()", "2": "rename()", "3": "get_file()", "4": "split()", "5": "output()", "6": "delete()"}
    print("请选择你想要使用的功能：")
    print("1：1的功能是根据文件名字进行判断文件是否相同")
    print("2：2的功能是把图片的名字全部更换为指定前缀名")
    print("3：3的功能是把目录里的所以图片都移动到一个文件夹里（做之前要先把整个文件夹名字都重命名一遍不然会报错）")
    print("4：4的功能是把横竖屏的图片分开到两个不同的文件夹存放")
    print("5：5的功能是把相同的文件放到一个文件夹里去")
    print("6：6的功能是把所有相同的文件都删掉")
    o = OpePicture()

    while True:
        k = input("请输入你要选择的功能（例如1）：")
        if k=="1":
            path1 = input("需要对比的文件1（绝对路径）：")
            path2 = input("需要对比的文件2（绝对路径）：")
            o.compare()
            break
        elif k=="2":
            path = input("需要重命名的文件（绝对路径）：")
            name = input("请输入名字的前缀（壁纸--）：")
            o.rename()
            break
        elif k=="3":
            path = input("需要移动的文件（绝对路径）：")
            o.move_file()
            break
        elif k=="4":
            path = input("要分开的文件的目录（绝对路径）：")
            o.split()
            break
        elif k=="5":
            path = input("需要对比文件大小的文件夹：")
            o.output(path=path)
            break
        elif k=="6":
            path = input("要删除的图片路径：")
            o.delete(path=path)
            break
        else:
            print("请重新输入（例如1）")
            continue

