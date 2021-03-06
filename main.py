from data_providers.DataProvider import Producer
from models.EncoderDecoder import Normal
from trainers.Trainer import MbTrainer
from testers.Tester import MBTester
from data_providers.ImagesProvider import SequenceImagesProvider
from flow_net.OpticalFlow import Flow
import os
from argparse import ArgumentParser

parser = ArgumentParser("Description to add")
parser.add_argument("model", help="Specify model, for example: SD, css-ft-sd, CSS", default="s")
args = parser.parse_args()


def init_data_provider():
    data_provider = Producer(path="data.txt",
                             batch_size=10)
    data_provider.load()
    return data_provider


def init_images_provider():
    images_provider = SequenceImagesProvider(sequence_path="paper.mp4")
    return images_provider


def init_flownet_model():

    class Args:
        deployproto = "models/FlowNet2-" + args.model + "_deploy.prototxt.template"
        verbose = False
        caffemodel = "models/FlowNet2-" + args.model + "_weights.caffemodel.h5"
        gpu = 0
        out = "result.flo"

    # check if provided paths exists
    if not os.path.exists(Args.caffemodel):
        raise BaseException('caffemodel does not exist: '+Args.caffemodel)

    if not os.path.exists(Args.deployproto):
        raise BaseException('deploy-proto does not exist: '+Args.deployproto)

    flow_net = Flow(args=Args)
    return flow_net

data_pro = init_data_provider()
data_img = init_images_provider()
opt_net = init_flownet_model()

# train
# trainer = MbTrainer(model=Normal(),
#                     data_provider=data_pro,
#                     output_net_name="trained_net.meta",
#                     logs_dir="./logs")
# trainer.train(1000, 500000)

# test
tester = MBTester(data_provider=data_img,
                  flownet_provider=opt_net,
                  net_name="trained_net.meta.meta",
                  test_method="flow_deform",
                  output_path="../data/")

tester.test()

