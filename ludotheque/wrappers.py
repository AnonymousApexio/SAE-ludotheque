from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'joueur_id' not in request.session:
            return redirect('ludotheque:connexion')
        return view_func(request, *args, **kwargs)
    return wrapper