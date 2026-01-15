'use client';

import { ChatInformationProvider } from "./contexts/ChatInformationContext";
import { OptionContextProvider } from "./contexts/OptionContext";


import SourcesPanel from "./components/SourcesPanel";
import StudioPanel from "./components/FunctionPanel";
import OptionContainer from "./components/OptionContainer";


export default function Home() {
  
  return (
    <div className="flex overflow-hidden bg-background">
      <ChatInformationProvider>
        <SourcesPanel/>
        
        <OptionContextProvider>
          <OptionContainer/>
          <StudioPanel/>
        </OptionContextProvider>
      </ChatInformationProvider>     
    </div>
  )
}
