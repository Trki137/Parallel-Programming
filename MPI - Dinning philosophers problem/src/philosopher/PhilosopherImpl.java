package philosopher;

import mpi.Comm;
import mpi.MPI;
import mpi.Status;
import philosopher.enums.PhilosopherState;
import philosopher.enums.Tags;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

public class PhilosopherImpl extends AbstractPhilosopher {
    private static final int WAIT_TIME = 1000;
    private final Integer myRank;
    private final Integer numOfProcesses;
    private final Comm communicator;
    private final Fork[] forks;
    private PhilosopherState philosopherState;
    private Set<Integer> queueReq = new HashSet<>();

    public PhilosopherImpl(Integer myRank, Comm communicator) throws InterruptedException {
        super();
        this.myRank = myRank;
        this.communicator = communicator;
        this.numOfProcesses = communicator.Size();
        this.forks = new Fork[]{null, null};
        if (myRank == 0) {
            this.forks[0] = new Fork();
            this.forks[1] = new Fork();
        } else if (myRank < communicator.Size() - 1) {
            this.forks[0] = new Fork();
            this.forks[1] = null;
        }

        loop();
    }

    @Override
    public void think(Long seconds) throws InterruptedException {
        this.philosopherState = PhilosopherState.THINK;
        print(this.philosopherState.getStatement(), seconds);

        checkQueue();

        final LocalDateTime endTime = LocalDateTime.now().plusSeconds(seconds);
        do {
            Thread.sleep(WAIT_TIME);
            checkMessages();

        } while (!LocalDateTime.now().isAfter(endTime));
    }


    @Override
    public void getForks() throws InterruptedException {
        this.philosopherState = PhilosopherState.FORK_SEARCHING;

        final int leftSource = getLeftPhilosopherRank();
        final int rightSource = getRightPhilosopherRank();

        while (this.forks[0] == null || this.forks[1] == null) {
            if (this.forks[0] == null) {
                print(String.format("%s {%d} (Lijeva vilica)", this.philosopherState.getStatement(), leftSource), null);
                sendMessage(leftSource, Tags.SEND_FORK_REQUEST_TAG);
            }

            if (this.forks[1] == null) {
                print(String.format("%s {%d} (Desna vilica)", this.philosopherState.getStatement(), rightSource), null);
                sendMessage(rightSource, Tags.SEND_FORK_REQUEST_TAG);
            }

            while (true) {
                Thread.sleep(1000);

                Status leftStatus = communicator.Iprobe(leftSource, MPI.ANY_TAG);
                Status rightStatus = communicator.Iprobe(rightSource, MPI.ANY_TAG);

                boolean gotLeftFork = checkStatus(leftStatus, leftSource, 0);
                boolean gotRightFork = checkStatus(rightStatus, rightSource, 1);

                if (gotLeftFork || gotRightFork) break;
            }
        }
    }

    @Override
    public void eat(Long seconds) throws InterruptedException {
        this.philosopherState = PhilosopherState.EAT;
        print(this.philosopherState.getStatement(), seconds);

        Thread.sleep(seconds * 1000);

        for (Fork fork : this.forks) {
            fork.setDirty(true);
        }
    }

    private void checkMessages() {
        final int leftSource = getLeftPhilosopherRank();
        final int rightSource = getRightPhilosopherRank();

        final Status leftStatus = communicator.Iprobe(leftSource, MPI.ANY_TAG);
        final Status rightStatus = communicator.Iprobe(rightSource, MPI.ANY_TAG);

        checkForkReq(leftStatus, leftSource, 0);
        checkForkReq(rightStatus, rightSource, 1);

    }

    private void checkForkReq(Status status, int source, int index) {
        if (status != null) {
            receiveMessage(source);
            if (Tags.SEND_FORK_REQUEST_TAG.getTag() == status.tag) {
                if (this.forks[index] != null && this.forks[index].isDirty()) {
                    sendMessage(source, Tags.ACCEPTED_FORK_REQUEST_TAG);
                    this.forks[index] = null;
                }
            }
        }
    }

    private boolean checkStatus(Status status, int source, int index) {
        final int leftSource = getLeftPhilosopherRank();
        final String phil;

        if (status != null) {
            receiveMessage(source);
            if (Tags.ACCEPTED_FORK_REQUEST_TAG.getTag() == status.tag) {
                if (leftSource == source){
                    phil = "Lijevog filozofa";
                }else {
                    phil = "Desnog filozofa";
                }
                print(String.format("Dobio vilicu od {%d} (%s)",source,phil), null);
                this.forks[index] = new Fork(false);
                return true;
            } else if (Tags.SEND_FORK_REQUEST_TAG.getTag() == status.tag) {
                if (this.forks[index] != null && this.forks[index].isDirty()) {
                    if (leftSource == source){
                        phil = "Lijevom filozofu";
                    }else {
                        phil = "Desnom filozofu";
                    }
                    print(String.format("Šaljem vilicu prema {%d}, (%s)", source, phil),null);
                    sendMessage(source, Tags.ACCEPTED_FORK_REQUEST_TAG);
                    this.forks[index] = null;
                    return false;
                } else {
                    queueReq.add(status.source);
                }
            }
        }

        return false;
    }

    private void print(String statement, Long seconds) {
        final String tab = "\t".repeat(this.myRank);
        final String sec = String.format("(%d sec)", seconds);
        final String msg;
        if (seconds == null){
            msg = String.format("[%s] %s philosopher.Philosopher %d.: %s", timeFormatter.format(LocalDateTime.now()), tab, this.myRank, statement);
        }else {
            msg = String.format("[%s] %s philosopher.Philosopher %d.: %s %s", timeFormatter.format(LocalDateTime.now()), tab, this.myRank, statement, sec);
        }
        System.out.println(msg);
    }

    private void sendMessage(int source, Tags tag) {
        communicator.Isend(
                new byte[]{1},
                0,
                1,
                MPI.BYTE,
                source,
                tag.getTag()
        );
    }

    private void receiveMessage(int source) {
        communicator.Irecv(
                new byte[]{1},
                0,
                1,
                MPI.BYTE,
                source,
                MPI.ANY_TAG
        );
    }

    private void checkQueue() {
        if (queueReq.isEmpty()) return;

        print("Red nije prazan", null);

        for (int source : queueReq){
            print("Šaljem vilicu procesu s brojem " + source, null);
            sendMessage(source, Tags.ACCEPTED_FORK_REQUEST_TAG);
            if (source == getLeftPhilosopherRank()) {
                this.forks[0] = null;
            } else {
                this.forks[1] = null;
            }
        }

        queueReq = new HashSet<>();
    }

    private int getLeftPhilosopherRank() {
        return this.myRank == this.numOfProcesses - 1 ? 0 : this.myRank + 1;
    }

    private int getRightPhilosopherRank() {
        return this.myRank == 0 ? this.numOfProcesses - 1 : this.myRank - 1;
    }
}
