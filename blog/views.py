from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from .models import Post
from .forms import CommentForm
from django.contrib.auth.models import User

# CLASS-BASED VIEW FOR POST LIST
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6

# FUNCTION-BASED VIEW FOR POST DETAIL AND COMMENT HANDLING
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(approved=True).order_by('-created_on')
    comment_count = comments.count()

    if request.method == "POST":
        print("Received a POST request")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    print("About to render template")

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )

# FUNCTION-BASED VIEW FOR EVENTS
def event_detail(request, event_id):
    queryset = Event.objects.all()
    event = get_object_or_404(queryset, event_id=event_id)

    return render(
        request,
        "events/event_detail.html",
        {"event": event}
    )
