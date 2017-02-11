from rest_framework.generics import CreateAPIView

from .serializers import QuestionSerializer


class CreateQuestionEndpoint(CreateAPIView):
    serializer_class = QuestionSerializer
