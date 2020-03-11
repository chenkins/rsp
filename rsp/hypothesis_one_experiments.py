from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

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
                                       number_of_shortest_paths_per_agent=[10, 10, 1],
                                       max_window_size_from_earliest=[np.inf, np.inf, 1])
    # Define the desired speed profiles
    speed_data = {1.: 0.25,  # Fast passenger train
                  1. / 2.: 0.25,  # Fast freight train
                  1. / 3.: 0.25,  # Slow commuter train
                  1. / 4.: 0.25}  # Slow freight train
    return parameter_ranges, speed_data


def get_first_agenda_pipeline_params() -> Tuple[ParameterRanges, Dict[float, float]]:
    parameter_ranges = ParameterRanges(agent_range=[2, 50, 30],
                                       size_range=[30, 50, 10],
                                       in_city_rail_range=[6, 6, 1],
                                       out_city_rail_range=[2, 2, 1],
                                       city_range=[20, 20, 1],
                                       earliest_malfunction=[20, 20, 1],
                                       malfunction_duration=[20, 20, 1],
                                       number_of_shortest_paths_per_agent=[10, 10, 1],
                                       max_window_size_from_earliest=[np.inf, np.inf, 1])
    # Define the desired speed profiles
    speed_data = {1.: 0.25,  # Fast passenger train
                  1. / 2.: 0.25,  # Fast freight train
                  1. / 3.: 0.25,  # Slow commuter train
                  1. / 4.: 0.25}  # Slow freight train
    return parameter_ranges, speed_data


def hypothesis_one_pipeline(parameter_ranges: ParameterRanges,
                            speed_data: Dict[float, float],
                            experiment_ids: Optional[List[int]],
                            copy_agenda_from_base_directory: Optional[str] = None):
    """
    Run full pipeline A - B - C

    Parameters
    ----------
    parameter_ranges
    speed_data
    experiment_ids
        filter for experiment ids
    copy_agenda_from_base_directory
        base directory from the same agenda with serialized schedule and malfunction.
        - if given, the schedule is not re-generated
        - if not given, a schedule is generate in a non-deterministc fashion
    """

    # A. Experiment Planning: Create an experiment agenda out of the parameter ranges
    experiment_agenda = create_experiment_agenda(
        experiment_name="exp_hypothesis_one",
        speed_data=speed_data,
        parameter_ranges=parameter_ranges,
        experiments_per_grid_element=1
    )
    # B. Experiments: setup, then run
    experiment_folder_name, experiment_data_folder = run_experiment_agenda(
        experiment_agenda=experiment_agenda,
        run_experiments_parallel=True,
        show_results_without_details=True,
        verbose=False,
        experiment_ids=experiment_ids,
        copy_agenda_from_base_directory=copy_agenda_from_base_directory
    )
    # C. Experiment Analysis
    hypothesis_one_data_analysis(
        experiment_base_directory=experiment_folder_name,
        analysis_2d=True,
        analysis_3d=False,
        qualitative_analysis_experiment_ids=[]
    )


if __name__ == '__main__':
    parameter_ranges, speed_data = get_first_agenda_pipeline_params()

    hypothesis_one_pipeline(parameter_ranges=parameter_ranges,
                            speed_data=speed_data,
                            experiment_ids=None,  # no filtering
                            copy_agenda_from_base_directory=None  # regenerate schedules
                            )
