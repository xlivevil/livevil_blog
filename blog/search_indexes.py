from django.utils import timezone
from haystack import indexes
from .models import Post


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    modified_time = indexes.DateTimeField(model_attr='modified_time')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(modified_time__lte=timezone.now())
