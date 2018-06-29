import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from astropy.table import Table
from .base import BaseValidationTest, TestResult
from .catalog_reader import RMReader

class RandomsRicnhessTest(BaseValidationTest):
    def __init__(self, **kwargs):
        self.quantities_needed = ["catalogName,LAMBDA_CHISQ","catalogName,Z_LAMBDA", "random, ZTRUE", "random,AVG_LAMBDAOUT"]
    
    def run(self, configpath, outputdir):
        reader = RMReader(configpath)
        quantities = reader.get_quantities(self.quantities_needed)
        cat_lambda = quantities["catalogName,LAMBDA_CHISQ"]
        cat_z = quantities["catalogName,Z_LAMBDA"]
        rand_lambda = quantities["random,AVG_LAMBDAOUT"]
        rand_z = quantities["random, ZTRUE"]
        cat_data = [cat_lambda, cat_z]
        rand_data =  [rand_lambda, rand_z]
        self.makeplot(cat_data, rand_data, outputdir)
        return TestResult(inspect_only=True)
    
    def rich(self, data, zmin, zmax):
            z = data[1] 
            lambd = data[0]
            mask = ((z>zmin) & (z<zmax))
            new_lambda = lambd[mask]
            return (new_lambda)
        
    def makeplot(self, cat_data, rand_data, outputdir):
         zmin = [0.1, 0.4, 0.7]
         zmax = [0.4, 0.7, 1]
         f, ax = plt.subplots(1,3, figsize = (15,5))
         bi_space = np.linspace(0,150)
         for i in range (0,3):
            cat = self.rich(cat_data, zmin[i], zmax[i])
            ran = self.rich(rand_data, zmin[i], zmax[i])
            ax[i].hist(ran, bins = bi_space, color = 'orange', normed = True, histtype = 'step', lw = 2, label = 'randoms')
            ax[i].hist(cat, bins = bi_space, color = 'blue', normed = True, histtype = 'step', lw = 2, label= 'data')
            ax[i].set_xlim(0,150)
            ax[i].legend(loc = 'upper right')
            ax[i].set_xlabel ('Richness')
            ax[i].set_title('Richness for z:  ' + str(zmin[i]) + '-'+ str(zmax[i]))
         f.savefig(outputdir+"RandomsRichness.png")
         plt.close(f)
