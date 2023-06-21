import turtle
import math
import random
import time


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Break the UFO")
wn.tracer(60) 
wn.setup(500, 600)

wn.bgpic("Space.png")

pen = turtle.Turtle()
pen.speed(10)
pen.hideturtle()



# 모양들
shapes = ["wing.gif", "bullet.gif", "ufo.gif","dis_ufo.gif", "lazer.gif"]

for shape in shapes:
    wn.register_shape(shape)

class Sprite():

    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

#UFO 클래스 생성
class UFO(Sprite):  # UFO 클래스를 Sprite 클래스를 상속받도록 변경합니다.
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)  # 상위 클래스 생성자 호출


#스프라이트 객체 생성
wing = Sprite(0, -180, 52, 50, "wing.gif") #비행선
bullet = Sprite(1000, 1000, 10, 20, "bullet.gif") #총알
ufo = Sprite(1000, 1000, 50, 50, "ufo.gif") #ufo
dis_ufo = Sprite(1000, 1000, 70, 70, "dis_ufo.gif") #파괴된 ufo
lazer = Sprite(1000, 1000 , 30, 100, "lazer.gif") #운석

#스프라이트 모음 리스트
sprites = [wing, bullet, ufo, dis_ufo, lazer]

#ufo들이 들어갈 리스트
ufos = []

#비행선 이동
def wing_move_left():
    if wing.x > -164:   #왼쪽이동
        wing.x -= 12
    else:   #맵밖으로 나갈시 반대편으로 이동
        x = wing.x
        y = wing.y
        wing.x = -x+50
        wing.y = y

def wing_move_right():
    if wing.x < 164:    #오른쪽이동
        wing.x += 12
    else:   #맵밖으로 나갈시 반대편으로 이동
        x = wing.x
        y = wing.y
        wing.x = -(x+50)
        wing.y = y

def wing_move_up():
    if wing.y < 275:
        wing.y += 7

def wing_move_down():
    if wing.y > -260:
        wing.y -= 7

def fire_bullet():
    bullet.x = wing.x  # 총알을 비행선의 현재 위치로 설정
    bullet.y = wing.y + wing.height/2  # 총알을 비행선의 위쪽으로 설정

#총알 발사
def shoot_bullet():
    fire_bullet()
    wn.ontimer(shoot_bullet, 500)  # 0.5 초마다 shoot_bullet 함수를 호출

def fire_lazer(): # 처음 적의 공격
    lazer.x = random.randint(-180, 180)
    lazer.y = 2000


for _ in range(5):  # 5개의 UFO 생성 (원하는 개수로 수정 가능)
    ufo_x = random.randint(-180, 180)  # X 좌표를 -250에서 250 범위에서 랜덤하게 선택
    ufo_y = 350    # Y 좌표를 50에서 200 범위에서 랜덤하게 선택
    ufo = UFO(ufo_x, ufo_y, 50, 50, "ufo.gif")
    ufos.append(ufo)
    sprites.append(ufo)  # UFO 객체를 스프라이트 모음 리스트에 추가합니다.

# 이벤트 처리
wn.listen()
wn.onkeypress(wing_move_left, "Left")
wn.onkeypress(wing_move_right, "Right")
wn.onkeypress(wing_move_up, "Up")
wn.onkeypress(wing_move_down, "Down")


shoot_bullet()
fire_lazer()

#총알에 맞은 ufo
collided_ufos = []

#맞춘 ufo 스코어
hit_score = 0

# 게임 시간 설정 (초 단위)
game_duration = 30
start_time = time.time()  # 게임 시작 시간 기록

#타이머 그리기
timer_pen = turtle.Turtle()
timer_pen.speed(0)
timer_pen.color("white")
timer_pen.penup()
timer_pen.hideturtle()
timer_pen.goto(-230, 260)  # 왼쪽 상단 위치



while time.time() - start_time <= game_duration:  #게임 시간 설정
    pen.clear() # 스프라이트 이동흔적 삭제
    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)

    bullet.y += 1
    lazer.y -= 0.3

    #적의 운석 
    if lazer.y < -500:
        lazer.y = 1000
        lazer.x = wing.x + random.randint(-50,50)
    
    #적 등장
    for ufo in ufos:
        if ufo.y > 50:
            ufo.y -= 0.1

    for ufo in ufos:
        if bullet.is_aabb_collision(ufo):
            collided_ufos.append(ufo)  # 충돌한 ufo를 리스트에 추가
            bullet.x = 1000  # 미사일을 화면 밖으로 이동하여 사라지게 함
            hit_score += 310 # ufo당 점수
            dis_ufo.x = ufo.x
            dis_ufo.y = ufo.y

    # 충돌한 ufo 이동
    for ufo in collided_ufos:
        ufo.y = 600
        ufo.x = random.randint(-180, 180)
        collided_ufos.remove(ufo) 

    if wing.is_aabb_collision(lazer):
        start_time -= game_duration

    # 타이머 업데이트
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, game_duration - elapsed_time)
    timer_pen.clear()
    timer_pen.write(f"Time: {remaining_time}", align="left", font=("Courier", 20, "normal"))




    
    
    wn.update()
pen.clear()
result_pen = turtle.Turtle()
result_pen.speed(0)
result_pen.color("white")
result_pen.penup()
result_pen.hideturtle()
result_pen.goto(0, 0)
result_pen.write(f"Score: {hit_score}", align="center", font=("Courier", 20, "normal"))


wn.mainloop
turtle.done()