# Classe auxiliar para criar um objeto de som "falso" que não faz nada.
class _DummySound:
    def play(self):
        pass

class Sounds:
    """
    Esta é uma classe de Sons 'fantasma'. Ela existe para que o jogo não quebre,
    mas não carrega ou toca nenhum arquivo de áudio, evitando erros no Colab.
    """
    def __init__(self):
        # Todos os sons são substituídos por um objeto falso e inofensivo.
        self.die = _DummySound()
        self.hit = _DummySound()
        self.point = _DummySound()
        self.swoosh = _DummySound()
        self.wing = _DummySound()

    def mute(self):
        # Esta função não precisa mais fazer nada, mas a mantemos por segurança.
        pass
