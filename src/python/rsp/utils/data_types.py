"""Data types used in the experiment for the real time rescheduling research
project."""
import pprint
from typing import Dict
from typing import List
from typing import Mapping
from typing import NamedTuple
from typing import Tuple

from rsp.schedule_problem_description.data_types_and_utils import RouteDAGConstraints
from rsp.schedule_problem_description.data_types_and_utils import RouteDAGConstraintsDict

SpeedData = Mapping[float, float]

# @deprecated(reason="You should use hiearchy level ranges.")
ParameterRanges = NamedTuple(
    "ParameterRanges",
    [
        # infrastructure and agent placement
        # 0: size_range
        ("size_range", List[int]),
        # 1: agent_range
        ("agent_range", List[int]),
        # 2: in_city_rail_range
        ("in_city_rail_range", List[int]),
        # 3: out_city_rail_range
        ("out_city_rail_range", List[int]),
        # 4: city_range
        ("city_range", List[int]),
        # malfunction
        # 5: earliest_malfunction
        ("earliest_malfunction", List[int]),
        # 6: malfunction_duration
        ("malfunction_duration", List[int]),
        # rescheduling
        # 7: number_of_shortest_paths_per_agent
        ("number_of_shortest_paths_per_agent", List[int]),
        # 8: max_window_size_from_earliest
        ("max_window_size_from_earliest", List[int]),
        # 9: asp_seed_value
        ("asp_seed_value", List[int]),
        # 10: weight_route_change
        ("weight_route_change", List[int]),
        # 11: weight_lateness_seconds
        ("weight_lateness_seconds", List[int]),
    ],
)
# @deprecated(reason="You should use hiearchy level ranges.")
ParameterRangesAndSpeedData = NamedTuple("ParameterRangesAndSpeedData", [("parameter_ranges", ParameterRanges), ("speed_data", SpeedData)])

InfrastructureParameters = NamedTuple(
    "InfrastructureParameters",
    [
        ("infra_id", int),
        ("width", int),
        ("height", int),
        ("flatland_seed_value", int),
        ("max_num_cities", int),
        ("grid_mode", bool),
        ("max_rail_between_cities", int),
        ("max_rail_in_city", int),
        ("number_of_agents", int),
        ("speed_data", SpeedData),
        ("number_of_shortest_paths_per_agent", int),
    ],
)

InfrastructureParametersRange = NamedTuple(
    "InfrastructureParameters",
    [
        ("width", List[int]),
        ("height", List[int]),
        ("flatland_seed_value", List[int]),
        ("max_num_cities", List[int]),
        ("max_rail_between_cities", List[int]),
        ("max_rail_in_city", List[int]),
        ("number_of_agents", List[int]),
        ("number_of_shortest_paths_per_agent", List[int]),
    ],
)

ScheduleParameters = NamedTuple(
    "ScheduleParameters", [("infra_id", int), ("schedule_id", int), ("asp_seed_value", int), ("number_of_shortest_paths_per_agent_schedule", int)]
)

ScheduleParametersRange = NamedTuple("ScheduleParametersRange", [("asp_seed_value", List[int]), ("number_of_shortest_paths_per_agent_schedule", List[int])])

ReScheduleParametersRange = NamedTuple(
    "ReScheduleParametersRange",
    [
        # 5: earliest_malfunction
        ("earliest_malfunction", List[int]),
        # 6: malfunction_duration
        ("malfunction_duration", List[int]),
        #
        ("malfunction_agent_id", List[int]),
        # rescheduling
        # 7: number_of_shortest_paths_per_agent
        ("number_of_shortest_paths_per_agent", List[int]),
        # 8: max_window_size_from_earliest
        ("max_window_size_from_earliest", List[int]),
        # 9: asp_seed_value
        ("asp_seed_value", List[int]),
        # 10: weight_route_change
        ("weight_route_change", List[int]),
        # 11: weight_lateness_seconds
        ("weight_lateness_seconds", List[int]),
    ],
)

ReScheduleParameters = NamedTuple(
    "ReScheduleParameters",
    [
        # 5: earliest_malfunction
        ("earliest_malfunction", int),
        # 6: malfunction_duration
        ("malfunction_duration", int),
        ("malfunction_agent_id", int),
        # rescheduling
        # 7: number_of_shortest_paths_per_agent
        ("number_of_shortest_paths_per_agent", int),
        # 8: max_window_size_from_earliest
        ("max_window_size_from_earliest", int),
        # 9: asp_seed_value
        ("asp_seed_value", int),
        # 10: weight_route_change
        ("weight_route_change", int),
        # 11: weight_lateness_seconds
        ("weight_lateness_seconds", int),
    ],
)

# the experiment_id is unambiguous within the agenda for the full parameter set!
ExperimentParameters = NamedTuple(
    "ExperimentParameters",
    [
        ("experiment_id", int),  # unique per execution (there may be multiple `experiment_id`s for the same `grid_id`
        ("grid_id", int),  # same if all params are the same
        ("infra_id_schedule_id", int),
        ("infra_parameters", InfrastructureParameters),
        ("schedule_parameters", ScheduleParameters),
        ("earliest_malfunction", int),
        ("malfunction_duration", int),
        ("malfunction_agent_id", int),
        ("weight_route_change", int),
        ("weight_lateness_seconds", int),
        ("max_window_size_from_earliest", int),
    ],
)

ExperimentAgenda = NamedTuple("ExperimentAgenda", [("experiment_name", str), ("experiments", List[ExperimentParameters])])


def parameter_ranges_and_speed_data_to_hiearchical(
    parameter_ranges_and_speed_data: ParameterRangesAndSpeedData, flatland_seed_value: int = 12
) -> Tuple[InfrastructureParametersRange, SpeedData, ScheduleParametersRange, ReScheduleParametersRange]:
    return (
        InfrastructureParametersRange(
            width=parameter_ranges_and_speed_data.parameter_ranges.size_range,
            height=parameter_ranges_and_speed_data.parameter_ranges.size_range,
            flatland_seed_value=[flatland_seed_value, flatland_seed_value, 1],
            max_num_cities=parameter_ranges_and_speed_data.parameter_ranges.city_range,
            max_rail_in_city=parameter_ranges_and_speed_data.parameter_ranges.in_city_rail_range,
            max_rail_between_cities=parameter_ranges_and_speed_data.parameter_ranges.out_city_rail_range,
            number_of_agents=parameter_ranges_and_speed_data.parameter_ranges.agent_range,
            number_of_shortest_paths_per_agent=parameter_ranges_and_speed_data.parameter_ranges.number_of_shortest_paths_per_agent,
        ),
        parameter_ranges_and_speed_data.speed_data,
        ScheduleParametersRange(
            asp_seed_value=parameter_ranges_and_speed_data.parameter_ranges.asp_seed_value,
            # TODO SIM-622 hard-code to 1/evaluate
            number_of_shortest_paths_per_agent_schedule=parameter_ranges_and_speed_data.parameter_ranges.number_of_shortest_paths_per_agent,
        ),
        ReScheduleParametersRange(
            earliest_malfunction=parameter_ranges_and_speed_data.parameter_ranges.earliest_malfunction,
            malfunction_duration=parameter_ranges_and_speed_data.parameter_ranges.malfunction_duration,
            malfunction_agent_id=[0, 0, 1],
            number_of_shortest_paths_per_agent=parameter_ranges_and_speed_data.parameter_ranges.number_of_shortest_paths_per_agent,
            max_window_size_from_earliest=parameter_ranges_and_speed_data.parameter_ranges.max_window_size_from_earliest,
            asp_seed_value=parameter_ranges_and_speed_data.parameter_ranges.asp_seed_value,
            weight_route_change=parameter_ranges_and_speed_data.parameter_ranges.weight_route_change,
            weight_lateness_seconds=parameter_ranges_and_speed_data.parameter_ranges.weight_lateness_seconds,
        ),
    )


LeftClosedInterval = NamedTuple("LeftClosedInterval", [("from_incl", int), ("to_excl", int)])
Resource = NamedTuple("Resource", [("row", int), ("column", int)])
ResourceOccupation = NamedTuple("ResourceOccupation", [("interval", LeftClosedInterval), ("resource", Resource), ("direction", int), ("agent_id", int)])

# sorted list of non-overlapping resource occupations per resource
SortedResourceOccupationsPerResource = Dict[Resource, List[ResourceOccupation]]

# sorted list of resource occupations per agent; resource occupations overlap by release time!
SortedResourceOccupationsPerAgent = Dict[int, List[ResourceOccupation]]

# list of resource occupations per agent and time-step (there are multiple resource occupations if the previous resource is not released yet)
ResourceOccupationPerAgentAndTimeStep = Dict[Tuple[int, int], List[ResourceOccupation]]

ScheduleAsResourceOccupations = NamedTuple(
    "ScheduleAsResourceOccupations",
    [
        ("sorted_resource_occupations_per_resource", SortedResourceOccupationsPerResource),
        ("sorted_resource_occupations_per_agent", SortedResourceOccupationsPerAgent),
        ("resource_occupations_per_agent_and_time_step", ResourceOccupationPerAgentAndTimeStep),
    ],
)

TimeWindow = ResourceOccupation
# list of time windows per resource sorted by lower bound; time windows may overlap!
TimeWindowsPerResourceAndTimeStep = Dict[Tuple[Resource, int], List[TimeWindow]]

# sorted list of time windows per agent
TimeWindowsPerAgentSortedByLowerBound = Dict[int, List[TimeWindow]]

SchedulingProblemInTimeWindows = NamedTuple(
    "SchedulingProblemInTimeWindows",
    [
        ("time_windows_per_resource_and_time_step", TimeWindowsPerResourceAndTimeStep),
        ("time_windows_per_agent_sorted_by_lower_bound", TimeWindowsPerAgentSortedByLowerBound),
    ],
)

_pp = pprint.PrettyPrinter(indent=4)


def experiment_freeze_dict_pretty_print(d: RouteDAGConstraintsDict):
    for agent_id, route_dag_constraints in d.items():
        prefix = f"agent {agent_id} "
        experiment_freeze_pretty_print(route_dag_constraints, prefix)


def experiment_freeze_pretty_print(route_dag_constraints: RouteDAGConstraints, prefix: str = ""):
    print(f"{prefix}earliest={_pp.pformat(route_dag_constraints.earliest)}")
    print(f"{prefix}latest={_pp.pformat(route_dag_constraints.latest)}")
