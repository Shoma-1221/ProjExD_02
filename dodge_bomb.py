import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(rect:pg.Rect) -> tuple[bool, bool]:
    yoko, tate =True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate

def kk_k():
    #演習1の関数
    kk_img0 = pg.transform.rotozoom(pg.image.load("ex02/fig/3.png"), 0, 2.0)
    #左を向いているこうかとんのロード
    kk_img1 = pg.transform.flip(kk_img0, True, False)
    #右を向いているこうかとんの作成
    return{(0, 0):kk_img0, 
           (-5, 0):kk_img0,
           (-5, -5):pg.transform.rotozoom(kk_img0, -45, 1.0),
           (-5, +5):pg.transform.rotozoom(kk_img0, 45, 1.0),
           (0, -5):pg.transform.rotozoom(kk_img1, 90, 1.0),
           (+5, -5):pg.transform.rotozoom(kk_img1, 45, 1.0),
           (+5, 0):pg.transform.rotozoom(kk_img1, 0, 1.0),
           (+5, +5):pg.transform.rotozoom(kk_img1, -45, 1.0),
           (0, +5):pg.transform.rotozoom(kk_img1, -90, 1.0)
           }  #こうかとんが進む方向を向くこうかとんの画像のリスト



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_imgs = kk_k()  #こうかとんの角度のリストの関数との連携
    kk_img = kk_imgs[(0,0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))  #練習1
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bd_rct = bd_img.get_rect()
    bd_rct.center = x, y
    vx, vy = +5, +5  #練習2  
    clock = pg.time.Clock()
    tmr = 0
   
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバー")
            return  #こうかとんと爆弾がぶつかったらゲームオーバーと表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #こうかとんが画面端で止まる
        kk_img = kk_imgs[tuple(sum_mv)]  #こうかとんの進行方向に方向転換
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *=-1  #画面端に行ったときに反転
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()