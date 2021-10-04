from config.Factory import ConfigFactory
from runner.Runner import Runner
from datasets import download_datasets
import argparse, os


parser = argparse.ArgumentParser(description='Multiprocessing example')
parser.add_argument('dataset', type=str)
args = parser.parse_args()

download_datasets()

path = os.path.join('datasets', args.dataset + '.csv')
if not os.path.exists(path):
    raise Exception('Dataset not found')

runner = Runner(path, ConfigFactory.from_name(args.dataset))
runner.run()