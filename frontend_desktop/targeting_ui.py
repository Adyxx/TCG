from ursina import *

current_highlights = []

def clear_highlights():
    for h in current_highlights:
        destroy(h)
    current_highlights.clear()

def visual_target_selector(targets, on_target_chosen):
    clear_highlights()

    for target in targets:
        if not hasattr(target, 'ui_entity'):
            continue 

        highlight = Entity(
            model='quad',
            color=color.rgba(255, 255, 0, 100),
            parent=target.ui_entity,
            scale=1.1,
            z=-0.01
        )

        def on_click(t=target):
            clear_highlights()
            on_target_chosen(t)

        target.ui_entity.on_click = on_click

        current_highlights.append(highlight)
