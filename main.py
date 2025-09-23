from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()


grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')

arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound',loop = False, autoplay = False)

sky_texture = load_texture('assets/skybox.png')
block_pick = 1

window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False

block_types = {
    "grass": grass_texture,
    "stone": stone_texture,
    "brick": brick_texture,
    "dirt": dirt_texture
}


inventory = {
    "grass": 10,
    "stone": 10,
    "brick": 10,
    "dirt": 10
}

def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
        
    else:
        hand.passive()  

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4


class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=None):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture if texture is not None else grass_texture,
            color=color.white,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                selected_slot = inventory.get_selected_item()

                if selected_slot.item and selected_slot.quantity > 0:
                    punch_sound.play()

                    Voxel(
                        position=self.position + mouse.normal,
                        texture=block_types[selected_slot.item]
                    )

                    
                    selected_slot.quantity -= 1
                    selected_slot.text = str(selected_slot.quantity)

                    if selected_slot.quantity <= 0:
                        destroy(selected_slot.icon_entity)
                        selected_slot.item = None
                        selected_slot.text = ''

            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)

class Inventory(Entity):
    def __init__(self, block_types, **kwargs):
        super().__init__(parent=camera.ui)

        self.slots = []
        self.size = 9
        self.selected_index = 0  

        for i in range(self.size):
            slot = Button(
                parent=self,
                model='quad',
                color=color.gray,
                scale=(0.08, 0.08),
                position=(-0.4 + i*0.09, -0.45),
                text='0' 
            )
            slot.item = None
            slot.quantity = 0
            slot.text_entity.scale *= 1.2  
            slot.text = ''  
            self.slots.append(slot)

        
        self.slots[self.selected_index].color = color.azure

       
        for block_name, texture in block_types.items():
            self.add_item(block_name, texture, amount=30)

    def add_item(self, item_name, icon, amount=1):
        
        for slot in self.slots:
            if slot.item == item_name:
                slot.quantity += amount
                slot.text = str(slot.quantity)
                return

       
        for slot in self.slots:
            if slot.item is None:
                slot.item = item_name
                
                slot.icon_entity = Entity(
                    parent=slot,
                    model='quad',
                    texture=icon,
                    scale=(0.07, 0.07)
                )
                slot.quantity = amount
                slot.text = str(slot.quantity)
                return

      
        for slot in self.slots:
            if slot.item is None:
                slot.item = item_name
                slot.icon = icon
                slot.icon_entity = Entity(
                    parent=slot,
                    model='quad',
                    texture=icon,
                    scale=(0.07, 0.07)
                )
                slot.quantity = amount
                slot.text = str(slot.quantity)
                return

    def select_slot(self, index):
        
        for slot in self.slots:
            slot.color = color.gray
       
        self.selected_index = index
        self.slots[index].color = color.azure

    def get_selected_item(self):
        return self.slots[self.selected_index]

    def input(self, key):
       
        for i in range(1, self.size+1):
            if key == str(i):
                self.select_slot(i-1)


class sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 200,
            double_sided = True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6)
        )


    def active(self):
        self.position = Vec2(0.3,-0.5)
        

    def passive(self):
        self.position = Vec2(0.4,-0.6)
    
for z in range(50):
    for x in range(50):
        y = int(math.sin(x * 0.3) * 2 + math.cos(z * 0.3) * 2)
        voxel = Voxel(position=(x, y, z))

player = FirstPersonController()
sky = sky()
hand = Hand()
block_types = {
    'grass': 'assets/grass_block.png',
    'stone': 'assets/stone_block.png',
    'brick': 'assets/brick_block.png',
    'dirt': 'assets/dirt_block.png',
}

inventory = Inventory(block_types)
sun = DirectionalLight()

sun.look_at(Vec3(1,-1,-1))

def update():
    sun.rotation_x += time.dt * 5  

app.run()