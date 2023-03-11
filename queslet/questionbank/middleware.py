from django.contrib.auth.decorators import login_required

from django.shortcuts import render,redirect


# def login_check(request):
#     return request.user.is_authenticated

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):


        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        response = self.get_response(request)
        if path == '/users/login_user':
            return response

        if not request.user.is_authenticated :
            return redirect('/users/login_user')
        else: 
            if request.user.username == "admin":
                if "admin" in path:
                    return response
                return redirect('/admin/')

            return response
        
class ManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):

        # Code to be executed for each request before
            # the view (and later middleware) are called.
        
        manager_paths = ["register_user","manage"]
        User = request.user
        path = request.path
        response = self.get_response(request)

        if any( item in path for item in manager_paths ):
            if isManger(User) :
                return response
            return redirect('forbiden')
        else: 
            return response

class ImportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        import_paths = ["import"]
        User = request.user
        path = request.path
        response = self.get_response(request)
        print("Go in import")
        if any( item in path for item in import_paths):
            
            try:
                forward = request.session['forward'] 
            except:
                forward = False

            if forward:
                return response
            else:
                request.session['forward'] = True
                return redirect('import_view')
        else: 
            return response


  

   
def isManger(User):
    return User.groups.filter(name='manager').exists() 