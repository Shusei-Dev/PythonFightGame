import pygame as pg

class LayerManager:
    
    def __init__(self):
        self.layers_table = {}
        
        # Create the front layer
        self.add_layer(999)
        
        
    def add_layer(self, n, type=None, name=None):
        if n not in self.layers_table.keys():
            self.layers_table[n] = Layer(n, type, name)
            if len(self.layers_table.keys()) > 1:
                self.layers_table = dict(sorted(self.layers_table.items()))
            return True
        else:
            return False
            
    def draw_layers(self):
        sorted_layers = sorted(self.layers_table.keys())
        sorted_sprites = []
        
        for n in sorted_layers:
            for i in self.layers_table[n].visible_spr:
                sorted_sprites.append((i.image, i.position))
                
        return sorted_sprites
    
    def move_to_front(self, sprite):

        if len(self.layers_table[999].visible_spr) >= 1:
            
            while len(self.layers_table[999].visible_spr) != 0:
                self.move_spr_org(self.layers_table[999].visible_spr[0])
                        
        self.move_spr_to(sprite, 999)

                
    def moves_to_front(self, sprites=list()):
        
        if len(self.layers_table[999].visible_spr) >= 1:
            while len(self.layers_table[999].visible_spr) != 0:
                self.move_spr_org(self.layers_table[999].visible_spr[0])
                
        for sprite in sprites:
            self.move_spr_to(sprite, 999, sprite.state)
            
            
    def find_back(self, layer):
        layers = list(self.layers_table.keys())
        try:
            if layer == 999:
                return layers[-2]
            else:
                return layers[layers.index(layer) - 1]
        except:
            return layer
    
    def find_front(self, layer):
        layers = self.layers_table.keys()
        try:
            
            return layers[layers.index(layer) + 1]
        except:
            return "[ERROR] Another layer front dosnt exist !"
        
    def get_layer_of_sprite(self, sprite):
        for layers in self.layers_table.keys():
            for sprites in self.layers_table[layers].spr_list:
                if sprites == sprite:
                    return layers

    
    def move_spr_to(self, sprite, layer, state=True):
        spr_layer = self.get_layer_of_sprite(sprite)
        self.layers_table[spr_layer].remove_sprite(sprite)
        self.layers_table[layer].add_sprite(sprite, state)
        
    def move_spr_org(self, sprite):
        spr_layer = self.get_layer_of_sprite(sprite)
        self.layers_table[spr_layer].remove_sprite(sprite)
        self.layers_table[sprite.org_layer].add_sprite(sprite)
        
    def print_all_layers(self):
        print_out = {}
        for layer in self.layers_table.keys():
            n_layer = self.layers_table[layer]
            print_out[layer] = ""
            for spr in n_layer.visible_spr:
                if len(n_layer.visible_spr) >= 2:
                        print_out[layer] += f"name: {spr.name} id: {spr.sprite_id} | "
                else:    
                    print_out[layer] += f"name: {spr.name} id: {spr.sprite_id}"
                
            if print_out[layer] == "":
                print_out[layer] = "none"
                
            if print_out[layer][-1] == " ":
                print_out[layer] = print_out[layer][:-3]
            
        str_print_out = ""
        found = False
        for str_print in str(print_out):
            if str_print != ")" and not found:
                str_print_out += str_print
            else:
                if not found:
                    found = True
                    str_print_out += str_print
                else:
                    if str_print == ",":
                        str_print_out += str_print + "\n"
                    found = False
        print(str_print_out + "}")
        
        
    def get_visible_sprites(self, layer):
        return self.layers_table[layer].visible_spr
        
class Layer:
    
    def __init__(self, n, type=None, name=None):
        
        self.number = n
        self.spr_list = []
        self.visible_spr = []
        self.type = type
        self.name = name
        self.state = True
        
    def add_sprite(self, sprite, state=True):
        if sprite not in self.spr_list:
            self.spr_list.append(sprite)
            sprite.layer_nmb = self.number

            if state and sprite not in self.visible_spr:
                self.visible_spr.append(sprite)
                
    def remove_sprite(self, sprite):
        if sprite in self.spr_list:
            self.spr_list.remove(sprite)
            
        if sprite in self.visible_spr:
            self.visible_spr.remove(sprite)
                
                
    def change_state(self, sprite):
        #print(self.get_state(sprite))
        if self.get_state(sprite) == True:
            self.show_sprite(sprite)
        else:
            self.hide_sprite(sprite)
            
    
    def get_state(self, sprite):
        return self.spr_list[self.spr_list.index(sprite)].state
        
    def hide_sprite(self, sprite):
        if sprite in self.visible_spr:
            self.visible_spr.remove(sprite)
            
    def show_sprite(self, sprite):
        if sprite not in self.visible_spr:
            self.visible_spr.append(sprite)
          
    def __len__(self):
        return self.spr_list