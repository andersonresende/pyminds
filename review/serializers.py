from rest_framework import serializers

from .models import Question
from .views import create_all, create_tags


def _normalize_and_split_data(text):
    # Remove first and last itens and split the string into a list.
    text = text.strip()
    last_open_sqbra = text.rfind('[')
    message = text
    categories_str = ''
    if text.endswith(']') and last_open_sqbra != -1:
        categories_str = text[last_open_sqbra + 1:-1]
        message = text[:last_open_sqbra]
    return message.strip(), categories_str


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
