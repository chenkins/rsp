"""Run experiments not in parallel, only one trial and only a subset of them in
order to allow for debugging."""
from rsp.hypothesis_one_experiments import get_pipeline_params
from rsp.solvers.asp.asp_experiment_solver import ASPExperimentSolver
from rsp.utils.experiments import create_experiment_agenda
from rsp.utils.experiments import run_specific_experiments_from_research_agenda

if __name__ == '__main__':
    parameter_ranges, speed_data = get_pipeline_params()

    # Create an experiment agenda out of the parameter ranges
    experiment_agenda = create_experiment_agenda(experiment_name="exp_hypothesis_one",
                                                 speed_data=speed_data,
                                                 parameter_ranges=parameter_ranges,
                                                 trials_per_experiment=1)

    # Import the solver for the experiments
    solver = ASPExperimentSolver()

    # Run experiments
    run_specific_experiments_from_research_agenda(
        solver=solver,
        experiment_agenda=experiment_agenda,
        experiment_ids=list(range(200, 301)),
        run_experiments_parallel=True,
        show_results_without_details=False,
        verbose=False)
