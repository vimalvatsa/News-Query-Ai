from rest_framework import serializers


class DocumentUploadSerializers(serializers.Serializer):
    """This contains serializers to upload Documents"""

    document_id = serializers.CharField()
    document_file = serializers.FileField()
    type_of_search = serializers.CharField()


class DocumentDeleteSerializers(serializers.Serializer):
    """This contains serializers to delete Documents"""

    document_id = serializers.CharField()
    type_of_search = serializers.CharField()


class DocumentCheckSerializers(serializers.Serializer):
    """This contains serializers to check Documents"""

    document_id = serializers.CharField()
    type_of_search = serializers.CharField()
