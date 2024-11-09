import serial
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from labels import *
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

sensor1_value = 0
sensor2_value = 0
sensor3_value = 0
sensor4_value = 0
sensor5_value = 0
sensor6_value = 0
millis_value = 0

current_P = 0
current_I = 0
current_D = 0
current_set_point = 0
current_PWMDirect = 0
current_override = 0

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []

x_values_number = 100


def open_website(event):
    website_url = website_str
    webbrowser.open_new(website_url)


def read_from_arduino():
    global \
        sensor1_value, \
        sensor2_value, \
        sensor3_value, \
        sensor4_value, \
        sensor5_value, \
        sensor6_value, \
        millis_value
    global \
        current_P, \
        current_I, \
        current_D, \
        current_set_point, \
        current_override, \
        current_PWMDirect
    while True:
        try:
            if arduinoData.in_waiting > 0:
                # Read data from Arduino
                arduino_string = arduinoData.readline().decode("utf-8").strip()
                print(arduino_string)
                # Split the data into individual sensor values
                data_values = arduino_string.split("/")
                # Update the global variables
                sensor1_value = float(data_values[0])
                sensor2_value = float(data_values[1])
                sensor3_value = float(data_values[2])
                sensor4_value = float(data_values[3])
                sensor5_value = float(data_values[4])
                sensor6_value = float(data_values[5])

                millis_value = float(data_values[6]) / 1000

                current_P = float(data_values[7])
                current_I = float(data_values[8])
                current_D = float(data_values[9])
                current_set_point = float(data_values[10])

                current_override = float(data_values[11])
                current_PWMDirect = float(data_values[12])

                # Update the GUI fields
                update_gui_fields()
        except serial.SerialException:
            messagebox.showerror("Error", "Connection to Arduino is lost")
            break


def update_gui_fields():
    global \
        sensor1_label, \
        sensor2_label, \
        sensor3_label, \
        sensor4_label, \
        sensor5_label, \
        sensor6_label, \
        millis_label
    global current_P_label, current_D_label, current_I_label, current_set_point_label
    global current_override_label, current_PWMDirect_label

    # Update labels with sensor values
    sensor1_label.config(text=f"{sensor1_str}: {sensor1_value}")
    sensor2_label.config(text=f"{sensor2_str}: {sensor2_value}")
    sensor3_label.config(text=f"{sensor3_str}: {sensor3_value}")
    sensor4_label.config(text=f"{sensor4_str}: {sensor4_value}")
    sensor5_label.config(text=f"{sensor5_str}: {sensor5_value}")
    sensor6_label.config(text=f"{sensor6_str}: {sensor6_value}")
    millis_label.config(text=f"{ard_time_str}: {millis_value}")
    current_P_label.config(text=f"Current P: {current_P}")
    current_I_label.config(text=f"Current I: {current_I}")
    current_D_label.config(text=f"Current D: {current_D}")
    current_set_point_label.config(text=f"Current set point: {current_set_point}")
    current_override_label.config(text=f"Override?: {current_override}")
    current_PWMDirect_label.config(text=f"PWM Direct: {current_PWMDirect}")


def send_PID_values():
    global p_entry, i_entry, d_entry, set_point_entry, override_entry, PWMDirect_entry
    global \
        current_P, \
        current_I, \
        current_D, \
        current_set_point, \
        current_PWMDirect, \
        current_override
    try:
        # Get input values from entry fields
        p = float(p_entry.get()) if p_entry.get() else current_P
        i = float(i_entry.get()) if i_entry.get() else current_I
        d = float(d_entry.get()) if d_entry.get() else current_D
        set_point = (
            float(set_point_entry.get()) if set_point_entry.get() else current_set_point
        )
        override = (
            float(override_entry.get()) if override_entry.get() else current_override
        )
        PWMDirect = (
            float(PWMDirect_entry.get()) if PWMDirect_entry.get() else current_PWMDirect
        )
    except ValueError:
        # If any input is not a number, revert to current values and display error message
        messagebox.showerror("Error", "Please enter numerical values only.")
        return
    str_sent = f"{p},{i},{d},{set_point},{override},{PWMDirect}/".encode()
    print(str_sent)
    arduinoData.write(str_sent)


def update_plot():
    global x, y1, y2, y3, y4, y5, ax, canvas, root
    global \
        sensor1_value, \
        sensor2_value, \
        sensor3_value, \
        sensor4_value, \
        sensor5_value, \
        millis_value
    global x_values_number

    # Append current time to x list
    x.append(millis_value)
    # Append new sensor value to y list
    y1.append(sensor1_value)
    y2.append(sensor2_value)
    y3.append(sensor3_value)
    y4.append(sensor4_value)
    y5.append(sensor5_value)

    # Remove data points older than x_values_number seconds
    while x[-1] - x[0] > x_values_number:
        x.pop(0)
        y1.pop(0)
        y2.pop(0)
        y3.pop(0)
        y4.pop(0)
        y5.pop(0)

    # Update plot with new data
    ax.clear()
    ax.plot(x, y1, label=sensor1_str)
    ax.plot(x, y2, label=sensor2_str)
    ax.plot(x, y3, label=sensor3_str)
    ax.plot(x, y4, label=sensor4_str)
    ax.plot(x, y5, label=sensor5_str)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(graph_title)
    ax.legend()
    ax.legend(loc="lower right")
    ax.grid()

    canvas.draw()
    root.after(100, update_plot)


def submit_options():
    global x_values_number, x_entry
    x_values_number = int(x_entry.get())
    print(x_values_number)


def main():
    global \
        sensor1_label, \
        sensor2_label, \
        sensor3_label, \
        millis_label, \
        sensor4_label, \
        sensor5_label, \
        sensor6_label
    global p_entry, i_entry, d_entry, set_point_entry, override_entry, PWMDirect_entry
    global \
        current_P_label, \
        current_D_label, \
        current_I_label, \
        current_set_point_label, \
        current_override_label, \
        current_PWMDirect_label
    global root, ax, canvas, x_entry, arduinoData

    try:
        arduinoData = serial.Serial(USB_port, 115200, timeout=0.1)
    except serial.SerialException:
        messagebox.showerror("Error", "Could not connect to Arduino.")
        return

    # Start a thread to read data from Arduino
    arduino_thread = threading.Thread(target=read_from_arduino)
    arduino_thread.daemon = True
    arduino_thread.start()
    root = tk.Tk()
    root.resizable(False, False)
    root.title(software_title)

    # Create a frame for sensor values
    sensor_frame = ttk.Frame(root, padding=(10, 10))
    sensor_frame.grid(row=0, column=0)

    # Create labels for sensor values
    tk.Label(sensor_frame, text=sensor_section_str, font=("Arial", 12, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5
    )
    sensor1_label = tk.Label(sensor_frame, text=sensor1_str)
    sensor1_label.grid(row=1, column=0, sticky="e")
    sensor2_label = tk.Label(sensor_frame, text=sensor2_str)
    sensor2_label.grid(row=2, column=0, sticky="e")
    sensor3_label = tk.Label(sensor_frame, text=sensor3_str)
    sensor3_label.grid(row=3, column=0, sticky="e")
    sensor4_label = tk.Label(sensor_frame, text=sensor4_str)
    sensor4_label.grid(row=4, column=0, sticky="e")
    sensor5_label = tk.Label(sensor_frame, text=sensor5_str)
    sensor5_label.grid(row=5, column=0, sticky="e")
    sensor6_label = tk.Label(sensor_frame, text=sensor6_str)
    sensor6_label.grid(row=6, column=0, sticky="e")
    millis_label = tk.Label(sensor_frame, text=ard_time_str)
    millis_label.grid(row=7, column=0, sticky="e")

    # Create a separator line
    separator = ttk.Separator(root, orient="vertical")
    separator.grid(row=0, column=1, rowspan=5, sticky="ns")
    separator = ttk.Separator(root, orient="vertical")
    separator.grid(row=0, column=4, rowspan=5, sticky="ns")

    # Create a frame for PID values
    pid_frame = ttk.Frame(root, padding=(10, 10))
    pid_frame.grid(row=0, column=2)

    # Create labels for PID values
    tk.Label(pid_frame, text=pid_section_str, font=("Arial", 12, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5
    )
    current_P_label = tk.Label(pid_frame, text="Current P: ")
    current_P_label.grid(row=1, column=0, sticky="e")
    current_I_label = tk.Label(pid_frame, text="Current I: ")
    current_I_label.grid(row=2, column=0, sticky="e")
    current_D_label = tk.Label(pid_frame, text="Current D: ")
    current_D_label.grid(row=3, column=0, sticky="e")
    current_set_point_label = tk.Label(pid_frame, text="Current set point: ")
    current_set_point_label.grid(row=4, column=0, sticky="e")
    current_override_label = tk.Label(pid_frame, text="Override?: ")
    current_override_label.grid(row=5, column=0, sticky="e")
    current_PWMDirect_label = tk.Label(pid_frame, text="PWM Direct: ")
    current_PWMDirect_label.grid(row=6, column=0, sticky="e")

    # Create a frame for sending values
    sending_frame = ttk.Frame(root, padding=(10, 10))
    sending_frame.grid(row=0, column=6)
    # Create labels for options
    tk.Label(sending_frame, text=sending_section_str, font=("Arial", 12, "bold")).grid(
        row=0, column=1, columnspan=1
    )

    # Create entry fields for PID values
    tk.Label(sending_frame, text="P: ").grid(row=7, column=0, sticky="e")
    p_entry = tk.Entry(sending_frame)
    p_entry.grid(row=7, column=1)
    tk.Label(sending_frame, text="I: ").grid(row=8, column=0, sticky="e")
    i_entry = tk.Entry(sending_frame)
    i_entry.grid(row=8, column=1)
    tk.Label(sending_frame, text="D: ").grid(row=9, column=0, sticky="e")
    d_entry = tk.Entry(sending_frame)
    d_entry.grid(row=9, column=1)
    tk.Label(sending_frame, text="Set point: ").grid(row=10, column=0, sticky="e")
    set_point_entry = tk.Entry(sending_frame)
    set_point_entry.grid(row=10, column=1)
    tk.Label(sending_frame, text="Override: ").grid(row=11, column=0, sticky="e")
    override_entry = tk.Entry(sending_frame)
    override_entry.grid(row=11, column=1)
    tk.Label(sending_frame, text="PWM Direct: ").grid(row=12, column=0, sticky="e")
    PWMDirect_entry = tk.Entry(sending_frame)
    PWMDirect_entry.grid(row=12, column=1)

    # Create send button
    send_button = tk.Button(sending_frame, text=send_btn_str, command=send_PID_values)
    send_button.grid(row=14, column=1, columnspan=2)

    # Create a Matplotlib figure
    fig = Figure(figsize=(10, 5), dpi=100, facecolor="#f0f0f0")
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=9, column=0, columnspan=10)

    # Create a frame for X axis number of values entry and submit button
    x_axis_frame = ttk.Frame(root, padding=(10, 10))
    x_axis_frame.grid(row=10, column=0, columnspan=10)

    # Create labels and entry field for X axis number of values
    tk.Label(x_axis_frame, text=x_axis_option_str).grid(row=0, column=0, sticky="e")
    x_entry = tk.Entry(x_axis_frame)
    x_entry.grid(row=0, column=1)

    # Create submit button
    submit_button = tk.Button(
        x_axis_frame, text=options_btn_str, command=submit_options
    )
    submit_button.grid(row=2, column=1, padx=5, columnspan=2)

    # Create a frame for the image
    image_frame = ttk.Frame(root, padding=(10, 10))
    image_frame.grid(row=0, column=10, rowspan=10, columnspan=1)

    # Load and resize the image
    image = Image.open(logo_path)
    # Resize the image as needed, e.g., to fit a certain width
    width, height = 200, 200  # Adjust width and height as needed
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(image_frame, image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection
    label.pack(expand=True, fill="both")
    label.bind("<Button-1>", open_website)

    # Update the plot
    update_plot()

    root.mainloop()


if __name__ == "__main__":
    main()
