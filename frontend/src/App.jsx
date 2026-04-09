import React, { useState, useEffect } from 'react';
import './styles/tailwind.css';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [files, setFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [candidateName, setCandidateName] = useState('');
  const [candidateEmail, setCandidateEmail] = useState('');
  const [candidatePhone, setCandidatePhone] = useState('');
  const [uploading, setUploading] = useState(false);
  const [candidates, setCandidates] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [weights, setWeights] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load data on component mount
  useEffect(() => {
    loadCandidates();
    loadWeights();
  }, []);

  const loadCandidates = async () => {
    try {
      const response = await fetch('http://localhost:5000/candidates');
      const data = await response.json();
      setCandidates(data.candidates || []);
    } catch (error) {
      console.error('Error loading candidates:', error);
    }
  };

  const loadWeights = async () => {
    try {
      const response = await fetch('http://localhost:5000/weights');
      const data = await response.json();
      setWeights(data.weights || []);
    } catch (error) {
      console.error('Error loading weights:', error);
    }
  };

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleNameChange = (e) => {
    setCandidateName(e.target.value);
  };

  const handleEmailChange = (e) => {
    setCandidateEmail(e.target.value);
  };

  const handlePhoneChange = (e) => {
    setCandidatePhone(e.target.value);
  };

  const handleFileUpload = async () => {
    if (files.length === 0) {
      alert("Please select files to upload.");
      return;
    }

    setUploading(true);

    try {
      // Upload each file individually
      for (const file of files) {
        const formData = new FormData();
        formData.append("resume", file);
        formData.append("name", candidateName || 'Unknown');
        formData.append("email", candidateEmail || '');
        formData.append("phone", candidatePhone || '');
        formData.append("job_description", jobDescription);

        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Failed to upload ${file.name}`);
        }

        const data = await response.json();
        console.log(`File ${file.name} uploaded successfully:`, data);
      }

      alert("All files uploaded successfully!");
      // Clear form and reload candidates
      setFiles([]);
      setJobDescription('');
      setCandidateName('');
      setCandidateEmail('');
      setCandidatePhone('');
      loadCandidates();

    } catch (error) {
      console.error("Error uploading files:", error);
      alert(`An error occurred while uploading the files: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleRankCandidates = async () => {
    console.log('Starting ranking process...');
    setLoading(true);
    try {
      const requestData = {
        weights: {
          skill_match: 0.25,
          jd_alignment: 0.30,
          exp_years: 0.20,
          projects: 0.15,
          education: 0.10
        }
      };
      console.log('Sending request:', requestData);

      const response = await fetch('http://localhost:5000/rank', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);

      if (response.ok) {
        setRankings(data.ranked_candidates || []);
        console.log('Rankings set:', data.ranked_candidates);
        setActiveTab('rankings');
        alert(`Successfully ranked ${data.total_candidates} candidates!`);
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      console.error('Error ranking candidates:', error);
      alert(`Error ranking candidates: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteAllCandidates = async () => {
    if (!confirm('Are you sure you want to delete ALL candidates? This action cannot be undone!')) return;

    try {
      const response = await fetch('http://localhost:5000/candidates', {
        method: 'DELETE',
      });

      if (response.ok) {
        const data = await response.json();
        loadCandidates();
        setRankings([]); // Clear rankings as well
        alert(data.message);
      } else {
        alert('Error deleting all candidates');
      }
    } catch (error) {
      console.error('Error deleting all candidates:', error);
      alert('Error deleting all candidates');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-center relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slower"></div>
        <div className="absolute top-40 left-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slowest"></div>
        <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-yellow-400 rounded-full mix-blend-multiply filter blur-lg opacity-10 animate-float"></div>
        <div className="absolute bottom-1/4 left-1/4 w-24 h-24 bg-cyan-400 rounded-full mix-blend-multiply filter blur-lg opacity-15 animate-scale-gentle"></div>
      </div>

      <div className="container mx-auto px-6 py-8 max-w-7xl relative z-10">
        <div className="text-center mb-12">
          <div className="inline-block p-1 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 rounded-2xl mb-6 shadow-2xl animate-glow">
            <div className="bg-slate-900 rounded-xl px-6 py-3">
              <h1 className="text-6xl font-black bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-2 tracking-tight animate-pulse-slow">
                Resume Ranking System
              </h1>
            </div>
          </div>
          <p className="text-slate-300 text-xl font-light tracking-wide animate-fade-in">AI-powered candidate evaluation and ranking</p>
          <div className="mt-4 flex justify-center space-x-2">
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-pink-400 rounded-full animate-pulse animation-delay-1000"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse animation-delay-2000"></div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-12">
          <div className="backdrop-blur-lg bg-white/10 rounded-2xl p-2 shadow-2xl border border-white/20">
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-8 py-4 rounded-xl font-bold transition-all duration-300 transform ${
                activeTab === 'upload'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl scale-105 backdrop-blur-sm'
                  : 'text-slate-300 hover:text-white hover:bg-white/10 hover:scale-105'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-xl">📤</span>
                <span>Upload Resume</span>
              </span>
            </button>
            <button
              onClick={() => setActiveTab('candidates')}
              className={`px-8 py-4 rounded-xl font-bold transition-all duration-300 transform ${
                activeTab === 'candidates'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl scale-105 backdrop-blur-sm'
                  : 'text-slate-300 hover:text-white hover:bg-white/10 hover:scale-105'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-xl">👥</span>
                <span>Candidates ({candidates.length})</span>
              </span>
            </button>
            <button
              onClick={() => setActiveTab('rankings')}
              className={`px-8 py-4 rounded-xl font-bold transition-all duration-300 transform ${
                activeTab === 'rankings'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl scale-105 backdrop-blur-sm'
                  : 'text-slate-300 hover:text-white hover:bg-white/10 hover:scale-105'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-xl">🏆</span>
                <span>Rankings</span>
              </span>
            </button>
            <button
              onClick={() => setActiveTab('weights')}
              className={`px-8 py-4 rounded-xl font-bold transition-all duration-300 transform ${
                activeTab === 'weights'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-2xl scale-105 backdrop-blur-sm'
                  : 'text-slate-300 hover:text-white hover:bg-white/10 hover:scale-105'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-xl">⚖️</span>
                <span>Weights</span>
              </span>
            </button>
          </div>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="flex justify-center">
            <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-2xl w-full max-w-3xl border border-white/20">
              <div className="text-center mb-10">
                <div className="inline-block p-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl mb-6 shadow-2xl">
                  <div className="text-7xl mb-2">📄</div>
                </div>
                <h2 className="text-4xl font-bold text-white mb-3 tracking-tight">Upload Resume</h2>
                <p className="text-slate-300 text-lg">Upload PDF resumes for automatic analysis and ranking</p>
              </div>

              <div className="space-y-8">
                <div className="text-center">
                  <label className="block text-lg font-semibold text-white mb-4">Select Resume Files</label>
                  <input
                    type="file"
                    multiple
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="block w-full p-6 text-white border-2 border-dashed border-white/30 rounded-2xl hover:border-purple-400 transition-all duration-300 cursor-pointer mx-auto bg-white/5 backdrop-blur-sm hover:bg-white/10"
                  />
                  {files.length > 0 && (
                    <div className="mt-6 p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-2xl mx-auto max-w-lg border border-white/20 backdrop-blur-sm">
                      <p className="text-white font-semibold text-center flex items-center justify-center space-x-2">
                        <span className="text-2xl">📎</span>
                        <span>{files.length} file(s) selected: {files.map(f => f.name).join(', ')}</span>
                      </p>
                    </div>
                  )}
                </div>

                <div className="text-center">
                  <h3 className="text-2xl font-bold text-white mb-6">Candidate Information (Optional)</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-lg mx-auto">
                    <input
                      type="text"
                      value={candidateName}
                      onChange={handleNameChange}
                      placeholder="Candidate Name"
                      className="block w-full p-4 text-white placeholder-slate-300 border-2 border-white/20 rounded-xl focus:border-purple-400 focus:ring-2 focus:ring-purple-400/50 transition-all bg-white/5 backdrop-blur-sm"
                    />
                    <input
                      type="email"
                      value={candidateEmail}
                      onChange={handleEmailChange}
                      placeholder="Email Address"
                      className="block w-full p-4 text-white placeholder-slate-300 border-2 border-white/20 rounded-xl focus:border-purple-400 focus:ring-2 focus:ring-purple-400/50 transition-all bg-white/5 backdrop-blur-sm"
                    />
                  </div>
                  <input
                    type="tel"
                    value={candidatePhone}
                    onChange={handlePhoneChange}
                    placeholder="Phone Number"
                    className="block w-full p-4 mt-6 text-white placeholder-slate-300 border-2 border-white/20 rounded-xl focus:border-purple-400 focus:ring-2 focus:ring-purple-400/50 transition-all bg-white/5 backdrop-blur-sm max-w-lg mx-auto"
                  />
                </div>

                <div className="text-center">
                  <label className="block text-lg font-semibold text-white mb-4">Job Description</label>
                  <textarea
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    placeholder="Enter job description for better candidate matching..."
                    className="w-full p-4 text-white placeholder-slate-300 border-2 border-white/20 rounded-xl focus:border-purple-400 focus:ring-2 focus:ring-purple-400/50 transition-all bg-white/5 backdrop-blur-sm max-w-lg mx-auto"
                    rows="4"
                  />
                </div>

                <div className="text-center pt-6">
                  <button
                    onClick={handleFileUpload}
                    disabled={uploading}
                    className={`px-12 py-5 text-xl font-bold rounded-2xl shadow-2xl transition-all duration-300 transform ${
                      uploading
                        ? 'bg-gray-600 cursor-not-allowed text-gray-300'
                        : 'bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:from-purple-700 hover:via-pink-700 hover:to-blue-700 text-white hover:shadow-purple-500/25 hover:scale-105'
                    }`}
                  >
                    {uploading ? (
                      <span className="flex items-center space-x-3">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                        <span>🚀 Uploading...</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-3">
                        <span>📤</span>
                        <span>Upload Resumes</span>
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Candidates Tab */}
        {activeTab === 'candidates' && (
          <div className="flex justify-center">
            <div className="backdrop-blur-xl bg-white/10 p-8 rounded-3xl shadow-2xl w-full max-w-7xl border border-white/20 text-center">
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-4xl font-bold text-white flex-1">Candidates ({candidates.length})</h2>
                <div className="flex gap-4">
                  <button
                    onClick={deleteAllCandidates}
                    disabled={candidates.length === 0}
                    className={`px-6 py-3 rounded-xl font-bold transition-all duration-300 transform ${
                      candidates.length === 0
                        ? 'bg-gray-600/50 cursor-not-allowed text-gray-400 border border-gray-500/50'
                        : 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-xl hover:shadow-red-500/25 hover:scale-105 border border-red-500/50'
                    }`}
                  >
                    <span className="flex items-center space-x-2">
                      <span>🗑️</span>
                      <span>Delete All</span>
                    </span>
                  </button>
                  <button
                    onClick={handleRankCandidates}
                    disabled={loading || candidates.length === 0}
                    className={`px-8 py-3 rounded-xl font-bold transition-all duration-300 transform ${
                      loading || candidates.length === 0
                        ? 'bg-gray-600/50 cursor-not-allowed text-gray-400 border border-gray-500/50'
                        : 'bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:from-purple-700 hover:via-pink-700 hover:to-blue-700 text-white shadow-xl hover:shadow-purple-500/25 hover:scale-105 border border-purple-500/50'
                    }`}
                  >
                    {loading ? (
                      <span className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        <span>Ranking...</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-2">
                        <span>🏆</span>
                        <span>Rank Candidates</span>
                      </span>
                    )}
                  </button>
                </div>
              </div>

              {candidates.length === 0 ? (
                <div className="text-center py-16">
                  <div className="inline-block p-6 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl mb-8 border border-white/20">
                    <div className="text-8xl mb-4">📄</div>
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-4">No candidates uploaded yet</h3>
                  <p className="text-slate-300 text-lg mb-8">Upload some resumes to get started!</p>
                  <button
                    onClick={() => setActiveTab('upload')}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 rounded-xl font-bold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-purple-500/25"
                  >
                    <span className="flex items-center space-x-2">
                      <span>📤</span>
                      <span>Upload Resumes</span>
                    </span>
                  </button>
                </div>
              ) : (
                <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                  {candidates.map((candidate) => (
                    <div key={candidate.id} className="backdrop-blur-lg bg-white/10 p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:shadow-purple-500/10 transition-all duration-300 transform hover:scale-105 text-center group">
                      <div className="flex items-start justify-between mb-6">
                        <div className="flex-1 text-center">
                          <h3 className="font-bold text-2xl text-white mb-2 group-hover:text-purple-300 transition-colors">{candidate.name}</h3>
                          <p className="text-slate-300 text-sm mb-1">{candidate.email}</p>
                          <p className="text-slate-300 text-sm">{candidate.phone}</p>
                        </div>
                        <button
                          onClick={() => deleteCandidate(candidate.id)}
                          className="text-red-400 hover:text-red-300 p-2 rounded-full hover:bg-red-500/20 transition-all duration-300 transform hover:scale-110"
                          title="Delete candidate"
                        >
                          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>

                      <div className="grid grid-cols-2 gap-4 text-sm text-center">
                        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 p-4 rounded-2xl border border-blue-400/30 backdrop-blur-sm">
                          <div className="text-blue-300 font-semibold text-sm mb-1">Skill Match</div>
                          <div className="text-2xl font-bold text-blue-200">{(candidate.skill_match * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 p-4 rounded-2xl border border-green-400/30 backdrop-blur-sm">
                          <div className="text-green-300 font-semibold text-sm mb-1">JD Alignment</div>
                          <div className="text-2xl font-bold text-green-200">{(candidate.jd_alignment * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 p-4 rounded-2xl border border-purple-400/30 backdrop-blur-sm">
                          <div className="text-purple-300 font-semibold text-sm mb-1">Experience</div>
                          <div className="text-2xl font-bold text-purple-200">{(candidate.exp_years * 20).toFixed(1)} yrs</div>
                        </div>
                        <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 p-4 rounded-2xl border border-orange-400/30 backdrop-blur-sm">
                          <div className="text-orange-300 font-semibold text-sm mb-1">Projects</div>
                          <div className="text-2xl font-bold text-orange-200">{(candidate.projects * 10).toFixed(0)}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Rankings Tab */}
        {activeTab === 'rankings' && (
          <div className="flex justify-center">
            <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-2xl w-full max-w-6xl border border-white/20">
              <div className="text-center mb-10">
                <div className="inline-block p-4 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl mb-6 shadow-2xl">
                  <div className="text-7xl mb-2">🏆</div>
                </div>
                <h2 className="text-4xl font-bold text-white mb-3 tracking-tight">Candidate Rankings</h2>
                <p className="text-slate-300 text-lg">TOPSIS algorithm results based on multi-criteria evaluation</p>
              </div>

              <div className="flex justify-center mb-8">
                <button
                  onClick={handleRankCandidates}
                  disabled={loading}
                  className={`px-10 py-4 rounded-2xl font-bold transition-all duration-300 transform ${
                    loading
                      ? 'bg-gray-600/50 cursor-not-allowed text-gray-400 border border-gray-500/50'
                      : 'bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 hover:from-yellow-600 hover:via-orange-600 hover:to-red-600 text-white shadow-xl hover:shadow-yellow-500/25 hover:scale-105 border border-yellow-500/50'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center space-x-3">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                      <span>🔄 Refreshing...</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-3">
                      <span>🔄</span>
                      <span>Refresh Rankings</span>
                    </span>
                  )}
                </button>
              </div>

              {rankings.length === 0 ? (
                <div className="text-center py-16">
                  <div className="inline-block p-6 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-3xl mb-8 border border-white/20">
                    <div className="text-8xl mb-4">📊</div>
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-4">No rankings available yet</h3>
                  <p className="text-slate-300 text-lg mb-8">Upload candidates and rank them to see results!</p>
                  <div className="flex justify-center gap-6">
                    <button
                      onClick={() => setActiveTab('upload')}
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 rounded-xl font-bold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-purple-500/25"
                    >
                      <span className="flex items-center space-x-2">
                        <span>📤</span>
                        <span>Upload Resumes</span>
                      </span>
                    </button>
                    <button
                      onClick={handleRankCandidates}
                      disabled={loading}
                      className={`px-8 py-4 rounded-xl font-bold transition-all duration-300 transform ${
                        loading
                          ? 'bg-gray-600/50 cursor-not-allowed text-gray-400 border border-gray-500/50'
                          : 'bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white shadow-xl hover:shadow-green-500/25 hover:scale-105 border border-green-500/50'
                      }`}
                    >
                      {loading ? (
                        <span className="flex items-center space-x-2">
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                          <span>Ranking...</span>
                        </span>
                      ) : (
                        <span className="flex items-center space-x-2">
                          <span>🏆</span>
                          <span>Rank Now</span>
                        </span>
                      )}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-8">
                  {rankings.map((candidate, index) => (
                    <div key={candidate.id || index} className={`p-8 rounded-3xl border-l-8 shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-102 backdrop-blur-lg ${
                      index === 0 ? 'border-yellow-400 bg-gradient-to-r from-yellow-500/10 to-orange-500/10' :
                      index === 1 ? 'border-gray-400 bg-gradient-to-r from-gray-500/10 to-slate-500/10' :
                      index === 2 ? 'border-orange-400 bg-gradient-to-r from-orange-500/10 to-red-500/10' :
                      'border-blue-400 bg-gradient-to-r from-blue-500/10 to-indigo-500/10'
                    } border border-white/20`}>
                      <div className="flex justify-between items-start">
                        <div className="flex-1 text-center">
                          <div className="flex items-center justify-center gap-6 mb-6">
                            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-3xl font-bold shadow-xl ${
                              index === 0 ? 'bg-gradient-to-r from-yellow-400 to-orange-400 text-white' :
                              index === 1 ? 'bg-gradient-to-r from-gray-400 to-slate-400 text-white' :
                              index === 2 ? 'bg-gradient-to-r from-orange-400 to-red-400 text-white' :
                              'bg-gradient-to-r from-blue-400 to-indigo-400 text-white'
                            }`}>
                              #{candidate.rank}
                            </div>
                            <div className="text-center">
                              <h3 className="text-3xl font-bold text-white mb-2">{candidate.name || 'Unknown'}</h3>
                              <p className="text-slate-300 text-lg">{candidate.email || 'No email'}</p>
                            </div>
                          </div>

                          <div className="text-center mb-6">
                            <div className="inline-block p-4 bg-gradient-to-r from-purple-600/20 to-pink-600/20 rounded-2xl border border-white/20 backdrop-blur-sm">
                              <div className="text-5xl font-bold text-white mb-1">
                                {((candidate.topsis_score || 0) * 100).toFixed(2)}%
                              </div>
                              <div className="text-sm text-slate-300">TOPSIS Score</div>
                            </div>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6 text-sm text-center">
                          <div className="bg-white/10 p-6 rounded-2xl border border-white/20 backdrop-blur-sm">
                            <div className="text-blue-300 font-semibold text-sm mb-2">Skill Match</div>
                            <div className="text-3xl font-bold text-blue-200">{((candidate.skill_match || 0) * 100).toFixed(1)}%</div>
                          </div>
                          <div className="bg-white/10 p-6 rounded-2xl border border-white/20 backdrop-blur-sm">
                            <div className="text-green-300 font-semibold text-sm mb-2">JD Alignment</div>
                            <div className="text-3xl font-bold text-green-200">{((candidate.jd_alignment || 0) * 100).toFixed(1)}%</div>
                          </div>
                          <div className="bg-white/10 p-6 rounded-2xl border border-white/20 backdrop-blur-sm">
                            <div className="text-purple-300 font-semibold text-sm mb-2">Experience</div>
                            <div className="text-3xl font-bold text-purple-200">{((candidate.exp_years || 0) * 20).toFixed(1)} yrs</div>
                          </div>
                          <div className="bg-white/10 p-6 rounded-2xl border border-white/20 backdrop-blur-sm">
                            <div className="text-orange-300 font-semibold text-sm mb-2">Projects</div>
                            <div className="text-3xl font-bold text-orange-200">{((candidate.projects || 0) * 10).toFixed(0)}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Weights Tab */}
        {activeTab === 'weights' && (
          <div className="flex justify-center">
            <div className="backdrop-blur-xl bg-white/10 p-10 rounded-3xl shadow-2xl w-full max-w-5xl border border-white/20">
              <div className="text-center mb-10">
                <div className="inline-block p-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl mb-6 shadow-2xl">
                  <div className="text-7xl mb-2">⚖️</div>
                </div>
                <h2 className="text-4xl font-bold text-white mb-3 tracking-tight">Weight Configurations</h2>
                <p className="text-slate-300 text-lg">Customize evaluation criteria weights for ranking</p>
              </div>

              {weights.length === 0 ? (
                <div className="text-center py-16">
                  <div className="inline-block p-6 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-3xl mb-8 border border-white/20">
                    <div className="text-8xl mb-4">📊</div>
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-4">No custom weights configured yet</h3>
                  <p className="text-slate-300 text-lg">Create custom weight configurations to fine-tune candidate evaluation.</p>
                </div>
              ) : (
                <div className="grid gap-8 md:grid-cols-2">
                  {weights.map((weight) => (
                    <div key={weight.id} className="backdrop-blur-lg bg-white/10 p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300 transform hover:scale-105 text-center group">
                      <h3 className="font-bold text-3xl text-white mb-6 group-hover:text-blue-300 transition-colors">{weight.name}</h3>
                      <div className="grid grid-cols-2 gap-6">
                        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 p-6 rounded-2xl border border-blue-400/30 backdrop-blur-sm">
                          <div className="text-blue-300 font-semibold text-sm mb-2">Skill Match</div>
                          <div className="text-3xl font-bold text-blue-200">{(weight.skill_match * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 p-6 rounded-2xl border border-green-400/30 backdrop-blur-sm">
                          <div className="text-green-300 font-semibold text-sm mb-2">JD Alignment</div>
                          <div className="text-3xl font-bold text-green-200">{(weight.jd_alignment * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 p-6 rounded-2xl border border-purple-400/30 backdrop-blur-sm">
                          <div className="text-purple-300 font-semibold text-sm mb-2">Experience</div>
                          <div className="text-3xl font-bold text-purple-200">{(weight.exp_years * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 p-6 rounded-2xl border border-orange-400/30 backdrop-blur-sm">
                          <div className="text-orange-300 font-semibold text-sm mb-2">Projects</div>
                          <div className="text-3xl font-bold text-orange-200">{(weight.projects * 100).toFixed(1)}%</div>
                        </div>
                      </div>
                      <div className="mt-8 pt-6 border-t border-white/20">
                        <div className="text-center">
                          <div className="text-slate-300 text-sm mb-2">Education Weight</div>
                          <div className="text-2xl font-bold text-white">{(weight.education * 100).toFixed(1)}%</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
