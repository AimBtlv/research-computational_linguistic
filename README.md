## reasearch-Computational Linguistics

###  **Culturomics: Testing Quantitative Analysis of Culture on the Wikipedia Revision History Corpus**
***A Case Study on J.B. Michel article: “Quantitative analysis of culture using millions of digitized books”***


##### Description: 
Culturomics is a method for studying culture through large-scale text data. It was introduced by Michel  (2011) and quickly became one of the most discussed contributions at the intersection of computational linguistics and digital humanities. 
*****

##### About Project: 
This project starts with a simple question. Can the methods of culturomics work on a corpus that was never designed for them?
The question comes from Michel (2011), who introduced culturomics in their foundational Science paper "Quantitative Analysis of Culture Using Millions of Digitized Books." They analysed 500 billion words from 5 million digitised books to show that language and culture can be studied quantitatively through n-gram frequency over time. The results were striking. But Pechenick(2015) later showed that the Google Books corpus carries a hidden problem. After 1900, scientific publications dominate the archive, and one bestselling book reprinted a hundred times counts as a hundred separate books. The corpus does not reflect culture as much as it reflects what got digitised and how often.
This project takes that critique seriously. It applies three of the six original methods to the Wikipedia revision history from 2001 to 2024, a corpus that is genre-homogeneous, openly editable, and built on entirely different principles from Google Books. The corpus consists of 85 articles spanning 21 annual snapshots and reaching 763,041 tokens in its final year. The results show that lexical growth patterns hold, collective memory patterns transform, and the suppression index partially transfers with important conceptual adjustments. Scale alone does not guarantee insight. What matters is understanding what each corpus actually measures and being honest about the boundaries of that measurement.

***
##### Research Questions:
 **RQ1** “When the same analytical logic (as in J.B.Michel) is applied to a structurally different dataset do the culturomics patterns hold, break down, or transform into something methodologically distinct?"
>* Michel, J.-B., Shen, Y. K., Presser Aiden, A., Veres, A., Gray, M. K., Pickett, J. P., et al. (2011). Quantitative analysis of culture using millions of digitized books. Science, 331(6014), 176–182. https://doi.org/10.1126/science.1199644 
***
##### Corpus:

| Parameter | Michel (2011) | This Study |
|---|---|---|
| **Source** | Google Books (digitised books) | Wikipedia Revision History |
| **Access method** | Google Books Ngram Corpus | MediaWiki Revisions API |
| **Size** | 500 billion words, 5M books | 6.6M tokens, 85 articles |
| **Period** | 1500–2000 | 2001–2024 |
| **Languages** | 7 (EN, FR, DE, ES, RU, ZH, HE) | English only |
| **Genre** | Mixed (all published books) | Encyclopaedic prose only |
| **Selection criterion** | OCR and metadata quality | Thematic diversity across topics |
| **Caching** | N/A | `corpus_cache.json` (MediaWiki API) | 

***
#### Repository Structure:
##### **intro/** 
>**background reading:**
___
>caseArticle_Michel:  
>criticalArticle_Pechenic.pdf:  
>criticalArticleBohannon.pdf:    
>linguisticAnalyse_Firth.pdf:   
>aboutCulturomics 2.0.docx:     
##### datasets/
##### notebooks/
>Three Jupyter Notebooks, describing Methodological Process:  
___ 
1.culturomics_M1.ipynb.  
2.culturomics_M3.ipynb.  
3.culturomics_M6.ipynb.  

##### **scripts/**
>**fetch_wiki.py** 
____
 Wikipedia corpus builder. Fetches yearly text snapshots of predefined articles  via the MediaWiki Revisions API (2001–2024) and saves  them to corpus_cache.json. Run once before the notebooks. Do not re-run if corpus_cache.json already exists.
 ##### images/
 >Visualization of Methods OutPut:
 ---
 1.method1_lexicon_summary.png    
 2.method3_collective_memory.png     
 3.method6_suppression.png   
 #####  bibliography/
 >Source List
 ___
 1.References.md
 ##### documentation/
 #####  outputs/
 > Final output: What we have in the end? 
 ___
 1.Report.pdf     
 2.
***
##### Methodology:
Six analytical methods are described in Michel et al. (2011). This study planned to adapt all six and successfully implemented three. The table below documents the status and rationale for each.

| Method | Michel (2011)| Our Adaptation |  Status | 
|---|---|---|---
| **1.Lexical Growth** | Counted all 1-grams with frequency > 1 per billion in Google Books across 1900, 1950, and 2000. Found English lexicon grew from 544,000 words (1900) to 1,022,000 words (2000). Cross-checked against OED and Merriam-Webster Unabridged: 52% of words used in books were absent from both dictionarie labelled "lexical dark matter" . | Track unique word types (vocabulary size), TTR, hapax legomena, and cumulative vocabulary per annual Wikipedia snapshot (2001–2024). Estimate dark matter against WordNet and Free Dictionary API as proxy for reference dictionary coverage.  | Done| 
| **2.Grammar Evolution** | Studied regularisation of 177 English irregular verbs across 200 years. Found 16% of verbs changed regularity by more than 10%. Six verbs fully regularised (burn, chide, smell, spell, spill, thrive). Regularisation originated in the US and spread to the UK. "Snuck" is replacing "sneaked" at approximately 1% of English speakers per year.| - | Not| 
| **3.Collective Memory** | Measured how often specific historical year-strings ( "1951", "1883") appeared in books published after those years. Found a characteristic two-component curve: a sharp short-term peak followed by slow long-term decay. "1880" lost half its peak frequency within 32 years, "1973" within just 10 years. Concluded that collective forgetting is accelerating across generations. | Track the frequency of historical year-strings (1945, 1969, 1989, 2001, 2008, 2016, 2020) in Wikipedia annual snapshots taken after those years. Compare half-life of mention frequency with Michel(2011) values to test whether digital encyclopaedic memory decays at the same rate.  | Done| 
| **4.Technology Diffusion** | Tracked 147 inventions as 1-grams across three 40-year cohorts (1800–1840, 1840–1880, 1880–1920). Measured years from invention to 25% of peak frequency. Found S-curves of cultural adoption shortened from over 66 years (earliest cohort) to 27 years (latest cohort), demonstrating that society absorbs new technologies progressively faster. | - | Not|
| **5.Fame Tracking** | Used 740,000  person entries to build name lists, then tracked name frequency in Google Books over time (1800–1950 cohorts, 50 most famous people per birth year). Found peak fame occurs consistently at 75 years after birth. | - | Not | 
| **6.Censorship / Suppression** | Proposed the suppression index: s = freq(contested period) / freq(baseline). Marc Chagall's full name appeared only once in German books across 1936–1944 (s ≈ 0), while English frequency rose continuously. Applied to five categories of people on Nazi banned lists: artists suppressed by 56%, philosophers by 76%, politicians by 60%, historians by 9%, writers by 27%. Nazi party members surged by 500%. 9.8% of individuals in German corpus showed strong suppression (s < 0.2). | Adapt the suppression index to detect endogenous editorial self-censorship in Wikipedia, replacing external state censorship with shifts in community-driven discourse | Done| 

***
##### Tools:  
Python 3.x. Python Software Foundation. https://www.python.org/.    
requests (v. 2.34.2). Kenneth Reitz. https://pypi.org/project/requests/.   
nltk — Natural Language Toolkit. Bird, Steven, Edward Loper, and Ewan Klein. Natural Language Processing with Python. O'Reilly Media, 2009. https://www.nltk.org/.    
pandas. The Pandas Development Team. https://pandas.pydata.org/.     
matplotlib. Hunter, John D. "Matplotlib: A 2D Graphics Environment." Computing in Science and Engineering 9, no. 3 (2007): 90–95. https://doi.org/10.1109/MCSE.2007.55.     
scipy. Virtanen, Pauli, et al. "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python." Nature Methods 17 (2020): 261–272. https://doi.org/10.1038/s41592-020-0772-5.     
numpy. Harris, Charles R., et al. "Array Programming with NumPy." Nature 585 (2020): 357–362. https://doi.org/10.1038/s41586-020-2649-2.     
Jupyter Notebook / JupyterLab. Project Jupyter. https://jupyter.org/.     
MediaWiki API. Wikimedia Foundation, 2024. https://www.mediawiki.org/wiki/API:Main\_page.    
***
##### References
Michel, Jean-Baptiste, et al. "Quantitative Analysis of Culture Using Millions of Digitized Books." Science 331, no. 6014 (2011): 176–182. https://doi.org/10.1126/science.1199644

Pechenick, Eitan Adam, Christopher M. Danforth, and Peter Sheridan Dodds. "Characterizing the Google Books Corpus." PLOS ONE 10, no. 10 (2015): e0137041. https://doi.org/10.1371/journal.pone.0137041

Jurafsky, Daniel, and James H. Martin. Speech and Language Processing. 3rd ed. draft, 2023. https://web.stanford.edu/~jurafsky/slp3/

Sinclair, John. Corpus, Concordance, Collocation. Oxford University Press, 1991.

---
##### Author:
Aim Batalova — Ca'Foscari University — email: aim.b14.04git@gmail.com
***
##### License:

