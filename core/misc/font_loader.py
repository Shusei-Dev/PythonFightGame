import pygame as pg

def FontText(font_path, size, color, text, smooth=False):
    font = pg.font.Font(font_path, size)
    render_text = font.render(text, smooth, color)
    return render_text