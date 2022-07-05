import random
import pygame as pg
import sys

def main():
    clock = pg.time.Clock()

    pg.display.set_caption("逃げ！こうかとん")
    screen_sfc = pg.display.set_mode((1600, 900))
    screen_rct = screen_sfc.get_rect()

    # 背景の表示
    bgimg_sfc = pg.image.load("fig/pg_bg.jpg")
    bgimg_rct = bgimg_sfc.get_rect()
    screen_sfc.blit(bgimg_sfc, bgimg_rct)

    # こうかとん
    kkimg_sfc = pg.image.load("fig/6.png")
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0)
    kkimg_rct = kkimg_sfc.get_rect()
    kkimg_rct.center = 500, 300
    kkimg_sfc.blit(kkimg_sfc, kkimg_rct)

    # 爆弾
    bom_sfc = pg.Surface((20, 20))
    bom_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_sfc, (255, 0, 0), (10, 10), 10)
    bom_rct = bom_sfc.get_rect()
    bom_rct.centerx = random.randint(0, screen_rct.width)
    bom_rct.centery = random.randint(0, screen_rct.height)
    vx, vy = +1, +1

    while True:
        screen_sfc.blit(bgimg_sfc, bgimg_rct)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 

        # キーによってこうかとんを移動させる
        key_status = pg.key.get_pressed()

        if key_status[pg.K_UP]    == True: kkimg_rct.centery -= 1
        if key_status[pg.K_DOWN]  == True: kkimg_rct.centery += 1
        if key_status[pg.K_LEFT]  == True: kkimg_rct.centerx -= 1
        if key_status[pg.K_RIGHT] == True: kkimg_rct.centerx += 1
        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        # 爆弾を移動させる
        bom_rct.move_ip(vx, vy)

        # 爆弾を生成する
        screen_sfc.blit(bom_sfc, bom_rct)

        pg.display.update()
        clock.tick(1000)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()