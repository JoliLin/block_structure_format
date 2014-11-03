block_stucture_format
=====================
python bsFormat.py original_data<br>
or<br>
python bsFormat.py original_data -tfidf<br>

To convert a csv-like format to the format for libFM of block structure.

requirements
---------------------
- nltk==2.0.4

origin text format:
---------------------
item1:user1:score1<br>
item2:user2:score2<br>
item3:user3:score3<br>
.<br>
.<br>

after executing, it creates a new directory named 'block_data', it contains:
---------------------
- ans.data
- mapping
- mapping_i
- rel-iid
- rel-iid.data
- rel-iid2num
- rel-iwid
- rel-iwid.data
- rel-uid
- rel-uid.data
- rel-uid2num
- rel-uwid
- rel-uwid.data
- rel-wid
- rel-wid2num

