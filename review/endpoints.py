from rest_framework.generics import CreateAPIView

from review.serializers import QuestionSerializer
from review.permissions import SlackTokenPermission


class CreateQuestionEndpoint(CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (SlackTokenPermission,)
