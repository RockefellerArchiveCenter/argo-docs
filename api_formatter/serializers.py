from django.urls import reverse
from rest_framework import serializers


class ExternalIdentifierSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    source = serializers.CharField()


class DateSerializer(serializers.Serializer):
    expression = serializers.CharField()
    begin = serializers.DateField()
    end = serializers.CharField(allow_null=True)
    label = serializers.DateField()
    type = serializers.CharField()


class ExtentSerializer(serializers.Serializer):
    value = serializers.FloatField()
    type = serializers.CharField()


class LanguageSerializer(serializers.Serializer):
    expression = serializers.CharField()
    identifier = serializers.CharField()


class SubnoteSerializer(serializers.Serializer):
    type = serializers.CharField()
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        """Coerce content into a list so it can be serialized as JSON."""
        return list(obj.content)


class NoteSerializer(serializers.Serializer):
    type = serializers.CharField()
    title = serializers.CharField()
    source = serializers.CharField()
    subnotes = SubnoteSerializer(many=True)


class RightsGrantedSerializer(serializers.Serializer):
    act = serializers.CharField()
    begin = serializers.DateField()
    end = serializers.DateField()
    restriction = serializers.CharField()
    notes = NoteSerializer(many=True, allow_null=True)


class RightsStatementSerializer(serializers.Serializer):
    determination_date = serializers.DateField()
    type = serializers.CharField()
    rights_type = serializers.CharField()
    begin = serializers.DateField()
    end = serializers.DateField()
    copyright_status = serializers.CharField(allow_null=True)
    other_basis = serializers.CharField(allow_null=True)
    jurisdiction = serializers.CharField(allow_null=True)
    notes = NoteSerializer(many=True, allow_null=True)
    rights_granted = RightsGrantedSerializer(many=True)


class ReferenceSerializer(serializers.Serializer):
    title = serializers.CharField()
    identifier = serializers.CharField()
    order = serializers.IntegerField(allow_null=True)
    type = serializers.CharField(allow_null=True)


class BaseListSerializer(serializers.Serializer):
    uri = serializers.SerializerMethodField()
    title = serializers.CharField()

    def get_uri(self, obj):
        basename = self.context.get('view').basename or obj.type
        return reverse('{}-detail'.format(basename), kwargs={"pk": obj.meta.id})


class BaseDetailSerializer(serializers.Serializer):
    uri = serializers.CharField()
    title = serializers.CharField()
    type = serializers.CharField()
    external_identifiers = ExternalIdentifierSerializer(many=True)


class AgentSerializer(BaseDetailSerializer):
    description = serializers.CharField(allow_null=True)
    dates = DateSerializer(many=True, allow_null=True)
    notes = NoteSerializer(many=True, allow_null=True)
    collections = ReferenceSerializer(many=True, allow_null=True)
    objects = ReferenceSerializer(many=True, allow_null=True)


class AgentListSerializer(BaseListSerializer):
    pass


class CollectionSerializer(BaseDetailSerializer):
    level = serializers.CharField()
    languages = LanguageSerializer(many=True, allow_null=True)
    extents = ExtentSerializer(many=True)
    dates = DateSerializer(many=True, allow_null=True)
    notes = NoteSerializer(many=True, allow_null=True)
    rights_statements = RightsStatementSerializer(many=True, allow_null=True)
    agents = ReferenceSerializer(many=True, allow_null=True)
    creators = ReferenceSerializer(many=True, allow_null=True)
    terms = ReferenceSerializer(many=True, allow_null=True)
    ancestors = ReferenceSerializer(many=True, allow_null=True)
    children = ReferenceSerializer(many=True, allow_null=True)


class CollectionListSerializer(BaseListSerializer):
    pass


class ObjectSerializer(BaseDetailSerializer):
    languages = LanguageSerializer(many=True, allow_null=True)
    extents = ExtentSerializer(many=True, allow_null=True)
    dates = DateSerializer(many=True, allow_null=True)
    notes = NoteSerializer(many=True, allow_null=True)
    rights_statements = RightsStatementSerializer(many=True, allow_null=True)
    agents = ReferenceSerializer(many=True, allow_null=True)
    terms = ReferenceSerializer(many=True, allow_null=True)
    ancestors = ReferenceSerializer(many=True, allow_null=True)


class ObjectListSerializer(BaseListSerializer):
    pass


class TermSerializer(BaseDetailSerializer):
    collections = ReferenceSerializer(many=True, allow_null=True)
    objects = ReferenceSerializer(many=True, allow_null=True)


class TermListSerializer(BaseListSerializer):
    pass


class HitSerializer(BaseListSerializer):
    type = serializers.CharField()
    dates = DateSerializer(many=True, allow_null=True)
