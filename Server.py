from flask import Flask, request, render_template
import numpy as np
from keras.models import load_model
import tensorflow
from emo_utils import *
import emoji

app = Flask(__name__)

model = load_model('emojfier.h5')

maxLen = 10 

word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('data/glove.6B.50d2.txt')

def sentences_to_indices(X, word_to_index, max_len):
    m = X.shape[0]                              
    X_indices = np.zeros([m,max_len])
    for i in range(m):                          
        sentence_words = X[i].lower().split()
        j = 0
        for w in sentence_words:
            if w in word_to_index:
                X_indices[i, j] =  word_to_index[w]
                j += 1
    return X_indices

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input sentence from the form
        sentence = request.form['sentence']

        # Convert the sentence to indices
        x_test = np.array([sentence])
        X_test_indices = sentences_to_indices(x_test, word_to_index, maxLen)

        # Predict using the model
        prediction = model.predict(X_test_indices)
        emoji_label = label_to_emoji(np.argmax(prediction))

        # Return the result to the user
        return render_template('index.html', sentence=sentence, emoji=emoji_label)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
