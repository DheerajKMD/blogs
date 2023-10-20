# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType

from post.models import Blog,Comment

class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = ("id","title", "author", "publish_date","description")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "author", "text", "post")


# Creation of  Blog Post
class CreateBlogMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        publish_date = graphene.String(required=False)
        description = graphene.String(required=True)

    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info, title, author, publish_date, description):
        # Create a new Blog instance
        blog = Blog(
            title=title,
            author=author,
            publish_date=publish_date,
            description=description
        )
        blog.save()
        return CreateBlogMutation(blog=blog)




# Updation of Blog Post
class BlogMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title=graphene.String(required=True)
        author=graphene.String(required=True)
        publish_date=graphene.String(required=False)
        # The input arguments for this mutation
        description = graphene.String(required=True)

    # The class attributes define the response of the mutation
    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info,  id,title,author,publish_date,description):
        blog = Blog.objects.get(pk=id)
        blog.title = title
        blog.author = author
        blog.publish_date = publish_date
        blog.description = description
        blog.save()
        # Notice we return an instance of this mutation
        return BlogMutation(blog=blog)


# Delete Comment by ID
class DeleteCommentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # ID of the comment to be deleted
    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return DeleteCommentMutation(success=True)
        except Comment.DoesNotExist:
            return DeleteCommentMutation(success=False)

class Mutation(graphene.ObjectType):
    create_blog = CreateBlogMutation.Field()
    update_blog = BlogMutation.Field()
    delete_comment = DeleteCommentMutation.Field()



# Listing is listed below
class Query(graphene.ObjectType):
    all_blogs = graphene.List(BlogType)
    all_comments = graphene.List(CommentType)
    comments_for_blog = graphene.List(CommentType, blog_id=graphene.ID(required=True))
    def resolve_all_comments(root, info):
        # Return all Blog objects.
        return Comment.objects.all()


    def resolve_all_blogs(root, info):
        # Return all Blog objects.
        return Blog.objects.all()     
    
    def resolve_comments_for_blog(root, info, blog_id):
        return Comment.objects.filter(post=blog_id)
    
    

schema = graphene.Schema(query=Query,mutation=Mutation)
