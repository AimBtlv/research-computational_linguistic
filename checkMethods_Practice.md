### Basic Approach 
---
**Featured articles** are articles on the English Wikipedia that the Wikipedia community has deemed to be of the highest quality. They are:thoroughly reviewed,well written, neutral, contain high-quality sources, high-quality examples.
There are only a few thousand of them, while the English Wikipedia has over 7 million articles.
#### Method 1
Метод 1 — Лексикон
Michel et al.|Наш эксперимент
|-------|-------|
Все 1-граммы в Google Books по годам | Все уникальные слова в Wikipedia English по годам (через годовые дампы revision history)|
Рост с 544K (1900) до 1.02M слов (2000)|Рост лексикона Wikipedia 2001→202452% |
«тёмная материя» — не в словарях| Доля слов Wikipedia не в WordNet/словарях

---
Параметры Эксперимента
Параметр|Значение
|----|---|
|Корпус|50–100 Wikipedia Featured Articles, разные темы|
Период|2001–2024 (годовые срезы)
Источник текста|MediaWiki Revisions API
Словари для "тёмной материи"|WordNet (NLTK) + Free Dictionary API
Метрики|Types, Tokens, TTR, Hapax legomena, Cumulative vocabulary, Heaps' Law

Методологическая Проблема, Которую Нужно Явно Прописать
Это критически важно для секции Limitations/Methodology — и вот почему обе твои интуиции (про "весь корпус" и про OED) были абсолютно правильными методологическими инстинктами:

Проблема Выборки vs. Полного Корпуса


>Unlike Michel et al., who analysed n-gram frequencies across their entire 5-million-book corpus, this study uses a sample of 50–100 Wikipedia Featured Articles as a proxy corpus. This is a deliberate trade-off between API access constraints and methodological rigor: Featured Articles are themselves a quality-filtered subset (curated and peer-reviewed by Wikipedia editors), which creates a loose parallel to Michel et al.'s own quality-based filtering of 5M books from 15M digitised. However, this sample is not statistically representative of the full English Wikipedia corpus (6.8M+ articles), and any generalisations beyond the sampled articles should be treated as exploratory rather than confirmatory.

Проблема WordNet vs. Oxford English Dictionary 

>Michel et al. validated lexical coverage against two independent reference dictionaries (OED and Merriam-Webster Unabridged) to estimate the proportion of "lexical dark matter." This study uses WordNet as the primary reference — not because it is equivalent to OED, but because it is the only freely programmable lexical database accessible without institutional subscription. WordNet differs structurally from OED: it is a semantic network organised around synsets (139,000+ words) rather than a historical lexicographic record (600,000+ words with etymology). This substitution likely overestimates the proportion of "dark matter," since many genuinely common words may be absent from WordNet's more limited and NLP-oriented coverage. Cross-validating against the Free Dictionary API partially mitigates — but does not eliminate — this limitation.

Это твой готовый текст для секции Limitations — academically честный и показывает что ты понимаешь разницу.

---
ШАГ 1: Получить список Featured Articles
        → Wikipedia API: Category:Featured_articles
        → Отобрать 50-100 случайных / стратифицированных по теме

ШАГ 2: Для каждой статьи получить годовые срезы 2001-2024
        → Revisions API (как в предыдущем коде)
        → Кешировать в JSON (чтобы не повторять запросы)

ШАГ 3: Построить годовой АГРЕГИРОВАННЫЙ корпус
        → corpus[year] = объединённый текст ВСЕХ статей за этот год
        → Это и есть твой "годовой подкорпус", аналог книг 1900 года у Michel et al.

ШАГ 4: Вычислить метрики по годам
        → tokens, types, TTR, hapax, cumulative vocabulary

ШАГ 5: Построить Heaps' Law проверку
        → log(tokens) vs log(types) → должна быть прямая линия

ШАГ 6: Проверить "тёмную материю"
        → Для словаря 2024 года: какой % НЕ в WordNet
        → Дополнительно: какой % НЕ в Free Dictionary API
        → Сравнить два процента

ШАГ 7: Визуализация (как в Fig. 2A-B Michel et al.)
        → График роста словаря
        → График TTR
        → Heaps' Law scatter
        → Bar chart покрытия словарей


>В статье авторы построили огромный корпус книг. Для каждого года они имели 1800 -98 миллионов слов, для 1900 -1.8 миллиарда слов. После этого они считали:частоту слов, изменение словаря, грамматику, популярность людей, появление технологий, коллективную память. То есть сначала создавался годовой корпус, а потом проводились различные исследования.


####  Method 1  Lexicon Growth, TTR, Hapax Legomena

For each year, we pool the text of all articles that existed by that year into a single yearly sub-corpus (this mirrors Michel(2011) yearly word bins, e.g. "98 million words by 1800").    
In other words, the unit of analysis is not a single book or article, but the entire text for a single year. This allows us to construct time series and observe how the use of words, terms, and topics changes over time. This principle directly replicates the methodology of Michel et al., but instead of millions of digitized books, we use historical versions of Wikipedia articles.

We compute:
- **Tokens**:  total word count
- **Types**: unique word count (vocabulary size)
- **TTR**: Type-Token Ratio = types / tokens
- **Hapax legomena**: words occurring exactly once
- **Cumulative vocabulary**:  running total of all unique words ever seen up to that year

#### Связь с подходом Michel et al.

Этот код реализует ту же идею, что и в статье Michel et al., но на другом типе данных. В статье авторы сначала объединяли все книги одного года в единый корпус, а затем подсчитывали общее число слов, уникальных слов и частоты отдельных слов для этого года.

В вашем notebook происходит аналогичный процесс:

Берутся все статьи Википедии за определённый год.
Их тексты объединяются в единый годовой подкорпус (year_tokens).
Для этого подкорпуса вычисляются количественные характеристики:
tokens — общий объём корпуса в словах;
types — количество различных слов;
TTR — показатель лексического разнообразия;
cumulative vocabulary — накопленный словарь за все годы;
n_articles — число статей, вошедших в корпус.

Таким образом, каждая строка df_lex представляет собой статистическое описание Википедии за один год, что позволяет затем исследовать, как менялись объём текста, разнообразие словаря и развитие лексики во времени.
5.В статье Michel et al. авторы задавали вопрос:

Сколько слов реально используется в языке, но отсутствует в словарях?

Для этого они сравнивали огромный корпус Google Books с традиционными словарями и показали существование большого пласта "лексической тёмной материи" — слов, которые встречаются в текстах, но не зафиксированы в словарях.

Notebook повторяет ту же идею, но меняет источник данных и словарь сравнения:

корпус — исторические версии статей Википедии (2024 год);
лексический эталон — WordNet.

Поэтому интерпретация результата должна звучать аккуратно:

out_wn — это не "все неизвестные слова языка", а количество слов из корпуса Википедии, которые отсутствуют в WordNet. Среди них могут быть новые термины, собственные имена, географические названия, аббревиатуры, специализированная лексика и даже ошибки. Поэтому этот показатель рассматривается как WordNet-relative lexical dark matter — «лексическая тёмная материя относительно покрытия WordNet», а не как абсолютная оценка словарного состава английского языка.

---

#### Концептуальная Разница: Книги vs. Wikipedia
Michel et al. измеряли пассивную память — книги пишутся один раз и не меняются. Если год упоминается реже — его забыли.
Wikipedia — это активно редактируемый документ. Это значит:

Забывание в Wikipedia может выглядеть иначе — не как затухание частоты, а как реорганизация памяти: год не исчезает из текста, но меняет своё место (из основного нарратива в сноску, из введения в раздел «History»).

Это твой оригинальный «and so what» для эссе — проверяешь не просто воспроизводится ли паттерн Michel et al., но и меняется ли сама природа забывания в цифровом медиуме.