from ursina import *

app = Ursina()

Entity(model='plane', scale=(50,1,50), texture='white_cube', texture_scale=(50,50), color=color.gray)
Sky()

player = Entity(model='cube', color=color.orange, scale_y=2)

camera_pivot = Entity(y=2)
camera.parent = camera_pivot
camera.position = (0, 0, -10)
camera.rotation = (20, 0, 0)

rotation_speed = 100
zoom_speed = 20
min_zoom, max_zoom = 4, 20
zoom_distance = 10

mouse.locked = False


from game_session import GameSession
from backend.models import Deck

deck1 = Deck.objects.first()
deck2 = Deck.objects.all()[1]

session = GameSession(deck1, deck2)

def play_first_card():
    session.play_card(0)

def end_turn():
    session.end_turn()

Button(text="Play Card 0", on_click=play_first_card)
Button(text="End Turn", on_click=end_turn)



def update():
    global zoom_distance

    camera_pivot.rotation_y += mouse.velocity[0] * rotation_speed
    camera.rotation_x -= mouse.velocity[1] * rotation_speed
    camera.rotation_x = clamp(camera.rotation_x, -30, 60)

    if held_keys['scroll up']:
        zoom_distance = max(min_zoom, zoom_distance - zoom_speed * time.dt)
    if held_keys['scroll down']:
        zoom_distance = min(max_zoom, zoom_distance + zoom_speed * time.dt)

    camera.position = (0, 0, -zoom_distance)

    camera_pivot.position = player.position + Vec3(0, 2, 0)

    move_dir = Vec3(
        camera_pivot.right * (held_keys['d'] - held_keys['a']) +
        camera_pivot.forward * (held_keys['w'] - held_keys['s'])
    ).normalized()
    move_dir.y = 0
    player.position += move_dir * 5 * time.dt

    if move_dir.length() > 0:
        player.look_at(player.position + move_dir)


npc = Entity(model='cube', color=color.cyan, scale=(1.5, 2, 1.5), position=(5,1,0))

def input(key):
    if key == 'e' and distance(player.position, npc.position) < 2.5:
        print("Entering TCG combat!")
    if key == 'tab':
        mouse.locked = not mouse.locked


EditorCamera(enabled=False)
app.run()
