import { useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_URL || "https://agentresume-ai-3.onrender.com";


const defaultJobDescription = `We are looking for a Full Stack Developer.

Required Skills:
- HTML
- CSS
- JavaScript
- React.js
- Node.js
- Express.js
- MongoDB
- REST API
- Git and GitHub
- Basic knowledge of Data Structures and Algorithms

Responsibilities:
- Build responsive web applications.
- Develop REST APIs.
- Work with databases.
- Collaborate with development teams.
- Write clean and maintainable code.
`;

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [activePage, setActivePage] = useState("Dashboard");

  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState(
    defaultJobDescription
  );

  const [parsedResume, setParsedResume] = useState(null);
  const [atsResult, setAtsResult] = useState(null);
  const [jobMatch, setJobMatch] = useState(null);
  const [careerReport, setCareerReport] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [stats, setStats] = useState({
    atsScore: 0,
    skills: 0,
    matchPercentage: 0,
    applications: 0,
  });

  const showMessage = (text) => {
    setMessage(text);
    setError("");
  };

  const showError = (text) => {
    setError(text);
    setMessage("");
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      showError("Please select a PDF resume.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      showError("File size must be less than 5 MB.");
      return;
    }

    setSelectedFile(file);
    showMessage(`${file.name} selected successfully.`);
  };

  const uploadResume = async () => {
    if (!selectedFile) {
      showError("Please select a PDF resume first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      showMessage("Uploading and processing resume...");

      const response = await fetch(
        `${API_BASE}/api/resume/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume upload failed."
        );
      }

      const extractedText = data.extracted_text || "";

      setResumeText(extractedText);

      showMessage(
        `Resume processed using ${
          data.extraction_method || "text extraction"
        }.`
      );

      setActivePage("Resume");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const parseResume = async () => {
    if (!resumeText.trim()) {
      showError("Please upload and process your resume first.");
      return;
    }

    try {
      setLoading(true);
      showMessage("Parsing resume information...");

      const response = await fetch(
        `${API_BASE}/api/resume/parse`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: resumeText,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume parsing failed."
        );
      }

      const parsedData = data.data || data;

      setParsedResume(parsedData);

      setStats((previous) => ({
        ...previous,
        skills: parsedData.skills?.length || 0,
      }));

      showMessage("Resume parsed successfully.");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const analyzeResume = async () => {
    if (!resumeText.trim()) {
      showError("Please upload and process your resume first.");
      return;
    }

    try {
      setLoading(true);
      showMessage("Running ATS analysis...");

      const response = await fetch(
        `${API_BASE}/api/resume/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: resumeText,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "ATS analysis failed."
        );
      }

      setAtsResult(data);

      setStats((previous) => ({
        ...previous,
        atsScore: data.ats_score ?? data.score ?? 0,
      }));

      showMessage("ATS analysis completed successfully.");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const matchWithJob = async () => {
    if (!resumeText.trim()) {
      showError("Please upload and process your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      showError("Please paste a job description.");
      return;
    }

    try {
      setLoading(true);
      showMessage("Matching resume with job description...");

      const response = await fetch(
        `${API_BASE}/api/resume/job-match`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Job matching failed."
        );
      }

      setJobMatch(data);

      setStats((previous) => ({
        ...previous,
        matchPercentage: data.match_percentage || 0,
      }));

      showMessage("Job matching completed successfully.");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateCareerReport = async () => {
    if (!parsedResume) {
      showError("Please parse your resume first.");
      return;
    }

    try {
      setLoading(true);
      showMessage("Generating career recommendations...");

      const response = await fetch(
        `${API_BASE}/api/resume/career-recommendation`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            parsed_resume: parsedResume,
            job_description: jobDescription,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Career report generation failed."
        );
      }

      setCareerReport(data);
      showMessage("Career report generated successfully.");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const clearAllData = () => {
    setSelectedFile(null);
    setResumeText("");
    setParsedResume(null);
    setAtsResult(null);
    setJobMatch(null);
    setCareerReport(null);

    setStats({
      atsScore: 0,
      skills: 0,
      matchPercentage: 0,
      applications: 0,
    });

    setMessage("All resume data cleared.");
    setError("");
  };

  const navigationItems = [
    {
      name: "Dashboard",
      icon: "⌂",
    },
    {
      name: "Resume",
      icon: "▤",
    },
    {
      name: "ATS Analyzer",
      icon: "◉",
    },
    {
      name: "Job Matching",
      icon: "⌕",
    },
    {
      name: "Career AI",
      icon: "✦",
    },
    {
      name: "Reports",
      icon: "▥",
    },
  ];

  return (
    <div className={darkMode ? "app dark-mode" : "app light-mode"}>
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">
            AR
          </div>

          <div>
            <h2>AgentResume</h2>
            <span>AI Career Platform</span>
          </div>
        </div>

        <div className="sidebar-label">
          WORKSPACE
        </div>

        <nav className="sidebar-nav">
          {navigationItems.map((item) => (
            <button
              key={item.name}
              className={
                activePage === item.name
                  ? "nav-item active"
                  : "nav-item"
              }
              onClick={() => setActivePage(item.name)}
            >
              <span className="nav-icon">
                {item.icon}
              </span>

              <span>{item.name}</span>

              {item.name === "Dashboard" && (
                <span className="nav-dot" />
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-label settings-label">
          SETTINGS
        </div>

        <button
          className={
            activePage === "Settings"
              ? "nav-item active"
              : "nav-item"
          }
          onClick={() => setActivePage("Settings")}
        >
          <span className="nav-icon">⚙</span>
          <span>Settings</span>
        </button>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon">✦</div>
            <h4>Upgrade your career</h4>
            <p>
              Improve your resume and discover new opportunities.
            </p>
            <button
              onClick={() => setActivePage("Career AI")}
            >
              Explore AI
            </button>
          </div>

          <div className="profile-card">
            <div className="profile-avatar">
              AS
            </div>

            <div className="profile-details">
              <strong>Ashutosh Singh</strong>
              <span>Student Account</span>
            </div>

            <button
              className="profile-menu"
              onClick={() => setActivePage("Profile")}
              title="Profile"
            >
              ⋮
            </button>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="mobile-brand">
            <div className="brand-logo">
              AR
            </div>
            <strong>AgentResume AI</strong>
          </div>

          <div className="breadcrumb">
            Workspace <span>/</span>{" "}
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-actions">
            <button
              className="theme-button"
              onClick={() => setDarkMode(!darkMode)}
              title="Toggle theme"
            >
              {darkMode ? "☀" : "☾"}
            </button>

            <div className="notification">
              ♧
              <span />
            </div>

            <div className="top-avatar">
              AS
            </div>
          </div>
        </header>

        <section className="page-content">
          <div className="page-heading">
            <div>
              <span className="eyebrow">
                YOUR AI-POWERED CAREER ASSISTANT
              </span>

              <h1>
                {activePage === "Dashboard"
                  ? "Welcome back, Ashutosh"
                  : activePage}
              </h1>

              <p>
                Analyze your resume, improve your ATS score and
                find your next career opportunity.
              </p>
            </div>

            <div className="heading-actions">
              <button
                className="secondary-button"
                onClick={clearAllData}
              >
                ↻ Reset
              </button>

              <button
                className="primary-button"
                onClick={() => setActivePage("Resume")}
              >
                + Upload Resume
              </button>
            </div>
          </div>

          {message && (
            <div className="alert success-alert">
              ✓ {message}
            </div>
          )}

          {error && (
            <div className="alert error-alert">
              ⚠ {error}
            </div>
          )}

          {loading && (
            <div className="loading-bar">
              <span />
            </div>
          )}

          {activePage === "Dashboard" && (
            <>
              <section className="stats-grid">
                <StatCard
                  icon="◉"
                  title="ATS Resume Score"
                  value={`${stats.atsScore}%`}
                  subtitle="Resume compatibility"
                  color="purple"
                />

                <StatCard
                  icon="✦"
                  title="Detected Skills"
                  value={stats.skills}
                  subtitle="Technical skills found"
                  color="blue"
                />

                <StatCard
                  icon="⌕"
                  title="Job Match"
                  value={`${stats.matchPercentage}%`}
                  subtitle="Target job compatibility"
                  color="pink"
                />

                <StatCard
                  icon="▥"
                  title="Resume Status"
                  value={resumeText ? "Ready" : "Pending"}
                  subtitle="Upload your resume"
                  color="green"
                />
              </section>

              <section className="dashboard-grid">
                <div className="panel upload-panel">
                  <PanelHeader
                    number="01"
                    title="Upload Your Resume"
                    subtitle="Start your AI resume analysis"
                  />

                  <div className="upload-zone">
                    <div className="upload-icon">
                      ↑
                    </div>

                    <h3>
                      Upload your resume PDF
                    </h3>

                    <p>
                      Drag and drop your resume or select a PDF
                      file from your computer.
                    </p>

                    <label className="file-button">
                      Choose PDF File
                      <input
                        type="file"
                        accept=".pdf,application/pdf"
                        onChange={handleFileChange}
                      />
                    </label>

                    {selectedFile && (
                      <div className="selected-file">
                        <span>▤</span>
                        <div>
                          <strong>
                            {selectedFile.name}
                          </strong>
                          <small>
                            {(selectedFile.size / 1024).toFixed(1)} KB
                          </small>
                        </div>
                      </div>
                    )}

                    <button
                      className="primary-button full-button"
                      onClick={uploadResume}
                      disabled={loading}
                    >
                      {loading
                        ? "Processing..."
                        : "Process Resume →"}
                    </button>
                  </div>
                </div>

                <div className="panel quick-panel">
                  <PanelHeader
                    number="02"
                    title="Quick Actions"
                    subtitle="Continue your resume journey"
                  />

                  <div className="quick-actions">
                    <QuickAction
                      icon="▤"
                      title="Parse Resume"
                      description="Extract profile and skills"
                      onClick={parseResume}
                    />

                    <QuickAction
                      icon="◉"
                      title="Analyze ATS"
                      description="Check resume compatibility"
                      onClick={analyzeResume}
                    />

                    <QuickAction
                      icon="⌕"
                      title="Match Job"
                      description="Compare with job description"
                      onClick={() => setActivePage("Job Matching")}
                    />

                    <QuickAction
                      icon="✦"
                      title="Career AI"
                      description="Get career recommendations"
                      onClick={generateCareerReport}
                    />
                  </div>
                </div>
              </section>

              <section className="dashboard-grid bottom-grid">
                <ParsedResumePanel
                  parsedResume={parsedResume}
                />

                <AtsPanel atsResult={atsResult} />
              </section>
            </>
          )}

          {activePage === "Resume" && (
            <section className="single-page-grid">
              <div className="panel">
                <PanelHeader
                  number="01"
                  title="Resume Processing"
                  subtitle="Upload and extract resume text"
                />

                <div className="upload-zone large-upload">
                  <div className="upload-icon">
                    ↑
                  </div>

                  <h3>Upload PDF Resume</h3>

                  <p>
                    Maximum file size: 5 MB
                  </p>

                  <label className="file-button">
                    Select Resume
                    <input
                      type="file"
                      accept=".pdf,application/pdf"
                      onChange={handleFileChange}
                    />
                  </label>

                  {selectedFile && (
                    <p className="file-name">
                      Selected: {selectedFile.name}
                    </p>
                  )}

                  <button
                    className="primary-button"
                    onClick={uploadResume}
                  >
                    Upload and Extract
                  </button>
                </div>
              </div>

              <div className="panel">
                <PanelHeader
                  number="02"
                  title="Extracted Resume Text"
                  subtitle="Review extracted text before parsing"
                />

                <textarea
                  className="resume-textarea"
                  value={resumeText}
                  onChange={(event) =>
                    setResumeText(event.target.value)
                  }
                  placeholder="Your extracted resume text will appear here..."
                />

                <div className="button-row">
                  <button
                    className="primary-button"
                    onClick={parseResume}
                  >
                    Parse Resume
                  </button>

                  <button
                    className="secondary-button"
                    onClick={analyzeResume}
                  >
                    Analyze ATS
                  </button>
                </div>
              </div>

              <ParsedResumePanel
                parsedResume={parsedResume}
              />

              <AtsPanel atsResult={atsResult} />
            </section>
          )}

          {activePage === "ATS Analyzer" && (
            <section className="single-page-grid">
              <div className="panel">
                <PanelHeader
                  number="04"
                  title="ATS Resume Analysis"
                  subtitle="Analyze your resume for ATS compatibility"
                />

                <div className="ats-large-layout">
                  <AtsCircle
                    score={
                      atsResult?.ats_score ??
                      atsResult?.score ??
                      0
                    }
                  />

                  <div className="ats-summary">
                    <h3>
                      Your ATS score is{" "}
                      {atsResult?.ats_score ??
                        atsResult?.score ??
                        0}
                      %
                    </h3>

                    <p>
                      {atsResult
                        ? "Your resume analysis has been completed."
                        : "Upload and analyze your resume to see your score."}
                    </p>

                    <button
                      className="primary-button"
                      onClick={analyzeResume}
                    >
                      Analyze Resume
                    </button>
                  </div>
                </div>
              </div>

              <AtsPanel atsResult={atsResult} />
            </section>
          )}

          {activePage === "Job Matching" && (
            <section className="single-page-grid">
              <div className="panel">
                <PanelHeader
                  number="05"
                  title="Job Description Matching"
                  subtitle="Paste a job description to find matching and missing skills."
                />

                <textarea
                  className="job-textarea"
                  value={jobDescription}
                  onChange={(event) =>
                    setJobDescription(event.target.value)
                  }
                  placeholder="Paste job description here..."
                />

                <button
                  className="primary-button"
                  onClick={matchWithJob}
                >
                  Match With Job →
                </button>
              </div>

              <JobMatchPanel jobMatch={jobMatch} />
            </section>
          )}

          {activePage === "Career AI" && (
            <section className="single-page-grid">
              <div className="panel">
                <PanelHeader
                  number="06"
                  title="Multi-Agent Career AI"
                  subtitle="Get career recommendations based on your resume"
                />

                <div className="career-intro">
                  <div className="career-icon">
                    ✦
                  </div>

                  <h3>
                    Discover your career direction
                  </h3>

                  <p>
                    Our AI agents analyze your profile, skills,
                    gaps and target job requirements.
                  </p>

                  <button
                    className="primary-button"
                    onClick={generateCareerReport}
                  >
                    Generate Career Report →
                  </button>
                </div>
              </div>

              <CareerPanel careerReport={careerReport} />
            </section>
          )}

          {activePage === "Reports" && (
            <section className="single-page-grid">
              <ParsedResumePanel
                parsedResume={parsedResume}
              />

              <AtsPanel atsResult={atsResult} />

              <JobMatchPanel jobMatch={jobMatch} />

              <CareerPanel careerReport={careerReport} />
            </section>
          )}

          {activePage === "Settings" && (
            <section className="panel settings-panel">
              <PanelHeader
                number="07"
                title="Settings"
                subtitle="Customize your AgentResume AI workspace"
              />

              <div className="setting-row">
                <div>
                  <h3>Appearance</h3>
                  <p>Switch between dark and light mode.</p>
                </div>

                <button
                  className="secondary-button"
                  onClick={() => setDarkMode(!darkMode)}
                >
                  {darkMode
                    ? "Switch to Light"
                    : "Switch to Dark"}
                </button>
              </div>

              <div className="setting-row">
                <div>
                  <h3>Clear Resume Data</h3>
                  <p>
                    Remove uploaded resume and analysis results.
                  </p>
                </div>

                <button
                  className="danger-button"
                  onClick={clearAllData}
                >
                  Clear Data
                </button>
              </div>
            </section>
          )}

          {activePage === "Profile" && (
            <section className="panel profile-page">
              <div className="large-profile-avatar">
                AS
              </div>

              <h2>Ashutosh Singh</h2>
              <p>Student Account · CSE AIML</p>

              <div className="profile-info-grid">
                <div>
                  <span>Role</span>
                  <strong>Student Developer</strong>
                </div>

                <div>
                  <span>Platform</span>
                  <strong>AgentResume AI</strong>
                </div>

                <div>
                  <span>Status</span>
                  <strong>Active</strong>
                </div>
              </div>
            </section>
          )}
        </section>

        <footer className="footer">
          <span>© 2026 AgentResume AI</span>
          <span>Built with React + FastAPI + AI</span>
        </footer>
      </main>
    </div>
  );
}

function StatCard({
  icon,
  title,
  value,
  subtitle,
  color,
}) {
  return (
    <div className={`stat-card ${color}`}>
      <div className="stat-top">
        <div className="stat-icon">
          {icon}
        </div>

        <span className="stat-badge">
          Live
        </span>
      </div>

      <h3>{value}</h3>
      <strong>{title}</strong>
      <p>{subtitle}</p>
    </div>
  );
}

function PanelHeader({
  number,
  title,
  subtitle,
}) {
  return (
    <div className="panel-header">
      <div className="section-number">
        {number}
      </div>

      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>
  );
}

function QuickAction({
  icon,
  title,
  description,
  onClick,
}) {
  return (
    <button
      className="quick-action"
      onClick={onClick}
    >
      <span className="quick-action-icon">
        {icon}
      </span>

      <span className="quick-action-text">
        <strong>{title}</strong>
        <small>{description}</small>
      </span>

      <span className="quick-arrow">
        →
      </span>
    </button>
  );
}

function ResultBlock({
  title,
  value,
}) {
  return (
    <div className="result-block">
      <span>{title}</span>
      <p>{value || "Not detected"}</p>
    </div>
  );
}

function ParsedResumePanel({
  parsedResume,
}) {
  return (
    <div className="panel">
      <PanelHeader
        number="03"
        title="Parsed Resume Profile"
        subtitle="Information extracted from your resume"
      />

      <div className="result-content">
        <ResultBlock
          title="Name"
          value={parsedResume?.name}
        />

        <ResultBlock
          title="Email"
          value={parsedResume?.email}
        />

        <ResultBlock
          title="Phone"
          value={parsedResume?.phone}
        />

        <div className="result-block">
          <span>Detected Skills</span>

          {parsedResume?.skills?.length ? (
            <div className="skill-list">
              {parsedResume.skills.map((skill) => (
                <span
                  className="skill-tag"
                  key={skill}
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p>No skills detected.</p>
          )}
        </div>

        <ResultBlock
          title="Education"
          value={parsedResume?.education}
        />

        <ResultBlock
          title="Projects"
          value={parsedResume?.projects}
        />
      </div>
    </div>
  );
}

function AtsPanel({
  atsResult,
}) {
  const score =
    atsResult?.ats_score ??
    atsResult?.score ??
    0;

  return (
    <div className="panel">
      <PanelHeader
        number="04"
        title="ATS Resume Analysis"
        subtitle="Check your resume compatibility"
      />

      <div className="ats-panel-content">
        <AtsCircle score={score} />

        <h3>
          {atsResult
            ? "Your resume analysis has been completed."
            : "Analyze your resume to see your score."}
        </h3>

        <div className="ats-mini-details">
          <div>
            <span>Word Count</span>
            <strong>
              {atsResult?.word_count || 0}
            </strong>
          </div>

          <div>
            <span>Keywords</span>
            <strong>
              {atsResult?.keyword_count || 0}
            </strong>
          </div>
        </div>

        {atsResult?.improvements?.length > 0 && (
          <div className="improvement-box">
            <strong>Improvements</strong>

            <ul>
              {atsResult.improvements
                .slice(0, 4)
                .map((item, index) => (
                  <li key={index}>
                    {item}
                  </li>
                ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

function AtsCircle({
  score,
}) {
  return (
    <div
      className="ats-circle"
      style={{
        "--score": `${score * 3.6}deg`,
      }}
    >
      <div className="ats-circle-inner">
        <strong>{score}</strong>
        <span>%</span>
      </div>
    </div>
  );
}

function JobMatchPanel({
  jobMatch,
}) {
  return (
    <div className="panel">
      <PanelHeader
        number="05"
        title="Job Match Result"
        subtitle="Matched and missing skills"
      />

      <div className="match-result">
        <div className="match-score">
          <span>Match Percentage</span>
          <strong>
            {jobMatch?.match_percentage || 0}%
          </strong>
        </div>

        <div className="match-section">
          <h3>Matched Skills</h3>

          {jobMatch?.matched_skills?.length ? (
            <div className="skill-list">
              {jobMatch.matched_skills.map((skill) => (
                <span
                  className="skill-tag success-tag"
                  key={skill}
                >
                  ✓ {skill}
                </span>
              ))}
            </div>
          ) : (
            <p>No matching skills found.</p>
          )}
        </div>

        <div className="match-section">
          <h3>Missing Skills</h3>

          {jobMatch?.missing_skills?.length ? (
            <div className="skill-list">
              {jobMatch.missing_skills.map((skill) => (
                <span
                  className="skill-tag missing-tag"
                  key={skill}
                >
                  + {skill}
                </span>
              ))}
            </div>
          ) : (
            <p>No major missing skills detected.</p>
          )}
        </div>

        {jobMatch?.suggestions?.length > 0 && (
          <div className="suggestion-box">
            <h3>Suggestions</h3>

            <ul>
              {jobMatch.suggestions.map(
                (suggestion, index) => (
                  <li key={index}>
                    {suggestion}
                  </li>
                )
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

function CareerPanel({
  careerReport,
}) {
  return (
    <div className="panel">
      <PanelHeader
        number="06"
        title="Multi-Agent Career Report"
        subtitle="AI-powered career recommendations"
      />

      {careerReport ? (
        <div className="career-result">
          <h3>Recommended Career Paths</h3>

          <div className="career-list">
            {careerReport.recommendations?.map(
              (recommendation, index) => (
                <div
                  className="career-item"
                  key={index}
                >
                  <span>✦</span>
                  <strong>{recommendation}</strong>
                </div>
              )
            )}
          </div>

          <div className="report-text">
            {careerReport.final_report}
          </div>
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-icon">
            ✦
          </div>

          <h3>No career report yet</h3>

          <p>
            Parse your resume and generate your personalized
            career recommendations.
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
