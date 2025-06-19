import type { GenerateVideoResponse } from "@/types/video-generator"
import { create } from "zustand"

interface VideoStore {
  data: GenerateVideoResponse | null
  setData: (data: GenerateVideoResponse) => void
  clearData: () => void
}

export const useVideoStore = create<VideoStore>((set) => ({
  data: null,
  setData: (data) => set({ data }),
  clearData: () => set({ data: null }),
}))
