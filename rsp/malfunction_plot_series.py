from rsp.compute_time_analysis.compute_time_analysis import extract_schedule_plotting, get_difference_in_time_space_trajectories, plot_delay_propagation_2d, \
    trajectories_from_resource_occupations_per_agent
from rsp.hypothesis_two_encounter_graph import plot_delay_propagation_graph, compute_disturbance_propagation_graph
from rsp.utils.experiments import load_and_expand_experiment_results_from_data_folder, EXPERIMENT_DATA_SUBDIRECTORY_NAME

experiment_base_directory = '../rsp-data/agent_0_malfunction_2020_06_22T11_48_47/'
agent_of_interest = 26

experiment_data_directory = f'{experiment_base_directory}/{EXPERIMENT_DATA_SUBDIRECTORY_NAME}'

# ========================================================
# Plotting differnt figures for malfunciton investigation
# #========================================================


for experiment_id in range(48):
    experiment_of_interest = experiment_id
    file_name = "../rsp-data/Call_Emma/delay_propagation_{}.png".format(str(experiment_id).zfill(5))
    file_name_2d = "../rsp-data/Call_Emma/spacial_delay_propagation_{}.png".format(str(experiment_id).zfill(5))
    exp_results_of_experiment_of_interest = load_and_expand_experiment_results_from_data_folder(
        experiment_data_folder_name=experiment_data_directory,
        experiment_ids=[experiment_of_interest],
        nonify_problem_and_results=False
    )[0]
    plotting_data = extract_schedule_plotting(experiment_result=exp_results_of_experiment_of_interest, sorting_agent_id=agent_of_interest)

    transmission_chains, distance_matrix, minimal_depth = compute_disturbance_propagation_graph(schedule_plotting=plotting_data)
    schedule_resource_occupations = plotting_data.schedule_as_resource_occupations.sorted_resource_occupations_per_agent
    schedule_trajectories = trajectories_from_resource_occupations_per_agent(schedule_resource_occupations
                                                                             , plotting_data.plotting_information)

    reschedule_resource_occupations = plotting_data.reschedule_delta_as_resource_occupations.sorted_resource_occupations_per_agent
    reschedule_trajectories = trajectories_from_resource_occupations_per_agent(reschedule_resource_occupations,
                                                                               plotting_data.plotting_information)

    changed_trajectories, changed_agents_dict = get_difference_in_time_space_trajectories(
        base_trajectories=schedule_trajectories,
        target_trajectories=reschedule_trajectories)

    # Get resource occupation and time-space trajectories for full reschedule

    plot_delay_propagation_graph(minimal_depth=minimal_depth, distance_matrix=distance_matrix, file_name=file_name, changed_agents=changed_agents_dict)

    # Compute actual changes and plot the effects of this

    plot_delay_propagation_2d(plotting_data=plotting_data,
                              delay_information=exp_results_of_experiment_of_interest.lateness_delta_after_malfunction,
                              depth_dict=minimal_depth,
                              changed_agents=changed_agents_dict,
                              file_name=file_name_2d)
