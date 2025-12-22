import Header from "./components/Header";
import OptionsBanner from "./components/OptionsBanner";
import NotebooksContainer from "./components/NotebooksContainer";


export default function Home() {
  return (
      <div className="flex flex-col flex-1 overflow-hidden py-6 px-42 space-y-6  bg-background">
        <OptionsBanner />

        <NotebooksContainer />
      </div>
  )
}
