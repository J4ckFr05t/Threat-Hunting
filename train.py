from cProfile import label
from turtle import TPen
from utilities import *

traning_data = "DATA/labeled-data-samples/trainingset.csv"
testing_data = "DATA/labeled-data-samples/testset.csv"

# Get training features and labeles
training_features, training_labels = get_data_details(traning_data)
# Get testing features and labels
testing_features, testing_labels = get_data_details(testing_data)

print("\n\n=-=-=-=-=-=-=- Decision Tree Classifier -=-=-=-=-=-=-=-\n")
# Instanciate the classifier
attack_classifier = tree.DecisionTreeClassifier(criterion='gini')
# Train the model
attack_classifier.fit(training_features, training_labels)

# Predict
predictions = attack_classifier.predict(testing_features)
print("Precision : " + str(get_accuracy(testing_labels,predictions, 1)) + "%")
# Save the trained classifier
model_location = save_model(attack_classifier,"dt")
print("You model has been saved at {}".format(model_location))

# TP = 1338 FP = 79
# FN = 3    TN = 8171

#precision = 94.42
#accuracy = 99.14
#TPR = 99.77
#FPR = 0.95

