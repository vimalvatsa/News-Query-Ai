from rest_framework.views import APIView
from rest_framework.response import Response
from Constants.constants import (
    flatten_serializer_errors,
    TypeOfSearch,
)
from VectorDB.VectorDB import vector_db
from Application.Utilities.RAGCommon import create_collection_name
from Application.serializer.DocumentAssess import DocumentAssessSerializers
from DocAssess.query import assess_doc


class DocAssessClass(APIView):
    def get(self, request):
        data = {
            "document_id": request.GET.get("documentID")
        }
        header = request.headers.get("Org")
        serializer = DocumentAssessSerializers(data=data)
        if serializer.is_valid():
            document_id = serializer.validated_data["document_id"]
            collection_name = create_collection_name(header, TypeOfSearch.default)
            document_exists = vector_db.check_file_existence(
                document_id, collection_name, TypeOfSearch.default
            )
            if document_exists:
                result = assess_doc(
                    header=header,
                    collection_name=collection_name,
                    doc_id=document_id
                )
                return Response(data=result, status=200)
            else:
                return Response(
                    {"Message": "Document is not available"},
                    status=400,
                )
        else:
            return Response(
                status=400,
                data={"Message": flatten_serializer_errors(serializer.errors)},
            )
