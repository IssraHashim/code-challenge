from pydoc import doc
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from documents.forms import DocumentForm
from .models import Document
from .serializers import DocumentSerializer



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
            print(url)
            g = open(url, 'r')
            print(g.readable())
            print(g.read())
            g.seek(0)
            print(g.readline())
            print(g.readlines())
            # with open('media/doc1_QqnKXb1.txt') as fp:
            #     line = fp.readline()
            #     cnt = 1
            #     while line:
            #         print("Line {}: {}".format(cnt, line.strip()))
            #         line = fp.readline()
            #         cnt += 1
            # f = open(f'{url}', 'r')
            # if f.mode == 'r':
            #     contents = f.read()
            #     print(contents)
            return Response(status=status.HTTP_200_OK)
        except:
            print('error')
            return Response(status=status.HTTP_404_NOT_FOUND)

