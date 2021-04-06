from bs4 import BeautifulSoup
from collections import Counter
from janome.tokenizer import Tokenizer
import termextract.janome
import termextract.core

with open('docs/src/index.html', 'r', encoding='UTF-8') as f:
    html = f.read()

soup = BeautifulSoup(html,"html.parser")

for script in soup(["script", "style"]):
    script.decompose()

text = soup.get_text()
lines = [line.strip() for line in text.splitlines()]
lines = []
for line in text.splitlines():
    lines.append(line.strip())

text = "\n".join(line for line in lines if line)

t = Tokenizer()
tokenize_text = t.tokenize(text)
frequency = termextract.janome.cmp_noun_dict(tokenize_text)

term_imp = termextract.core.score_pp(
    frequency,
    ignore_words=termextract.mecab.IGNORE_WORDS,
    average_rate=1)

# FrequencyからLR(単語の左右の連接情報)を生成
lr = termextract.core.score_lr(
    frequency,
    ignore_words=termextract.mecab.IGNORE_WORDS,
    lr_mode=1, average_rate=1)

# FrequencyとLRからFLRの重要度を求める
term_imp = termextract.core.term_importance(frequency, lr)
terms = Counter(term_imp)

c = Counter()
for cmp, value in terms.items():
    if len(cmp.split(' ')) != 1:
        c[termextract.core.modify_agglutinative_lang(cmp)] = value

for cmp, value in terms.most_common():
    print(cmp, value, sep='\t')