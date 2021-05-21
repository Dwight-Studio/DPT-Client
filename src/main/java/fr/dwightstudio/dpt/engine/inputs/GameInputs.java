package fr.dwightstudio.dpt.engine.inputs;

public enum GameInputs {
    MOVE_RIGHT('d'),
    MOVE_LEFT('q'),
    JUMP(' '),
    INTERACT('e'),
    LEFT_CLICK(0),
    RIGHT_CLICK(1),
    MIDDLE_CLICK(2);

    private int button;

    GameInputs(int button) {
        this.button = button;
    }

    public int getKey() {
        return this.button;
    }

    public void setKey(int button) {
        this.button = button;
    }
}
