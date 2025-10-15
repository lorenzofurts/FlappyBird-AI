import sys
import os # Importamos a biblioteca 'os' para manipular variáveis de ambiente

# --- A SOLUÇÃO DEFINITIVA ---
# Esta linha DEVE ser executada ANTES de 'pygame.init()'
# Ela diz à biblioteca SDL (usada pelo Pygame) para usar um driver de áudio 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from .entities import Background, Floor, Pipes, Player, PlayerMode, Score
from .utils import GameConfig, Images, Sounds, Window

class Flappy:
    def __init__(self, headless=True):
        """
        Inicializa o jogo.
        headless=True: Roda sem tela, para treinamento rápido.
        headless=False: Roda com tela, para visualização.
        """
        # Agora o pygame.init() vai rodar sem tentar encontrar uma placa de som.
        pygame.init()
        
        pygame.display.set_caption("Flappy Bird AI")
        window = Window(288, 512)

        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        if headless:
            fps = 500
        else:
            fps = 30

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=fps,
            window=window,
            images=images,
            sounds=Sounds(),
        )

        self.config.sounds.mute()
        self.headless = headless
        self.reset()

    def reset(self):
        self.background = Background(self.config)
        self.floor = Floor(self.config)
        self.player = Player(self.config)
        self.pipes = Pipes(self.config)
        self.score = Score(self.config)
        self.player.set_mode(PlayerMode.NORMAL)
        return None

    def game_step(self, action: int):
        if not self.headless:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        if action == 1:
            self.player.flap()

        self.background.tick()
        self.floor.tick()
        self.pipes.tick()
        self.player.tick()

        reward = 0.1
        game_over = False

        if self.player.collided(self.pipes, self.floor):
            reward = -1.0
            game_over = True
            return reward, game_over, self.score.score

        player_crossed_pipe = False
        for pipe in list(self.pipes.upper):
            if self.player.crossed(pipe):
                player_crossed_pipe = True
                break
        
        if player_crossed_pipe:
            self.score.add()
            reward = 1.0

        if not self.headless:
            self.score.tick()
            pygame.display.update()
        
        self.config.tick()

        return reward, game_over, self.score.score
