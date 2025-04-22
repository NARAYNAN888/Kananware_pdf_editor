from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import PyPDF2
from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader, PdfWriter
import io
from django.contrib import messages
import fitz
from django.http import FileResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import SupportRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'htt.html', {'error': 'Invalid credentials'})
    return render(request, 'htt.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def superuser_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Only allow superusers
                login(request, user)
                return redirect("admin_dashboard")  # Redirect to admin dashboard or home
            else:
                messages.error(request, "Only superadmins can log in.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "htt.html")  # Your custom login template
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')(view_func)


@superuser_required  # Apply the decorator
def admin_only_page(request):
    return render(request, "admin.html")


# @staff_member_required  # Ensures only admin/staff users can access
# def admin_only_page(request):
#     return render(request, "admin.html")  # Your admin HTML template
# @login_required
def settings(request):
    return render(request, 'settings.html')


def signup_acc(request):
    return render(request, 'signup.html')
# @login_required
# Restrict the view to POST requests only:
def merge_pdf(request):
    if request.method == "POST":
        merger = PdfMerger()
        for file in request.FILES.getlist("pdfs"):
            merger.append(file)

        output_stream = io.BytesIO()
        merger.write(output_stream)
        merger.close()
        output_stream.seek(0)

        response = FileResponse(output_stream, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="merged.pdf"'
        return response
    else:
        return HttpResponseNotAllowed(['POST'])
#
#Handle GET requests appropriately:
@csrf_exempt  # Optional: Disable CSRF for testing (remove in production)
def merge_pdf(request):
    if request.method == "POST":
        merger = PdfMerger()
        for file in request.FILES.getlist("pdfs"):
            merger.append(file)

        output_stream = io.BytesIO()
        merger.write(output_stream)
        merger.close()
        output_stream.seek(0)

        response = FileResponse(output_stream, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="merged.pdf"'
        return response
    elif request.method == "GET":
        # Optionally, render a template with the merge form.
        return render(request, "merge_pdf.html")
# def merge_pdf(request):
#     return render(request, 'merge_pdf.html')


@csrf_exempt
def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf"):
        uploaded_file = request.FILES["pdf"]
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, "wb") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return JsonResponse({"file_url": f"/media/{uploaded_file.name}"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def save_pdf(request):
    if request.method == "POST":
        file_name = request.POST.get("file_name")
        annotations = request.POST.get("annotations")

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        doc = fitz.open(file_path)

        if annotations:
            annotations = eval(annotations)  # Convert JSON string to Python list
            for ann in annotations:
                if ann["type"] == "highlight":
                    page = doc[int(ann["page"])]
                    rect = fitz.Rect(ann["x"], ann["y"], ann["x"] + 100, ann["y"] + 20)
                    page.add_highlight_annot(rect)

        new_file_path = os.path.join(settings.MEDIA_ROOT, "modified_" + file_name)
        doc.save(new_file_path)
        return JsonResponse({"file_url": f"/media/modified_{file_name}"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def convert_pdf_to_word(request):
    return render(request, 'convert_pdf_to_word.html')

# @login_required
def convert_pdf_to_excel(request):
    return render(request, 'convert_excel.html')

def faq(request):
    return render(request, 'faq.html')
def recent_files(request):
    return render(request, 'recentfile.html')
# @login_required
# Render the Split PDF page
def split_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        ranges = request.POST.get('ranges')

        # Process the PDF and split it based on the ranges
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_ranges = parse_page_ranges(ranges)  # You need a function to parse ranges (e.g., "1-3,5,7-10")
            pdf_writer = PyPDF2.PdfWriter()

            # Loop through ranges and add pages to the writer
            for start, end in page_ranges:
                for page_num in range(start, end + 1):
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])

            # Prepare the response with the new PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="split.pdf"'
            pdf_writer.write(response)
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    return render(request, 'split.html')

def parse_ranges(ranges_str):
    result = []
    parts = ranges_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
        else:
            start = end = int(part)
        result.append((start, end))
    return result


def feedback_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")
        changes = request.POST.get("changes")
        screenshot = request.FILES.get("file")

        # Save feedback to the database
        Feedback.objects.create(
            name=name,
            email=email,
            rating=rating,
            comments=comments,
            changes=changes,
            screenshot=screenshot,
        )

        # (Optional) Send an email notification to the admin
        send_mail(
            subject="New Feedback Received",
            message=f"Feedback from {name} ({email}):\n\nRating: {rating}\n\nComments:\n{comments}\n\nSuggested Changes:\n{changes}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@example.com"],  # Change to your admin email
        )

        return JsonResponse({"message": "Thank you for your feedback!"})

    return render(request, "feedback.html")

# @login_required
# def compress_pdf_view(request):
#     return render(request, 'compress.html')


def compress_pdf_view(request):
    """Render the compression page."""
    return render(request, "compress.html")

def convert_word_to_pdf(request):
    """Render the compression page."""
    return render(request, "convert_word_to_pdf.html")


# @app.route('/convert-pdf-to-word', methods=['POST'])
def convert_word_to_pdf_fun(request):
    if request.method == "POST" and request.FILES.get("word_file"):
        word_file = request.FILES["word_file"]

        # Save uploaded file temporarily
        temp_word_path = default_storage.save("temp.docx", word_file)

        # Convert to PDF (Ensure docx2pdf is installed: pip install docx2pdf)
        temp_pdf_path = temp_word_path.replace(".docx", ".pdf")
        convert(temp_word_path, temp_pdf_path)

        # Read converted PDF
        with open(temp_pdf_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=converted.pdf"

        # Cleanup temporary files
        os.remove(temp_word_path)
        os.remove(temp_pdf_path)

        return response

    return HttpResponse("Invalid request", status=400)

def compress_pdf(request):
    """Handle PDF compression and return the compressed file."""
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        compression_level = request.POST.get("level", "medium")

        # Define file paths
        input_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, "compressed_" + pdf_file.name)

        # Save the uploaded file
        try:
            with open(input_pdf_path, "wb") as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Open the PDF for compression
            doc = fitz.open(input_pdf_path)

            # Compression settings
            if compression_level == "low":
                doc.save(output_pdf_path, garbage=4, deflate=True, deflate_images=True)
            elif compression_level == "medium":
                doc.save(output_pdf_path, garbage=4, deflate=True, deflate_images=True, clean=True)
            else:  # High compression
                doc.save(output_pdf_path, garbage=4, deflate=True, deflate_images=True, clean=True, incremental=False)

            doc.close()

            # Return the compressed file as a response
            return FileResponse(open(output_pdf_path, "rb"), as_attachment=True, filename="compressed_" + pdf_file.name)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def submit_support_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        SupportRequest.objects.create(
            name=data["name"],
            email=data["email"],
            mobile=data["mobile"],
            message=data["message"]
        )
        return JsonResponse({"message": "Your request has been submitted successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
def rotate_pdf(request):
    return render(request, 'rotate.html')

# @login_required
def extract_text(request):
    return render(request, 'extract_text.html')

# @login_required
def watermark_removal(request):
    return render(request, 'watermark_pdf.html')

# @login_required
def add_annotations(request):
    return render(request, 'add_annotations.html')

# @login_required
def remove_pages(request):
    return render(request, 'remove_page.html')
# @csrf_exempt  # Remove this if you're using CSRF tokens in JS
def remove_page(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf')
        pages = request.POST.get('pages')

        if not pdf_file or not pages:
            return HttpResponse("Missing file or pages", status=400)

        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            pages_to_remove = [int(p.strip()) - 1 for p in pages.split(',') if p.strip().isdigit()]
            total_pages = len(reader.pages)

            for i in range(total_pages):
                if i not in pages_to_remove:
                    writer.add_page(reader.pages[i])

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)

            return HttpResponse(output.read(), content_type='application/pdf')

        except Exception as e:
            return HttpResponse(f"Error processing PDF: {str(e)}", status=500)
    else:
        return HttpResponse("Invalid request", status=405)

# @login_required
def rearrange_pages(request):
    return render(request, 'rearrange_pages.html')

# @login_required
def sign_pdf(request):
    return render(request, 'sign_pdf.html')

# @login_required

# @login_required
def convert_pdf_to_image(request):
    return render(request, 'convert_pdf_to_image.html')

# @login_required
def ocr(request):
    return render(request, 'ocr.html')



def support(request):
    return render(request, 'support.html')

@login_required
def admin_page(request):
    return render(request, 'admin_page.html')

@login_required
def edit_pdf(request):
    return render(request, 'edit_pdf.html')


# @login_required
def shared_files(request):
    return render(request, 'sharedfiles.html')