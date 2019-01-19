"""
Use TextBlog spelling correction on the sentence 'the rain in sspain
stayss mainly on the plan'
"""

# make the textblog package available
import textblob

# our phrase to correction
sentence = 'the raain in sspain stayys mainly on the plane'

# create an instance of TextBlog using our sentence
blog = textblob.TextBlob(sentence)

# correct the spelling errors
corrected = blog.correct()

sentence2 = 'proffesor Dumbledore is my faverite'

blog2 = textblob.TextBlob(sentence2)

corrected2 = blog2.correct()

print(corrected)
print(corrected2)
