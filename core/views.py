from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.http import FileResponse
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import os
from project.settings import MEDIA_ROOT

# Directory view
class Directory(TemplateView):
    template_name = 'pages/dir.html'

    # Get requested directory
    def get_real_path(self, *args, **kwargs):
        if self.request.GET.get('dir'):
            # Combine requested path with MEDIA_ROOT
            dir = os.path.join(MEDIA_ROOT, self.request.GET.get('dir'))
            # Normalize path (remove '../' and './')
            dir = os.path.normpath(dir)
            # Check if requested path is inside MEDIA_ROOT
            if os.path.commonprefix([dir, MEDIA_ROOT]) == MEDIA_ROOT:
                if os.path.exists(dir):
                    return dir
        return MEDIA_ROOT

    def get_relative_path(self, *args, **kwargs):
        return os.path.relpath(self.get_real_path(), MEDIA_ROOT)

    # Send directory info and requested path to template
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dir'] = os.scandir(self.get_real_path())
        context['path'] = self.get_relative_path()
        return context
    '''
    # Render directory only if get_real_path() returns anything but None
    def render_to_response(self, context, **kwargs):
        if self.get_real_path() is not MEDIA_ROOT:
            return super().render_to_response(context, **kwargs)
        # Otherwise redirect to MEDIA_ROOT directory
        else:
            return redirect('home')
    '''
    # Save uploaded file into current folder
    def post(self, *args, **kwargs):
        dir = self.get_real_path()
        uploaded_file = self.request.FILES['document']
        if dir:
            fs = FileSystemStorage(location=dir)
            fs.save(uploaded_file.name, uploaded_file)
        return self.render_to_response(self.get_context_data())
        


# Download view
class Download(View):
    def get(self, *args, **kwargs):
        path_to_file = self.request.GET.get('path')
        file_name = os.path.basename(path_to_file)
        wrapper = FileWrapper(open(path_to_file))
        response = HttpResponse(wrapper, content_type='multipart/form-data')
        response['Content-Length'] = os.path.getsize(path_to_file)
        return response

class NewFolder(View):
    def get(self, *args, **kwargs):
        path_to_file = self.request.GET.get('path')
        pass