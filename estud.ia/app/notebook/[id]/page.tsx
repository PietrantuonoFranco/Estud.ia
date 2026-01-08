'use client';

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import SourcesPanel from "./components/SourcesPanel";
import ChatPanel from "./components/Chat/ChatPanel";
import StudioPanel from "./components/FunctionPanel";

import Notebook from "@/app/lib/interfaces/Notebook";


export default function Home() {
  const [notebook, setNotebook] = useState<Notebook | null >(null);
  
  const params = useParams();
  const id = params.id as string; // Extract the id from the route parameters

  const API_URL = process.env.API_URL || 'http://localhost:5000';

  useEffect(() => {
    if (id) {
      // Fetch notebook data when id is available
      const fetchNotebook = async () => {
        try {
          const response = await fetch(`${API_URL}/notebooks/${id}`); // Adjust the API endpoint as needed

          if (!response.ok) {
            throw new Error('Failed to fetch notebook');
          }
      
          const data: Notebook = await response.json();
            setNotebook(data);
          } catch (error) {
            console.error(error);
        }
        };

        fetchNotebook();
    }
  }, [id]);

  return (
      <div className="flex overflow-hidden bg-background">
        <SourcesPanel notebook={notebook}/>
        <ChatPanel notebook={notebook}/>
        <StudioPanel notebook={notebook}/>
      </div>
  )
}
