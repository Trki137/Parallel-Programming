package philosopher.enums;

public enum PhilosopherState {
    EAT("Jedem"),
    THINK("Mislim"),
    FORK_SEARCHING("Tražim vilicu");

    private final String statement;

    PhilosopherState(String statement) {
        this.statement = statement;
    }

    public String getStatement() {
        return statement;
    }
}
