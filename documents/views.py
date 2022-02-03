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
            stopwords = set(line.strip() for line in open('stopwords.txt'))
            stopwords = stopwords.union(set(['the', 'a', 'to', 'on']))
            
            print(stopwords)
            wordcount = {}
            # with open(url) as fp:
            #     lines = fp.readlines()
            #     newLines = ''.join(map(str,lines))
            #     text = list(line.split() for line in lines)
            for words in g.lower().split():
                words = words.replace('.', '')
                words = words.replace(',' ,'')
                words = words.replace('!' , '')
                words = words.replace('?' , '')
                if words not in stopwords:
                    wordcount[words] = 1
                else:
                    wordcount[words] += 1

            word_counter = Counter(wordcount)
            for word, count in word_counter.most_common():
                print(word, count)
                    # print(max(set(list(new_sentence)), key=list(new_sentence).count))
                # new_list = [word for sentence in words for word in sentence]
                # data = Counter(new_list)
                # print(data.most_common(1)[0][0])
            return Response(status=status.HTTP_200_OK)
        except:
            print('error')
            return Response(status=status.HTTP_404_NOT_FOUND)

