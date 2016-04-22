__author__ = 'Samuele Zoppi'

import os
import matplotlib.pyplot as plt
import networkx as nx
import operator
import numpy

from logProcessor import LogProcessor
from operator import itemgetter
from topologyProcessor import TopologyLogProcessor

gl_dump_path = os.getcwd() + '/../'
gl_image_path = os.getenv("HOME") + ''


class DataSetProcessor(LogProcessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_total_packets(self):
        tot_packets= self.packets
        return len(tot_packets)

    def get_total_duration(self):
        t0 = self.packets[0].asn_first
        t1 = self.packets[-1].asn_last
        return (t1-t0)*0.015  # in seconds

    def get_seen_nodes(self):
        seen_nodes = []
        node_occurrences = []

        for pkt in self.packets:
            for node in pkt.get_path(full=True):
                if not (node in seen_nodes):
                    seen_nodes.append(node)
                    node_occurrences.append(1)
                else:
                    node_idx = seen_nodes.index(node)
                    node_occurrences[node_idx] += 1
        dict = {}
        for node in seen_nodes:
            dict[node] = node_occurrences[seen_nodes.index(node)]

        return dict

    def get_seen_channels(self):
        seen_channels = []
        channels_occurrences = []

        for pkt in self.packets:
            for channel in pkt.get_channels():
                if not (channel in seen_channels):
                    seen_channels.append(channel)
                    channels_occurrences.append(1)
                else:
                    channel_idx = seen_channels.index(channel)
                    channels_occurrences[channel_idx] += 1
        dict = {}
        for channel in seen_channels:
            dict[channel] = channels_occurrences[seen_channels.index(channel)]
        return dict


if __name__ == '__main__':

    folders= ('tdma','shared')
    files= ('no_interference.log','interference.log','induced_interference.log')

    tot_packets=[]
    duration=[]
    tot_per_node_packets=[]
    tot_per_channel_packets = []

    # create subplots
    f, axs = plt.subplots(2,3)

    for i,folder in enumerate(folders):
        for j,file in enumerate(files):
            path = gl_dump_path + folder + '/' + file
            #print(path)
            d = DataSetProcessor(filename=path)
            tp=d.get_total_packets()
            nodes_occurrences=d.get_seen_nodes()
            channels_occurrences=d.get_seen_channels()
            dur=d.get_total_duration()/60 #in minutes

            print("\n")
            print(folder+'-'+file)

            print("Total duration [min]:\n", dur)
            print("Total number of packets:\n", tp)

            #print("Nodes occurrences:\n",nodes_occurrences)
            #print("Channels occurrences:\n", channels_occurrences)

            tot_avg_node_occurr = numpy.mean(list(nodes_occurrences.values()))
            tot_avg_channel_occurr = numpy.mean(list(channels_occurrences.values()))

            print("Nodes occurrences (avg):\n", tot_avg_node_occurr)
            print("Channels occurrences (avg):\n", tot_avg_channel_occurr)

            tot_packets.append(tp)
            duration.append(dur)
            tot_per_channel_packets.append(tot_avg_channel_occurr)
            tot_per_node_packets.append(tot_avg_node_occurr)

            p = TopologyLogProcessor(filename=path)
            p.plot_colormap(axis=axs[i,j])

    print(duration)
    print(tot_per_node_packets)
    print(tot_per_channel_packets)
    print(tot_packets)

    plt.show()