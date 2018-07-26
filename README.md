# cape-splitter [![CircleCI](https://circleci.com/gh/bloomsburyai/cape-splitter.svg?style=svg&circle-token=68966f5dec4f929336d0ef75917c895d12152e98)](https://circleci.com/gh/bloomsburyai/cape-splitter)

## Functionality 

Cape splitter provides the following functionality:
    
   * Split documents into groups, keeping full sentences and extracting overlapping text before and after the group.
   * Return batches, grouping batches by number of words.

## Performance 

Tokenization and splitting is done in 3.7 secs for [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) on a MacBook Pro (mid-2015 with 2.2 GHz Intel Core i7). 