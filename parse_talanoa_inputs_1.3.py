'''
    August Granath
    IAF Capstone
    Parse PDFs
'''

LOSS_AND_DAMAGE = [
    ['loss', 'and', 'damage']
]

ADAPTATION_MITIGATION = [
    ['prevent'], 
    ['avoid'], 
    ['proactive'],
    ['reducing', 'and', 'reversing', 'loss', 'and', 'damage'], 
    ['reducing', 'and', 'minimizing'],
    ['averting', 'and', 'reducing'],
    ['minimizing', 'risks'],
    ['potential', 'loss', 'and', 'damage'], 
    ['potential', 'impact'],
    ['loss', 'and', 'damage', 'is', 'under', 'adaptation'],
    ['humanitarian', 'response'],
    ['unfortunate']
]

RISK_MANAGEMENT = [
    ['climate', 'risk', 'management'], 
    ['comprehensive', 'climate', 'management'],
    ['holistic'],
    ['total', 'risk'], 
    ['risk', 'layering'], 
    ['high-level', 'losses'],
    ['changing', 'risk', 'profile'], 
    ['evolving', 'risk'], 
    ['socio-economic', 'thresholds'], 
    ['extreme', 'events'],
    ['downside', 'risks'], 
    ['risk', 'financing'], 
    ['financial', 'instruments'],
    ['risk', 'management', 'tools'], 
    ['objective', 'data', 'driven', 'solutions'], 
    ['operational', 'solutions'],
    ['early', 'intervention'], 
    ['risk', 'reduction'], 
    ['early', 'warning', 'systems'],
    ['risk', 'pooling'], 
    ['regional', 'risk', 'pool'], 
    ['contingency', 'planning'],
    ['post-disaster', 'recovery'], 
]

LIMITS_TO_ADAPTATION = [
    ['limits', 'to', 'adaptation'], 
    ['adaptation', 'limits'],
    ['adaptation', 'constraints'], 
    ['physical', 'limits'],
    ['social', 'limits'], 
    ['beyond', 'adaptation'],
    ['residual', 'loss', 'and', 'damage'], 
    ['residual', 'impacts'],
    ['migration'], 
    ['saline', 'intrusion'], 
    ['non-economic', 'losses'], 
    ['climate-related', 'stressors'],
    ['community-based'],  
    ['livelihoods'], 
    ['vulnerable'], 
    ['poor', 'and', 'marginalized'],
    ['micro', 'insurance']
]

EXISTENTIAL = [
    ['residual', 'harm'], 
    ['permanent'], 
    ['irreversible'], 
    ['irreplaceable'], 
    ['gone', 'forever'], 
    ['reality'], 
    ["it's", 'happening'], 
    ['undeniable'],
    ['unavoidable'], 
    ['nonmarket', 'loss', 'and', 'damage'], 
    ['non-economic', 'losses'], 
    ['sea-level', 'rise'], 
    ['islands'], 
    ['displacement'], 
    ['refugees'],
    ['loss', 'of', 'homeland'],
    ['resettlement'], 
    ['reconstruction'], 
    ['rehabilitation'], 
    ['restoration'], 
    ['compensation'], 
    ['ex', 'post'], 
    ['responsibility'], 
    ['anthropogenic', 'climate', 'change'],
    ['justice'],
    ['liability'], 
    ['equity'],
    ['human', 'rights'], 
    ['increase', 'mitigation'], 
    ['more', 'serious', 'about', 'mitigation']
]

KEYWORD_LISTS = [
    LOSS_AND_DAMAGE,
    ADAPTATION_MITIGATION, 
    RISK_MANAGEMENT, 
    LIMITS_TO_ADAPTATION, 
    EXISTENTIAL
    ]

CATEGORY_NAMES = [
    'Loss and Damage',
    'Adaptation and Mitigation',
    'Risk Management',
    'Limits to Adaptation',
    'Existential'
]

DIRECTORY = 'Talanoa_txt_v2/'

from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import csv
import os

def open_txt(filename):
    '''
        function open_txt
        parameters: filename, a string containing the name of the txt file to
                        open.
        returns: txt_list a list containing the data imported from the txt file
        does: opens a txt file and imports the data into a previously empty 
              list and returns the list containing the information from the txt
    '''

    txt_list = []
    
    # open the txt file
    with open(filename, 'r') as txt:

        # append the data in the txt file to previously empty list
        for item in txt: 
            txt_list.append(item)

    # return the list with the txt data
    return txt_list

def format_txt(txt):
    '''
        function clean_txt
        parameters: txt, a list of strings
        returns: clean_txt, a list of strings, prepared for processing
        does: takes a list of strings and creates a new list that contains
              single, lower-case, words, stripped of white spaces.
        sources: 
        https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        https://chrisalbon.com/python/basics/cleaning_text/
        https://streamhacker.com/2011/10/31/fuzzy-string-matching-python/
    '''

    # tokenize list of strings from .txt
    tokenized_txt = [word_tokenize(element) for element in txt]

    # create an empty list to contain formatted text
    clean_txt = []

    # iterate over tokenized text and turn all text into lower case, strip
    # leading and trailing spaces, and append each individual word to the
    # clean_txt list
    for sublist in tokenized_txt:
        for item in sublist:
            item = item.lower()
            item = item.strip()
            clean_txt.append(item)

    # return formatted list of words
    return clean_txt

def ngram_txt(txt, num):
    '''
        function ngram_txt
        parameters: txt, a formatted list of individual words
                    num, an integer, the number of words the caller wants to
                    include in each ngram
        returns: ngram_list, a list, ngramified txt
    '''

    # initialize numgram, a variable to contain the list of tuples returned by
    # the ngrams function
    numgram = list(ngrams(txt, num))

    # initialize empty list to contain formatted ngram
    ngram_list = []

    # iterate over list of tuples
    # save each tuple as a list
    # append it to ngram_list
    for tuple in numgram:
        ngram_list.append(list(tuple))
    
    return ngram_list

def count_keywords(txt, category):
    '''
        function count_keywords
        parameters: txt, a list of lists of strings, formatted .txt data
                    category, a list of lists of strings, keywords
        returns: category_score, an integer, the total number of words or phrases from
                    keywords found in txt
                 keyword_list, a list of lists, unique words or phrases found 
                    in txt
                 keyword_count, a list of integers, count of each unique word
                    or phrase found in keyword_list. Index of keyword_count
                    matches index of keyword_list
    '''

    # initialize variables to be returned
    category_score = 0
    keyword_list = []
    keyword_count = []

    # iterate over list of keywords
    for keyword in category:
        
        # initialize a variable to indicate if the keyword has
        # already been appended to keyword_list
        # 0 = not yet added / 1 = already added
        already_added = 0
        
        # for every word or phrase in the txt
        for word_or_phrase in txt:

            # if the word or phrase matches a keyword has already been added, skip it
            if already_added == 1:
                break

            # if the word or phrase matches a keyword, add the keyword as a new
            # key to keywordcount_dict with a value of 0.
            # change value of already_added to indicate that the keyword has 
            # been added
            elif word_or_phrase == keyword:
                keyword_list.append(word_or_phrase)
                keyword_count.append(0)
                already_added += 1

    # now that we have a comprehensive list of keywords that appear in this txt
    # iterate over the txt and count the number of times each keyword appears 
    for word_or_phrase in txt:

        for keyword in keyword_list:
        
            if word_or_phrase == keyword:
                category_score += 1
                keyword_count[keyword_list.index(keyword)] += 1  

    return category_score, keyword_list, keyword_count

def initialize_output(keyword_lists, max_n):
    '''
        function initialize_output
        parameters: 
            keyword_lists, a list of variables, each containing 
                a list of lists of strings, each list of strings representing
                a key word or phrase
            max_n, integer, the largest number of words in a keyphrase

        returns: 
            output_list, a list of lists of strings, the first list
                of lists containing headers for a .csv readout
        does: takes a list of variables representing keyword_lists and creates
            a new list of lists, output_list. The first list in output list 
            contains the field names for a .csv output. ouput_list is designed
            so that each new file analyzed will yield results that can be
            appended as a new row to the output_list
    '''

    # initialize output_list with first two fieldnames in header list
    output_list = [['Key', 'Filename']]
    output_index = [['Key', 'Filename']]

    #  iterate over category lists and append category titles to header list
    for name in CATEGORY_NAMES:
        output_list[0].append(name)
        output_index[0].append(name)

    # iterate over category lists
    for category in keyword_lists:

        # iterate over each list containing key words or phrases
        # create and append a string containing the key word or phrase as a new
        # fieldname in the header list
        for keyword in category:

            output_index[0].append(keyword)

            field_name = ''

            for i in list(range(max_n)):

                if len(keyword) == i+1:
                    index = list(range(len(keyword)))

                    for i in index:
                        field_name += keyword[i] + ' '
            
            field_name = field_name.strip()
            output_list[0].append(field_name)

    return output_list, output_index

def main():

    output_filename = 'Parse_Talanoa_Inputs_Results_v1.3'
    
    output_list, output_index = initialize_output(KEYWORD_LISTS, 6)

    file_num = 0

    # iterate over .txt files
    for file in os.listdir(DIRECTORY):
    #for file in FILE_LIST:

        #output_txt.write('File: ' + file)
        # exclude hidden files
        if not file.startswith('.'):
            
            # open and clean .txt data
            txt = open_txt(DIRECTORY + file)
            clean_txt = format_txt(txt)

            # initialize a list to contain keyword count data
            new_row = [file_num, file]
            category_results = {}

            # add placeholder 0s to contain keyword count data
            for i in range(len(output_list[0])-2):
                new_row.append(0)
        
            # increase file_num by one
            file_num += 1
        
            # iterate over ngrams of various sizes
            for n in [1,2,3,4]:
                ngram = ngram_txt(clean_txt, n)

            #output_txt.write('For' + n + 'gram')

                # count keywords
                for category in KEYWORD_LISTS:
                    category_score, keyword_list, keyword_count = count_keywords(ngram, category)

                    # update category score in new_row
                    new_row[output_list[0].index(CATEGORY_NAMES[KEYWORD_LISTS.index(category)])] += category_score
                    #output_txt.write(CATEGORY_NAMES[KEYWORD_LISTS.index(category)]+ ' Scored: ' + category_score,)
                
                    # update key word or phrase score in new_row
                    for keyword in keyword_list:
                        #output_txt.write('As ' + keyword + 'appeared ' + keyword_count[keyword_list.index(keyword)] + 'times.')
                        new_row[output_index[0].index(keyword)] += keyword_count[keyword_list.index(keyword)]

            # create txt readout for file
            #output_txt.write('File:', file)

            #   for category in KEYWORD_LISTS:
            #       output_txt.write(CATEGORY_NAMES[KEYWORD_LISTS.index(category)]), 'Score:', new_row[KEYWORD_LISTS.index(category)+2])  
        
            output_list.append(new_row)
            print(file_num, 'files parsed\n')
            #output_txt.write('')
    
    #write results to csv
    with open(output_filename + '.csv', 'w') as output_csv:
        wr = csv.writer(output_csv, quoting=csv.QUOTE_ALL)
        
        for i in range(len(output_list)):
            wr.writerow(output_list[i])

main()
