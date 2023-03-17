# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 01:22:27 2021

@author: G
"""

from fastai.vision.all import *

path = Path('Nekos')
fnames = get_image_files(path)
print(f"Total Images:{len(fnames)}")
def label_func(x): return x.parent.name
dls = ImageDataLoaders.from_path_func(path, fnames, label_func, bs=16, item_tfms=Resize(224))

dls.valid.show_batch(max_n=4, nrows=1)

learn = cnn_learner(dls, resnet152, metrics=error_rate)

#lr_min, lr_steep = learn.lr_find()
#print(f"Minimum/10: {lr_min:.2e}, steepest point: {lr_steep:.2e}")
lrs = learn.lr_find(suggest_funcs=(minimum, steep, valley, slide))
print(f"Minimum/10: {lrs.minimum:.2e}, steepest point: {lrs.steep:.2e}")

learn.fine_tune(3, base_lr=1.74e-04)

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(5, nrows=1)

losses, idxs = interp.top_losses(20)
print(idxs)
dls.valid_ds.items[50]

learn.export()