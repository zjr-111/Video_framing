# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import cv2
import os
# copy a file using shutil.copyfile() method
import shutil

# 定义计算时间的函数
def time_show(sum_zhen,speed_zhen):
    s = int(sum_zhen / speed_zhen)
    h = int(s // 3600)
    min = int((s - (h * 3600)) // 60)
    s = int(s - (h * 3600) - (min * 60))
    return h,min,s

# 定义记事本的保存和读取函数
def save_text(text):
    with open('saved_text.txt', 'w' , encoding='utf-8') as file:
        file.write(text)

def load_text():
    with open('saved_text.txt', 'r' , encoding='utf-8') as file:
        text = file.read()
    return text

# 检查记事本是否已经存在，如不在则创建
path_obs = os.path.dirname(os.path.abspath(__file__))
path_txt = path_obs + '\\'+'saved_text.txt'
obs_result = os.path.exists(path_txt)
if obs_result == False:
    input_text = ''
    save_text(input_text)

def cap_set(src :str, target :str, frame_num :int, interval :int):
    """1.视频列表"""
    paths = os.listdir(src)
    # print(paths)
    """2. 创建窗口"""
    # 创建窗口用于展示抽帧结果
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("result", (1920, 1080))

    """3. 创建文件保存路径"""
    # 创建存储抽针结果的文件夹
    if not os.path.exists(target):
        os.mkdir(target)

    """4. 设置要跳转到的帧数"""
    group = 1
    # 自动快进状态
    auto_forward = False
    img_count = 0  # 标识图片的顺序
    begin = 0
    end = 0
    after_vidio = False
    interval = interval * frame_num
    # 记录当前视频所在的列表序号
    i = 0

    while (i < len(paths)):

        # 记录当前所在帧数
        if after_vidio == True:
            loaded_text = load_text()
            loaded_text_part = loaded_text.split('#')
            tip_temp = int(loaded_text_part[1])
            after_vidio = False
        else:
            tip_temp = 0

        # 打开的视频的路径
        mingzi = paths[i]
        path = a + "\\" + mingzi

        # 打开视频
        cap = cv2.VideoCapture(path)

        # 检查视频是否成功打开
        if not cap.isOpened():
            fail_path = target + "fail/" + src.split("/")[-1]
            os.mkdir(os.path.join(target, "fail"))
            shutil.copyfile(src, os.path.join(fail_path, fail_path))
            print("读取失败:", src)

        is_open = cap.isOpened()
        cap_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while (is_open and tip_temp < cap_len):
            # 跳转到指定帧数并读取
            cap.set(cv2.CAP_PROP_POS_FRAMES, tip_temp)
            ret, frame = cap.read()

            # 打开后显示图片并等待键盘输入
            if ret:
                cv2.imshow('result', frame)
                key = cv2.waitKey(1)

                # 快进
                if key == ord('d'):
                    if tip_temp >= (cap_len - interval):
                        continue
                    tip_temp += interval  # 跳转指定帧数
                    # print("快进")

                # 自动快进： 第一次点击为自动快进。再次点击为退出自动快进
                elif key == ord('r'):
                    auto_forward = not auto_forward

                # 后退
                elif key == ord('e'):
                    if tip_temp == 0:
                        # print("已到达最最开始位置")
                        continue
                    tip_temp -= interval
                    # print("后退", frame_num, "帧")

                # 后退num帧
                elif key == ord('a'):
                    if tip_temp == 0:
                        continue
                    tip_temp -= frame_num

                # 前进num帧
                elif key == ord('f'):
                    if tip_temp >= (cap_len - frame_num):
                        continue
                    tip_temp += frame_num

                # 开始位置
                elif key == ord('b'):
                    begin = tip_temp

                # 结束位置- ed都用了所以就用n吧
                elif key == ord('n'):
                    end = tip_temp

                # 对指定范围内视频进行抽帧
                elif key == ord('s'):
                    while begin <= end:
                        # 跳转到指定帧数并读取
                        cap.set(cv2.CAP_PROP_POS_FRAMES, begin)
                        ret, frame = cap.read()
                        mingzi_half = mingzi.split('.')
                        if ret:
                            cv2.imwrite(target +'\\'+ str(mingzi_half[0]) + "_%d_group%d.jpg" % (img_count, group),
                                        cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA))
                            img_count += 1

                            # 跳转到下一节点
                            begin += frame_num
                        else:
                            begin += frame_num
                    group += 1
                    # 跳过指定位置
                elif key == ord('t'):
                    skip_time = str(input("请输入一个时间(00:00:00)："))
                    time_list = skip_time.split(":")
                    int_time_list = []
                    for t in time_list:
                        if (t[0] == "0"):
                            int_time_list.append(int(t[1]))
                        else:
                            int_time_list.append(int(t))
                    second = (int_time_list[0] * 3600) + (int_time_list[1] * 60) + int_time_list[2]
                    if second * cap.get(5) >= cap_len:
                        # 超出范围定位到最后
                        tip_temp = cap_len - frame_num
                        continue
                    tip_temp = int(second * cap.get(5))
                    # tip_temp = find_max_multiple(frame_num, second * 15)
                # 结束运行
                elif key == ord('q'):
                    input_text = str(i) +'#'+ str(tip_temp)
                    save_text(input_text)
                    sys.exit(0)
                # 下一个视频
                elif key == ord('z'):
                    vidio_index = paths.index(mingzi)
                    if(vidio_index < len(paths)-1):
                       i = vidio_index+1
                       break
                    continue
                # 上一个视频
                elif key == ord('x'):
                    if i<=0:
                       continue
                    i = paths.index(mingzi) - 1
                    break
                # 显示当前视频信息并跳转到固定视频
                elif key == ord('c'):
                    print('文件夹内的视频都有')
                    xu = 1
                    for ele in paths:
                        print(str(xu) + '.' + ele)
                        xu += 1
                    print('您当前所在的视频是'+str(mingzi)+'位于第'+str(paths.index(mingzi)+1))
                    h,min,s = time_show(cap_len,cap.get(5))
                    print('当前视频时长为'+str(h)+'时'+str(min)+'分'+str(s)+'秒')
                    h, min, s = time_show(tip_temp,cap.get(5))
                    print('当前视频已经观看了' + str(h) + '时' + str(min) + '分'+ str(s)+'秒')
                    redisue = cap_len - tip_temp
                    h,min,s = time_show(redisue,cap.get(5))
                    print('当前视频剩余时长为' + str(h) + '时' + str(min) + '分')
                    print('')
                    tj = input('是否跳转视频Y/N\n')
                    if tj == 'y':
                        i = input('输入你想观看的视频所在的排序\n')
                        i = int(i) - 1
                        break
                    else:
                        continue
                        # 跳转到上一次的进度
                elif key == ord('T'):
                    loaded_text = load_text()
                    loaded_text_part = loaded_text.split('#')
                    if loaded_text == '':
                        print('您当前还没有记录')
                        continue
                    else:
                        i = int(loaded_text_part[0])
                        after_vidio = True
                        break
                '''
                # 记事本
                elif key == ord('p'):
                    # input_text = input('输入你要保存的内容')
                    input_text = str(i)+'#'+str(tip_temp)
                    save_text(input_text)
                    print("信息已保存！")
                    continue
                '''



                # 在没有任何键盘输入时判断是否是自动快进操作
                if auto_forward:
                    if tip_temp >= (cap_len - interval):
                        auto_forward = not auto_forward
                        continue
                    tip_temp += interval
        cap.release()
    cv2.destroyAllWindows()

print("操作方式：\nr自动播放/停止\ne后退\na逐帧后退\nd前进\nf逐帧前进\nb标记抽帧的初始位置\nn标记抽帧的结束位置\ns保存截取的视频\nt在终端里输入跳过的时间段\nT跳转到上一次观看的位置\nq退出\nz下一个视频\nx上一个视频\nc查看视频信息，并决定是否跳转别的视频\np记录信息")

#a = input("视频文件地址*该文件夹仅存在视频*\n")
#a = str(a)
a = 'F:\project\\vidios'
#b = input("保存图片地址\n")
#b = str(b)
b = 'F:\project\D01_20230525\\picture'
c = 7
c = int(c)
d = 6
d = int(d)
cap_set(a,b,c,d)

# if __name__ == '__main__':
#     cap_set("F:\project\D02_20230502090939.mp4", "F:\project\\now\\result", 7, 6)