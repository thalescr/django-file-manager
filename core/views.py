from django.views.generic import TemplateView
from django.views.static import serve
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os
import shutil

from project.settings import MEDIA_ROOT
from .forms import UploadForm, NewFolderForm, DeleleForm

# Directory view
@method_decorator(login_required, name='dispatch')
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

    # Get relative path for requested directory
    def get_relative_path(self, *args, **kwargpath_to_files):
        return os.path.relpath(self.get_real_path(), MEDIA_ROOT)

    # Send directory info and requested path to template
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Upload form, new folder form and delete form
        context['upload_form'] = UploadForm(self.request.POST or None, self.request.FILES or None)
        context['new_folder_form'] = NewFolderForm(self.request.POST or None)
        context['delete_form'] = DeleleForm(self.request.POST or None)
        # List of files from requested directory and it's relative path
        context['dir'] = os.scandir(self.get_real_path())
        context['path'] = self.get_relative_path()
        return context

    # Save uploaded file into current folder
    def post(self, *args, **kwargs):
        # Get requested directory, new folder form, upload form and delete form
        dir = self.get_real_path()
        new_folder_form = self.get_context_data()['new_folder_form']
        upload_form = self.get_context_data()['upload_form']
        delete_form = self.get_context_data()['delete_form']
        # File upload request
        if upload_form.is_valid() and dir:
            uploaded_file = self.request.FILES['document']
            fs = FileSystemStorage(location=dir)
            fs.save(uploaded_file.name, uploaded_file)
        # Folder creation request
        elif new_folder_form.is_valid() and dir:
            folder_name = os.path.join(dir, new_folder_form.cleaned_data['folder_name'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
        # Delete file/folder(s) request
        elif delete_form.is_valid() and dir:
            if delete_form.cleaned_data['delete'] and self.request.GET.get('file'):
                to_delete = os.path.join(dir, self.request.GET.get('file'))
                if os.path.exists(to_delete):
                    if os.path.isfile(to_delete) or os.path.islink(to_delete):
                        os.unlink(to_delete)
                    else:
                        shutil.rmtree(to_delete)

        return self.render_to_response(self.get_context_data())
        
# Download view
@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)