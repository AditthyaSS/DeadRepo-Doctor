import { useState } from "react";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setReport(null);

    try {
      // ✅ STEP 1: CALL /api/fetch
      const fetchResponse = await fetch("http://127.0.0.1:8000/api/fetch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      const fetchData = await fetchResponse.json();

      if (!fetchResponse.ok || !fetchData.local_path) {
        throw new Error("Failed to fetch repository");
      }

      // ✅ STEP 2: CALL /api/analyze
      const analyzeResponse = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ local_path: fetchData.local_path }),
      });

      const analyzeData = await analyzeResponse.json();

      if (!analyzeResponse.ok || !analyzeData.analysis_report) {
        throw new Error("Failed to analyze repository");
      }

      // ✅ STEP 3: SAVE REPORT TO UI
      setReport(analyzeData.analysis_report);

    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold mb-4 text-red-500">DeadRepo Doctor 💀</h1>
      <p className="text-gray-400 mb-8">Reviving abandoned codebases</p>

      <input
        type="text"
        placeholder="Enter GitHub Repo URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        className="w-full max-w-md p-3 rounded bg-gray-800 border border-gray-700 mb-4"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading || !repoUrl}
        className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded font-semibold disabled:opacity-50"
      >
        {loading ? "Analyzing..." : "Fetch & Analyze"}
      </button>

      {/* ✅ ERROR MESSAGE */}
      {error && <p className="text-red-500 mt-4">{error}</p>}

      {/* ✅ REPORT UI */}
      {report && (
        <div className="mt-6 bg-gray-900 p-6 rounded max-w-lg w-full">
          <h2 className="text-xl mb-2 text-green-400">Analysis Report ✅</h2>
          <p>Total Packages: {report.summary.total_packages}</p>
          <p>Outdated: {report.summary.outdated_count}</p>
          <p>Health Score: {report.health_score}</p>
        </div>
      )}
    </div>
  );
}

export default App;
