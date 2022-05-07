import pygame
import os

TIMER_EVENT= pygame.USEREVENT + 2  # 定时器事件

#游戏刷新帧率，每秒40次
FRAME_PER_SEC = 40
SCREEN_RECT = pygame.Rect(0, 0, 1000, 700)
FULLSCREEN = -2147483648

image1_path="./pic/linzhilin.png"
image2_path="./pic/linxilei.png"
image3_path="./pic/liudehua.png"
image4_path="./pic/zhguorong.png"
image1 = pygame.image.load(image1_path)
image2 = pygame.image.load(image2_path)
image3 = pygame.image.load(image3_path)
image4 = pygame.image.load(image4_path)
#将图片统一变为展示大小
image1 = pygame.transform.smoothscale(image1, (500, 500))
image2 = pygame.transform.smoothscale(image2, (500, 500))
image3 = pygame.transform.smoothscale(image3, (500, 500))
image4 = pygame.transform.smoothscale(image4, (500, 500))

def event_handler(screen):

    for event in pygame.event.get():
        # 判断是否退出游戏
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(0)
        if event.type == pygame.KEYDOWN: #按键按下事件
            key_pressed = pygame.key.get_pressed()
            print(event.type)
            print(key_pressed[pygame.K_ESCAPE])
            print(key_pressed[pygame.K_DOWN])
            print(key_pressed[pygame.K_UP])
            print(key_pressed[pygame.K_LEFT])
            print(key_pressed[pygame.K_RIGHT])
            # ESC键退出游戏
            if key_pressed[pygame.K_ESCAPE] == 1:
                pygame.quit()
                os._exit(0)  #这个注释会报错

            elif key_pressed[pygame.K_DOWN] == 1 :
                # 左键弹出图片1，右键弹出图片2，上键弹出图片3，下键弹出图片4
                screen.blit(image4,(0, 0))
            elif key_pressed[pygame.K_UP] == 1 :
                screen.blit(image1, (0, 0))
            elif key_pressed[pygame.K_LEFT] == 1 :
                screen.blit(image2, (0, 0))
            elif key_pressed[pygame.K_RIGHT] == 1 :
                screen.blit(image3, (0, 0))
        elif event.type == pygame.MOUSEBUTTONDOWN: #鼠标点击事件
            #do somethin
            pass

if __name__ == '__main__':
    pygame.init()
    #获取屏幕大小分辨率？
    info = pygame.display.Info()
    SCREEN_RECT.size = (info.current_w, info.current_h)
    print(SCREEN_RECT.size)
    screen = pygame.display.set_mode(SCREEN_RECT.size , FULLSCREEN)  #全屏显示

    #定时器，暂时用不到
    clock = pygame.time.Clock()
    pygame.time.set_timer(TIMER_EVENT, 500)

    while True:
        # 1.设置刷新帧率
        clock.tick(FRAME_PER_SEC)

        # 2.事件监听 (用户事件，按钮事件，鼠标事件)
        event_handler(screen)

        # 3.pygame更新显示，这两个函数不知道有啥区别
        pygame.display.update()
        #pygame.display.flip()
