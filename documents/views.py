import collections
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from nltk.corpus import stopwords
from tabulate import tabulate
class DocumentListView(APIView):

    def get(self, _request):
        documents = Document.objects.all()
        serialized_documents = DocumentSerializer(documents, many=True)
        return Response(serialized_documents.data, status=status.HTTP_200_OK)


class DocumentDetailView(APIView):
    def get(self, request, pk):
        try:
            document = Document.objects.get(id=pk)
            serialized_document = DocumentSerializer(document)
            url = serialized_document.data['file'].replace('/', '')
            file = open(url)
            g = file.read()
            stop_words = set(stopwords.words('english'))
            wordcount = {}
            for words in g.lower().split():
                words = words.replace('.', '')
                words = words.replace(',' ,'')
                words = words.replace('!' , '')
                words = words.replace('?' , '')
                words = words.replace('-' , '')
                words = words.replace('\'s' , '')
                words = words.replace('\'ve' , '')
                words = words.replace('\'re' , '')
                if words != '':
                    if words not in stop_words:
                        if words not in wordcount:
                                wordcount[words] = 1
                        else:
                            wordcount[words] += 1

            word_counter = collections.Counter(wordcount)
            new_word_counter = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
            first_ten = new_word_counter[0:10]
            results = []
            for key, value in first_ten:
                if key != 'us' and key != 'let' and key != 'we' and key != 'you' and key !='would' and key!= 'must':
                    print(key)

                    sentences = []
                    for sentence in g.split('.'):
                        if ((key in (sentence.split(' '))) or (key.capitalize() in (sentence.split(' ')))):
                            sentence = sentence.replace('\n', '')
                            sentence = sentence.replace('\"', '')
                            sentences.append(sentence)
                    
                    results.append([key, value, sentences])

            col_names = ['words', 'occurences', 'sentences']
            table = tabulate(results, headers=col_names)
            return Response(results, status=status.HTTP_200_OK)

        except:
            print('error')
            return Response(status=status.HTTP_404_NOT_FOUND)



