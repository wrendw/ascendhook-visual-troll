import glfw
import imgui
import os
import subprocess
from imgui.integrations.glfw import GlfwRenderer

if not glfw.init():
    raise Exception("glfw can't be initialized")

window = glfw.create_window(644, 820, " ", None, None)
glfw.make_context_current(window)

imgui.create_context()
impl = GlfwRenderer(window)

style = imgui.get_style()
style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (10 / 255, 10 / 255, 10 / 255, 1)
style.colors[imgui.COLOR_BUTTON] = (18 / 255, 18 / 255, 18 / 255, 1)
style.colors[imgui.COLOR_BUTTON_HOVERED] = (28 / 255, 28 / 255, 28 / 255, 1)
style.colors[imgui.COLOR_BUTTON_ACTIVE] = (38 / 255, 38 / 255, 38 / 255, 1)

style.colors[imgui.COLOR_FRAME_BACKGROUND] = (15 / 255, 15 / 255, 15 / 255, 1)           
style.colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (38 / 255, 38 / 255, 38 / 255, 1) 
style.colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (30 / 255, 30 / 255, 30 / 255, 1)  
style.colors[imgui.COLOR_CHECK_MARK] = (98 / 255, 166 / 255, 200 / 255, 1)             
style.colors[imgui.COLOR_SLIDER_GRAB] = (55 / 255, 55 / 255, 55 / 255, 1)  
style.colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (55 / 255, 55 / 255, 1)      

style.window_padding = (10, 10)  
style.item_spacing = (10, 10)       

active_tab = "Encoder"
hide_window = True
toggle_console = False
console_process = None  

def open_console():
    global console_process
    if console_process is None:
        command = [
            'cmd', '/k', 
            'title com.squirrel.Discord.Discord && mode con: cols=72 lines=20 && echo [ascend] loaded in pid: 2160 && pause >nul'
        ]
        console_process = subprocess.Popen(
            command, 
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

def close_console():
    global console_process
    if console_process:  
        console_process.terminate()
        console_process = None

def main():
    global active_tab, hide_window, toggle_console, console_process

    gain_value = 1.0
    bitrate_value = 2147483647

    decoder_db_checker = False
    client_user_detection = False
    turn_off_decoder = False

    button_width = 123
    button_height = 25
    button_spacing = 5
    num_buttons = 5
    total_button_width = num_buttons * button_width + (num_buttons - 1) * button_spacing

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(644, 820)
        imgui.begin("Main Window", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        window_width = imgui.get_window_width()
        start_x = (window_width - total_button_width) / 2
        imgui.set_cursor_pos_x(start_x)

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (button_spacing, 5))
        if imgui.button("Encoder", width=button_width, height=button_height):
            active_tab = "Encoder"
        imgui.same_line()
        if imgui.button("Decoder", width=button_width, height=button_height):
            active_tab = "Decoder"
        imgui.same_line()
        if imgui.button("Spoofing", width=button_width, height=button_height):
            active_tab = "Spoofing"
        imgui.same_line()
        if imgui.button("Debug", width=button_width, height=button_height):
            active_tab = "Debug"
        imgui.same_line()
        if imgui.button("Filters", width=button_width, height=button_height):
            active_tab = "Filters"
        
        imgui.separator()

        if active_tab == "Encoder":
            changed, gain_value = imgui.slider_float("Gain", gain_value, 0.0, 10.0, format="%.3f")
            changed, bitrate_value = imgui.slider_float("Bitrate", bitrate_value, 0.0, 10.0, format="%.3f")

        elif active_tab == "Decoder":
            changed, decoder_db_checker = imgui.checkbox("Decoder DB Checker", decoder_db_checker)
            changed, client_user_detection = imgui.checkbox("Client User Detection", client_user_detection)
            changed, turn_off_decoder = imgui.checkbox("Turn Off Decoder", turn_off_decoder)

        elif active_tab == "Spoofing":
            _, hide_window = imgui.checkbox("Hide Window", hide_window)
            changed, new_toggle_console = imgui.checkbox("Toggle Console", toggle_console)
            if changed:
                if new_toggle_console:
                    open_console()
                else:
                    close_console()
            toggle_console = new_toggle_console

        elif active_tab == "Debug":
            imgui.text("0.1.1 | Hook By Ascend")

        imgui.pop_style_var()
        imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    close_console()  
    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
