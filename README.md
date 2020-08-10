# MACK
The unofficial Enron email corpus search engine.

## Installing / Running

### Pre-requites
1. Install Python 3.5 or above
2. Download and save the sample and full enron email corpus as `enron` and `enron_mail_20150507`, respectively.

Build and install the package.
```
python setup.py build && python setup.py install
```

Run MACK. Make sure to run MACK in the same directory where the email corpus is located.
```
mack --search app
```

## What's next?
- MOAR UNIT TESTS. The unit test coverage is very low, and I would want to get that at 100%.
- The MACK search engine does not score the documents retrieved from a query. I found a ton of choices while I was researching about search engines, and it would be a cool weekend project to add scoring functionality. Some example choices: BM25, PageRank, tf-idf.
- Reduce index build time. The build time takes about 12 seconds for the sample data set which is about 12mb. I briefly used Python's `cProfiler` and `guppy` to profile runtime and memory, but I felt it wasn't enough time to really find some optimizations. I could also take a step back and look at the architecture from a high-level and judge if it is really optimal.
- Support multi-term querying. You can provide multiple terms to MACK, but it will only use the first term to query the inverted index. When I was started the challenge, I wanted to support phrase querying but quickly realized it was extremely ambitious to support that in two days.

## Resources I used to help me complete the challenge.
- https://nlp.stanford.edu/IR-book/html/htmledition/positional-indexes-1.html
- https://www.youtube.com/watch?v=cY7pE7vX6MU&t=1106s
- https://artem.krylysov.com/blog/2020/07/28/lets-build-a-full-text-search-engine/

## F.A.Q.
- Q: What does MACK stand for? A: Absolutely, nothing.
