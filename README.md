# NTRexample_FRevNCA

Example code producing novelty, transience, and resonance for a sample of legislative speech during the French Revolution, as documented in [Individuals, Institutions, and Innovation in the Debates of the French Revolution](https://arxiv.org/abs/1710.06867).

## Data

* `example_FRev_speech_data_rawspeechonly_1790-06-01_1790-07-01.txt` contains one month of raw speeches from the [French Revolution Digital Archive](https://frda.stanford.edu/en/ap).

## Scripts

Get help on arguments for each python file via `python <script name>.py -h`.

* `calculate_novelty_transience_resonance.py` takes a text file of topic mixtures as rows and produces the three named measures.
* `learn_topics.py` produces topics, topic mixtures, and vocabulary given a text file, one document per row.  In this example, documents are speeches.
* `text_topic_ntr.py` is a convenience script taking a file of documents, producing topics, and creating novelty, transience, and resonance in succession. 
  - `make_example_NTR.sh` provides a command-line example for using this script.

## Notebooks

* `density_plots_TvN_RvN.ipynb` creates density plots for transience v. novelty and resonance v. novelty.

## Script requirements (versions used)

* numpy (1.13.1)
* scikit-learn (0.19.0)
* lda (1.0.5)

### Notebook requirements

* jupyter (1.0.0)
* matplotlib (2.0.2)
* pandas (0.20.3)
