import React, { ReactNode } from 'react';
import { 
  Home, 
  Settings, 
  Play, 
  HelpCircle,
  User,
  LogOut,
  CreditCard
} from 'lucide-react';
import { AppView, User as UserType } from '../types';

interface LayoutProps {
  children: ReactNode;
  currentView: AppView;
  setView: (view: AppView) => void;
  user: UserType;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  currentView, 
  setView, 
  user, 
  onLogout 
}) => {
  return (
    <div className="min-h-screen bg-zinc-50 flex flex-col">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-zinc-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-black flex items-center justify-center rounded-lg">
              <span className="text-white font-black text-lg">EV</span>
            </div>
            <div>
              <h1 className="text-lg font-black uppercase tracking-tight">EstateVision AI</h1>
              <p className="text-xs text-zinc-500 font-medium">Property Video Generator</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-zinc-100 px-3 py-1.5 rounded-full text-xs font-black uppercase tracking-widest">
              <CreditCard size={12} />
              <span>{user.credits} Credits</span>
            </div>
            
            <div className="flex items-center gap-2 border border-zinc-200 px-3 py-1.5 rounded-full text-xs font-medium">
              <div className="w-6 h-6 bg-black flex items-center justify-center text-white text-xs font-black rounded-full">
                {user.name.charAt(0)}
              </div>
              <span>{user.name}</span>
            </div>
            
            <button 
              onClick={onLogout}
              className="p-2 hover:bg-zinc-100 rounded-full transition-colors"
              title="Logout"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar Navigation */}
        <nav className="w-20 bg-white border-r border-zinc-200 flex flex-col py-6">
          <div className="space-y-8 flex-1">
            <button
              onClick={() => setView(AppView.DASHBOARD)}
              className={`p-3 rounded-xl flex flex-col items-center transition-all ${
                currentView === AppView.DASHBOARD 
                  ? 'bg-black text-white' 
                  : 'text-zinc-400 hover:bg-zinc-100'
              }`}
              title="Dashboard"
            >
              <Home size={20} />
              <span className="text-[8px] font-black uppercase tracking-widest mt-1">Home</span>
            </button>
            
            <button
              onClick={() => setView(AppView.GENERATE)}
              className={`p-3 rounded-xl flex flex-col items-center transition-all ${
                currentView === AppView.GENERATE 
                  ? 'bg-black text-white' 
                  : 'text-zinc-400 hover:bg-zinc-100'
              }`}
              title="Generate Video"
            >
              <Play size={20} />
              <span className="text-[8px] font-black uppercase tracking-widest mt-1">Create</span>
            </button>
            
            <button
              onClick={() => setView(AppView.SETTINGS)}
              className={`p-3 rounded-xl flex flex-col items-center transition-all ${
                currentView === AppView.SETTINGS 
                  ? 'bg-black text-white' 
                  : 'text-zinc-400 hover:bg-zinc-100'
              }`}
              title="Settings"
            >
              <Settings size={20} />
              <span className="text-[8px] font-black uppercase tracking-widest mt-1">Config</span>
            </button>
            
            <button
              onClick={() => setView(AppView.HELP)}
              className={`p-3 rounded-xl flex flex-col items-center transition-all ${
                currentView === AppView.HELP 
                  ? 'bg-black text-white' 
                  : 'text-zinc-400 hover:bg-zinc-100'
              }`}
              title="Help"
            >
              <HelpCircle size={20} />
              <span className="text-[8px] font-black uppercase tracking-widest mt-1">Help</span>
            </button>
          </div>
        </nav>

        {/* Main Content Area */}
        <main className="flex-1 p-6 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;