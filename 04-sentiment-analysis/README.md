## Análisis de sentimientos y percepción de consumidor

Este módulo se dedica a la construcción del marco de trabajo
matemático necesario para el análisis del sentimientos. Para ello,
vamos a hacer una revisión de la referencia bibliográfica:

* [Bing Liu, *Sentiment Analysis: Mining Opinions, Sentiments, and Emotions*, Cambridge
  University Press, 2015](https://www.cambridge.org/9781108486378).

En particular, vamos a hacer un estudio profundo de los siguientes capítulos del
libro:

1. Introduction
    * Sentiment Analysis Applications
    * Sentiment Analysis Research
      - Different Levels of Analysis
      - Sentiment Lexicon and Its Issues
      - Analyzing Debates and Comments
      - Mining Intentions
      - Opinion Spam Detection and Quality of Reviews
    * Sentiment Analysis as Mini NLP


2. The Problem of Sentiment Analysis
    * Definition of Opinion
      * Opinion Definition
      * Sentiment Target
      * Sentiment of Opinion
      * Opinion Definition Simplified
      * Reason and Qualifier for Opinion
      * Objective and Tasks of Sentiment Analysis
    * Definition of Opinion Summary
    * Affect, Emotion, and Mood
      * Affect, Emotion, and Mood in Psychology
      * Affect, Emotion, and Mood in Sentiment Analysis
    * Different Types of Opinions
      * Regular and Comparative Opinions
      * Subjective and Fact-Implied Opinions
      * First-Person and Non-First-Person Opinions
      * Meta-Opinions 44 Author and Reader Standpoint 45 Summary 45
  
3. Document Sentiment Classification
    * Supervised Sentiment Classification
      * Classification Using Machine Learning Algorithms
      * Classification Using a Custom Score Function
    * Unsupervised Sentiment Classification
      * Classification Using Syntactic Patterns and Web Search
      * Classification Using Sentiment Lexicons
    * Sentiment Rating Prediction
    * Cross-Domain Sentiment Classification
    * Cross-Language Sentiment Classification
    * Emotion Classification of Documents
  

En particular, prestaremos especial atención a la clasificación 
supervisada y no supervisada de sentimientos a nivel de documentos,
que tendrá como final la codificación del [algoritmo de Turney](turney-algorithm/turney-algorithm.ipynb), y 
potenciales modificaciones cambiando la métrica asociada.

La versión pip-instalable del algoritmo de Turney se puede encontrar en el 
directorio [sentiment-miner](sentiment-miner).

El contenido de este capítulo se encuentra en las transparencias facilitadas
durante el curso en la plataforma oficial de la Universidad.
