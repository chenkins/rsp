import networkx as nx
from flatland.envs.rail_trainrun_data_structures import TrainrunWaypoint
from flatland.envs.rail_trainrun_data_structures import Waypoint

from rsp.schedule_problem_description.data_types_and_utils import get_sinks_for_topo
from rsp.schedule_problem_description.route_dag_constraints.route_dag_generator_utils import propagate_earliest
from rsp.schedule_problem_description.route_dag_constraints.route_dag_generator_utils import propagate_latest
from rsp.utils.data_types import RouteDAGConstraints


def _get_route_dag_constraints_for_scheduling(
        topo: nx.DiGraph,
        source_waypoint: Waypoint,
        minimum_travel_time: int,
        latest_arrival: int
) -> RouteDAGConstraints:
    return RouteDAGConstraints(
        freeze_visit=[],
        freeze_earliest=propagate_earliest(
            banned_set=set(),
            earliest_dict={source_waypoint: 0},
            minimum_travel_time=minimum_travel_time,
            force_freeze_dict={},
            subdag_source=TrainrunWaypoint(waypoint=source_waypoint, scheduled_at=0),
            topo=topo,
        ),
        freeze_latest=propagate_latest(
            banned_set=set(),
            latest_dict={sink: latest_arrival - 1 for sink in get_sinks_for_topo(topo)},
            earliest_dict={},
            latest_arrival=latest_arrival,
            minimum_travel_time=minimum_travel_time,
            force_freeze_dict={},
            topo=topo,
        ),
        freeze_banned=[],
    )