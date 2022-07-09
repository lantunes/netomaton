__version__ = "1.2.0"

from .evolution import evolve_topology, init_simple2d, init_random, check_np, do_activity_rule, evolve_activities, \
    NodeContext, UpdateOrder, init_simple, evolve, TopologyContext, PerturbationContext, MemoizationKey

from .asynchronous_rule import AsynchronousRule

from .hopfield_net import HopfieldNet

from .reversible_rule import ReversibleRule

from .analysis import shannon_entropy, mutual_information, joint_shannon_entropy, average_mutual_information, \
    average_node_entropy

from .rule_tables import table_walk_through, random_rule_table, table_rule

from .hexplot import plot_hex_grid, animate_hex

from .sandpile import Sandpile

from .turing_machine import HeadCentricTuringMachine, TapeCentricTuringMachine, TuringMachine

from .utils import animate_activities, binarize_for_plotting, animate_L_system, animate_network, animate_plot1D, \
    bifurcation_plot, get_activities_over_time_as_list, plot_activities, plot_degree_distribution, plot_grid_multiple, \
    plot_L_system, poincare_plot, plot_grid, plot_network, plot1D, ncr

from .hopfield_tank_tsp_net import HopfieldTankTSPNet

from .substitution_system import SubstitutionSystem

from .wolfram_physics_model import WolframPhysicsModel

from .fungal_growth_model import FungalGrowthModel

from .state import State, Network

from .turtle import Turtle

from .ctrbl_rule import CTRBLRule, VonNeumannNeighbourhood

from .langtons_loop import LangtonsLoop

from . import topology
from . import rules
from . import vis
