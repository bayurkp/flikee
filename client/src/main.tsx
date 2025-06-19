import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter, Routes } from "react-router"
import "./index.css"
import { Route } from "react-router"
import GeneratePage from "@/pages/generate"
import EditPage from "@/pages/edit"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

const queryClient = new QueryClient()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/generate" element={<GeneratePage />}></Route>
          <Route path="/edit" element={<EditPage />}></Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
)
