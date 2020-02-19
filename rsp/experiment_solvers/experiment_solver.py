import pprint
from typing import Callable

from flatland.action_plan.action_plan import ControllerFromTrainruns
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_trainrun_data_structures import TrainrunDict

from rsp.experiment_solvers.asp.asp_problem_description import ASPProblemDescription
from rsp.experiment_solvers.asp.asp_solve_problem import replay
from rsp.experiment_solvers.asp.asp_solve_problem import solve_problem
from rsp.experiment_solvers.data_types import SchedulingExperimentResult
from rsp.experiment_solvers.experiment_solver_utils import create_action_plan
from rsp.route_dag.generators.route_dag_generator_reschedule_full import get_freeze_for_full_rescheduling
from rsp.route_dag.generators.route_dag_generator_reschedule_perfect_oracle import perfect_oracle
from rsp.route_dag.generators.route_dag_generator_schedule import schedule_problem_description_from_rail_env
from rsp.route_dag.route_dag import ScheduleProblemDescription
from rsp.utils.data_types import experimentFreezeDictPrettyPrint
from rsp.utils.data_types import ExperimentMalfunction
from rsp.utils.data_types import ExperimentResults
from rsp.utils.experiment_solver import AbstractSolver


class ASPExperimentSolver(AbstractSolver):
    """Implements `AbstractSolver` for ASP.

    Methods
    -------
    run_experiment_trial:
        Returns the correct data format to run tests on full research pipeline
    """
    _pp = pprint.PrettyPrinter(indent=4)

    def run_experiment_trial(
            self,
            static_rail_env: RailEnv,
            malfunction_rail_env: RailEnv,
            malfunction_env_reset,
            k: int = 10,
            disable_verification_by_replay: bool = False,
            verbose: bool = False,
            debug: bool = False,
            rendering: bool = False
    ) -> ExperimentResults:
        """Runs the experiment.

        Parameters
        ----------
        static_rail_env: RailEnv
            Rail environment without any malfunction
        malfunction_rail_env: RailEnv
            Rail environment with one single malfunction

        Returns
        -------
        ExperimentResults
        """
        rendering = True
        tc_schedule_problem = schedule_problem_description_from_rail_env(static_rail_env, k)
        schedule_result = asp_schedule_wrapper(tc_schedule_problem,
                                               rendering=rendering,
                                               static_rail_env=static_rail_env,
                                               debug=debug)

        schedule_trainruns: TrainrunDict = schedule_result.trainruns_dict

        if verbose:
            print(f"  **** schedule_solution={schedule_trainruns}")

        # --------------------------------------------------------------------------------------
        # 1. Generate malfuntion
        # --------------------------------------------------------------------------------------

        malfunction_env_reset()
        controller_from_train_runs: ControllerFromTrainruns = create_action_plan(
            train_runs_dict=schedule_trainruns,
            env=malfunction_rail_env)
        malfunction_env_reset()
        malfunction = replay(
            controller_from_train_runs=controller_from_train_runs,
            env=malfunction_rail_env,
            stop_on_malfunction=True,
            solver_name="ASP",
            disable_verification_in_replay=True)
        if malfunction is None:
            return None
        malfunction_env_reset()
        # replay may return None (if the given malfunction does not happen during the agents time in the grid
        if malfunction is None:
            raise Exception("Could not produce a malfunction")

        if verbose:
            print(f"  **** malfunction={malfunction}")

        # --------------------------------------------------------------------------------------
        # 2. Re-schedule Full
        # --------------------------------------------------------------------------------------
        full_reschedule_result = asp_reschedule_wrapper(
            malfunction=malfunction,
            malfunction_env_reset=malfunction_env_reset,
            malfunction_rail_env=malfunction_rail_env,
            tc=get_freeze_for_full_rescheduling(
                malfunction=malfunction,
                schedule_trainruns=schedule_trainruns,
                minimum_travel_time_dict=tc_schedule_problem.minimum_travel_time_dict,
                latest_arrival=malfunction_rail_env._max_episode_steps,
                topo_dict=tc_schedule_problem.topo_dict
            ),
            rendering=rendering,
            debug=debug
        )
        malfunction_env_reset()

        full_reschedule_trainruns = full_reschedule_result.trainruns_dict

        if verbose:
            print(f"  **** full re-schedule_solution=\n{full_reschedule_trainruns}")

        # --------------------------------------------------------------------------------------
        # 3. Re-Schedule Delta
        # --------------------------------------------------------------------------------------
        delta_reschedule_problem = perfect_oracle(
            full_reschedule_trainrun_waypoints_dict=full_reschedule_trainruns,
            malfunction=malfunction,
            # TODO SIM-146 code smell: why do we need env????
            max_episode_steps=tc_schedule_problem.max_episode_steps,
            schedule_topo_dict=tc_schedule_problem.topo_dict,
            schedule_trainrun_dict=schedule_trainruns,
            minimum_travel_time_dict=tc_schedule_problem.minimum_travel_time_dict
        )
        delta_reschedule_result = asp_reschedule_wrapper(
            malfunction=malfunction,
            malfunction_rail_env=malfunction_rail_env,
            tc=delta_reschedule_problem,
            rendering=rendering,
            debug=debug,
            malfunction_env_reset=lambda *args, **kwargs: None
        )
        malfunction_env_reset()

        if verbose:
            print(f"  **** delta re-schedule solution")
            print(delta_reschedule_result.trainruns_dict)

        # --------------------------------------------------------------------------------------
        # 4. Result
        # --------------------------------------------------------------------------------------
        current_results = ExperimentResults(time_full=schedule_result.solve_time,
                                            time_full_after_malfunction=full_reschedule_result.solve_time,
                                            time_delta_after_malfunction=delta_reschedule_result.solve_time,
                                            solution_full=schedule_result.trainruns_dict,
                                            solution_full_after_malfunction=full_reschedule_result.trainruns_dict,
                                            solution_delta_after_malfunction=delta_reschedule_result.trainruns_dict,
                                            costs_full=schedule_result.optimization_costs,
                                            costs_full_after_malfunction=full_reschedule_result.optimization_costs,
                                            costs_delta_after_malfunction=delta_reschedule_result.optimization_costs,
                                            route_dag_constraints_full=schedule_result.route_dag_constraints,
                                            route_dag_constraints_full_after_malfunction=full_reschedule_result.route_dag_constraints,
                                            route_dag_constraints_delta_after_malfunction=delta_reschedule_result.route_dag_constraints,
                                            malfunction=malfunction,
                                            topo_dict=tc_schedule_problem.topo_dict,
                                            nb_resource_conflicts_full=schedule_result.nb_conflicts,
                                            nb_resource_conflicts_full_after_malfunction=full_reschedule_result.nb_conflicts,
                                            nb_resource_conflicts_delta_after_malfunction=delta_reschedule_result.nb_conflicts
                                            )
        return current_results


_pp = pprint.PrettyPrinter(indent=4)


def asp_schedule_wrapper(tc: ScheduleProblemDescription,
                         static_rail_env: RailEnv,
                         rendering: bool = False,
                         debug: bool = False,
                         ) -> SchedulingExperimentResult:
    """Solves the Full Scheduling Problem for static rail env (i.e. without
    malfunctions).

    Parameters
    ----------
    k:int
        number of routing alterantives to consider
    static_rail_env: RailEnv
    rendering: bool
    debug: bool

    Returns
    -------
    SchedulingExperimentResult
        the problem description and the results
    """

    # --------------------------------------------------------------------------------------
    # Produce a full schedule
    # --------------------------------------------------------------------------------------
    schedule_problem = ASPProblemDescription.factory_scheduling(
        tc=tc)

    schedule_result, schedule_solution = solve_problem(
        env=static_rail_env,
        problem=schedule_problem,
        rendering=rendering,
        debug=debug)

    return schedule_result


def asp_reschedule_wrapper(
        tc: ScheduleProblemDescription,
        malfunction: ExperimentMalfunction,
        malfunction_rail_env: RailEnv,
        malfunction_env_reset: Callable[[], None],
        debug: bool = False,
        rendering: bool = False
) -> SchedulingExperimentResult:
    """Solve the Full Re-Scheduling Problem for static rail env (i.e. without
    malfunctions).

    Returns
    -------
    SchedulingExperimentResult
    """

    # --------------------------------------------------------------------------------------
    # Full Re-Scheduling
    # --------------------------------------------------------------------------------------
    full_reschedule_problem: ASPProblemDescription = ASPProblemDescription.factory_rescheduling(
        tc=tc
    )

    if debug:
        print("###reschedule")
        experimentFreezeDictPrettyPrint(tc.route_dag_constraints_dict)

    full_reschedule_result, full_reschedule_solution = solve_problem(
        env=malfunction_rail_env,
        problem=full_reschedule_problem,
        rendering=rendering,
        debug=debug,
        expected_malfunction=malfunction,
        # SIM-155 decision: we do not replay against FLATland any more but check the solution on the Trainrun data structure
        disable_verification_in_replay=True
    )
    malfunction_env_reset()

    if debug:
        print("###reschedule")
        print(_pp.pformat(full_reschedule_result.solution.get_trainruns_dict()))

    return full_reschedule_result