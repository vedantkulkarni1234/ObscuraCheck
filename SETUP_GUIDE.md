# Prompt Manager - Setup & Deployment Guide

## Prerequisites

- **Python**: 3.10 or higher
- **pip**: Python package manager
- **Git**: Version control (optional, for cloning)
- **System Memory**: 512 MB minimum
- **Disk Space**: 100 MB for app + data

## Installation Steps

### 1. Clone or Download Repository

```bash
# Via git
git clone <repository_url>
cd prompt-manager

# Or download ZIP and extract
# Then navigate to the folder
cd prompt-manager
```

### 2. Create Virtual Environment (Recommended)

A virtual environment isolates project dependencies from your system Python.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Upgrade pip

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit==1.32.2 - Web app framework
- pydantic==2.5.0 - Data validation
- pandas==2.1.3 - Data manipulation
- pyperclip==1.8.2 - Clipboard support
- And other support libraries

### 5. Run the Application

```bash
streamlit run main.py
```

The app will start and automatically open in your browser at:
```
http://localhost:8501
```

## First Run Experience

### Initial Setup (< 1 minute)

1. **Database Created**: `data/prompts.db` is automatically created
2. **Settings File**: `data/settings.json` is created with defaults
3. **Welcome Screen**: Shows navigation and quick stats

### Creating Your First Prompt

1. Click **"➕ Create"** in sidebar
2. Fill in details:
   - **Title**: "My First Prompt"
   - **Category**: "General" (or create new)
   - **Content**: "Hello {{name}}, welcome to Prompt Manager!"
3. The app auto-detects `{{name}}` as a variable
4. Click **"💾 Save Prompt"**
5. Navigate back to **Home** to see your prompt
6. Click **"▶️ Use"** to fill in variables and test

### Import Sample Prompts

1. Go to **⚙️ Settings** → **📥 Import**
2. Click "Choose JSON file"
3. Select `SAMPLE_DATA.json` from the project folder
4. Click **"✅ Import Prompts"**
5. You'll now have 10 example prompts to explore!

## Directory Structure After Setup

```
prompt-manager/
├── main.py                 # Start here: streamlit run main.py
├── config.py              # Configuration
├── database.py            # Database logic
├── services.py            # Business logic
├── components.py          # UI components
├── styles.py              # Theming
├── utils.py               # Utilities
│
├── pages/
│   ├── 1_🏠_Home.py       # Browse prompts
│   ├── 2_✏️_Create.py     # Create/edit
│   ├── 3_▶️_Use.py        # Use prompts
│   └── 4_⚙️_Settings.py   # Settings
│
├── data/                  # Created on first run
│   ├── prompts.db        # SQLite database
│   └── settings.json     # User settings
│
├── venv/                  # Virtual environment
├── requirements.txt       # Dependencies
├── SAMPLE_DATA.json      # Example prompts
├── .gitignore            # Git ignore rules
├── README.md             # Main documentation
├── SETUP_GUIDE.md        # This file
├── ARCHITECTURE.md       # System design
└── DESIGN_SYSTEM.md      # Visual design
```

## Configuration

### Adjust Display Settings

1. Go to **⚙️ Settings** → **📋 Display Preferences**
2. Options:
   - **Theme Mode**: auto, light, or dark
   - **Items per page**: 5-50 (default 20)
   - **Sort by**: created_at, title, or use_count

### Change Colors (Advanced)

Edit `config.py`:

```python
LIGHT_THEME = {
    "primary": "#2563EB",      # Change blue
    "accent": "#EC4899",        # Change pink
    # ... more colors
}
```

Then restart the app.

### Database Location

By default: `data/prompts.db`

To use a different location, edit `config.py`:

```python
DB_PATH = Path("/custom/path/prompts.db")
```

## Troubleshooting

### App Won't Start

**Error**: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Port Already in Use

**Error**: "Address already in use: ('127.0.0.1', 8501)"

**Solution 1**: Use different port
```bash
streamlit run main.py --server.port 8502
```

**Solution 2**: Kill process using port
```bash
# On macOS/Linux
lsof -ti:8501 | xargs kill -9

# On Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Database Errors

**Error**: "database is locked" or corruption

**Solution**:
```bash
# Delete the database (it will rebuild)
rm data/prompts.db

# Or from Python
import os
os.remove("data/prompts.db")

# Then restart app
streamlit run main.py
```

### Copy to Clipboard Not Working

**Error**: "Could not copy to clipboard"

**Solution**:
- Ensure `pyperclip` is installed: `pip install pyperclip`
- Some browsers/systems may require manual copy
- Text will still be displayed for manual copying

### Settings Not Persisting

**Error**: Theme/preferences reset on restart

**Solution**:
```bash
# Check settings.json exists
ls data/settings.json

# If missing, it will be recreated with defaults
# Delete data/settings.json to reset to defaults
```

## Deployment Options

### Option 1: Local Machine (Recommended for Personal Use)

```bash
# Follow the installation steps above
streamlit run main.py
```

**Pros**: Simplest, fully local, offline
**Cons**: Only accessible on your machine

### Option 2: Streamlit Community Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from GitHub repository
4. App accessible from anywhere

**Setup**:
```bash
git push origin main
# Then deploy from Streamlit Cloud dashboard
```

### Option 3: Docker Containerization

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
```

Build and run:
```bash
docker build -t prompt-manager .
docker run -p 8501:8501 prompt-manager
```

### Option 4: Self-Hosted Server

1. Install Python 3.10+ on server
2. Clone repository
3. Create virtual environment
4. Install dependencies
5. Run with process manager:

```bash
# Using systemd
sudo systemctl start prompt-manager

# Or using supervisor
supervisord -c /etc/supervisor/conf.d/prompt-manager.conf
```

## Performance Tuning

### Large Database (1000+ prompts)

1. **Increase pagination**: Settings → 30-50 items per page
2. **Add indexes**: Already configured for category, favorites, tags
3. **Use search filters**: Narrow down results before browsing

### Memory Usage

- **Default**: ~200 MB
- **With 1000 prompts**: ~400 MB
- **Max reasonable**: ~1 GB (with 10,000+ prompts)

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[client]
showErrorDetails = false
maxUploadSize = 50

[logger]
level = "warning"

[theme]
primaryColor = "#2563EB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F9FAFB"
textColor = "#1F2937"

[server]
maxUploadSize = 50
enableCORS = false
headless = true
```

## Backup & Recovery

### Automated Backup

```bash
# Create daily backup script (backup.sh)
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp data/prompts.db backups/prompts_${TIMESTAMP}.db
cp data/settings.json backups/settings_${TIMESTAMP}.json
```

### Manual Export

1. Settings → Export → Download JSON
2. Saves prompts to `prompts_export_YYYYMMDD_HHMMSS.json`

### Restore from Backup

1. Replace `data/prompts.db` with backup
2. Or use Settings → Import to add prompts

## Security Considerations

### Local Installation (Recommended)

- No authentication needed (single-user)
- No external connections
- Data never leaves your machine
- No cloud sync

### Network Sharing (Advanced)

If sharing via network, add authentication layer:

```bash
# Use basic auth proxy
# OR restrict with firewall
ufw allow from 192.168.1.0/24 to any port 8501
```

### Data Privacy

- No telemetry
- No usage tracking
- No analytics
- Full local control

## Updating

### Check Version

```bash
streamlit --version
pip show streamlit
```

### Update Dependencies

```bash
# Update all packages
pip install -r requirements.txt --upgrade

# Or specific package
pip install streamlit --upgrade
```

### Update App Code

```bash
git pull origin main
# OR
# Download new version and replace files
```

## Getting Help

### Documentation

- `README.md` - Overview and features
- `ARCHITECTURE.md` - System design
- `DESIGN_SYSTEM.md` - Visual design
- `SETUP_GUIDE.md` - This file

### Troubleshooting Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Pydantic Docs](https://docs.pydantic.dev)
- [SQLite Docs](https://www.sqlite.org/docs.html)

### Common Questions

**Q: Is my data secure?**
A: Yes, everything stays locally. Only you have access.

**Q: Can I share prompts with others?**
A: Yes, export as JSON and they can import into their app.

**Q: How much storage do I need?**
A: ~10KB per prompt, so 1000 prompts ≈ 10 MB.

**Q: Can I run multiple instances?**
A: Yes, but they'll use separate databases (use different ports).

**Q: Is there a web version?**
A: You can deploy to Streamlit Cloud (Option 2 above).

---

## Next Steps

1. ✅ **Installation**: Follow steps 1-5 above
2. ✅ **First Run**: Create a sample prompt
3. ✅ **Import Samples**: Load SAMPLE_DATA.json
4. ✅ **Explore Features**: Test each page
5. ✅ **Customize**: Adjust settings to your preference
6. ✅ **Share**: Export and backup your prompts

## Support

For issues or questions:
1. Check README.md for features overview
2. Review ARCHITECTURE.md for design details
3. Consult troubleshooting section above
4. Check Streamlit documentation

**Enjoy using Prompt Manager! 🚀**
