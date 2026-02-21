import turtle
import time
import random
import winsound

delay = 0.08

# score
score = 0
high_score = 0

# ---------------- THEMES (MUST BE BEFORE FUNCTIONS) ----------------
snake_themes = [
    {"head": "white", "body": "green"},
    {"head": "yellow", "body": "orange"},
    {"head": "cyan", "body": "blue"},
    {"head": "pink", "body": "purple"},
    {"head": "lime", "body": "darkgreen"},
]
current_theme_index = 0


# ---------------- HELPER FUNCTIONS (MUST BE BEFORE HEAD) ----------------
def get_head_color():
    return snake_themes[current_theme_index]["head"]

def get_body_color():
    return snake_themes[current_theme_index]["body"]


# ---------------- SCREEN SETUP ----------------
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("#0f172a")
wn.setup(width=600, height=600)
wn.tracer(0)


# ---------------- SNAKE HEAD ----------------
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color(get_head_color())
head.penup()
head.goto(0, 0)
head.direction = "stop"
head.shapesize(1.2, 1.2)  # optional: bigger head

# ---------------- FOOD ----------------
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# ---------------- SCORE PEN ----------------
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0 High Score = 0", align="center", font=("Courier", 24, "normal"))


# ================= FUNCTIONS =================

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"


# ✅ FIXED movement
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)


# game over melody
def game_over_sound():
    melody = [
        (800, 120),
        (600, 120),
        (500, 120),
        (400, 200),
        (300, 300),
    ]
    for freq, dur in melody:
        winsound.Beep(freq, dur)


# change snake theme
def change_snake_color():
    global current_theme_index
    current_theme_index = (current_theme_index + 1) % len(snake_themes)

    # update head
    head.color(get_head_color())

    # update body
    for segment in segments:
        segment.color(get_body_color())


# food pulse animation
def animate_food():
    size = food.shapesize()[0]
    if size >= 1.2:
        food.shapesize(1, 1)
    else:
        food.shapesize(1.2, 1.2)


# ================= KEY BINDINGS =================
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(change_snake_color, "c")


# ================= MAIN LOOP =================
while True:
    wn.update()

    # border collision
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        game_over_sound()

        score = 0
        delay = 0.08

        pen.clear()
        pen.write(f"Score: {score} High Score = {high_score}",
                  align="center", font=("Courier", 24, "normal"))

    # food collision
    if head.distance(food) < 20:
        winsound.Beep(1200, 100)

        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # ✅ new segment with body color
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(get_body_color())
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001

        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"Score: {score} High Score = {high_score}",
                  align="center", font=("Courier", 24, "normal"))

    # move body
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # self collision
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            game_over_sound()

            score = 0
            delay = 0.08

            pen.clear()
            pen.write(f"Score: {score} High Score = {high_score}",
                      align="center", font=("Courier", 24, "normal"))

    animate_food()
    time.sleep(delay)

wn.mainloop()