inkling "2.0"
using Math
using Goal

type SimConfig {
    n_cities: number,
}

type SimState {
    n_cities: number,
    score: number,
    seconds_run: number,
}

type ObservableState {
    n_cities: number,
}

type SimAction {
    pop_size: number<10 .. 1000 step 10>,
    generations: number<10 .. 500 step 10>,
    elite_size: number<0 .. 100 step 5>,
    mutation_rate: number<0.0 .. 1.0 step 0.05>
}

function Reward(state: SimState) {
    return -(state.score + state.seconds_run)/ state.n_cities
}

function Terminal(state: SimState) {
    if state.score <= 0 {
        return false
    }
    return true
}

simulator Simulator(action: SimAction, config: SimConfig): SimState {
}

graph (input: ObservableState): SimAction {
    concept TuneHyperparams(input): SimAction {
        curriculum {
            source Simulator
            reward Reward
            terminal Terminal

            lesson VaryCities {
                scenario {
                    n_cities: number<3 .. 20 step 1>,
                }
            }
        }
    }
}
