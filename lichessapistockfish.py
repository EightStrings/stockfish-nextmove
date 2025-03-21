import chess
import chess.pgn
import requests
import os

os.chdir("D:\\Synced\\Coding\\Stockfish Openings\\output")
# Funzione per ottenere la mossa migliore tramite Lichess Cloud Evaluation API
def get_best_move_from_lichess(board):
    fen = board.fen()
    url = f"https://lichess.org/api/cloud-eval?fen={fen}&multiPv=1"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore nella richiesta: {response.status_code}")
        return None

    data = response.json()
    if "pvs" in data and len(data["pvs"]) > 0:
        best_move_uci = data["pvs"][0]["moves"].split()[0]
        return chess.Move.from_uci(best_move_uci)
    else:
        print("Nessuna mossa trovata")
        return None

# Funzione per chiedere quante mosse l'utente vuole vedere
def get_num_moves():
    print("\nQuante mosse vuoi che vengano giocate? (scrivi 'fino alla fine' per far giocare fino alla fine della partita)")
    user_input = input().lower()
    
    if user_input == 'fino alla fine':
        return 'fino alla fine'  # Ritorna una stringa per indicare che vogliamo continuare fino alla fine
    try:
        num_moves = int(user_input)
        return num_moves
    except ValueError:
        print("Input non valido. Inserisci un numero intero o 'fino alla fine'.")
        return get_num_moves()  # Chiedi di nuovo in caso di input errato

# Funzione per eseguire le mosse richieste
def play_moves(board, num_moves):
    move_count = 1
    moves_played = 0

    while not board.is_game_over():
        if num_moves != 'fino alla fine' and moves_played >= num_moves:
            break  # Se il numero di mosse è stato raggiunto, fermati

        # Mossa di Lichess tramite l'API
        best_move = get_best_move_from_lichess(board)
        if best_move:
            board.push(best_move)
            moves_played += 1  # Incrementa il numero di mosse giocate da Lichess
            print(f"\nMossa {move_count}: {best_move}")
            print(board)  # Stampa la scacchiera dopo ogni mossa
            move_count += 1  # Incrementa il contatore delle mosse
        else:
            break  # Se non ci sono mosse disponibili, esci dal ciclo

# Funzione per gestire la continuazione del gioco
def continue_game(board):
    while True:
        user_choice = input("\nVuoi continuare a giocare? (sì/no): ").lower()
        if user_choice == "sì":
            num_moves = get_num_moves()  # Chiedi di nuovo il numero di mosse
            play_moves(board, num_moves)  # Esegui le mosse
        elif user_choice == "no":
            print("Partita terminata.")
            break
        else:
            print("Scelta non valida. Prova di nuovo.")

# Creazione del file PGN
def save_game_as_pgn(board):
    pgn_file_path = input("Dimmi il nome di come vuoi salvare il file pgn: ")

    # Sanitizza il nome del file per evitare errori nei percorsi
    pgn_file_path = pgn_file_path.replace('/', '_').replace('\\', '_').strip()

    # Crea il gioco PGN
    game = chess.pgn.Game()  # Crea un oggetto di gioco PGN
    game.headers["Event"] = "Partita tra NM CiaoBimbi e FM Acheniosogno"  # Metti un evento nel file PGN
    game.headers["White"] = "NM CiaoBimbiPuntoIT"
    game.headers["Black"] = "FM Acheniosogno"
    game.headers["WhiteElo"] = "9600"  # ELO di Lichess (Stockfish)
    game.headers["BlackElo"] = "2400"  # ELO di un giocatore
    game.headers["Result"] = board.result()  # Aggiungi il risultato della partita (1-0, 0-1, 1/2-1/2)

    # Aggiungi le mosse al PGN
    node = game  # Inizializza il nodo
    for move in board.move_stack:
        node = node.add_variation(move)  # Aggiungi ogni mossa come variazione al nodo
        print(f"Aggiunta mossa al PGN: {move}")  # Debug: stampa ogni mossa aggiunta

    # Scrivi il file PGN
    with open(pgn_file_path, "w") as pgn_file:
        pgn_file.write(str(game))  # Scrive direttamente il PGN nel file

    print(f"File PGN generato: {pgn_file_path}")

# Inizializza la scacchiera
board = chess.Board()

# Input delle mosse iniziali dell'utente
print("Inserisci le mosse di apertura (separate da spazio, ad esempio: e4 c5 Nf3 Nc6):")
opening_moves = input().split()  # L'utente inserisce le mosse in formato come "e4 c5 Nf3 Nc6"

# Esegui le mosse di apertura inserite dall'utente
move_count = 1
for move in opening_moves:
    try:
        board.push_san(move)  # Esegui la mossa dell'utente
        print(f"\nMossa {move_count}: {move}")
        print(board)  # Stampa la scacchiera dopo ogni mossa dell'utente
        move_count += 1  # Incrementa il contatore delle mosse
    except ValueError:
        print(f"Mossa non valida: {move}")
        continue

# Chiedi quante mosse l'utente vuole vedere inizialmente
num_moves = get_num_moves()

# Gioca le mosse iniziali richieste
play_moves(board, num_moves)

# Chiedi se l'utente vuole continuare
continue_game(board)

# Salva il file PGN
save_game_as_pgn(board)
