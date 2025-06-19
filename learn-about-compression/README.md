# FILE TO STRING Conversion 
    - In this experiment, I am trying to build a simple compression tool to maybe include my notes inside a row in the database. In trying to achieve that, I have few things in my mind that may work in achieving that goal. 

## Tools
    - My vibe coding tool to use at the moment is **Cursor IDE**.
    - Compression tools:
        - gzip
        - bzip2
        - zstandard
    - language
        - Python

## Methodology
    1. In my mind, the way to go is to use base64 string then use that when inserting inside a column.
    2. Another way that I can think of solving my problem is to compress the file that i am trying to convert, then show it's base64 string.

## What happenned
    - Using the first approach did not proceed very well. Converting the file into base64 increased the size of the file by about 30% which is huge if i needed contain the string in a smaller column.
    - Approach number 2 looked promising in my mind. I thought of looking for recommendations that could fit my needs. Through looking I managed to try several compression algorithms that are available. **GZIP**, **BZIP2** gave me the results that significantly reduced the file size to over 30% which is very good compared to the first approach.
    - The last recommendation that I was able to get is to just avoid base64 string and instead just use binary. After a few code revisions, I managed to reduce the file size reduced from 30%-40% approximately. This is even better however unsable for my case. 

## Summary
    - After a series of trying different methods, the smallest compression that was recommended and probably the having the best result is by converting my notes into binary. However, due to technical limitations of the targets, this may not be viable for the moment. This is a fun working experience and may help me sometime in the future.