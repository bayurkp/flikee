import { httpClient } from "@/lib/http-client"
import type { GenerateVideoResponse } from "@/types/video-generator"

export const generateVideoFn = async (
  text: string
): Promise<GenerateVideoResponse> =>
  httpClient.post("/generate-dummy", { text }).then((res) => res.data)
