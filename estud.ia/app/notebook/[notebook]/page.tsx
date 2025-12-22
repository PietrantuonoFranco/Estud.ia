
import SourcesPanel from "./components/SourcesPanel";
import ChatPanel from "./components/Chat/ChatPanel";
import StudioPanel from "./components/FunctionPanel";

export default function Home() {
  return (
    <div className="flex h-screen flex-col bg-background">
      <div className="flex flex-1 overflow-hidden">
        <SourcesPanel />
        <ChatPanel />
        <StudioPanel />
      </div>
    </div>
  )
}
