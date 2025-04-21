# v1.0.1

from gc import callbacks
import obspython as S
import time
import pyautogui

_version_ = "v1.0.1"
lastX = 0
lastY = 0
lastMove = time.time()
x_speed = 1
y_speed = 1

isCursor = False
hide_cursor = False  

def update_text():
    global image_x, image_y, x_speed, y_speed, isCursor, lastX, lastY, lastMove, hide_cursor
    scene = S.obs_get_scene_by_name(scene_name)
    scene_item = S.obs_scene_find_source(scene, source_name)

    if not scene_item:
        return  

    pos = S.vec2()
    try:
        x, y = pyautogui.position()
    except:
        x = 0
        y = 0

    if (x != lastX or y != lastY) and x > image_half and y > image_half:
        lastX = x 
        lastY = y
        lastMove = time.time()

    if x > monitor_x - image_half or x < image_half or y < image_half or y > monitor_y - image_half or (time.time() - lastMove) > input_s:
        if isCursor:
            image_x = min(lastX, monitor_x - image_half)
            image_y = min(lastY, monitor_y - image_half)
            x_speed = speed_var
            y_speed = speed_var

        if (image_x >= (monitor_x - image_half)) or (image_x < image_half):
            x_speed = -x_speed
        if (image_y >= (monitor_y - image_half)) or (image_y < image_half):
            y_speed = -y_speed
        image_x += x_speed
        image_y += y_speed
        pos.x = image_x - image_half
        pos.y = image_y - image_half
        isCursor = False
    else:
        pos.x = x - image_half 
        pos.y = y - image_half
        isCursor = True

    S.obs_sceneitem_set_pos(scene_item, pos)

    if hide_cursor:
        S.obs_sceneitem_set_visible(scene_item, False) 
    else:
        S.obs_sceneitem_set_visible(scene_item, True)   

    S.obs_scene_release(scene)

description = """
<h2 style="color:lightpink">SillyCursor Version : {_version_}</h2>
<a>ponicursor edit , credits: </a><a style="color:lightpink" href="https://github.com/jojoe77777">jojoe77777</a>
<h3>Author:</h3>
<a style="color:lightpink" href="https://www.twitch.tv/pauule">pauule</a> 
""".format(
    **locals()
)

def script_description():
    return description

def script_update(settings):
    S.timer_remove(update_text)
    S.timer_add(update_text, 10)

    global scene_name
    scene_name = S.obs_data_get_string(settings, "_scene")
    print("selected scene:", scene_name) 

    global source_name
    source_name = S.obs_data_get_string(settings, "_source")
    print("selected source:", source_name) 

    global speed_var
    speed_var = S.obs_data_get_double(settings, "_speed")
    print(speed_var) 

    global monitor_x
    monitor_x = S.obs_data_get_double(settings, "_monitor_x")
    print(monitor_x) 

    global monitor_y
    monitor_y = S.obs_data_get_double(settings, "_monitor_y")
    print(monitor_y) 

    global input_s
    input_s = S.obs_data_get_double(settings, "_seconds")
    print(input_s) 

    global image_xy
    image_xy = S.obs_data_get_double(settings, "_image_xy")
    print(image_xy)

    global image_x
    image_x = image_xy

    global image_y
    image_y = image_xy

    global image_half
    image_half = image_xy / 2

    global hide_cursor  
    hide_cursor = S.obs_data_get_bool(settings, "_hide")
    print("Hide cursor:", hide_cursor)

def script_properties():
    props = S.obs_properties_create()
    disabled = S.obs_properties_add_bool(props, "_hide", "Hidden")
    S.obs_property_set_long_description(disabled, """<a style="color:lightpink">Do you want to hide the cursor?</a>""")
    S.obs_properties_add_int(props, "_monitor_x", "Monitor res (x)", 696, 10000, 1)
    S.obs_properties_add_int(props, "_monitor_y", "Monitor res (y)", 392, 10000, 1)
    S.obs_properties_add_int(props, "_seconds", "No input (s)", 0, 10, 1)
    S.obs_properties_add_float_slider(props, "_speed", "Speed", 0.5, 10, 0.1)
    p1 = S.obs_properties_add_list(props, "_scene", "Cursor scene", S.OBS_COMBO_TYPE_EDITABLE, S.OBS_COMBO_FORMAT_STRING)
    p2 = S.obs_properties_add_list(props, "_source", "Source", S.OBS_COMBO_TYPE_EDITABLE, S.OBS_COMBO_FORMAT_STRING) 
    S.obs_properties_add_int_slider(props, "_image_xy", "Image size", 25, 500, 1)

    scenes = S.obs_frontend_get_scenes()
    for scene in scenes:
        name = S.obs_source_get_name(scene)
        S.obs_property_list_add_string(p1, name, name)
    S.source_list_release(scenes)

    sources = S.obs_enum_sources()
    for source in sources:
        name = S.obs_source_get_name(source)
        S.obs_property_list_add_string(p2, name, name)
    S.source_list_release(sources)

    return props
