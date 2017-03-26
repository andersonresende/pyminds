from rest_framework import serializers

from review.helpers import _normalize_and_split_data, create_all, create_tags
from review.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    tags = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ('text', 'tags')

    def create(self, validated_data):
        text, tags = _normalize_and_split_data(validated_data['text'])
        question = Question.objects.create(text=text)
        if tags:
            create_tags(question, tags)
        create_all()
        return question
