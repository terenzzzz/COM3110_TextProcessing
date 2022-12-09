## Environment
- Python 3.9.12(PC Default)
## Library using and Install method
1. argparse
2. panda:
    ```python
    pip install pandas
    ```
3. pickle
4. nltk:
    ```python
    pip install nltk
    ```
5. nltk(averaged_perceptron_tagger):
    ```python
    pythonn3
    import nltk
    nltk.download('averaged_perceptron_tagger')
    ```
6. nltk.corpus(stopwords):
    ```python
    pythonn3
    import nltk
    nltk.download('stopwords')
    ```
7. nltk.stem.porter
8. matplotlib.pyplot:
    ```python
    pip install matplotlib
    ```
9. itertools

### Before Running
- Must have a `models` folder in the root directory to store the trinned model
- Must have a `results` folder in the root directory to store the predict result

### Running comand
- Basic running command:
    ```python
    python NB_sentiment_analyser.py moviereviews/train.tsv moviereviews/dev.tsv moviereviews/test.tsv -class 3 -feature all_words
    ```
    - -class: means the scale of the sentiment
    - -feature: all_words or features
    - -output_files (default:false): will output the dev set and test set predicted result to result folder with specified name
    - -confusion_matrix (default:false): will show the confusion matrix for dev set

- Quick run geting F1-score for all situation
    ```python
    python run.py
    ```


- 3_class_all_words with output_file and confusion matrix
    ```python
    python NB_sentiment_analyser.py moviereviews/train.tsv moviereviews/dev.tsv moviereviews/test.tsv -class 3 -feature all_words -output_files -confusion_matrix
    ```
- 3_class_features with output_file and confusion matrix
    ```python
    python NB_sentiment_analyser.py moviereviews/train.tsv moviereviews/dev.tsv moviereviews/test.tsv -class 3 -feature features -output_files -confusion_matrix
    ```

- 5_class_all_words with output_file and confusion matrix
    ```python
    python NB_sentiment_analyser.py moviereviews/train.tsv moviereviews/dev.tsv moviereviews/test.tsv -class 5 -feature all_words -output_files -confusion_matrix
    ```

- 5_class_features with output_file and confusion matrix
    ```python
    python NB_sentiment_analyser.py moviereviews/train.tsv moviereviews/dev.tsv moviereviews/test.tsv -class 5 -feature features -output_files -confusion_matrix
    ```
