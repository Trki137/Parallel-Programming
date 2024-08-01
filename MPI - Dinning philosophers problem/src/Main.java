import mpi.MPI;
import philosopher.PhilosopherImpl;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        MPI.Init(args);

        new PhilosopherImpl(
                MPI.COMM_WORLD.Rank(),
                MPI.COMM_WORLD
        );

        MPI.Finalize();
    }
}