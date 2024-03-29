from LSTMModel import lstm
from dataset import getData
from parser_my import args
import matplotlib.pyplot as plt
import torch


def eval():
    # model = torch.load(args.save_file)
    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)
    checkpoint = torch.load(args.save_file)
    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []
    predict_list = []
    real_list = []
    close_max, close_min, train_loader, test_loader = getData(args.corpusFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.squeeze(1).cuda()  # batch_size,seq_len,input_size
        else:
            x = x.squeeze(1)
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())
        print(preds)
    for i in range(len(preds)):
        print(i)
        print('预测值是%.2f,真实值是%.2f' % (
        preds[i][0] * (close_max - close_min) + close_min, labels[i] * (close_max - close_min) + close_min))
        predict_list.append(preds[i][0] * (close_max - close_min) + close_min)
        real_list.append(labels[i] * (close_max - close_min) + close_min)
    fig = plt.figure()
    plt.plot(predict_list)
    plt.plot(real_list)
    plt.show()

eval()