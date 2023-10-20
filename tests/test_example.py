from base import *
import unittest
import random

class TestICMP(CSE123TestBase):

    def setUp(self):
        # debug enables captured packet printing
        self.setUpEnvironment(build=True, debug=False)
        # Any other initialization goes here
        self.nodes = [
            ('client', '10.0.1.100'),
            ('server1', '192.168.2.2'),
            ('server2', '172.64.3.10')
        ]

    def tearDown(self):
        self.tearDownEnvironment()
        # Any other cleanup goes here

    def test_icmp_custom_packet(self):
        # client to server1
        sw_node_name = 'sw0'
        src_node = self.nodes[0]    # client

        recv_gw_intf = self.mininet.get(src_node[0]).defaultIntf().link.intf2.name  # Receiving interface on the router from client
        src_mac = self.mininet.get(src_node[0]).MAC()                               # Client's MAC address
        dst_mac = self.mininet.get(sw_node_name).MAC(intf=recv_gw_intf)             # Router's MAC address on interface towards the client

        # Test ICMP server 1
        self.clearPcapBuffers()
        id = random.randint(1, 65535)
        dst_node = self.nodes[1]    # Server 1
        pkt = Ether(src=src_mac, dst=dst_mac)/IP(src=src_node[1], dst=dst_node[1], id=id)/ICMP(type=8, id=0x10)   # Echo request
        sent = self.sendPacket(pkt, node=src_node[0])
        # print(f"Sent: {sent[0]}")

        icmps = self.expectPackets(dst_node[0], type='icmp', timewait_sec=0.1)
        routed = False
        for icmp in icmps:
            if icmp[0][IP].id == pkt[IP].id:
                routed = True
        self.assertTrue(routed, msg="ICMP packet was not routed between {} and {}.".format(src_node[0], dst_node[0]))

        # Test ICMP server 2
        self.clearPcapBuffers()
        id = random.randint(1, 65535)
        dst_node = self.nodes[2]    # Server 2
        pkt = Ether(src=src_mac, dst=dst_mac)/IP(src=src_node[1], dst=dst_node[1], id=id)/ICMP(type=8, id=0x10)   # Echo request
        sent = self.sendPacket(pkt, node=src_node[0])
        # print(f"Sent: {sent[0]}")

        icmps = self.expectPackets(dst_node[0], type='icmp', timewait_sec=0.1)
        routed = False
        for icmp in icmps:
            if icmp[0][IP].id == pkt[IP].id:
                routed = True
        self.assertTrue(routed, msg="ICMP packet was not routed between {} and {}.".format(src_node[0], dst_node[0]))

    def test_icmp_cmd(self):
        client = self.mininet.get("client")
        output = client.cmd(f"ping -c 1 {self.nodes[1][1]}")
        self.assertTrue("1 packets received" in output, msg="ICMP request failed between client and server1")
        output = client.cmd(f"ping -c 1 {self.nodes[2][1]}")
        self.assertTrue("1 packets received" in output, msg="ICMP request failed between client and server2")

if __name__ == "__main__":
    unittest.main()
