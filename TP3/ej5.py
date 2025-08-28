import math
import random

#El tablero es una lista de strings, imprime tabla por consola
def print_board(board):
    symbols = [cell if cell != " " else str(i) for i, cell in enumerate(board)]
    print(f"\n{symbols[0]} | {symbols[1]} | {symbols[2]}")
    print("--+---+--")
    print(f"{symbols[3]} | {symbols[4]} | {symbols[5]}")
    print("--+---+--")
    print(f"{symbols[6]} | {symbols[7]} | {symbols[8]}\n")

#Chequea que si para un tablero particular gano el player
def check_winner(board, player):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(all(board[i] == player for i in combo) for combo in win_conditions)

#Si ya no queda espacio en la lista define empate
def is_draw(board):
    return " " not in board

#Puntua el tabero board, asigna puntaje por tablero ganador, por centro ocupado 
# y puntua por tablero cercano a ganar
def evaluate(board):
    # IA = "O", Humano = "X"
    if check_winner(board, "O"):
        return 10
    elif check_winner(board, "X"):
        return -10

    score = 0
    # Centro vale más
    if board[4] == "O":
        score += 1
    elif board[4] == "X":
        score -= 1

    # Revisar combinaciones ganadoras
    win_conditions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in win_conditions:
        line = [board[a], board[b], board[c]]
        if line.count("O") == 2 and line.count(" ") == 1:
            score += 3  # O casi gana
        if line.count("X") == 2 and line.count(" ") == 1:
            score -= 3  # X casi gana

    return score

#Devuelve celdas vacias
def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]

#Algoritmo recocido
def simulated_annealing_move(board, player="O", temp=10.0, cooling=0.95, steps=20):
    #Si no hay movimientos posibles, devuelvo none
    possible_moves = get_available_moves(board)
    if not possible_moves:
        return None

    #Busco movimiento aleatorio y lo evaluo
    current_move = random.choice(possible_moves)
    board_copy = board[:]
    board_copy[current_move] = player
    current_score = evaluate(board_copy)

    T = temp
    #Evaluo distintos tableros, si son mejores se eligen 
    # y si son peores se eligen a veces
    for step in range(steps):
        if T <= 0.01:
            break

        new_move = random.choice(possible_moves)
        new_board = board[:]
        new_board[new_move] = player
        new_score = evaluate(new_board)

        delta = new_score - current_score

        if delta > 0 or random.random() < math.exp(delta / T):
            current_move, current_score = new_move, new_score

        T *= cooling

    return current_move

def play_game():
    board = [" "] * 9
    human = "X"
    ai = "O"

    print("Bienvenido al Ta-te-ti con Recocido Simulado (IA = O, Humano = X)")

    # 🔹 Pedir temperatura al usuario
    try:
        temp = float(input("Ingrese la temperatura inicial de la IA: "))
    except ValueError:
        temp = 10.0
        print("Valor inválido, se usará temperatura por defecto:", temp)

    print_board(board)

    while True:
        # Turno humano
        human_move = None
        while human_move not in get_available_moves(board):
            try:
                human_move = int(input("Tu turno (0-8): "))
            except ValueError:
                continue
        board[human_move] = human

        print_board(board)
        if check_winner(board, human):
            print("¡Ganaste! 🎉")
            break
        if is_draw(board):
            print("Empate 🤝")
            break

        # Turno IA
        print("Turno de la IA...")
        ai_move = simulated_annealing_move(board, ai, temp=temp, cooling=0.90, steps=200)
        board[ai_move] = ai

        print_board(board)
        if check_winner(board, ai):
            print("La IA ganó 😈")
            break
        if is_draw(board):
            print("Empate 🤝")
            break

if __name__ == "__main__":
    play_game()
