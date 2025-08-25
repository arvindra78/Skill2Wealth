# Content Upload Workflow - Skill2Wealth Platform

## Overview
Complete workflow for uploading and managing ebooks and courses on your Skill2Wealth platform.

## 🚀 Quick Start

### 1. Create Admin User
```bash
python create_admin.py
```
- Enter your admin email and password
- This creates an admin user with username 'admin'

### 2. Start the Application
```bash
python run.py
```
- App runs on http://localhost:5000
- Admin panel available at http://localhost:5000/admin

### 3. Login as Admin
- Go to http://localhost:5000/auth/login
- Username: `admin`
- Password: (what you set during admin creation)

## 📁 Content Upload Methods

### Method 1: Single Upload
1. Navigate to **Admin Panel** → **Upload Content**
2. Fill in product details:
   - Product Name
   - Category (eBook/Course)
   - Description
   - Price
3. Upload files:
   - **Content File**: PDF for ebooks, Video for courses
   - **Product Image**: Optional cover image
4. Click "Upload Content"

### Method 2: Bulk Upload
1. Navigate to **Admin Panel** → **Bulk Upload**
2. Select category (eBook/Course)
3. Choose multiple files
4. Upload all at once
5. Edit individual products later

## 📋 File Requirements

### eBooks
- **Format**: PDF only
- **Max Size**: 50MB per file
- **Naming**: Use descriptive filenames (becomes product name)

### Courses
- **Formats**: MP4, AVI, MOV, WMV, FLV, WebM
- **Max Size**: 500MB per file
- **Quality**: HD recommended (720p+)

## 🛠️ Admin Panel Features

### Dashboard
- Overview of total products, ebooks, courses, users
- Recent products list
- Quick action buttons

### Product Management
- View all products with filters
- Edit product details
- Delete products
- Toggle active/inactive status
- Download content files

### Upload Features
- Single file upload with full details
- Bulk upload for multiple files
- File validation and size checking
- Auto-generated product names from filenames

## 🔒 Security Features

### Access Control
- Admin-only access to upload functionality
- User authentication required for content access
- Purchase verification for content downloads

### File Security
- Secure file serving with purchase verification
- Protected content directories
- Admin preview without purchase requirement

## 📂 Directory Structure
```
content/
├── ebooks/          # PDF files stored here
└── videos/          # Video files stored here

app/
├── static/
│   └── images/
│       └── products/ # Product images stored here
```

## 🔄 Workflow Steps

### For New Content:
1. **Upload** → Choose single or bulk upload
2. **Configure** → Set price, description, status
3. **Activate** → Make product visible to customers
4. **Test** → Verify purchase and download flow

### For Existing Content:
1. **Manage** → Go to Products page
2. **Edit** → Update details, replace files
3. **Monitor** → Check sales and downloads

## 🛡️ Best Practices

### Content Quality
- Use high-quality, original content
- Include detailed descriptions
- Add attractive cover images
- Test downloads before activation

### File Management
- Use descriptive filenames
- Organize content logically
- Regular backups recommended
- Monitor file sizes

### Security
- Regular admin password updates
- Monitor unauthorized access attempts
- Keep content directories secure

## 🚨 Troubleshooting

### Upload Issues
- Check file size limits
- Verify file formats
- Ensure admin permissions
- Check disk space

### Access Issues
- Verify admin user creation
- Check login credentials
- Confirm blueprint registration

## 📊 Content Analytics
- Track product views in admin dashboard
- Monitor successful uploads
- Review user purchase patterns

## 🔧 Technical Details

### Admin Access
- Username must be 'admin' for admin panel access
- Can be modified in `app/admin/routes.py` `is_admin()` function

### File Serving
- Protected routes require purchase verification
- Admin routes bypass purchase checks
- Secure file serving with Flask send_from_directory

### Database
- Products stored in SQLite database
- File paths stored as URLs in database
- Purchase verification through Orders table

---

**Ready to start uploading content!** 🎉

Run `python create_admin.py` to begin.
