# -*- coding: utf-8 -*-
'''使用focal loss来跑'''
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
import os
from Graduation_Project.Screws.U_Net import U_Net01
from Graduation_Project.Screws.U_Net import mydatasets
from Graduation_Project.Screws.U_Net import MyFocalLoss02

path = r'Datasets'
module = r'models/module_focal.pkl'
img_save_path = r'train_result'
# batch = 1

net = U_Net01.MainNet().cuda()
optimizer = torch.optim.Adam(net.parameters())


loss_func = MyFocalLoss02.BCEFocalLoss()

dataloader = DataLoader(mydatasets.MKDataset(path), batch_size=2, shuffle=True)

if os.path.exists(module):
    net.load_state_dict(torch.load(module))
    print('module is loaded !')
if not os.path.exists(img_save_path):
    os.mkdir(img_save_path)

batch=0
while True:
    batch += 1
    for i, (xs, ys) in enumerate(dataloader):
        xs = xs.cuda()
        ys = ys.cuda()

        xs_ = net(xs)

        loss = loss_func(xs_, ys)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if i % 5 == 0:
            print('epochs--{}--{}/{},input_count:{},loss:{}'.format(batch,i,len(dataloader),(i + 1) * 4, loss))

        torch.save(net.state_dict(), module)
        # print(i)
        # print('module is saved !')


        '''将输入图片、输出图片、标签图片展示在一张图上'''
        x = xs[0]
        x_ = xs_[0]
        y = ys[0]
        z = torch.cat((x, x_, y), 2)
        img_save = transforms.ToPILImage()(z.cpu())
        img_save.save(os.path.join(img_save_path, '{}.png'.format(i)))

    # 每20轮另外保存一个模型
    if batch % 20 == 0:
        torch.save(net.state_dict(), f'models/module_focal{batch}.pkl')


