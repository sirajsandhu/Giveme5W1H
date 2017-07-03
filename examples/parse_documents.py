import logging
import os
import sys

from extractor.extractor import FiveWExtractor
from extractor.extractors import action_extractor, environment_extractor, cause_extractor, method_extractor
from extractor.tools.file.handler import Handler


# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))

"""
Advanced example to use the extractor in combination with NewsPlease files
The output of the core_nlp_host is saved in the cache directory to speed up multiple runs. 
Documents are preloaded into memory and stay persistent for further calculations.

Documents are preprocessed just once, you have to set is_preprocessed to false, 
if you want to process them again by core_nlp
"""

# don`t forget to start up core_nlp_host
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

if __name__ == '__main__':
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    
    extractor = FiveWExtractor(extractors = [
                        #action_extractor.ActionExtractor,
                        #environment_extractor.EnvironmentExtractor,
                        #cause_extractor.CauseExtractor,
                        method_extractor.MethodExtractor()
                    ])
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'
    preprocessedPath = os.path.dirname(__file__) + '/cache'
    
    documents = (
                # initiate the file handler with the input directory
                Handler(inputPath)
                    # set a output directory
                    .setOutputPath(outputPath)
                    # set a path to save an load preprocessed documents - CoreNLP results
                    .setPreprocessedPath(preprocessedPath)
                    # limit the the to process documents (nice for development) 
                    .setLimit(1)
                    # add an optional extractor (it would do only copying without...)
                    .setExtractor(extractor)
                    # load and saves all document objects for further programming
                    .preLoadAndCacheDocuments()
                    # executing it
                    .process()
                    # get the processed documents
                    .getDocuments()
            )
    