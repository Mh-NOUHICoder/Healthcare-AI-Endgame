"use client";

import { useState } from "react";
import Link from "next/link";

const PRESET_SCENARIOS = [
  {
    category: "Cardiology",
    cases: [
      {
        label: "Chest Pain",
        payload: {
          jsonrpc: "2.0",
          id: "cardio-1",
          method: "a2a",
          params: {
            id: "task-1",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Cardiology" },
            input: { text: "I am experiencing sharp chest pain and shortness of breath.", data: {}, references: [] }
          }
        }
      },
      {
        label: "Hypertension Risks",
        payload: {
          jsonrpc: "2.0",
          id: "cardio-2",
          method: "a2a",
          params: {
            id: "task-2",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Cardiology" },
            input: { text: "What are the long-term risks of having a blood pressure of 140/90?", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Pediatrics",
    cases: [
      {
        label: "Infant Fever",
        payload: {
          jsonrpc: "2.0",
          id: "peds-1",
          method: "a2a",
          params: {
            id: "task-3",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Pediatrics" },
            input: { text: "My 6-month-old has a fever of 102F and is very fussy.", data: {}, references: [] }
          }
        }
      },
      {
        label: "MMR Schedule",
        payload: {
          jsonrpc: "2.0",
          id: "peds-2",
          method: "a2a",
          params: {
            id: "task-4",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Pediatrics" },
            input: { text: "What is the recommended schedule for the MMR vaccine?", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Drug Safety",
    cases: [
      {
        label: "Metformin/Ibuprofen",
        payload: {
          jsonrpc: "2.0",
          id: "drug-1",
          method: "a2a",
          params: {
            id: "task-5",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Drug Safety" },
            input: { text: "Is it safe to take Metformin with Ibuprofen?", data: {}, references: [] }
          }
        }
      },
      {
        label: "Lisinopril Side Effects",
        payload: {
          jsonrpc: "2.0",
          id: "drug-2",
          method: "a2a",
          params: {
            id: "task-6",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Drug Safety" },
            input: { text: "I started taking Lisinopril and now I have a persistent dry cough. Is this normal?", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Context & Edge Cases",
    cases: [
      {
        label: "Context-Aware Hypertension",
        payload: {
          jsonrpc: "2.0",
          id: "ctx-1",
          method: "a2a",
          params: {
            id: "task-7",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Context-Aware" },
            input: { text: "How does my hypertension affect my risk for other diseases?", data: {}, references: [] }
          }
        }
      },
      {
        label: "Out of Scope",
        payload: {
          jsonrpc: "2.0",
          id: "edge-1",
          method: "a2a",
          params: {
            id: "task-8",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Edge Cases" },
            input: { text: "What is the capital of France?", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Oncology",
    cases: [
      {
        label: "TNBC Early Treatment",
        payload: {
          jsonrpc: "2.0",
          id: "onco-1",
          method: "a2a",
          params: {
            id: "task-9",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Oncology" },
            input: { text: "What is the recommended treatment for triple-negative breast cancer in the early stages?", data: {}, references: [] }
          }
        }
      },
      {
        label: "Diagnosis Confirmation",
        payload: {
          jsonrpc: "2.0",
          id: "onco-2",
          method: "a2a",
          params: {
            id: "task-10",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Oncology" },
            input: { text: "How is a breast cancer diagnosis typically confirmed?", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Neurology",
    cases: [
      {
        label: "Migraine First-line",
        payload: {
          jsonrpc: "2.0",
          id: "neuro-1",
          method: "a2a",
          params: {
            id: "task-11",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Neurology" },
            input: { text: "I have severe migraines 6 times a month. What medications are first-line?", data: {}, references: [] }
          }
        }
      },
      {
        label: "Thunderclap Headache",
        payload: {
          jsonrpc: "2.0",
          id: "neuro-2",
          method: "a2a",
          params: {
            id: "task-12",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Neurology" },
            input: { text: "I just had a sudden thunderclap headache, the worst pain of my life.", data: {}, references: [] }
          }
        }
      }
    ]
  },
  {
    category: "Psychiatry",
    cases: [
      {
        label: "BPD Diagnostic Features",
        payload: {
          jsonrpc: "2.0",
          id: "psy-1",
          method: "a2a",
          params: {
            id: "task-13",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Psychiatry" },
            input: { text: "What are the core diagnostic features and recommended psychotherapy for Borderline Personality Disorder?", data: {}, references: [] }
          }
        }
      },
      {
        label: "Schizophrenia Pharma",
        payload: {
          jsonrpc: "2.0",
          id: "psy-2",
          method: "a2a",
          params: {
            id: "task-14",
            agent: "clinica-router-ai",
            status: { state: "PENDING", reason: "Testing Psychiatry" },
            input: { text: "What are the latest pharmacological recommendations for treating acute schizophrenia?", data: {}, references: [] }
          }
        }
      }
    ]
  }
];

export default function A2ATester() {
  const [requestPayload, setRequestPayload] = useState(
    JSON.stringify(
      {
        jsonrpc: "2.0",
        id: "test-req-1",
        method: "a2a",
        params: {
          id: "task-123",
          agent: "clinica-router-ai",
          status: {
            state: "PENDING",
            reason: "User query via tester",
          },
          input: {
            text: "What are the hypertension guidelines for adults?",
            data: {},
            references: [],
          },
        },
      },
      null,
      2
    )
  );

  const [responsePayload, setResponsePayload] = useState("");
  const [loading, setLoading] = useState(false);
  const [latency, setLatency] = useState<number | null>(null);

  const loadPreset = (payload:any) => {
    setRequestPayload(JSON.stringify(payload, null, 2));
  };

  const handleSend = async () => {
    try {
      setLoading(true);
      setResponsePayload("Loading...");
      
      let parsedPayload;
      try {
        parsedPayload = JSON.parse(requestPayload);
      } catch (err) {
        setResponsePayload("Invalid JSON payload:\n" + err);
        setLoading(false);
        return;
      }

      const startTime = performance.now();
      // Calls the python backend running on 8000
      const res = await fetch("http://127.0.0.1:8000/a2a", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(parsedPayload),
      });

      const endTime = performance.now();
      setLatency(Math.round(endTime - startTime));
      const data = await res.json();
      setResponsePayload(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setResponsePayload("Error connecting to backend API:\n" + err.message + "\n\nMake sure uvicorn is running on http://127.0.0.1:8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#050505] text-slate-300 font-sans">
      {/* Top Navigation */}
      <header className="h-16 border-b border-white/5 px-6 flex items-center justify-between bg-[#0a0a0a]">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-slate-500 hover:text-white transition-colors text-sm">
            ← Home
          </Link>
          <div className="h-4 w-px bg-white/10"></div>
          <h1 className="font-bold text-white tracking-tight">Protocol Tester v1.1</h1>
        </div>
        <div className="flex items-center gap-3">
          <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${loading ? "bg-blue-500/10 text-blue-400 animate-pulse" : "bg-emerald-500/10 text-emerald-400"}`}>
            {loading ? "Processing Graph" : "System Ready"}
          </div>
          <button 
            onClick={handleSend}
            disabled={loading}
            className="bg-white text-black px-4 py-1.5 rounded-md text-xs font-bold hover:bg-slate-200 disabled:opacity-50 transition-all shadow-lg shadow-white/5"
          >
            {loading ? "Executing..." : "Run Message"}
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Presets */}
        <aside className="w-72 border-r border-white/5 bg-[#080808] overflow-y-auto p-4 flex flex-col gap-6">
          <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest px-2">
            Library Scenarios
          </div>
          
          {PRESET_SCENARIOS.map((category, catIdx) => (
            <div key={catIdx} className="flex flex-col gap-1">
              <div className="text-[11px] font-bold text-blue-500/70 px-2 mb-1">{category.category}</div>
              {category.cases.map((preset, idx) => (
                <button 
                  key={idx} 
                  onClick={() => loadPreset(preset.payload)}
                  className="w-full text-left px-3 py-2 rounded-md text-xs hover:bg-white/5 hover:text-white transition-all border border-transparent hover:border-white/5"
                >
                  {preset.label}
                </button>
              ))}
            </div>
          ))}
        </aside>

        {/* Main Workspace */}
        <main className="flex-1 flex flex-col lg:flex-row bg-black overflow-hidden">
          {/* Editor Panel */}
          <div className="flex-1 flex flex-col border-r border-white/5">
            <div className="h-10 px-4 flex items-center justify-between bg-[#0a0a0a] border-b border-white/5">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Request Input</span>
              <span className="text-[9px] text-slate-600">JSON-RPC 2.0</span>
            </div>
            <textarea
              className="flex-1 w-full bg-black p-6 text-blue-300 font-mono text-xs focus:outline-none resize-none selection:bg-blue-500/20"
              value={requestPayload}
              onChange={(e) => setRequestPayload(e.target.value)}
              spellCheck="false"
            />
          </div>

          {/* Response Panel */}
          <div className="flex-1 flex flex-col">
            <div className="h-10 px-4 flex items-center justify-between bg-[#0a0a0a] border-b border-white/5">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Node Output</span>
              {latency && <span className="text-[9px] text-emerald-500 font-bold">{latency}ms</span>}
            </div>
            <div className="flex-1 p-6 font-mono text-xs overflow-y-auto bg-[#020202]">
              {responsePayload ? (
                <div className="text-emerald-400 whitespace-pre-wrap">{responsePayload}</div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center gap-4 text-slate-700">
                  <div className="w-12 h-12 border-2 border-slate-800 rounded-xl flex items-center justify-center animate-pulse">
                    <span className="text-xl">⚡</span>
                  </div>
                  <p className="text-[10px] uppercase tracking-widest">Awaiting interaction</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
