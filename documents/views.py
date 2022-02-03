import collections
from pydoc import doc
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from documents.forms import DocumentForm
from .models import Document
from .serializers import DocumentSerializer
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
class DocumentListView(APIView):

    # def upload_file(request):
    #     if request.method == 'POST':
    #         form = DocumentForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('')
    #     else:
    #         form = DocumentForm()
    #     return render(request, 'upload.html', {'form': form})

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
            # a = word_tokenize(g.lower())
            stop_words = set(stopwords.words('english'))
            # stop_words = stop_words.extend(['us', ' ', 'must'])
            wordcount = {}
            for words in g.lower().split():
                words = words.replace('.', '')
                words = words.replace(',' ,'')
                words = words.replace('!' , '')
                words = words.replace('?' , '')
                if words != '':
                    if words not in stop_words:
                        if words not in wordcount:
                                wordcount[words] = 1
                        else:
                            wordcount[words] += 1

            word_counter = collections.Counter(wordcount)
            new_word_counter = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
            first_ten = new_word_counter[0:10]
            for pair in first_ten:
                print(pair)
            return Response(status=status.HTTP_200_OK)

        except:
            print('error')
            return Response(status=status.HTTP_404_NOT_FOUND)



