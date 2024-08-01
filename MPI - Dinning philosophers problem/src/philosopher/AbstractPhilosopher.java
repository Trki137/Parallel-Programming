package philosopher;

import mpi.Comm;

import java.time.format.DateTimeFormatter;

public abstract class AbstractPhilosopher implements Philosopher {
    private static final int min = 1;
    private static final int max = 5;
    protected static final DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");

    @Override
    public void loop() throws InterruptedException {
        while (true) {
            think((long) (Math.random() * (max - min + 1)) + min);
            getForks();
            eat(((long) (Math.random() * (max - min + 1)) + min));
        }
    }
}
