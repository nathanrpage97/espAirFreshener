
// internal-variables (default values)
int last_spray_time = -1;
int interval = 600;
bool spray_now = false;
bool spray_on = true;
int current_time = 0;
int sleep_time = 0;

// corresponding state the machine is in
int state = 0;

// analysis tool
int wake_itr;
int spray_count = 0;


active proctype Main() {
    for (wake_itr : 0..99) {
        do
        :: (state != 5) -> {
            if
            :: (state == 0) -> {
                state = 1;
            }
            :: (state == 1) -> {
                bool connect_network = true;
                if
                :: (connect_network) -> {
                    state = 2;
                }
                :: else -> {
                    current_time = current_time + sleep_time;
                    state = 3;
                }
                fi
            }
            :: (state == 2) -> {
                // get server information
                // assume it always connects to the server for now
                bool connect_server = true;

                if
                :: (connect_server) ->  atomic {
                    interval = 600;
                    spray_now = false;
                    spray_on = true;
                    current_time = wake_itr * 60;
                }
                :: else ->  atomic {
                    current_time = current_time + sleep_time;
                }
                fi
                state = 3;
            }
            :: (state == 3) -> {
                spray_count = spray_count + 1;
                state = 4;
            }
            :: (state == 4) -> {
                // go to sleep
                sleep_time = (last_spray_time + interval - current_time) % 60;
                if
                :: (sleep_time == 0) -> {sleep_time = 60}
                fi
                assert(sleep_time > 0 && sleep_time <= 60);
                // sleep state
                state = 5;
            }
            fi
        }
        :: else -> break;
        od
        state = 0;
    }
}

/* active proctype Main() {

    // bounded model check of 100 wakes
    for (wake_itr : 0..99) {
        assert(current_time >= last_spray_time);
        do
        :: (state != 5) -> {
            if
            :: (state == 0) -> {
                // INIT state, not much to model here as it is mostly hw config
                state = 1;
            }
            :: (state == 1) -> {
                // connect to network
                // assume it always connects to the network for now
                bool connect_network = true;

                if
                :: (connect_network) -> d_step {
                    state = 2;
                }
                :: else -> d_step {
                    current_time = current_time + sleep_time;
                    state = 3;
                }
                fi
            }
            :: (state == 2) -> {
                // get server information
                // assume it always connects to the server for now
                bool connect_server = true;

                if
                :: (connect_server) -> d_step {
                    interval = 600;
                    spray_now = false;
                    spray_on = true;
                    current_time = wake_itr * 60;
                }
                :: else -> d_step {
                    current_time = current_time + sleep_time;
                }
                fi
                state = 3;
            }
            :: (state == 3) -> {
                // check to spray
                if
                :: (!spray_on || last_spray_time == -1) -> {
                    last_spray_time = current_time;
                }
                :: (spray_on && current_time + 5 >= last_spray_time + interval) -> {
                    spray_count = spray_count + 1;
                    last_spray_time = current_time;
                }
                fi

                if
                :: (spray_now) -> {
                    spray_count = spray_count + 1;
                }
                fi
                state = 4;
            }
            :: (state == 4) -> {
                // go to sleep
                sleep_time = (last_spray_time + interval - current_time) % 60;
                assert(sleep_time >= 0 && sleep_time <= 60);
                // sleep state
                state = 5;
            }
            fi
        }
        :: else -> break;
        od

        state = 0;
    }
} */

ltl invariant1 {<>[](spray_count > 0)}
