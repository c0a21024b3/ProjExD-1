import sys              # sysモジュールを読み込む
import pygame as pg     # pygameモジュールをpgとして読み込む
from random import randint     # randomモジュール内にあるrandint関数を読み込む

bar_num = 5  # 落ちてくる障害物の最大数
rz_num = 10 # 弾数を1000で初期化
HP = 500 # HPを500で初期化

# 変数:横井
HP = 500     # 体力の設定
time = 0     # timeを0で初期化
score = 0    # scoreを0で初期化
point = 0    # pointを0で初期化

# メインの画面を生成するクラス
class Screen:
    def __init__(self, title, wh, image):   # wh:幅高さタプル, image:背景画像ファイル名
        pg.display.set_caption(title)       # タイトルバーにtitleを表示
        self.sfc = pg.display.set_mode(wh)      # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.bgi_sfc = pg.image.load(image)     # Surface
        self.bgi_rct = self.bgi_sfc.get_rect()  # Rect  

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


# 自身の操作するPlayerを生成するクラス
class Player:
    def __init__(self, image, size, xy):    # image:画像ファイル名, size:拡大率, xy:初期座標タプル
        self.sfc = pg.image.load(image)                        # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)    # Surface
        self.rct = self.sfc.get_rect()                         # Rect
        self.rct.center = xy    # こうかとんを表示する座標をxyに設定
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr: Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_LEFT]:
            self.rct.centerx -= 1.0
        if key_states[pg.K_RIGHT]:
            self.rct.centerx += 1.0
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_LEFT]:
                self.rct.centerx += 1.0
            if key_states[pg.K_RIGHT]:
                self.rct.centerx -= 1.0
        self.blit(scr)


# 上から落ちてくるバーを生成するクラス
class Bar:
    def __init__(self, size, color, scr: Screen):
        self.sfc = pg.Surface(size)
        pg.Surface.fill(self.sfc, color)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
        self.rct.centery = -randint(0, 500)
        self.w, self.h = size
        self.rct.width = randint(80, self.w)
        self.vy  = 1
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
        
    def update(self, scr: Screen):
        self.rct.move_ip(0, self.vy)
        if self.rct.centery > scr.rct.height:
            self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
            self.rct.centery = -randint(0, 500)
            self.rct.width = randint(80, self.w)
        scr.sfc.blit(self.sfc, self.rct)

# メダルを生成するクラス:安野
class Medal:
    def __init__(self, scr):
        self.sfc = pg.Surface((100, 100))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, (255, 255, 0), (50, 50), 50)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr, player):
        self.rct.move_ip(0, 1)
        if self.rct.centery > scr.rct.height:
            self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
            self.rct.centery = -randint(0, 500)
        result = self.check_hit(player, scr)
        self.blit(scr)
        return result

    # メダルがプレイやーかレーザーにぶつかったときにスコアを増やすように命令する
    def check_hit(self, player, scr):
        global point # 横井
        if self.rct.colliderect(player.rct):
            # if self.rct.colliderect(player.rct) or self.rct.colliderect("razerオブジェクト"):
            self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
            self.rct.centery = -randint(0, 500)
            point += 1 # 横井
        return 0


# ゲームに登場するItemを生成するクラス:岡田
class Item:
    def __init__(self, r, color, scr: Screen):
        self.sfc = pg.Surface((r*2, r*2))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (r, r), r)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width-self.rct.width)
        self.rct.centery = 0
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
        
    def update(self, scr: Screen):
        self.rct.move_ip(0, 1) # 速度1で落下
        scr.sfc.blit(self.sfc, self.rct)

# ものが障害物にぶつかったことを感知する関数
def check_bound(rct, scr_rct):
    
    # [1] rct: こうかとん or 爆弾のRect
    # [2] scr_rct: スクリーンのRect

    yoko, tate = 1, 1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right:
        yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom:
        tate = -1 # 領域外
    return yoko, tate


# ダメージの演出をする関数:横井
def Damage(surface, scale):
    GB = min(255, max(0, round(255 * (1-scale))))
    surface.fill((255, GB, GB), special_flags = pg.BLEND_MULT)

# BGMを再生する関数：山本
def sound():
    pg.mixer.init(frequency = 44100)    # 初期設定
    pg.mixer.music.load("fig/test.mp3") # 音楽ファイルの読み込み
    pg.mixer.music.play(1)              # 音楽の再生回数(1回)

def main():
    # グローバル変数:横井
    global HP, time, score
    # グローバル変数:岡田
    global rz_num, HP

    # BGMを再生する関数の呼び出し:山本
    sound() #sound関数の反映
    
    # 変数:岡田
    inv_point = 0 # 無敵ゲージを0で初期化
    inv = False   # 無敵かどうかの判定する変数
    st = 0        # 無敵の開始時刻を保存する変数

    clock = pg.time.Clock()                          # 時間計測用のオブジェクト
    screen = Screen("", (700, 900), "fig/pg_bg.jpg") # スクリーンクラスの生成
    screen.blit()                                    # スクリーンの生成

    player = Player("fig/5.png", 1.5, (350, 848))
    
    bars = [0 for i in range(bar_num)] # 落ちてくるバーの生成
    for i in range(bar_num):
        bars[i] = Bar((120, 30), (0,0,0), screen)
        bars[i].blit(screen)

    # メダルをクラスから生成する:安野
    medal = Medal(screen)
    medal.blit(screen)

    rz_plus = Item(10, (255, 0, 0), screen)
    rz_plus.rct.centerx = -30 # 弾数追加アイテムを画面外で初期化

    heal = Item(10, (0, 128, 0), screen)
    heal.rct.centerx = -30

    # 常にゲームを再生し続ける
    while True:
        screen.blit()

        # HP計算の処理:横井
        score = time*500+point*10000 # scoreの計算式
        if HP != 0: # HPが0ではない間
            time = int(pg.time.get_ticks()/1000) # 時間を計測する

        # 無敵ゲージの表示:岡田
        time = pg.time.get_ticks()
        font = pg.font.Font(None, 40)
        txt = font.render("x"*inv_point, True, (0, 0, 0)) # 
        screen.sfc.blit(txt, (0, 150))
        # 岡田/
        
        # プレイヤーを更新する
        player.update(screen)

        # バーを表示する
        for bar in bars:
            bar.update(screen)
        
            # 横井
            if player.rct.colliderect(bar.rct): # こうかとんがbarに当たっているとき
                Damage(screen.sfc, 0.5) # 画面を赤く変化させる
                HP -= 1 # HPが1ずつ減少
        
        # 横井
        if HP <= 0:
            HP = 0
            player = Player("fig/8.png", 1.5, (350, 390)) # 画面の真ん中にこうかとんを移動させ、固定する
            over_txt = font.render(("GAME OVER"), True, "BLACK") # GAME OVERテキストの設定
            screen.sfc.blit(over_txt, (170, 450)) # 画面の真ん中にGAME OVERを表示する
            bars.clear() # 全てのbarを削除
     
        font = pg.font.Font(None, 80) # fontの設定
        txt1 = font.render(str(f"Time:{(str(time))}"), True, "BLACK") # 経過時間表示テキストの設定
        screen.sfc.blit(txt1, (10, 10)) # txt1を表示

        txt2 = font.render(str(f"HP:{int(HP)}"), True, "BLACK") # HP表示テキストの設定
        screen.sfc.blit(txt2, (500, 10)) # txt2を表示

        txt3 = font.render(str(f"Score:{int(score)}"), True, "BLACK") # スコア表示テキストの設定
        screen.sfc.blit(txt3, (10, 80)) # txt3を表示
        # 横井ここまで

        # 岡田
        if 0 <= time % 25000 <= 20: # 25秒おき
            rz_plus = Item(10, (255, 0, 0), screen) # 画面内に弾数追加アイテムを生成
            for bar in bars: # 障害物と被らないように
                while rz_plus.rct.colliderect(bar.rct):
                    rz_plus = Item(10, (255, 0, 0), screen)
        rz_plus.update(screen)

        if player.rct.colliderect(rz_plus.rct): # 弾数追加の処理
            rz_num += 3
            rz_plus.rct.centerx = -30
        
        if 0 <= time %40000 <= 20: # 40秒おき
            heal = Item(10, (0, 128, 0), screen) # 画面内に体力回復アイテムを生成
            for bar in bars: # 障害物と被らないように
                while heal.rct.colliderect(bar.rct):
                    heal = Item(10, (0, 128, 0), screen)
        heal.update(screen)

        if player.rct.colliderect(heal.rct): # 体力回復の処理
            HP += 100
            heal.rct.centerx = -30
        # 岡田/

        # メダルを更新する:安野
        result = medal.update(screen, player)
        # 画面のばつボタンをクリックしたときに終了する
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
                
        # 岡田
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT and inv_point == 10:
                    inv_point = 0
                    inv = True
                    st = time # 無敵の開始時刻を保存
        if time - st > 5000: # 無敵は5秒継続
            inv = False
        
        # スコアの計算:横井
        score += result*10000
        
        pg.display.update()   # 画面を更新する
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
