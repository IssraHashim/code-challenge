import collections
from webbrowser import get
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from nltk.corpus import stopwords
from .utils import split_and_clean_words

def get_file_text(pk: int) -> tuple[str, str]:
    """
    Given a document id, return a tuple of the (filename, file_text)
    """
    # Get document text into variable
    document = Document.objects.get(id=pk)
    serialized_doc = DocumentSerializer(document)
    title = document.title
    url = serialized_doc.data['file'].replace('/', '')
    with open(url) as file:
        return (title, file.read())

class DocumentListView(APIView):

    def get(self, _request):
        documents = Document.objects.all()
        serialized_documents = DocumentSerializer(documents, many=True)
        return Response(serialized_documents.data, status=status.HTTP_200_OK)


class DocumentDetailView(APIView):
    def get(self, request, pk):
        try:
            title, file_text = get_file_text(pk)
            # Split into words and clean
            # stop_words = set(stopwords.words('english'))
            # wordcount = {}
            # BAD_WORDS = ['us', 'let', 'we', 'you','would', 'must']
            # for word in file_text.lower().split():
            #     word = word.replace('.', '')
            #     word = word.replace(',' ,'')
            #     word = word.replace('!' , '')
            #     word = word.replace('?' , '')
            #     word = word.replace('-' , '')
            #     word = word.replace('\'s' , '')
            #     word = word.replace('\'ve' , '')
            #     word = word.replace('\'re' , '')
            #     if word != '':
            #         if word not in stop_words and word not in BAD_WORDS:
            #             if word not in wordcount:
            #                     wordcount[word] = 1
            #             else:
            #                 wordcount[word] += 1
            wordcount = split_and_clean_words(file_text)
            
            # Count remaining words
            word_counter = collections.Counter(wordcount)
            
            first_ten = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)[:10]
            results = [title]

            # Find sentences
            for key, value in first_ten:
                sentences = []
                for sentence in file_text.split('.'): 
                    if ((key in (sentence.split(' '))) or (key.capitalize() in (sentence.split(' ')))):
                        sentence = sentence.replace('\n', '')
                        sentence = sentence.replace('\"', '')
                        sentences.append(sentence)
                    
                results.append([key, value, sentences])

            # return response
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            print(f'The exception was {e}')
            return Response(status=status.HTTP_404_NOT_FOUND)



