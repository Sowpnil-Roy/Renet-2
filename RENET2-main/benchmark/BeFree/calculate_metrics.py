import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":
    gdas = []
    
    with open("n_out/cooc_FINAL.befree") as f:
        for line in f:
            items = line.split('\t')
            gdas.append([items[0], items[7], items[9], items[13], items[15]])

    gdas_befree = pd.DataFrame(np.array(gdas), columns=['pmid', 'geneId', 'gene_name', 'diseaseId', 'disease_name'])
    
    predicted_positive = gdas_befree.drop_duplicates(['pmid', 'geneId', 'diseaseId'])
    predicted_positive.to_csv("n_out/classification_result_befree.txt", index=False, columns=['pmid', 'geneId', 'diseaseId'])


    #actual_positive = pd.read_csv('../../testing_data/labels.csv')
    #actual_positive = pd.read_csv('/mnt/bal31/jhsu/old/data/new_renet_data/test/labels.txt')
    actual_positive = pd.read_csv('n_out/labels.txt')
    actual_positive = actual_positive[actual_positive['label'] == 1]

    print(actual_positive.head(3))
    print(actual_positive.shape)
    print(predicted_positive.head(3))
    print(predicted_positive.shape)

    actual_positive.pmid = actual_positive.pmid.astype(str)
    actual_positive.geneId = actual_positive.geneId.astype(str)


    true_positives = pd.merge(actual_positive, predicted_positive, how="inner")

    precision = true_positives.shape[0] / float(predicted_positive.shape[0])

    recall = true_positives.shape[0] / float(actual_positive.shape[0])

    Fscore = 2 * precision * recall /(precision + recall)

    print("precision:{}  recall:{}  F-score:{}".format(precision, recall, Fscore))
    print("{},{},{}".format(precision, recall, Fscore))
