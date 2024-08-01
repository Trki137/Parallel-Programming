package philosopher.enums;

public enum Tags {
    ACCEPTED_FORK_REQUEST_TAG(1),
    SEND_FORK_REQUEST_TAG(2);


    private final int tag;


    Tags(int tag){
        this.tag = tag;
    }

    public int getTag() {
        return tag;
    }
}
