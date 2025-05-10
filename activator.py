import pygame


class Activator:
    def __init__(self, rect: pygame.rect.Rect, call_back, **kwargs):
        self.rect = rect
        self.call_back = call_back
        self.kwargs = kwargs

    def check(self, mouse):
        return self.rect.collidepoint(*mouse)

    def call(self):
        self.call_back(**self.kwargs)
