import pickle
import random
import numpy as np
from src.flappy import Flappy

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.9995, min_exploration_rate=0.01):
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.min_epsilon = min_exploration_rate
        self.q_table = {}
        self.actions = [0, 1]

    def get_state_key(self, state):
        return tuple(state) # O estado já será uma tupla de inteiros

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = {a: 0 for a in self.actions}
            return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_table(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in self.actions}

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_state_key].values())
        
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state_key][action] = new_value

    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
            
    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"Tabela Q salva em {filename}")

    def load_q_table(self, filename="q_table.pkl"):
        with open(filename, "rb") as f:
            self.q_table = pickle.load(f)
        print(f"Tabela Q carregada de {filename}")


def get_game_state(player, pipes):
    """
    Função crucial que extrai as informações importantes do jogo
    e as transforma em um 'estado' para a IA. VERSÃO ATUALIZADA.
    """
    if not pipes.upper:
        return (100, 0, 0) # Estado padrão com distância grande

    next_pipe = None
    for pipe in pipes.upper:
        if pipe.x + pipe.w > player.x:
            next_pipe = pipe
            break
    
    if next_pipe is None:
        return (100, 0, 0) # Se não achar cano, estado padrão
        
    # --- NOVA INFORMAÇÃO CRUCIAL ---
    # Estado 1: Distância horizontal até o próximo cano
    delta_x = next_pipe.x - player.x
    
    # Estado 2: Distância vertical até o centro do buraco do cano
    gap_center_y = next_pipe.y + next_pipe.h + pipes.pipe_gap / 2
    delta_y = player.y - gap_center_y

    # Estado 3: Velocidade vertical do pássaro
    vel_y = player.vel_y

    # Discretização: Agrupamos os valores contínuos em "caixas" para 
    # reduzir o número de estados e acelerar o aprendizado.
    # Os números (10, 10, etc.) controlam o quão "granulado" é o estado.
    state = (
        int(delta_x // 10), # Agrupa a distância X a cada 10 pixels
        int(delta_y // 10), # Agrupa a distância Y a cada 10 pixels
        int(vel_y)          # A velocidade já é quase um inteiro
    )

    return state


if __name__ == "__main__":
    # Define se vamos treinar ou apenas assistir
    TRAIN_MODE = True

    env = Flappy(headless=TRAIN_MODE) # Roda sem tela se estiver treinando
    agent = QLearningAgent()

    if TRAIN_MODE:
        try:
            agent.load_q_table()
            print("Continuando treinamento com tabela Q existente.")
        except FileNotFoundError:
            print("Nenhuma tabela Q encontrada. Iniciando novo treinamento.")
        
        total_episodes = 50000
        max_score = 0

        for episode in range(total_episodes):
            env.reset()
            state = get_game_state(env.player, env.pipes)
            game_over = False
            
            while not game_over:
                action = agent.choose_action(state)
                reward, game_over, score = env.game_step(action)
                next_state = get_game_state(env.player, env.pipes)
                agent.update_q_table(state, action, reward, next_state)
                state = next_state
            
            agent.decay_epsilon()
            
            if score > max_score:
                max_score = score
                print(f"!!! NOVO RECORDE: {max_score} !!! Salvando tabela Q...")
                agent.save_q_table()

            if (episode + 1) % 100 == 0:
                print(f"Episódio: {episode + 1}/{total_episodes} | Pontuação: {score} | Recorde: {max_score} | Epsilon: {agent.epsilon:.4f}")

        print("Treinamento concluído!")
        agent.save_q_table()
    
    else: # MODO DE VISUALIZAÇÃO
        try:
            agent.load_q_table()
            agent.epsilon = 0 # Desliga totalmente as ações aleatórias
            print("Tabela Q carregada. Iniciando modo de visualização.")
        except FileNotFoundError:
            print("ERRO: Nenhuma tabela Q encontrada para carregar. Treine o agente primeiro.")
            exit()

        while True:
            env.reset()
            state = get_game_state(env.player, env.pipes)
            game_over = False
            while not game_over:
                action = agent.choose_action(state)
                reward, game_over, score = env.game_step(action)
                state = get_game_state(env.player, env.pipes)
            print(f"Partida finalizada com pontuação: {score}")