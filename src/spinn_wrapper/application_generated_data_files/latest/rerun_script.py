from spinn_front_end_common.utilities.utility_objs.executable_targets \
    import ExecutableTargets
from pacman.model.routing_tables.multicast_routing_tables \
    import MulticastRoutingTables
from pacman.model.placements.placements \
    import Placements
from pacman.model.placements.placement \
    import Placement
from pacman.model.tags.tags \
    import Tags
from spinn_machine.tags.iptag \
    import IPTag
from spinn_machine.tags.reverse_iptag \
    import ReverseIPTag
from spinn_front_end_common.utilities.reload.reload_routing_table \
    import ReloadRoutingTable
from spinn_front_end_common.utilities.reload.reload_buffered_vertex \
    import ReloadBufferedVertex
from spinn_front_end_common.utilities.notification_protocol.socket_address \
    import SocketAddress
from spinn_front_end_common.utilities.reload.reload \
    import Reload
import os
import logging
import sys

running = False
loading = False
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--run":
        running = True
    if sys.argv[i] == "--load":
        loading = True
if not running and not loading:
    running = True
    loading = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
for handler in logging.root.handlers:
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)-15s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"))

machine_name = "192.168.240.253"
version = 3
bmp_details = "None"
down_chips = "None"
down_cores = "None"
number_of_boards = None
height = None
width = None
auto_detect_bmp = False
enable_reinjection = True
scamp_connection_data = "None"
boot_port_num = None
reset_machine_on_start_up = False
max_sdram_per_chip = None

router_tables = MulticastRoutingTables()
iptags = list()
reverse_iptags = list()
app_data_runtime_folder = os.path.abspath(
    os.path.join(os.path.realpath("__file__"), os.pardir))
dsg_targets = dict()
exec_dse_on_host = True
dse_app_id = 31

buffered_tags = Tags()
buffered_placements = Placements()

wait_for_read_confirmation = True
database_socket_addresses = list()
database_file_path = r"/disk/users/mateev/catkin_ws/src/spinn_wrapper/src/spinn_wrapper/application_generated_data_files/latest/input_output_database.db"
send_start_notification = True

executable_targets = ExecutableTargets()
app_id = 30
runtime = 800000.0
time_scale_factor = 1
total_machine_timesteps = 800000
time_threshold = 5

iptags.append(
    IPTag("192.168.240.253", 0, "0.0.0.0", 17895, True)) 
reverse_iptags.append(
    ReverseIPTag("192.168.240.253", 1, 12346, 0, 0, 1))
router_tables.add_routing_table(
    ReloadRoutingTable.reload("picked_routing_table_for_1_0"))
router_tables.add_routing_table(
    ReloadRoutingTable.reload("picked_routing_table_for_0_0"))
router_tables.add_routing_table(
    ReloadRoutingTable.reload("picked_routing_table_for_1_1"))
database_socket_addresses.append(
    SocketAddress("localhost", 19996, None))
database_socket_addresses.append(
    SocketAddress("localhost", 19999, None))
dsg_targets[1, 0, 3] = \
    r"192.168.240.253_dataSpec_1_0_3.dat"
dsg_targets[0, 0, 9] = \
    r"192.168.240.253_dataSpec_0_0_9.dat"
dsg_targets[1, 1, 6] = \
    r"192.168.240.253_dataSpec_1_1_6.dat"
dsg_targets[1, 0, 1] = \
    r"192.168.240.253_dataSpec_1_0_1.dat"
dsg_targets[0, 0, 16] = \
    r"192.168.240.253_dataSpec_0_0_16.dat"
dsg_targets[1, 0, 6] = \
    r"192.168.240.253_dataSpec_1_0_6.dat"
dsg_targets[0, 0, 15] = \
    r"192.168.240.253_dataSpec_0_0_15.dat"
dsg_targets[1, 1, 7] = \
    r"192.168.240.253_dataSpec_1_1_7.dat"
dsg_targets[0, 0, 12] = \
    r"192.168.240.253_dataSpec_0_0_12.dat"
dsg_targets[1, 0, 7] = \
    r"192.168.240.253_dataSpec_1_0_7.dat"
dsg_targets[0, 0, 7] = \
    r"192.168.240.253_dataSpec_0_0_7.dat"
dsg_targets[1, 0, 4] = \
    r"192.168.240.253_dataSpec_1_0_4.dat"
dsg_targets[0, 0, 6] = \
    r"192.168.240.253_dataSpec_0_0_6.dat"
dsg_targets[1, 0, 5] = \
    r"192.168.240.253_dataSpec_1_0_5.dat"
dsg_targets[0, 0, 5] = \
    r"192.168.240.253_dataSpec_0_0_5.dat"
dsg_targets[0, 0, 4] = \
    r"192.168.240.253_dataSpec_0_0_4.dat"
dsg_targets[0, 0, 3] = \
    r"192.168.240.253_dataSpec_0_0_3.dat"
dsg_targets[1, 0, 10] = \
    r"192.168.240.253_dataSpec_1_0_10.dat"
dsg_targets[0, 0, 8] = \
    r"192.168.240.253_dataSpec_0_0_8.dat"
dsg_targets[0, 0, 2] = \
    r"192.168.240.253_dataSpec_0_0_2.dat"
dsg_targets[1, 0, 11] = \
    r"192.168.240.253_dataSpec_1_0_11.dat"
dsg_targets[1, 1, 10] = \
    r"192.168.240.253_dataSpec_1_1_10.dat"
dsg_targets[0, 0, 1] = \
    r"192.168.240.253_dataSpec_0_0_1.dat"
dsg_targets[1, 1, 9] = \
    r"192.168.240.253_dataSpec_1_1_9.dat"
dsg_targets[1, 0, 8] = \
    r"192.168.240.253_dataSpec_1_0_8.dat"
dsg_targets[0, 0, 11] = \
    r"192.168.240.253_dataSpec_0_0_11.dat"
dsg_targets[1, 0, 9] = \
    r"192.168.240.253_dataSpec_1_0_9.dat"
dsg_targets[1, 1, 1] = \
    r"192.168.240.253_dataSpec_1_1_1.dat"
dsg_targets[1, 0, 14] = \
    r"192.168.240.253_dataSpec_1_0_14.dat"
dsg_targets[0, 0, 14] = \
    r"192.168.240.253_dataSpec_0_0_14.dat"
dsg_targets[0, 0, 10] = \
    r"192.168.240.253_dataSpec_0_0_10.dat"
dsg_targets[1, 0, 15] = \
    r"192.168.240.253_dataSpec_1_0_15.dat"
dsg_targets[0, 0, 13] = \
    r"192.168.240.253_dataSpec_0_0_13.dat"
dsg_targets[1, 0, 12] = \
    r"192.168.240.253_dataSpec_1_0_12.dat"
dsg_targets[1, 1, 2] = \
    r"192.168.240.253_dataSpec_1_1_2.dat"
dsg_targets[1, 1, 3] = \
    r"192.168.240.253_dataSpec_1_1_3.dat"
dsg_targets[1, 0, 13] = \
    r"192.168.240.253_dataSpec_1_0_13.dat"
dsg_targets[1, 1, 5] = \
    r"192.168.240.253_dataSpec_1_1_5.dat"
dsg_targets[1, 1, 8] = \
    r"192.168.240.253_dataSpec_1_1_8.dat"
dsg_targets[1, 0, 16] = \
    r"192.168.240.253_dataSpec_1_0_16.dat"
dsg_targets[1, 0, 2] = \
    r"192.168.240.253_dataSpec_1_0_2.dat"
dsg_targets[1, 1, 4] = \
    r"192.168.240.253_dataSpec_1_1_4.dat"
executable_targets.add_processor(
    r"reverse_iptag_multicast_source.aplx", 0, 0, 1)
executable_targets.add_processor(
    r"live_packet_gather.aplx", 0, 0, 2)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 1)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 2)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 3)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 4)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 5)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 6)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 7)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 8)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 9)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 10)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 11)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 12)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 13)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 14)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 15)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 0, 16)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 3)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 4)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 5)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 6)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 7)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 8)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 9)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 10)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 11)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 12)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 13)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 14)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 15)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 0, 0, 16)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 1)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 2)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 3)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 4)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 5)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 6)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 7)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 8)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 9)
executable_targets.add_processor(
    r"IF_curr_exp.aplx", 1, 1, 10)

reloader = Reload(
    machine_name, version, bmp_details, down_chips,
    down_cores, number_of_boards, height, width,
    auto_detect_bmp, enable_reinjection,
    scamp_connection_data, boot_port_num,
    reset_machine_on_start_up, max_sdram_per_chip,
    router_tables, iptags, reverse_iptags,
    app_data_runtime_folder, dsg_targets,
    exec_dse_on_host, dse_app_id,
    buffered_tags, buffered_placements,
    wait_for_read_confirmation,
    database_socket_addresses, database_file_path,
    send_start_notification,
    executable_targets, app_id, runtime,
    time_scale_factor, total_machine_timesteps,
    time_threshold,
    running, loading)
