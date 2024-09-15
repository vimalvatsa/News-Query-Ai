from rest_framework import serializers


class DocumentAssessSerializers(serializers.Serializer):
    """This contains serializers to upload Documents for assessment"""

    document_id = serializers.CharField()
