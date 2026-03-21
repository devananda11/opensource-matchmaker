import { useState, useEffect } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // ✨ Cursor glow
  useEffect(() => {
    const handleMove = (e) => {
      const glow = document.getElementById("glow");
      if (glow) {
        glow.style.left = e.clientX - 80 + "px";
        glow.style.top = e.clientY - 80 + "px";
      }
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  const fetchRecommendations = async () => {
    if (!username) return;

    setLoading(true);
    setHasSearched(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/recommend/${username}`);
      const data = await res.json();
      setResults(data.recommendations || []);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0d1117] text-white relative overflow-hidden">

      {/* ✨ GRID BACKGROUND */}
      <div className="absolute inset-0 -z-20 bg-[linear-gradient(to_right,#22c55e10_1px,transparent_1px),linear-gradient(to_bottom,#22c55e10_1px,transparent_1px)] bg-[size:40px_40px]" />

      {/* ✨ SUBTLE GLOW LAYER */}
      <div className="absolute inset-0 -z-10 bg-green-500 opacity-10 blur-3xl animate-pulse" />

      {/* ✨ CURSOR GLOW */}
      <div
        id="glow"
        className="fixed w-40 h-40 bg-green-500 opacity-20 blur-3xl rounded-full pointer-events-none"
      ></div>

      {/* 🔹 LANDING */}
      {!hasSearched && (
        <div className="flex flex-col items-center justify-center h-screen px-4 text-center transition-all duration-500">

          <h1 className="text-5xl font-bold mb-4 tracking-tight">
            FirstIssue
          </h1>

          <p className="text-gray-400 mb-8 max-w-md">
            Discover open-source issues tailored to your skills
          </p>

          <div className="flex gap-2 bg-[#161b22] border border-gray-700 p-2 rounded-xl shadow-lg backdrop-blur-md">
            <input
              className="px-4 py-2 bg-transparent outline-none text-white placeholder-gray-500 w-64"
              placeholder="GitHub username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && fetchRecommendations()}
            />
            <button
              onClick={fetchRecommendations}
              className="bg-green-500 text-black px-4 py-2 rounded-lg hover:bg-green-400 transition"
            >
              Search
            </button>
          </div>

        </div>
      )}

      {/* 🔹 RESULTS */}
      {hasSearched && (
        <div className="p-6 max-w-3xl mx-auto animate-fade">

          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-semibold">Results</h1>

            <button
              onClick={() => {
                setHasSearched(false);
                setResults([]);
                setUsername("");
              }}
              className="text-sm text-gray-400 hover:text-white"
            >
              ← Back
            </button>
          </div>

          {/* Search again */}
          <div className="flex gap-2 mb-6 bg-[#161b22] border border-gray-700 p-2 rounded-xl">
            <input
              className="px-4 py-2 bg-transparent outline-none text-white placeholder-gray-500 w-full"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <button
              onClick={fetchRecommendations}
              className="bg-green-500 text-black px-4 py-2 rounded-lg hover:bg-green-400"
            >
              Search
            </button>
          </div>

          {/* Loading */}
          {loading && (
            <p className="text-gray-400">🔍 Finding best matches...</p>
          )}

          {/* Empty */}
          {!loading && results.length === 0 && (
            <p className="text-gray-500">No results found</p>
          )}

          {/* Cards */}
          <div className="space-y-4">
            {results.map((item, i) => (
              <div
                key={i}
                className="bg-[#161b22] p-5 rounded-xl border border-gray-700 hover:border-green-500 hover:shadow-lg transition transform hover:-translate-y-1"
              >
                <h2 className="text-lg font-semibold mb-1">
                  {item.issue_title}
                </h2>

                <p className="text-sm text-gray-400 mb-2">
                  {item.repo_name}
                </p>

                {/* Score bar */}
                <div className="w-full bg-gray-800 rounded-full h-2 mb-3">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all"
                    style={{ width: `${item.score * 10}%` }}
                  ></div>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-300">
                    Score: {item.score}
                  </span>

                  <a
                    href={item.issue_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-green-400 hover:underline"
                  >
                    View →
                  </a>
                </div>
              </div>
            ))}
          </div>

        </div>
      )}
    </div>
  );
}

export default App;