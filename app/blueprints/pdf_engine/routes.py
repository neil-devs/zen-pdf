# Add these imports to the top of routes.py
from app.blueprints.pdf_engine.workers.splitter import PDFSplitter
from app.blueprints.pdf_engine.workers.compressor import PDFCompressor
from app.blueprints.pdf_engine.workers.converter import ImageToPDF
import os
import uuid
# 1. ADD 'session' HERE
from flask import render_template, request, send_file, current_app, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

from app.blueprints.pdf_engine import pdf_bp
from app.blueprints.pdf_engine.workers.merger import PDFMerger
from app.models.file_meta import FileMeta
from app.models.activity_log import ActivityLog
from app.extensions import db

# 2. IMPORT YOUR DECORATOR HERE
from app.utils.decorators import guest_limit_required

# Helper to check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# --- MERGE ROUTE ---
@pdf_bp.route('/merge', methods=['GET', 'POST'])
@guest_limit_required  # <--- APPLIED DECORATOR
def merge_pdfs():
    if request.method == 'POST':
        # 1. Check if files are present
        if 'files[]' not in request.files:
            flash('No files uploaded', 'danger')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        
        # 2. Save files temporarily
        saved_paths = []
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Ensure upload directory exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                save_path = os.path.join(upload_folder, unique_name)
                file.save(save_path)
                saved_paths.append(save_path)
        
        if len(saved_paths) < 2:
            flash('Please upload at least 2 PDF files to merge.', 'warning')
            return redirect(request.url)

        # 3. Process the Merge
        merger = PDFMerger(upload_folder)
        output_name = f"merged_{uuid.uuid4().hex}.pdf"
        result_filename = merger.process(saved_paths, output_name)

        if result_filename:
            # 4. Record to Database (Enterprise Requirement)
            user_id = current_user.id if current_user.is_authenticated else None
            
            file_meta = FileMeta(
                user_id=user_id,
                original_filename="Merged_Result.pdf",
                stored_filename=result_filename,
                file_size=os.path.getsize(os.path.join(upload_folder, result_filename)),
                status='completed',
                mime_type='application/pdf'
            )
            db.session.add(file_meta)
            
            # Log activity
            log = ActivityLog(user_id=user_id, action='MERGE_PDF', ip_address=request.remote_addr)
            db.session.add(log)
            db.session.commit()

            # --- 3. INCREMENT GUEST COUNTER ---
            if not current_user.is_authenticated:
                session['guest_usage_count'] = session.get('guest_usage_count', 0) + 1
                session.permanent = True
            # ----------------------------------

            # 5. Send file to user
            safe_path = os.path.abspath(os.path.join(upload_folder, result_filename))
            return send_file(safe_path, as_attachment=True)
        else:
            flash('Error processing PDF.', 'danger')

    return render_template('pdf/editor_ui.html', 
                        tool_name="Merge PDF", 
                        file_accept=".pdf")

# --- SPLIT ROUTE ---
@pdf_bp.route('/split', methods=['GET', 'POST'])
@guest_limit_required  # <--- APPLIED DECORATOR
def split_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        start = int(request.form.get('start_page', 1))
        end = int(request.form.get('end_page', 1))
        
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            
            splitter = PDFSplitter(upload_folder)
            output_name = f"split_{uuid.uuid4().hex}.pdf"
            result_name = splitter.process(save_path, start, end, output_name)
            
            if result_name:
                # --- 3. INCREMENT GUEST COUNTER ---
                if not current_user.is_authenticated:
                    session['guest_usage_count'] = session.get('guest_usage_count', 0) + 1
                    session.permanent = True
                # ----------------------------------

                safe_path = os.path.abspath(os.path.join(upload_folder, result_name))
                return send_file(safe_path, as_attachment=True)
                
    return render_template('pdf/split_ui.html', tool_name="Split PDF")

# --- COMPRESS ROUTE ---
@pdf_bp.route('/compress', methods=['GET', 'POST'])
@guest_limit_required  # <--- APPLIED DECORATOR
def compress_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            
            compressor = PDFCompressor(upload_folder)
            output_name = f"compressed_{uuid.uuid4().hex}.pdf"
            result_name = compressor.process(save_path, output_name)
            
            if result_name:
                # --- 3. INCREMENT GUEST COUNTER ---
                if not current_user.is_authenticated:
                    session['guest_usage_count'] = session.get('guest_usage_count', 0) + 1
                    session.permanent = True
                # ----------------------------------

                safe_path = os.path.abspath(os.path.join(upload_folder, result_name))
                return send_file(safe_path, as_attachment=True)

    return render_template('pdf/simple_upload.html', tool_name="Compress PDF")

# --- CONVERT ROUTE ---
@pdf_bp.route('/convert', methods=['GET', 'POST'])
@guest_limit_required  # <--- APPLIED DECORATOR
def convert_pdf():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        upload_folder = current_app.config['UPLOAD_FOLDER']
        saved_paths = []
        
        for file in files:
            filename = secure_filename(file.filename)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            saved_paths.append(save_path)
            
        converter = ImageToPDF(upload_folder)
        output_name = f"converted_{uuid.uuid4().hex}.pdf"
        result_name = converter.process(saved_paths, output_name)
        
        if result_name:
            # --- 3. INCREMENT GUEST COUNTER ---
            if not current_user.is_authenticated:
                session['guest_usage_count'] = session.get('guest_usage_count', 0) + 1
                session.permanent = True
            # ----------------------------------

            safe_path = os.path.abspath(os.path.join(upload_folder, result_name))
            return send_file(safe_path, as_attachment=True)

    return render_template('pdf/editor_ui.html', 
                        tool_name="Images to PDF", 
                        file_accept=".jpg,.jpeg,.png")

@pdf_bp.route('/edit-pdf', methods=['GET', 'POST'])
@guest_limit_required  # <--- APPLIED DECORATOR
def edit_pdf():
    # Phase 1: Just serve the UI. 
    # Later we will handle the "Save" POST request here.
    return render_template('pdf/canvas_ui.html', title="Zen Editor")