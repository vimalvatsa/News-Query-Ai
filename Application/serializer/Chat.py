from rest_framework import serializers

class DocChatSerializers(serializers.Serializer):
    """This contains serializers to chat with document"""

    document_id = serializers.CharField()
    query = serializers.CharField()
    type_of_search = serializers.CharField(allow_blank=True, allow_null=True)
    top_k = serializers.IntegerField(default=10)
    threshold = serializers.FloatField(default=0.5)

    def validate(self, data):
        if data["type_of_search"] not in ["Document", "Model"]:
            raise serializers.ValidationError("Not a valid Search Option!")
        return data
