import numpy as np
from scipy.io import wavfile
import tensorflow as tf
import tensorflow_hub as hub
import librosa
from modules.example_feature import *
from configs.example_config import Config

modelvgg = hub.load('https://tfhub.dev/google/vggish/1')
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

def mask_acoustic_feat(X):
    mask_feat = []
    for filename in X.file_path.values:
        y,sr = librosa.load(filename)
        x = librosa.resample(y,sr, 16000)
        if len(x.shape)>1:
            x = np.mean(x,axis=1)
        xt, index = librosa.effects.trim(x)
        scores, embeddings, spectrogram = yamnet_model(xt)
        class_scores = tf.reduce_mean(scores, axis=0)
        f1 = np.array(class_scores)[0]
        f2 = np.array(class_scores)[42]
        if f2 >  Config.FITER_COUGH or (f2 < Config.FITER_COUGH and f1 > Config.FITER_SPEECH):
            mask_values = True
        else:
            mask_values = False
        mask_feat.append(mask_values)
    mask_feat = np.array(mask_feat)

    return mask_feat
    

def make_acoustic_feat(X):
    feat = []
    for filename in X.file_path.values:
        y,sr = librosa.load(filename)
        feature_values_vec = total_732_feature(y,sr, model = modelvgg)
        feature_values_vec = np.array(feature_values_vec)
        feat.append(feature_values_vec)
    feat = np.array(feat)
    feat = np.nan_to_num(feat, nan = np.nan)
    feat = np.clip(feat, -np.finfo(np.float32).max, np.finfo(np.float32).max)

    return feat
