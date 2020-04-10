from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from project.settings import MEDIA_ROOT

# Directory view
class Directory(TemplateView):
    template_name = 'pages/dir.html'

    # Get requested directory
    def get_directory(self, *args, **kwargs):
        if self.request.GET.get('dir'):
            # Combine requested path with MEDIA_ROOT
            dir = os.path.join(MEDIA_ROOT, self.request.GET.get('dir'))
            # Normalize path (remove '../' and './')
            dir = os.path.normpath(dir)
            # Check if requested path is within MEDIA_ROOT
            if os.path.commonprefix([dir, MEDIA_ROOT]) == MEDIA_ROOT:
                if os.path.exists(dir):
                    return dir
        return None

    # Send directory info and requested path to template
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dir'] = os.scandir(self.get_directory())
        context['path'] = self.request.GET.get('dir')
        return context

    # Render directory only if get_directory() returns anything but None
    def render_to_response(self, context, **kwargs):
        if self.get_directory():
            return super().render_to_response(context, **kwargs)
        # Otherwise redirect to MEDIA_ROOT directory
        else:
            return redirect('/?dir=.')

    # Save uploaded file into current folder
    def post(self, *args, **kwargs):
        dir = self.get_directory()
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
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['X-Sendfile'] = path_to_file
        return response