import pickle
import mpi4py
from game.BoardSolver import solve_task
from parallel.TaskResult import TaskResult


class Worker:
    def __init__(self, comm: mpi4py.MPI.COMM_WORLD):
        self.comm = comm

    def do_task(self):
        while True:
            status = mpi4py.MPI.Status()
            task = self.comm.recv(source=0, tag=mpi4py.MPI.ANY_TAG, status=status)
            if status.tag == 1:
                task = pickle.loads(task)
                node = task.node
                best_value = solve_task(task)
                task_result = TaskResult(score=best_value, node_id=node.node_id)
                self.comm.send(pickle.dumps(task_result), dest=0, tag=1)

            elif status.tag == 2:
                print("Worker done for today")
                return
            else:
                raise ValueError(f"Invalid tag {status.tag}!")
