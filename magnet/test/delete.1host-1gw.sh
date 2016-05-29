ip netns exec qgw ip link set veth0 down
ip netns exec qgw ip link set lo down
ip link set dev qgw-veth0.t down
brctl delif vbr-pext qgw-veth0.t
ip link delete qgw-veth0.t
ip netns delete qgw
ip netns exec qhost1 ip link set veth0 down
ip netns exec qhost1 ip link set lo down
ip link set dev qhost1-veth0.t down
brctl delif vbr-pext qhost1-veth0.t
ip link delete qhost1-veth0.t
ip netns delete qhost1
ip link set dev vbr-pext down
brctl delbr vbr-pext
