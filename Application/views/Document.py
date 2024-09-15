import boto3
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from Constants.constants import (
    Utilities,
    create_s3_key,
    flatten_serializer_errors,
    TypeOfSearch,
)
from VectorDB.VectorDB import vector_db
from Application.Utilities.RAGCommon import create_collection_name, create_response
from Application.serializer.Document import (
    DocumentUploadSerializers,
    DocumentDeleteSerializers,
    DocumentCheckSerializers,
)
import random
import logging
from Application.models import UserAPICall
from django.utils import timezone

s3 = boto3.client("s3")
logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    def get(self, request):
        responses = ["I'm alive!", "All systems operational.", "Ready to serve!"]
        return Response({"status": random.choice(responses)})

class DocumentClass(APIView):
    def post(self, request):
        data = {
            "document_file": request.FILES.get("file"),
            "document_id": request.POST.get("documentID"),
            "type_of_search": request.POST.get("type_of_search", TypeOfSearch.default),
        }
        header = request.headers.get("Org")
        serializer = DocumentUploadSerializers(data=data)
        if serializer.is_valid():
            document_file = serializer.validated_data["document_file"]
            document_id = serializer.validated_data["document_id"]
            type_of_search = serializer.validated_data["type_of_search"]
            collection_name = create_collection_name(header, type_of_search)
            document_exists = vector_db.check_file_existence(
                document_id, collection_name, type_of_search
            )
            if document_exists:
                if type_of_search == TypeOfSearch.vault_model:
                    vector_db.delete_files(document_id, collection_name, type_of_search)
                else:
                    return Response(
                        {"Message": "Document is already uploaded"},
                        status=400,
                    )
            document_name = document_file.name
            s3_key = create_s3_key(
                collection_name, type_of_search, document_name, document_id
            )
            s3.upload_fileobj(document_file, Utilities.s3_bucket_name, s3_key)
            vector_db.add_files(
                s3_key, document_id, collection_name, header, type_of_search
            )
            response = create_response(type_of_search, document_id)
            return Response(
                data=response,
                status=200,
            )
        else:
            return Response(
                status=400,
                data={"Message": flatten_serializer_errors(serializer.errors)},
            )

    def delete(self, request):
        data = {
            "document_id": request.GET.get("documentID"),
            "type_of_search": request.GET.get("type_of_search", TypeOfSearch.default),
        }
        header = request.headers.get("Org")
        serializer = DocumentDeleteSerializers(data=data)
        if serializer.is_valid():
            document_id = serializer.validated_data["document_id"]
            type_of_search = serializer.validated_data["type_of_search"]
            collection_name = create_collection_name(header, type_of_search)
            document_exists = vector_db.check_file_existence(
                document_id, collection_name, type_of_search
            )
            if document_exists:
                vector_db.delete_files(document_id, collection_name, type_of_search)
                return Response(
                    data={"Message": "Document is deleted successfully"},
                    status=200,
                )
            return Response(
                data={"Message": "Document does not exist"},
                status=400,
            )
        else:
            return Response(
                status=400,
                data={"Message": flatten_serializer_errors(serializer.errors)},
            )


class CheckDocExistenceClass(APIView):
    def get(self, request):
        data = {
            "document_id": request.GET.get("documentID"),
            "type_of_search": request.GET.get("type_of_search", TypeOfSearch.default),
        }
        header = request.headers.get("Org")
        serializer = DocumentCheckSerializers(data=data)
        if serializer.is_valid():
            document_id = serializer.validated_data["document_id"]
            type_of_search = serializer.validated_data["type_of_search"]

            collection_name = create_collection_name(header, type_of_search)
            document_exists = vector_db.check_file_existence(
                document_id, collection_name, type_of_search
            )
            if document_exists:
                return Response({"Message": "Available"}, status=200)
            else:
                return Response({"Message": "Unavailable"}, status=200)
        else:
            return Response(
                status=400,
                data={"Message": flatten_serializer_errors(serializer.errors)},
            )
