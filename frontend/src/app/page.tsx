import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col font-sans selection:bg-blue-500/30">
      {/* Navigation */}
      <nav className="w-full max-w-7xl mx-auto px-6 py-8 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white shadow-lg shadow-blue-600/20">C</div>
          <span className="font-bold text-xl tracking-tight">Clinica Router</span>
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium text-slate-400">
          <Link href="#" className="hover:text-white transition-colors">Features</Link>
          <Link href="#" className="hover:text-white transition-colors">Documentation</Link>
          <Link href="#" className="hover:text-white transition-colors">API</Link>
        </div>
      </nav>

      <main className="flex-1 flex flex-col items-center justify-center px-6 -mt-20">
        <div className="max-w-4xl text-center flex flex-col items-center">
          <div className="px-4 py-1 rounded-full border border-white/10 bg-white/5 text-[10px] font-bold tracking-[0.2em] text-blue-400 uppercase mb-8">
            Advanced Clinical Intelligence
          </div>
          
          <h1 className="text-6xl md:text-8xl font-medium tracking-tight mb-8 leading-[1.05]">
            Routing medical data <br />
            <span className="text-slate-500">with absolute precision.</span>
          </h1>
          
          <p className="text-slate-400 text-lg md:text-xl mb-12 max-w-2xl leading-relaxed">
            The next generation of agent-to-agent medical communication. Secure, compliant, and infinitely scalable clinical routing.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Link 
              href="/a2a-tester" 
              className="bg-white text-black px-10 py-4 rounded-full font-bold text-lg hover:bg-slate-200 transition-all flex items-center gap-2 group"
            >
              Launch Protocol Tester
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
            <button className="px-10 py-4 rounded-full font-bold text-lg border border-white/20 hover:bg-white/5 transition-all">
              Read Technical Spec
            </button>
          </div>
        </div>
      </main>

      {/* Footer / Stats */}
      <footer className="w-full max-w-7xl mx-auto px-6 py-12 border-t border-white/5 grid grid-cols-1 md:grid-cols-3 gap-12 text-sm">
        <div>
          <h4 className="font-bold text-slate-300 mb-2 italic">Standardized</h4>
          <p className="text-slate-500 leading-relaxed">Fully JSON-RPC 2.0 compliant A2A messaging for seamless platform integration.</p>
        </div>
        <div>
          <h4 className="font-bold text-slate-300 mb-2 italic">Verified</h4>
          <p className="text-slate-500 leading-relaxed">Evidence-backed clinical responses with automatic citation extraction from RAG stores.</p>
        </div>
        <div>
          <h4 className="font-bold text-slate-300 mb-2 italic">Specialized</h4>
          <p className="text-slate-500 leading-relaxed">Pre-routed intelligence for Cardiology, Oncology, Pediatrics, and more.</p>
        </div>
      </footer>
    </div>
  );
}
