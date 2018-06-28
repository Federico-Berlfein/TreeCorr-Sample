import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from astropy.table import Table
from .base import BaseValidationTest, TestResult
from .catalog_reader import RMReader

class RandomsRicnhessTest(BaseValidationTest):
    def __init__(self, **kwargs):
        self.quantities_needed = ["catalogName", "random"]
    
    def run(self, configpath, outputdir):
        reader = RMReader(configpath)
        quantities = reader.get_quantities(self.quantities_needed)
        catalog = quantities["catalogName"]
        random = quantities["random"]
        cat = Table.read(catalog)
        rand= Table.read(random)
        data = [cat, rand]
        self.makeplot(data, outputdir)
        return TestResult(inspect_only=True)
        
    def makeplot(self, data, outputdir):
        zmin = [0.1, 0.4, 0.7]
        zmax = [0.4, 0.7, 1]
        def rich(catalog, zmin, zmax):
            z = np.array(catalog['Z_LAMBDA'])
            mask = ((z>zmin) & (z<zmax))
            new_cat = catalog[mask]
            cat_lambda = np.array(new_cat['LAMBDA_CHISQ_C'])
            return (cat_lambda)
         f, ax = plt.subplots(1,3, figsize = (15,5))
         bi_space = np.linspace(0,150)
         for i in range (0,3):
            cat = rich(data[0], zmin[i], zmax[i])
            ran = rich(data[1], zmin[i], zmax[i])
            ax[i].hist(ran, bins = bi_space, color = 'orange', normed = True, histtype = 'step', lw = 2, label = 'randoms')
            ax[i].hist(cat, bins = bi_space, color = 'blue', normed = True, histtype = 'step', lw = 2, label= 'data')
            ax[i].set_xlim(0,150)
            ax[i].legend(loc = 'upper right')
            ax[i].set_xlabel ('Richness')
            ax[i].set_title('Richness for z:  ' + str(zmin[i]) + '-'+ str(zmax[i]))
         f.savefig(outputdir+"RandomsRichness.png")
         f.close()
