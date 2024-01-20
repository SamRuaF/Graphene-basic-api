import graphene
from graphene_django import DjangoObjectType
from books.models import Book





class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id","title","description","created_at","updated_at")


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title =  graphene.String()
        description =  graphene.String()

    book = graphene.Field(BookType)

    def mutate(self,into,title,description):
        book = Book(title=title,description=description)
        book.save()
        return CreateBookMutation(book=book)


class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id= graphene.ID(required= True)
        title= graphene.String()
        description= graphene.String()
    book = graphene.Field(BookType)
    def mutate(self,info,id,title,description):
       book =  Book.objects.get(pk=id)
       book.title = title
       book.description = description
       book.save()
       return UpdateBookMutation(book = book)
    

class Query(graphene.ObjectType):
    hello = graphene.String(default_value = "Hola")
    books = graphene.List(BookType)
    book =  graphene.Field(BookType, id = graphene.ID())

    def resolve_books(self,info):
        Book.objects.all()
    def resolve_book(self,info,id):
        return Book.objects.get(pk=id)
    

class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required= True)
    message = graphene.String()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message="Book Deleted")



class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()
    update_book = UpdateBookMutation.Field()

#Para utilizar este query
    
    
schema  = graphene.Schema(query = Query, mutation=Mutation)