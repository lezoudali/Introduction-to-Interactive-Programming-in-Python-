#Follow the link to link to go to game
#http://www.codeskulptor.org/#user30_NB9bcZbqD8_1.py
#
# template for "Stopwatch: The Game"
import simplegui 
# define global variables
time = 0
counterX = 0
counterY = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t%10
    t /=10
    C = t%10
    t/=10
    B = t  
    A = 0
    if B >= 6:
        A += B/6
        B = B%6
        
    return str(A) + ':' + str(B) + str(C) + '.'+ str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global time, counterX, counterY
    if timer.is_running():
        counterY += 1
        if not time%10:
            counterX += 1
    timer.stop()
def reset():
    global time, counterX, counterY
    counterX, counterY, time = 0, 0, 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer():
    global time
    time +=1
    pass

# define draw handler
def draw(canvas):
    global time, counterX, counterY
    counters = str(counterX) +'/'+ str(counterY)
    canvas.draw_text(format(time), (100, 100), 40, 'White')
    canvas.draw_text(counters, (260,20), 20, 'Green')
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers

frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer)

# start frame
frame.start()
# Please remember to review the grading rubric
