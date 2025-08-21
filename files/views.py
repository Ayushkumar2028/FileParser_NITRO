import threading
import time

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import FileUpload
from .serializer import FileUploadSerializer

import pandas as pd

import pdfplumber

import os
from django.conf import settings
# Create your views here.

class FileUploadView(APIView):
    def post(self,request):
        chunk = request.FILES.get("file")
        chunk_number = int(request.POST.get("chunk_number", 1))
        total_chunks = int(request.POST.get("total_chunks", 1))
        file_id = request.POST.get("file_id")

        if not file_id:
            file_record = FileUpload.objects.create(
                filename=chunk.name,
                status="uploading",
                progress=0,
            )
            file_id = str(file_record.id)
            temp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, f"{file_id}.part")
            with open(temp_path, "wb") as f:
                f.write(chunk.read())
            file_record.save()
        else:
            file_record = get_object_or_404(FileUpload, id=file_id)
            temp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
            temp_path = os.path.join(temp_dir, f"{file_id}.part")
            with open(temp_path, "ab") as f:
                f.write(chunk.read())

        progress = int(chunk_number / total_chunks * 100)
        file_record.progress = progress
        file_record.save()

        if chunk_number == total_chunks:
            final_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_record.filename)
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            os.rename(temp_path, final_path)

            file_record.file.name = os.path.relpath(final_path, settings.MEDIA_ROOT)
            file_record.save()


        thread=threading.Thread(target=parse_file,args=(file_record,))
        thread.daemon = True
        thread.start()

        return Response({"file_id":file_id, "progress": file_record.progress},status=201)

    def get(self,request):
        files=FileUpload.objects.all()
        serializer=FileUploadSerializer(files,many=True)
        return Response(serializer.data)

def parse_file(fileobj:FileUpload):
    try:
        fileobj.status="processing"
        fileobj.save()
        for i in range(0,100,20):
            fileobj.progress=i
            fileobj.save()
            time.sleep(10)

        parsedContent=None
        filepath = fileobj.file.path

        if filepath.endswith(".csv"):
            f=pd.read_csv(filepath)
            parsedContent=f.to_dict(orient="records")

        elif filepath.endswith(".xls") or filepath.endswith(".xlsx"):
            f = pd.read_excel(filepath)
            parsedContent= f.to_dict(orient="records")

        elif filepath.endswith(".pdf"):
            parsedContent = []
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        parsedContent.append({"page": page.page_number, "text": text})

        else:
            fileobj.status = "failed"
            fileobj.save()
            return

        fileobj.parsed_data=parsedContent
        fileobj.status="ready"
        fileobj.progress=100
        fileobj.save()

    except Exception as e:
        fileobj.status="failed"
        fileobj.save()

class FileProgressView(APIView):
    def get(self, request, file_id):
        fileobj = get_object_or_404(FileUpload, id=file_id)
        return Response({
            "file_id": str(fileobj.id),
            "status": fileobj.status,
            "progress": fileobj.progress,
        })


class FileContentView(APIView):
    def get(self, request, file_id):
        fileobj = get_object_or_404(FileUpload, id=file_id)

        if fileobj.status in ["uploading","processing"]:
            return Response({"message": "File upload or processing in progress. Try later."},status=202,)
        if fileobj.status == "failed":
            return Response(
                {"message": "Parsing failed.","error": fileobj.parsed_data.get("error") if fileobj.parsed_data else None,},
                status=500,)
        if fileobj.status == "ready":
            return Response(fileobj.parsed_data, status=200)


class FileDeleteView(APIView):
    def delete(self, request, file_id):
        fileobj = get_object_or_404(FileUpload, id=file_id)
        fileobj.delete()
        return Response({"message": "File deleted"}, status=204)


