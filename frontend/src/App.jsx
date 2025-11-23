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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 text-center">
      <div className="container mx-auto px-6 py-8 max-w-7xl">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            Resume Ranking System
          </h1>
          <p className="text-gray-600 text-lg">AI-powered candidate evaluation and ranking</p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-xl p-2 shadow-xl border border-gray-200">
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
                activeTab === 'upload'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              📤 Upload Resume
            </button>
            <button
              onClick={() => setActiveTab('candidates')}
              className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
                activeTab === 'candidates'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              👥 Candidates ({candidates.length})
            </button>
            <button
              onClick={() => setActiveTab('rankings')}
              className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
                activeTab === 'rankings'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              🏆 Rankings
            </button>
            <button
              onClick={() => setActiveTab('weights')}
              className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
                activeTab === 'weights'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              ⚖️ Weights
            </button>
          </div>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="flex justify-center">
            <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-2xl border border-gray-100">
              <div className="text-center mb-8">
                <div className="text-6xl mb-4">📄</div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Upload Resume</h2>
                <p className="text-gray-600">Upload PDF resumes for automatic analysis and ranking</p>
              </div>

              <div className="space-y-6">
                <div className="text-center">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Select Resume Files</label>
                  <input
                    type="file"
                    multiple
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="block w-full p-4 text-gray-700 border-2 border-dashed border-gray-300 rounded-xl hover:border-blue-400 transition-colors cursor-pointer mx-auto"
                  />
                  {files.length > 0 && (
                    <div className="mt-3 p-3 bg-blue-50 rounded-lg mx-auto max-w-md">
                      <p className="text-sm text-blue-700 font-medium text-center">
                        📎 {files.length} file(s) selected: {files.map(f => f.name).join(', ')}
                      </p>
                    </div>
                  )}
                </div>

                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Candidate Information (Optional)</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-md mx-auto">
                    <input
                      type="text"
                      value={candidateName}
                      onChange={handleNameChange}
                      placeholder="Candidate Name"
                      className="block w-full p-3 text-gray-700 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                    />
                    <input
                      type="email"
                      value={candidateEmail}
                      onChange={handleEmailChange}
                      placeholder="Email Address"
                      className="block w-full p-3 text-gray-700 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                    />
                  </div>
                  <input
                    type="tel"
                    value={candidatePhone}
                    onChange={handlePhoneChange}
                    placeholder="Phone Number"
                    className="block w-full p-3 mt-4 text-gray-700 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all max-w-md mx-auto"
                  />
                </div>

                <div className="text-center">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Job Description</label>
                  <textarea
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    placeholder="Enter job description for better candidate matching..."
                    className="w-full p-4 text-gray-700 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all max-w-md mx-auto"
                    rows="4"
                  />
                </div>

                <div className="text-center pt-4">
                  <button
                    onClick={handleFileUpload}
                    disabled={uploading}
                    className={`px-10 py-4 text-lg font-semibold rounded-xl shadow-lg transition-all duration-200 transform ${
                      uploading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white hover:shadow-xl hover:scale-105'
                    }`}
                  >
                    {uploading ? '🚀 Uploading...' : '📤 Upload Resumes'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Candidates Tab */}
        {activeTab === 'candidates' && (
          <div className="flex justify-center">
            <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-6xl text-center">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800 text-center flex-1">Candidates ({candidates.length})</h2>
                <div className="flex gap-3">
                  <button
                    onClick={deleteAllCandidates}
                    disabled={candidates.length === 0}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      candidates.length === 0
                        ? 'bg-gray-300 cursor-not-allowed text-gray-500'
                        : 'bg-red-600 hover:bg-red-700 text-white'
                    }`}
                  >
                    Delete All
                  </button>
                  <button
                    onClick={handleRankCandidates}
                    disabled={loading || candidates.length === 0}
                    className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                      loading || candidates.length === 0
                        ? 'bg-gray-400 cursor-not-allowed text-white'
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                    }`}
                  >
                    {loading ? 'Ranking...' : 'Rank Candidates'}
                  </button>
                </div>
              </div>

              {candidates.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📄</div>
                  <p className="text-gray-500 text-lg">No candidates uploaded yet.</p>
                  <p className="text-gray-400 mb-6">Upload some resumes to get started!</p>
                  <button
                    onClick={() => setActiveTab('upload')}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                  >
                    Upload Resumes
                  </button>
                </div>
              ) : (
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {candidates.map((candidate) => (
                    <div key={candidate.id} className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-xl border border-gray-200 hover:shadow-md transition-shadow text-center">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1 text-center">
                          <h3 className="font-bold text-xl text-gray-800 mb-1">{candidate.name}</h3>
                          <p className="text-gray-600 text-sm mb-1">{candidate.email}</p>
                          <p className="text-gray-600 text-sm">{candidate.phone}</p>
                        </div>
                        <button
                          onClick={() => deleteCandidate(candidate.id)}
                          className="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50 transition-colors"
                          title="Delete candidate"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3 text-sm text-center">
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <div className="text-blue-600 font-medium">Skill Match</div>
                          <div className="text-lg font-bold text-blue-800">{(candidate.skill_match * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-green-50 p-3 rounded-lg">
                          <div className="text-green-600 font-medium">JD Alignment</div>
                          <div className="text-lg font-bold text-green-800">{(candidate.jd_alignment * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-purple-50 p-3 rounded-lg">
                          <div className="text-purple-600 font-medium">Experience</div>
                          <div className="text-lg font-bold text-purple-800">{(candidate.exp_years * 20).toFixed(1)} yrs</div>
                        </div>
                        <div className="bg-orange-50 p-3 rounded-lg">
                          <div className="text-orange-600 font-medium">Projects</div>
                          <div className="text-lg font-bold text-orange-800">{(candidate.projects * 10).toFixed(0)}</div>
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
            <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-5xl border border-gray-100">
              <div className="text-center mb-8">
                <div className="text-6xl mb-4">🏆</div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Candidate Rankings</h2>
                <p className="text-gray-600">TOPSIS algorithm results based on multi-criteria evaluation</p>
              </div>

              <div className="flex justify-center mb-6">
                <button
                  onClick={handleRankCandidates}
                  disabled={loading}
                  className={`px-8 py-3 rounded-xl font-semibold transition-all duration-200 transform ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed text-white'
                      : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-lg hover:shadow-xl hover:scale-105'
                  }`}
                >
                  {loading ? '🔄 Refreshing...' : '🔄 Refresh Rankings'}
                </button>
              </div>

              {rankings.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📊</div>
                  <p className="text-gray-500 text-lg mb-4">No rankings available yet.</p>
                  <p className="text-gray-400 mb-6">Upload candidates and rank them to see results!</p>
                  <div className="flex justify-center gap-4">
                    <button
                      onClick={() => setActiveTab('upload')}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                    >
                      Upload Resumes
                    </button>
                    <button
                      onClick={handleRankCandidates}
                      disabled={loading}
                      className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                        loading
                          ? 'bg-gray-400 cursor-not-allowed text-white'
                          : 'bg-green-600 hover:bg-green-700 text-white'
                      }`}
                    >
                      {loading ? 'Ranking...' : 'Rank Now'}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  {rankings.map((candidate, index) => (
                    <div key={candidate.id || index} className={`p-6 rounded-2xl border-l-8 shadow-lg hover:shadow-xl transition-all duration-200 ${
                      index === 0 ? 'border-yellow-400 bg-gradient-to-r from-yellow-50 to-orange-50' :
                      index === 1 ? 'border-gray-400 bg-gradient-to-r from-gray-50 to-slate-50' :
                      index === 2 ? 'border-orange-400 bg-gradient-to-r from-orange-50 to-red-50' :
                      'border-blue-400 bg-gradient-to-r from-blue-50 to-indigo-50'
                    }`}>
                      <div className="flex justify-between items-start">
                        <div className="flex-1 text-center">
                          <div className="flex items-center justify-center gap-4 mb-3">
                            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl font-bold ${
                              index === 0 ? 'bg-yellow-400 text-white' :
                              index === 1 ? 'bg-gray-400 text-white' :
                              index === 2 ? 'bg-orange-400 text-white' :
                              'bg-blue-400 text-white'
                            }`}>
                              #{candidate.rank}
                            </div>
                            <div className="text-center">
                              <h3 className="text-2xl font-bold text-gray-800">{candidate.name || 'Unknown'}</h3>
                              <p className="text-gray-600">{candidate.email || 'No email'}</p>
                            </div>
                          </div>
                          
                          <div className="text-center mb-4">
                            <div className="text-4xl font-bold text-blue-600 mb-1">
                              {((candidate.topsis_score || 0) * 100).toFixed(2)}%
                            </div>
                            <div className="text-sm text-gray-500">TOPSIS Score</div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 text-sm text-center">
                          <div className="bg-white p-4 rounded-xl shadow-sm border">
                            <div className="text-blue-600 font-semibold">Skill Match</div>
                            <div className="text-2xl font-bold text-blue-800">{((candidate.skill_match || 0) * 100).toFixed(1)}%</div>
                          </div>
                          <div className="bg-white p-4 rounded-xl shadow-sm border">
                            <div className="text-green-600 font-semibold">JD Alignment</div>
                            <div className="text-2xl font-bold text-green-800">{((candidate.jd_alignment || 0) * 100).toFixed(1)}%</div>
                          </div>
                          <div className="bg-white p-4 rounded-xl shadow-sm border">
                            <div className="text-purple-600 font-semibold">Experience</div>
                            <div className="text-2xl font-bold text-purple-800">{((candidate.exp_years || 0) * 20).toFixed(1)} yrs</div>
                          </div>
                          <div className="bg-white p-4 rounded-xl shadow-sm border">
                            <div className="text-orange-600 font-semibold">Projects</div>
                            <div className="text-2xl font-bold text-orange-800">{((candidate.projects || 0) * 10).toFixed(0)}</div>
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
            <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-4xl border border-gray-100">
              <div className="text-center mb-8">
                <div className="text-6xl mb-4">⚖️</div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Weight Configurations</h2>
                <p className="text-gray-600">Customize evaluation criteria weights for ranking</p>
              </div>

              {weights.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📊</div>
                  <p className="text-gray-500 text-lg mb-4">No custom weights configured yet.</p>
                  <p className="text-gray-400">Create custom weight configurations to fine-tune candidate evaluation.</p>
                </div>
              ) : (
                <div className="grid gap-6 md:grid-cols-2">
                  {weights.map((weight) => (
                    <div key={weight.id} className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow text-center">
                      <h3 className="font-bold text-xl text-gray-800 mb-4">{weight.name}</h3>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <div className="text-blue-600 font-semibold text-sm">Skill Match</div>
                          <div className="text-2xl font-bold text-blue-800">{(weight.skill_match * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                          <div className="text-green-600 font-semibold text-sm">JD Alignment</div>
                          <div className="text-2xl font-bold text-green-800">{(weight.jd_alignment * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                          <div className="text-purple-600 font-semibold text-sm">Experience</div>
                          <div className="text-2xl font-bold text-purple-800">{(weight.exp_years * 100).toFixed(1)}%</div>
                        </div>
                        <div className="bg-orange-50 p-4 rounded-lg">
                          <div className="text-orange-600 font-semibold text-sm">Projects</div>
                          <div className="text-2xl font-bold text-orange-800">{(weight.projects * 100).toFixed(1)}%</div>
                        </div>
                      </div>
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <div className="text-center">
                          <div className="text-gray-500 text-sm">Education Weight</div>
                          <div className="text-lg font-semibold text-gray-700">{(weight.education * 100).toFixed(1)}%</div>
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
