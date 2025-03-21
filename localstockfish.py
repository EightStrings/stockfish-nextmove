import chess
import chess.engine
import chess.pgn
import os

# Cambia il percorso con quello corretto di Stockfish
stockfish_path = "D:\\Synced\\Coding\\Stockfish Openings\\stockfish-windows-x86-64-sse41-popcnt.exe"

# Cambia directory di lavoro
os.chdir("D:\\Synced\\Coding\\Stockfish Openings\\output")

# Debugging Motore
def start_engine():
    print(f"Avvio Stockfish dal percorso: {stockfish_path}")
    if not os.path.isfile(stockfish_path):
        print("Errore: il file Stockfish non esiste nel percorso specificato.")
        return None
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        print("Motore Stockfish avviato correttamente.")
        return engine
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Errore nell'avvio del motore Stockfish: {e}")
        return None

# Avvia il motore Stockfish
engine = start_engine()

# Inizializza la scacchiera
board = chess.Board()

# Variabile per contare le mosse
move_count = 1

# Input delle mosse iniziali dell'utente
print("Inserisci le mosse di apertura (separate da spazio, ad esempio: e4 c5 Nf3 Nc6):")
opening_moves = input().split()  # L'utente inserisce le mosse in formato come "e4 c5 Nf3 Nc6"

# Esegui le mosse di apertura inserite dall'utente
for move in opening_moves:
    try:
        board.push_san(move)  # Esegui la mossa dell'utente
        print(f"\nMossa {move_count}: {move}")
        print(board)  # Stampa la scacchiera dopo ogni mossa dell'utente
        move_count += 1  # Incrementa il contatore delle mosse
    except ValueError:
        print(f"Mossa non valida: {move}")
        continue

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

# Esegui un numero di mosse richieste dall'utente
def play_moves(num_moves):
    global move_count
    moves_played = 0  # Variabile per tenere traccia del numero di mosse giocate da Stockfish

    while not board.is_game_over():
        if num_moves != 'fino alla fine' and moves_played >= num_moves:
            break  # Se il numero di mosse è stato raggiunto, fermati

        # Mossa di Stockfish (tempo limite di 2 secondi per ogni mossa)
        if engine is None:
            print("Errore: Il motore non è stato inizializzato. Impossibile giocare mosse.")
            exit(1)
        
        result = engine.play(board, chess.engine.Limit(time=2.0))
        board.push(result.move)
        
        moves_played += 1  # Incrementa il numero di mosse giocate da Stockfish
        
        print(f"\nMossa {move_count}: {result.move}")
        print(board)  # Stampa la scacchiera dopo ogni mossa di Stockfish
        move_count += 1  # Incrementa il contatore delle mosse

# Funzione per gestire la continuazione del gioco
def continue_game():
    while True:
        user_choice = input("\nVuoi continuare a giocare? (sì/no): ").lower()
        if user_choice == "sì":
            num_moves = get_num_moves()  # Chiedi di nuovo il numero di mosse
            play_moves(num_moves)  # Esegui le mosse
        elif user_choice == "no":
            print("Partita terminata.")
            break
        else:
            print("Scelta non valida. Prova di nuovo.")

# Chiedi quante mosse l'utente vuole vedere inizialmente
num_moves = get_num_moves()

# Gioca le mosse iniziali richieste
play_moves(num_moves)

# Chiedi se l'utente vuole continuare
continue_game()

# Creazione del file PGN direttamente
pgn_file_path = input("Dimmi il nome di come vuoi salvare il file pgn: ")

# Sanitizza il nome del file per evitare errori nei percorsi
pgn_file_path = pgn_file_path.replace('/', '_').replace('\\', '_').strip()

# Crea il gioco PGN
game = chess.pgn.Game()  # Crea un oggetto di gioco PGN
game.headers["Event"] = "Partita tra Stockfish e Stockfish"  # Metti un evento nel file PGN
game.headers["White"] = "GM Acheniosogno"
game.headers["Black"] = "NM CiaoBimbiPuntoIT aka Magnus Carlsen"
game.headers["WhiteElo"] = "3600"  # ELO di Stockfish per il bianco
game.headers["BlackElo"] = "2882"  # ELO di Stockfish per il nero
game.headers["Result"] = board.result()  # Aggiungi il risultato della partita (1-0, 0-1, 1/2-1/2)

# Aggiungi le mosse al PGN
node = game  # Inizializza il nodo
for move in board.move_stack:
    node = node.add_variation(move)  # Aggiungi ogni mossa come variazione al nodo
    print(f"Aggiunta mossa al PGN: {move}")  # Debug: stampa ogni mossa aggiunta

# Scrivi il file PGN
with open(pgn_file_path, "w") as pgn_file:
    pgn_file.write(str(game))  # Scrive direttamente il PGN nel file

# Chiudi il motore Stockfish
engine.quit()

# Restituisce solo il percorso del file PGN generato
print(f"File PGN generato: {pgn_file_path}")
