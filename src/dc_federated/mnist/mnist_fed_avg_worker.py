"""
Simple runner to start FedAvgWorker for the MNIST dataset.
"""

import sys
import argparse

from dc_federated.fed_avg.fed_avg_worker import FedAvgWorker
from dc_federated.mnist.mnist_fed_model import MNISTModelTrainer, MNISTSubSet


def get_args():
    """
    Parse the argument for running the example local model for the distributed
    federated test.
    """
    # Make parser object
    p = argparse.ArgumentParser(
        description="Run this with the parameter provided by running the mnist_fed_avg_server\n")

    p.add_argument("--server-host-ip",
                   help="The ip of the host of server",
                   type=str,
                   required=True)
    p.add_argument("--server-port",
                   help="The ip of the host of server",
                   type=str,
                   required=True)

    p.add_argument("--digit-class",
                   help="The digit set this worker should focus on - allowed values are 0, 1 and 2.",
                   type=int,
                   required=True)

    p.add_argument("--round-type",
                   help="What defines a training round. Allowed values (batches, epochs)",
                   type=str,
                   default='batches',
                   required=False)

    p.add_argument("--rounds-per-iter",
                   help="The number of rounds per iteration of training of the worker.",
                   type=int,
                   default=10,
                   required=False)

    return p.parse_args()


def run():
    """
    This should be run to start a FedAvgWorker. Run this script with the --help option
    to see what the options are.

    --digit-class 0 corresponds to worker training only on digits 0 - 3,
    1 corresponds to worker training only on digits 4 - 6 and 2 to 7 - 9.
    """
    digit_classes = [[0, 1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]]

    args = get_args()

    data_transform = MNISTSubSet.default_input_transform()
    mnist_ds_train = MNISTSubSet.default_mnist_ds(is_train=True, input_transform=data_transform)
    mnist_ds_test = MNISTSubSet.default_mnist_ds(is_train=False, input_transform=data_transform)

    local_model_trainer = MNISTModelTrainer(
        train_loader=MNISTSubSet(
            mnist_ds_train,
            digits=digit_classes[args.digit_class],
            input_transform=data_transform
        ).get_data_loader(),
        test_loader=MNISTSubSet(
            mnist_ds_test,
            digits=digit_classes[args.digit_class],
            input_transform=data_transform
        ).get_data_loader(),
        round_type=args.round_type,
        rounds_per_iter=args.rounds_per_iter
    )

    fed_avg_worker = FedAvgWorker(local_model_trainer, args.server_host_ip, args.server_port)
    fed_avg_worker.run_worker_loop()


if __name__ == '__main__':
    run()
