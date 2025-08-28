import tkinter as tk

# Global variables
TURN_TIME = 60
remaining_time = TURN_TIME
timer_running = False
paused = False
num_segments = 20  # number of blocks in the progress bar

# Functions
def start_timer():
    global remaining_time, timer_running, paused
    if not timer_running:
        remaining_time = TURN_TIME
        timer_running = True
        paused = False
        pause_button.config(text="Pause")
        draw_progress_bar()  # reset blocks
        elapsed_time = TURN_TIME - remaining_time  # fill initial segment immediately
        fill_segments(elapsed_time)
        timer_label.config(text=f"{remaining_time} seconds remaining")
        update_timer()

def update_timer():
    global remaining_time, timer_running, paused
    if timer_running and not paused:
        if remaining_time > 0:
            timer_label.config(text=f"{remaining_time} seconds remaining")
            elapsed_time = TURN_TIME - remaining_time
            fill_segments(elapsed_time)
            remaining_time -= 1
            root.after(1000, update_timer)
        else:
            timer_label.config(text=f"⏰ Time's up!")
            fill_segments(TURN_TIME)
            timer_running = False

def pause_timer():
    global paused, timer_running
    if timer_running:
        paused = not paused
        if paused:
            pause_button.config(text="Resume")
            timer_label.config(text=f"Paused at {remaining_time} seconds")
        else:
            pause_button.config(text="Pause")
            update_timer()

def reset_timer():
    global remaining_time, paused, timer_running
    remaining_time = TURN_TIME
    paused = False
    timer_running = False  # stop the timer loop
    pause_button.config(text="Pause")
    timer_label.config(text=f"{remaining_time} seconds remaining")
    draw_progress_bar()
    elapsed_time = TURN_TIME - remaining_time
    fill_segments(elapsed_time)

def stop_timer():
    global timer_running, paused
    timer_running = False
    paused = False
    pause_button.config(text="Pause")
    timer_label.config(text="Timer stopped")

def set_duration(seconds):
    global TURN_TIME, remaining_time, timer_running, paused
    TURN_TIME = seconds
    remaining_time = TURN_TIME
    paused = False
    timer_running = False
    pause_button.config(text="Pause")
    duration_label.config(text=f"Turn length set to {TURN_TIME} seconds")
    timer_label.config(text=f"{remaining_time} seconds remaining")
    draw_progress_bar()
    elapsed_time = TURN_TIME - remaining_time
    fill_segments(elapsed_time)

# Canvas progress bar functions
def draw_progress_bar():
    canvas.delete("all")
    segment_width = canvas_width / num_segments
    for i in range(num_segments):
        canvas.create_rectangle(i*segment_width, 0, (i+1)*segment_width, canvas_height, fill='lightgray', outline='white')

def fill_segments(elapsed_time):
    canvas.delete("fill")
    segment_width = canvas_width / num_segments
    filled = int((elapsed_time / TURN_TIME) * num_segments)
    for i in range(filled):
        percent = i / num_segments
        if percent < 0.5:
            color = 'green'
        elif percent < 0.8:
            color = 'yellow'
        else:
            color = 'red'
        canvas.create_rectangle(i*segment_width, 0, (i+1)*segment_width, canvas_height, fill=color, outline='white', tags="fill")

# GUI Setup
root = tk.Tk()
root.title("D&D Turn Timer")
root.geometry("420x380")

timer_label = tk.Label(root, text="Press 'Start' to begin", font=("Arial", 16))
timer_label.pack(pady=20)

# Canvas for segmented progress bar
canvas_width = 300
canvas_height = 25
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack(pady=10)
draw_progress_bar()
elapsed_time = TURN_TIME - remaining_time
fill_segments(elapsed_time)

# Control buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

start_button = tk.Button(control_frame, text="Start", command=start_timer, font=("Arial", 12), width=8)
start_button.grid(row=0, column=0, padx=5, pady=4)

pause_button = tk.Button(control_frame, text="Pause", command=pause_timer, font=("Arial", 12), width=8)
pause_button.grid(row=0, column=1, padx=5, pady=4)

reset_button = tk.Button(control_frame, text="Reset", command=reset_timer, font=("Arial", 12), width=8)
reset_button.grid(row=0, column=2, padx=5, pady=4)

# Duration buttons
duration_label = tk.Label(root, text=f"Turn length set to {TURN_TIME} seconds", font=("Arial", 12))
duration_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

btn_60 = tk.Button(frame, text="60 sec", command=lambda: set_duration(60), font=("Arial", 12), width=8)
btn_60.grid(row=0, column=0, padx=8, pady=4)

btn_90 = tk.Button(frame, text="90 sec", command=lambda: set_duration(90), font=("Arial", 12), width=8)
btn_90.grid(row=0, column=1, padx=8, pady=4)

btn_120 = tk.Button(frame, text="120 sec", command=lambda: set_duration(120), font=("Arial", 12), width=8)
btn_120.grid(row=0, column=2, padx=8, pady=4)

# Stop button at the bottom
stop_button = tk.Button(root, text="Stop", command=stop_timer, font=("Arial", 12), width=10)
stop_button.pack(pady=10)

root.mainloop()