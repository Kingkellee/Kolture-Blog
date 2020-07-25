from django.views import generic
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def index (request):
    featured_post = Post.objects.filter(status=2).order_by('-created_on')[:4]
    featured = Post.objects.filter(status=2)
    cat_menu_list = Category.objects.all()

    return render (request, 'blog/index.html', {'featured_post': featured_post, 'featured': featured, 'cat_menu_list': cat_menu_list, })


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # featured_post = Post.objects.filter(status=2).order_by('-created_on')[:3]
    template_name = 'blog/home.html'
    paginate_by = 3
    cats = Category.objects.all()
    

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        cat_menu_list = cat_menu
        featured_post = Post.objects.filter(status=2).order_by('-created_on')[:2]
        context = super(PostList, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["featured_post"] = featured_post
        context["cat_menu_list"] = cat_menu_list
        return context


def post_draft_list(request):
    posts = Post.objects.filter(status=0).order_by('created_on')
    cat_menu_list = Category.objects.all()
    return render(request, 'blog/drafts.html', {'posts': posts, 'cat_menu_list': cat_menu_list})


def all_post(request):
    posts = Post.objects.all()
    post_draft = Post.objects.filter(status=0)
    published = Post.objects.filter(status=1)
    is_featured = Post.objects.filter(status=2)
    cat_menu_list = Category.objects.all()
    

    return render(request, 'blog/author_posts.html', {'posts': posts,
                                                    'post_draft': post_draft,
                                                    'published': published,
                                                    'is_featured': is_featured,
                                                    'cat_menu_list': cat_menu_list,
    
    })


def about (request):
    return render (request, 'blog/about.html')


   
def like_post(request, slug):

    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())
   

   
    


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        published = Post.objects.filter(status=1)
        post_draft = Post.objects.filter(status=0)
        featured = Post.objects.filter(status=2)
        cat_menu_list = Category.objects.all()
        query_likes= get_object_or_404(Post, id=self.object.pk)
        total_likes= query_likes.total_likes()
        is_liked = False
        if query_likes.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["published"] = published
        context["post_draft"] = post_draft
        context["is_liked"] = is_liked
        context["featured"] = featured
        context["cat_menu_list"]=cat_menu_list
        return context
      
    
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None   
    template_name = 'blog/add_comment.html'

    if request.method == 'POST':
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            # return HttpResponseRedirect(post.get_absolute_url(), slug)

    else:
        comment_form = CommentForm
        
    
    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })
   
# def post_detail(request, slug):
    # template_name = 'blog/post_detail.html'
    # post = get_object_or_404(Post, slug=slug)
    # comments = post.comments.filter(active=True)
    # new_comment = None
    # is_liked = False
   

    # if post.likes.filter(id=request.user.id).exists():
    #     is_liked = True
    
    
    # # comment posted

    # if request.method == 'POST':
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
            
    #         # Create Comment but Comment not saved to database
    #         new_comment = comment_form.save(commit=False)
    #         #Assign Current Post to the comment
    #         new_comment.post = post
    #         # Now save the comment to the database
    #         new_comment.save()
    # else:
    #      comment_form = CommentForm()

    # return render (request, template_name, {'post': post,
    #                                         'comments': comments,
    #                                         'new_comment': new_comment,
    #                                         'comment_form': comment_form,
    #                                         'is_liked': is_liked,
    #                                         'total_likes': post.total_likes(),
    #                                         })


class AddPostView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    # fields = '__all__'
    def get_context_data(self, *args, **kwargs):
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()
        context["cat_menu_list"]=cat_menu_list
        return context
    

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    template_name= 'blog/category_list.html'
    return render(request, template_name, {'cat_menu_list':cat_menu_list,})


def CategoryView(request, cats):
    category_post = Post.objects.filter(category=cats.replace('-', ' '))
    # object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(category_post, 3)
    page = request.GET.get('page')

    try:
        category_post = paginator.page(page)
    except PageNotAnInteger:
        category_post = paginator.page(1)

    except EmptyPage:
        category_post = paginator.page(paginator.num_pages)



    return render(request, 'blog/categories.html', {'cats': cats.title().replace('-', ' '),'category_post': category_post, 'page': page,})


class AddCategoryView(generic.CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super(AddCategoryView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()
        context["cat_menu_list"]=cat_menu_list
        return context
    



class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    fields = ['title', 'slug', 'category', 'content', 'snippet', 'status']

    def get_context_data(self, *args, **kwargs):
        context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()
        context["cat_menu_list"]=cat_menu_list
        return context
    



class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog-home')

    def get_context_data(self, *args, **kwargs):
        context = super(DeletePostView, self).get_context_data(*args, **kwargs)
        cat_menu_list = Category.objects.all()
        context["cat_menu_list"]=cat_menu_list
        return context
    

    