'use client';

import { ChatInformationProvider } from "./contexts/ChatInformationContext";

import SourcesPanel from "./components/SourcesPanel";
import ChatPanel from "./components/Chat/ChatPanel";
import StudioPanel from "./components/FunctionPanel";


export default function Home() {
  
  return (
    <div className="flex overflow-hidden bg-background">
      <ChatInformationProvider>
        <SourcesPanel/>
        <ChatPanel/>
        <StudioPanel/>
      </ChatInformationProvider>     
    </div>
  )
}
