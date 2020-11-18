from django import forms
from .models import Post,BlogComment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','tag','author','body')

        widgets ={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'tag':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control','placeholder':'username','id':'authore','type':'hidden'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','tag','body')

        widgets ={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'tag':forms.TextInput(attrs={'class':'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=BlogComment
        fields=('comment',)

        widgets ={
            'comment':forms.Textarea(attrs={'class':'form-control','rows':"2",'cols':"40",'placeholder':"Enter a Comment"}),
        }