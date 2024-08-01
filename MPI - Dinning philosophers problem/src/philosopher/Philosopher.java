package philosopher;

public interface Philosopher {
    void loop() throws InterruptedException;

    void think(Long seconds) throws InterruptedException;

    void getForks() throws InterruptedException;

    void eat(Long seconds) throws InterruptedException;
}
