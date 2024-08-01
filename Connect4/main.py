from mpi4py import MPI
from game.Connect4 import Connect4
from player.HumanPlayer import HumanPlayer
from player.MinMaxPlayer import MinMaxPlayer
from parallel.Worker import Worker

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank == 0:
    game = Connect4(6, 7)
    player1 = HumanPlayer("X")
    player2 = MinMaxPlayer("O", player1.player_mark, comm)

    first_player = True

    while True:
        game.print_board()
        if first_player:
            result = player1.make_move(game)
        else:
            result = player2.make_move(game)

        if result == 'win':
            game.print_board()
            print(f"Winner is {'player 1' if first_player else 'player 2'}")
            break
        elif result == 'draw':
            print("Draw")
            break

        first_player = not first_player

    for i in range(1, comm.Get_size()):
        comm.send(1, dest=i, tag=2)
else:
    worker = Worker(comm)
    worker.do_task()
