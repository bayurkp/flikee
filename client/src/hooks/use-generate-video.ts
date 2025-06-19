import { generateVideoFn } from "@/api/video-generator"
import { useVideoStore } from "@/stores/video-store"
import { useMutation } from "@tanstack/react-query"

export const useGenerateVideoMutation = () => {
  const videoStore = useVideoStore()

  return useMutation({
    mutationFn: (text: string) => generateVideoFn(text),
    onSuccess: (data) => {
      videoStore.setData(data)
    },
  })
}
