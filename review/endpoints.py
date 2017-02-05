from rest_framework.generics import CreateAPIView

from .serializers import QuestionSerializer
from .views import create_tags, create_all


class CreateQuestionEndpoint(CreateAPIView):
    serializer_class = QuestionSerializer

    # def post(self, request, *args, **kwargs):
    #   return self.create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     import pdb; pdb.set_trace()
    #     question = serializer.save()
    #     # tags = form['tags'].value()
    #     # if tags:
    #     #     create_tags(question, tags)
    #     # create_all()



