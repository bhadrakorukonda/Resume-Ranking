# Resume Ranker Frontend

A modern, responsive web interface for the Resume Ranker backend service.

## Features

- **Multiple PDF Upload**: Upload multiple resume PDFs at once
- **Job Description Input**: Enter detailed job requirements and skills
- **Real-time Processing**: Upload and rank resumes with live feedback
- **Detailed Rankings**: View per-criterion scores and overall rankings
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## Usage

1. **Start the Backend Server**:
   ```bash
   cd backend
   python app.py
   ```
   The server should run on `http://localhost:5000`

2. **Open the Frontend**:
   - Open `frontend/index.html` in your web browser
   - Or serve it with a local web server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

3. **Upload and Rank**:
   - Enter a job description in the text area
   - Select multiple PDF files using the file picker
   - Click "Upload Resumes" to process the files
   - Click "Rank Candidates" to get the ranking results

## Interface Components

### Upload Section
- **Job Description**: Large text area for entering job requirements
- **File Picker**: Drag-and-drop style file selection for PDFs
- **File List**: Shows selected files with size and remove options
- **Upload Button**: Processes all selected files
- **Rank Button**: Generates rankings (enabled after upload)

### Results Section
- **Ranking Table**: Displays candidates in ranked order
- **Per-Criterion Scores**: Shows individual scores for each criterion
- **Overall Score**: TOPSIS-based overall ranking score
- **Candidate Details**: Name and ID for each candidate

## API Integration

The frontend communicates with the Flask backend using these endpoints:

- `POST /upload` - Upload individual resume PDFs
- `POST /rank` - Get ranked candidates
- `GET /health` - Check backend status

## Styling

The interface uses:
- Modern CSS with flexbox and grid layouts
- Responsive design for mobile compatibility
- Smooth animations and hover effects
- Professional color scheme
- Clean typography

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## File Structure

```
frontend/
├── index.html          # Main application file
└── README.md          # This file
```

## Error Handling

The frontend includes comprehensive error handling for:
- Backend connectivity issues
- File upload failures
- Invalid file types
- Network timeouts
- Server errors

Error messages are displayed in a user-friendly format with clear instructions.
