import csv
import random
import math
import operator
import time
import statistics
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

def loadDataset(file_data):
    df = pd.read_csv(file_data)
    target = df['Patient']
    features = df.drop(['Sample','Patient'], axis = 1)
    target = target.where(target >= 0, 0)
    target = target.where(target <= 1, 1)
    return features, target

def train(x, y, max_count):
    total_count = 0
    TP, FP, TN, FN, P, N =0, 0, 0, 0, 0, 0

    while (total_count <= max_count):
        try:
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)

            # 'rbf' seems positive for specificity, 'poly' seems suitable for sensitivity
            svclassifier = SVC(kernel='rbf', gamma = 'auto', degree=3, coef0 = 0.0)
            svclassifier.fit(X_train, y_train)

            y_pred = svclassifier.predict(X_test)            
            for i in range(len(y_test)):
                if y_test[i] == 1 and y_pred[i] == 1:
                    TP, P = TP+1, P+1
                elif y_test[i] == 1 and y_pred[i] == 0:
                    FN, P = FN+1, P+1
                elif y_test[i] == 0 and y_pred[i] == 0:
                    TN, N = TN+1, N+1 
                elif y_test[i] == 0 and y_pred[i] == 1:
                    FP, N = FP+1, N+1         
            total_count += len(y_test)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            break
    sensitivity = (TP/P)*100
    specificity = (TN/N)*100
    accuracy = (TP+TN)/(P+N)*100
    precision = TP/(TP+FP)*100
    MCC = ((TP*TN)-(FP*FN))/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    return sensitivity, specificity, accuracy, precision, MCC, total_count, (TP, FP, TN, FN, P, N)
    # recall of the positive class is also known as “sensitivity”; recall of the negative class is “specificity”.


if __name__ == "__main__":
    start=time.time()
    file_data= 'wbc_janselect.csv'
    max_count = 50000   

    ### Load Data ###
    features, target = loadDataset(file_data)
    features = StandardScaler().fit_transform(features)
    
    sensitivity, specificity, accuracy, precision, MCC, total_count, nums = train(features, target.values, max_count)
    TP, FP, TN, FN, P, N = nums    

    print('========= File Data "%s' % file_data + '" ========= \n')
    print('Total =',total_count,'||  True Positive (1) =',TP,' ||  True Negatives (0) =', TN)
    print()
    print('(Sensitivity) True Positive Rate = %0.3f' %(specificity)+'%')
    print('(Specificity) True Negative Rate = %0.3f' %(specificity)+'%')
    print('(Accuracy) = %0.3f' %(accuracy)+'%')
    print('(Precision) Positive predictive value (PPV) = %0.3f' %(precision)+'%')
    print()
    print('False Negative Rate = %0.3f' %((FN/P)*100)+'%')
    print('False Positive Rate = %0.3f' %((FP/N)*100)+'%')
    print()
    print('MCC Matthews correlation coefficient = %0.3f' % MCC)
    print()
    print('Total Count = ',total_count)
    print('========= ========== ========= ========= =========\n')
    # print(classification_report(y_test,y_pred))

    ### END ###
    end=time.time()
    print('The run took %0.6fs' % (end-start)) 