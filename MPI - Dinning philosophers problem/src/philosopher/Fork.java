package philosopher;

public class Fork {
    private boolean isDirty;
    public Fork() {
        this(true);
    }

    public Fork(boolean isDirty) {
        this.isDirty = isDirty;
    }

    public boolean isDirty() {
        return isDirty;
    }

    public void setDirty(boolean dirty) {
        isDirty = dirty;
    }


}
