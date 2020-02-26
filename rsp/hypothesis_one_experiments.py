from typing import Dict
from typing import Tuple

from rsp.experiment_solvers.experiment_solver import ASPExperimentSolver
from rsp.hypothesis_one_data_analysis import hypothesis_one_data_analysis
from rsp.utils.data_types import ParameterRanges
from rsp.utils.experiments import create_experiment_agenda
from rsp.utils.experiments import run_experiment_agenda


def get_pipeline_params() -> Tuple[ParameterRanges, Dict[float, float]]:
    # Define the parameter ranges we would like to test
    parameter_ranges = ParameterRanges(agent_range=[2, 150, 40],
                                       size_range=[30, 150, 20],
                                       in_city_rail_range=[6, 6, 1],
                                       out_city_rail_range=[2, 2, 1],
                                       city_range=[20, 20, 1],
                                       earliest_malfunction=[20, 20, 1],
                                       malfunction_duration=[20, 20, 1],
                                       number_of_shortest_paths_per_agent=[10, 10, 1])
    # Define the desired speed profiles
    speed_data = {1.: 1.,  # Fast passenger train
                  1. / 2.: 0.,  # Fast freight train
                  1. / 3.: 0.,  # Slow commuter train
                  1. / 4.: 0.}  # Slow freight train
    return parameter_ranges, speed_data


def get_first_agenda_pipeline_params() -> Tuple[ParameterRanges, Dict[float, float]]:
    parameter_ranges = ParameterRanges(agent_range=[2, 50, 30],
                                       size_range=[30, 50, 10],
                                       in_city_rail_range=[6, 6, 1],
                                       out_city_rail_range=[2, 2, 1],
                                       city_range=[20, 20, 1],
                                       earliest_malfunction=[20, 20, 1],
                                       malfunction_duration=[20, 20, 1],
                                       number_of_shortest_paths_per_agent=[10, 10, 1])
    # Define the desired speed profiles
    speed_data = {1.: 1.,  # Fast passenger train
                  1. / 2.: 0.,  # Fast freight train
                  1. / 3.: 0.,  # Slow commuter train
                  1. / 4.: 0.}  # Slow freight train
    return parameter_ranges, speed_data


if __name__ == '__main__':
    parameter_ranges, speed_data = get_first_agenda_pipeline_params()

    # Create an experiment agenda out of the parameter ranges
    experiment_agenda = create_experiment_agenda(experiment_name="exp_hypothesis_one",
                                                 speed_data=speed_data,
                                                 parameter_ranges=parameter_ranges,
                                                 trials_per_experiment=1
                                                 )

    # Import the solver for the experiments
    solver = ASPExperimentSolver()

    # Run experiments
    experiment_folder_name = run_experiment_agenda(
        solver=solver,
        experiment_agenda=experiment_agenda,
        run_experiments_parallel=True,
        show_results_without_details=False,
        verbose=False)

    hypothesis_one_data_analysis(
        data_folder=experiment_folder_name,
        analysis_2d=True,
        analysis_3d=False,
        malfunction_analysis=False,
        qualitative_analysis_experiment_ids=range(len(experiment_agenda.experiments))
    )
