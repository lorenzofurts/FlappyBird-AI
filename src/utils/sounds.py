import pygame

# Classe auxiliar para criar um objeto de som "falso" que não faz nada quando .play() é chamado.
class _MuteSound:
    def play(self):
        pass

class Sounds:
    def __init__(self):
        self.die = pygame.mixer.Sound("assets/audio/die.ogg")
        self.hit = pygame.mixer.Sound("assets/audio/hit.ogg")
        self.point = pygame.mixer.Sound("assets/audio/point.ogg")
        self.swoosh = pygame.mixer.Sound("assets/audio/swoosh.ogg")
        self.wing = pygame.mixer.Sound("assets/audio/wing.ogg")

    def mute(self):
        """
        Substitui todos os sons por um objeto falso que não toca áudio.
        Isso efetivamente "muta" o jogo sem quebrar o código que chama .play().
        """
        self.die = _MuteSound()
        self.hit = _MuteSound()
        self.point = _MuteSound()
        self.swoosh = _MuteSound()
        self.wing = _MuteSound()