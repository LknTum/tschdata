import matplotlib.pyplot as plt
import numpy
from dataprocessing.basic_processor import BasicProcessor
from dataprocessing.toolbox import set_box_plot


def print_dataset_parameters():
    """
    TODO print all parameters nicely
    :return:
    """
    tot_packets = []
    duration = []
    tot_per_node_packets = []
    tot_per_channel_packets = []

    measurements_mote_lists = []
    measurements_channels_lists = []
    for i in range(1, 4):
        print("\n")

        d = BasicProcessor(filename="../../../WHData/Data/LKN_measurements_190716/Logs/%d.log" % i,
                   format="WHITENING")

        tp=d.get_number_of_packets()
        dur = d.get_total_duration() / 60  # in minutes
        nodes_occurrences=d.get_seen_nodes()
        channels_occurrences=d.get_seen_channels()

        print("File log: %d.log" % i)
        print("Total duration [min]:\n", dur)
        print("Total number of packets:\n", tp)

        #print("Nodes occurrences:\n",nodes_occurrences)
        #print("Channels occurrences:\n", channels_occurrences)
        tot_avg_node_occurr = numpy.mean(list(nodes_occurrences.values()))
        tot_avg_channel_occurr = numpy.mean(list(channels_occurrences.values()))

        measurements_mote_lists.append(list(nodes_occurrences.values()))
        measurements_channels_lists.append(list(channels_occurrences.values()))

        print("Nodes occurrences (avg):\n", tot_avg_node_occurr)
        print("Channels occurrences (avg):\n", tot_avg_channel_occurr)

        tot_packets.append(tp)
        duration.append(dur)
        tot_per_channel_packets.append(tot_avg_channel_occurr)
        tot_per_node_packets.append(tot_avg_node_occurr)

    print("\n")
    print(duration)
    print(tot_per_node_packets)
    print(tot_per_channel_packets)
    print(tot_packets)

    fig = plt.figure()
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    bp = ax.boxplot(measurements_mote_lists+measurements_channels_lists)
    set_box_plot(bp)

    ax.set_xticklabels(['Motes - Rnd', 'Ch - Rnd', 'Motes - White', 'Ch - White','Motes - Gld','Ch - Gld'])
    plt.title("Motes Channels occurrencies")
    plt.grid(True)
    plt.show()

def test_multichannel():
    """
    Test basic performance parameters for whitening measurements
    :return:
    """
    max_retxs = [4,2,4]

    for i in range(1, 3):
        p = BasicProcessor(filename="../../../WHData/Data/LKN_measurements_140716/Logs/%d.log" % i,
                       format="WHITENING")

        # p.plot_avg_hops()
        # p.plot_delays()

        # p.plot_timeline()

        p.correct_timeline()
        p.plot_motes_reliability()
        p.plot_channels_reliability("../../../WHData/Data/LKN_measurements_140716/Schedules/schedules_%d" % i,max_retxs
                                    [i-1])

        D=p.get_seen_nodes()

        plt.figure()
        plt.bar(range(len(D)), D.values(), align='center')
        plt.xticks(range(len(D)), D.keys())

        p.plot_hopping("../../../WHData/Data/LKN_measurements_140716/Schedules/schedules_%d" % i)

    plt.grid(True)
    plt.show()

    fig = plt.gcf()
    # Todo not working
    # fig.savefig("dataset_whitening.pdf", format='pdf', bbox='tight')


def plot_latencies():
    """
    TODO
    :return:
    """
    pass


def boxplot_motes(motes_occurrencies):


    return


if __name__ == '__main__':
    #test_multichannel()
    print_dataset_parameters()

