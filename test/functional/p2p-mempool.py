#!/usr/bin/env python3
# Copyright (c) 2015-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.mininode import *
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import *


class P2PMempoolTests(BitcoinTestFramework):

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 2

    def setup_network(self):
        self.nodes = [start_node(0, self.options.tmpdir, [
                                 "-peerbloomfilters=0"])]

    def run_test(self):
        # connect a mininode
        aTestNode = NodeConnCB()
        node = NodeConn('127.0.0.1', p2p_port(0), self.nodes[0], aTestNode)
        aTestNode.add_connection(node)
        NetworkThread().start()
        aTestNode.wait_for_verack()

        # request mempool
        aTestNode.send_message(msg_mempool())
        aTestNode.wait_for_disconnect()

        # mininode must be disconnected at this point
        assert_equal(len(self.nodes[0].getpeerinfo()), 0)


if __name__ == '__main__':
    P2PMempoolTests().main()
