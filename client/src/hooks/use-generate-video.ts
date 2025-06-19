import { generateVideoFn } from "@/api/video-generator"
import { useMutation } from "@tanstack/react-query"

export const useGenerateVideoMutation = () => {
  return useMutation({
    mutationFn: (text: string) => generateVideoFn(text),
  })
}
