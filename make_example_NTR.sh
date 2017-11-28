# Example calculation of novelty, transience, and resonance.

textfile="example_FRev_speech_data_rawspeechonly_1790-06-01_1790-07-01.txt"
num_topics=10
scale=10
outdir="."

python text_topic_ntr.py $textfile $num_topics $scale $outdir
