import pandas as pd
import re


def get_question(x):
    """
        Takes in a string and returns a tuple as a question/answer pair

        Inputs: x - string
        Outputs: question - string until the word "during" appears, and with a
                            blank in place of any starting capitalized words.
                 answer - string with words for the blank part of the question.
    """
    # Get rid of text post during
    try:
        x = x[:x.index('during')]
    except:
        pass
    answer = x
    # Find all text before the first lower case word
    try:
        first_lower_case_word = re.findall('\s[a-z]+', x)[0]
        answer = x[:x.index(first_lower_case_word)]
    except:
        pass
    # Sub capital words' letters with blanks
    # print(re.sub('(\S)','_',x))
    # Sub capital words with a blank
    question = x.replace(answer,"___________")
    return question, answer


# File to load with IPL photo descriptions
data_file_path = 'output.csv'
df = pd.read_csv(data_file_path,index_col=None)
# Remove carriage characters from the Description
df['Description'] = [s.replace('\r', '') for s in df['Description']]
# Get Question/Answer pairs and unpack them
df['Question/Answer'] = [get_question(x) for x in df['Description']]
df[['Question', 'Answer']] = pd.DataFrame(df['Question/Answer'].tolist(), index=df.index)
df.drop(['Question/Answer'], axis = 1, inplace = True)
# Save data to the same file as it was loaded from
df.to_csv(data_file_path, index = False)
print(df.head())
