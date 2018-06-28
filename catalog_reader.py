import numpy as np
from astropy.io import fits
import argparse
from utils import utils


class RMReader():

    def __init__(self, config="./config/reader.json"):
        params = utils.Params(config)
        self._path = params.catalogpath
        self.data = {
            "catalog": fits.open(self._path+params.catalogName, mode='readonly', memmap=True, lazy_load_hdus=True)[1].data,
            "members": fits.open(self._path+params.memberName, mode='readonly', memmap=True, lazy_load_hdus=True)[1].data,
            "areaZ": fits.open(self._path+params.areaZ, mode='readonly', memmap=True, lazy_load_hdus=True)[1].data,
            "random": fits.open(self._path+params.random, mode='readonly', memmap=True, lazy_load_hdus=True)[1].data
        }
        self.quantities = {}
        for item in self.data.keys():
            self.quantities[item] = self.data[item].names

    def list_quantities(self, name=None):
        if name is None:
            print("List All Quantities")
            for item in self.quantities.keys():
                print("#"*20)
                print("Quantitiy Name: {0}".format(item))
                print("-"*20)
                print(self.quantities[item])
        else:
            print(self.quantities[name])

    def get_quantities(self, quantities_list):
        output = {}
        for quantity in quantities_list:
            catalog, field = quantity.split(",")
            output[quantity] = self.data[catalog][field]
        return output
