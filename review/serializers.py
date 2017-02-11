from rest_framework import serializers

from .models import Question
from .views import create_all, create_tags


class QuestionSerializer(serializers.ModelSerializer):

    tags = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ('text', 'tags')

    def create(self, validated_data):
        question = Question.objects.create(text=validated_data['text'])
        tags = validated_data.get('tags')
        if tags:
            create_tags(question, tags)
        create_all()
        return question
